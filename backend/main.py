import os
import json
import tempfile
import pandas as pd
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

app = FastAPI(title="Multi-Format RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global in-memory storage for session vectorstore
vectorstore_store: Dict[str, FAISS] = {}

def load_documents_from_file(file_path: str, file_name: str) -> List[Document]:
    ext = os.path.splitext(file_name)[1].lower()
    docs = []

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
        docs = loader.load()

    elif ext in [".xlsx", ".xls", ".csv"]:
        if ext == ".csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        for idx, row in df.iterrows():
            row_text = "\n".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
            docs.append(
                Document(
                    page_content=f"[Row {idx + 1}]\n{row_text}",
                    metadata={"row": idx + 1, "source": file_name}
                )
            )

    elif ext == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, list):
            for i, item in enumerate(data):
                item_str = json.dumps(item, indent=2) if isinstance(item, (dict, list)) else str(item)
                docs.append(
                    Document(
                        page_content=f"[Item {i + 1}]\n{item_str}",
                        metadata={"item": i + 1, "source": file_name}
                    )
                )
        elif isinstance(data, dict):
            for k, v in data.items():
                v_str = json.dumps(v, indent=2) if isinstance(v, (dict, list)) else str(v)
                docs.append(
                    Document(
                        page_content=f"[{k}]\n{v_str}",
                        metadata={"key": k, "source": file_name}
                    )
                )
        else:
            docs.append(Document(page_content=str(data), metadata={"source": file_name}))

    return docs

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Multi-Format RAG API is running successfully!",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Multi-Format RAG API is running"}

@app.post("/api/index")
async def index_document(
    file: UploadFile = File(...),
    api_key: str = Form(...),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(150),
):
    if not api_key or not api_key.strip().startswith("sk-"):
        raise HTTPException(status_code=400, detail="Invalid OpenAI API Key. Must start with 'sk-'")

    filename = file.filename or "uploaded_document"
    ext = os.path.splitext(filename)[1].lower()

    if ext not in [".pdf", ".json", ".xlsx", ".xls", ".csv"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF, JSON, Excel, or CSV.")

    file_bytes = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        docs = load_documents_from_file(tmp_path, filename)
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(err)}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    if not docs:
        raise HTTPException(status_code=400, detail="No readable content found in the document.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = text_splitter.split_documents(docs)

    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key.strip())
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore_store["active_session"] = vectorstore
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"OpenAI Embedding Error: {str(err)}")

    return {
        "status": "success",
        "message": f"Successfully indexed {filename}",
        "filename": filename,
        "total_chunks": len(chunks)
    }

class ChatQueryRequest(BaseModel):
    question: str
    api_key: str
    model: Optional[str] = "gpt-4o-mini"
    top_k: Optional[int] = 4

@app.post("/api/chat")
async def chat_query(request: ChatQueryRequest):
    if "active_session" not in vectorstore_store:
        raise HTTPException(status_code=400, detail="No document has been indexed yet. Please upload a file first.")

    if not request.api_key or not request.api_key.strip().startswith("sk-"):
        raise HTTPException(status_code=400, detail="Invalid OpenAI API key.")

    vectorstore = vectorstore_store["active_session"]
    retriever = vectorstore.as_retriever(search_kwargs={"k": request.top_k or 4})

    try:
        retrieved_docs = retriever.invoke(request.question)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {str(err)}")

    formatted_context = []
    for d in retrieved_docs:
        source_tag = ""
        if "page" in d.metadata:
            source_tag = f"[Page {d.metadata['page'] + 1}]"
        elif "row" in d.metadata:
            source_tag = f"[Row {d.metadata['row']}]"
        elif "item" in d.metadata:
            source_tag = f"[Item {d.metadata['item']}]"
        elif "key" in d.metadata:
            source_tag = f"[Key: {d.metadata['key']}]"

        content = d.page_content.strip()
        formatted_context.append(f"{source_tag}\n{content}" if source_tag else content)

    context_str = "\n\n".join(formatted_context)

    RAG_PROMPT = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful assistant that answers questions strictly using the provided context from a document (PDF, JSON, Excel, or CSV).\n"
         "1. Answer ONLY from the context below\n"
         "2. If the answer is not in the context, say: \"I couldn't find that in the document.\"\n"
         "3. Cite the relevant page/row/item number(s) or key(s) if applicable.\n\n"
         "Context:\n{context}"),
        ("human", "{question}"),
    ])

    try:
        llm = ChatOpenAI(model=request.model or "gpt-4o-mini", temperature=0, api_key=request.api_key.strip())
        chain = RAG_PROMPT | llm | StrOutputParser()
        answer = chain.invoke({"context": context_str, "question": request.question})
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"OpenAI Chat API Error: {str(err)}")

    sources_data = [
        {
            "page_content": d.page_content,
            "metadata": d.metadata
        }
        for d in retrieved_docs
    ]

    return {
        "answer": answer,
        "sources": sources_data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
