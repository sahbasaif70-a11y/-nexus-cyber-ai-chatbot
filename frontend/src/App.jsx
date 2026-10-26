import React, { useState } from 'react';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { HeroSection } from './components/HeroSection';
import { IndexingStatus } from './components/IndexingStatus';
import { ChatInput } from './components/ChatInput';
import { SuggestionChips } from './components/SuggestionChips';
import { ChatMessage } from './components/ChatMessage';
import { Menu, Bot, Sparkles, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function App() {
  const API_BASE_URL = import.meta.env.VITE_API_URL || '';

  // Configuration state
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState('gpt-4o-mini');
  const [chunkSize, setChunkSize] = useState(1000);
  const [chunkOverlap, setChunkOverlap] = useState(150);
  const [topK, setTopK] = useState(4);

  // File & Indexing state
  const [uploadedFile, setUploadedFile] = useState(null);
  const [indexingStatus, setIndexingStatus] = useState(null); // 'indexing' | 'success' | 'error'
  const [errorMessage, setErrorMessage] = useState('');

  // Sidebar & Modal states
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [deployModalOpen, setDeployModalOpen] = useState(false);

  // Chat state
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // File Upload & Indexing Handler
  const handleFileUpload = async (file) => {
    if (!file) return;

    if (!apiKey) {
      setIndexingStatus('error');
      setErrorMessage('Please enter your OpenAI API key in the sidebar configuration first.');
      return;
    }

    setUploadedFile(file);
    setIndexingStatus('indexing');
    setErrorMessage('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('api_key', apiKey);
    formData.append('chunk_size', chunkSize);
    formData.append('chunk_overlap', chunkOverlap);

    try {
      const response = await fetch(`${API_BASE_URL}/api/index`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to index document');
      }

      setIndexingStatus('success');
      setMessages([]);
    } catch (err) {
      setIndexingStatus('error');
      setErrorMessage(err.message || 'Error parsing and indexing document.');
    }
  };

  const handleRemoveFile = () => {
    setUploadedFile(null);
    setIndexingStatus(null);
    setMessages([]);
  };

  // Chat Query Handler
  const handleSendMessage = async (text) => {
    if (!text.trim() || isLoading) return;

    if (!apiKey) {
      alert('Please enter your OpenAI API Key in the sidebar configuration.');
      return;
    }

    if (!uploadedFile || indexingStatus !== 'success') {
      alert('Please upload and index a document first.');
      return;
    }

    const userMsg = { id: Date.now().toString(), role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: text,
          api_key: apiKey,
          model: model,
          top_k: topK,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to generate answer.');
      }

      const assistantMsg = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        sources: data.sources || [],
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errorMsg = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `⚠️ **Error:** ${err.message || 'Unable to connect to OpenAI API.'}`,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-screen bg-[#080715] text-slate-100 overflow-hidden relative font-['Plus_Jakarta_Sans',sans-serif]">
      {/* Background Animated Gradient Orbs */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl pointer-events-none animate-pulse" />
      <div className="absolute bottom-0 right-1/4 w-[30rem] h-[30rem] bg-indigo-600/10 rounded-full blur-3xl pointer-events-none animate-pulse" />

      {/* Sidebar */}
      <Sidebar
        apiKey={apiKey}
        setApiKey={setApiKey}
        model={model}
        setModel={setModel}
        chunkSize={chunkSize}
        setChunkSize={setChunkSize}
        chunkOverlap={chunkOverlap}
        setChunkOverlap={setChunkOverlap}
        topK={topK}
        setTopK={setTopK}
        uploadedFile={uploadedFile}
        setUploadedFile={setUploadedFile}
        onFileUpload={handleFileUpload}
        onRemoveFile={handleRemoveFile}
        isOpen={sidebarOpen}
        setIsOpen={setSidebarOpen}
      />

      {/* Main Workspace */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative z-10">
        <Header onDeploy={() => setDeployModalOpen(true)} />

        {/* Mobile Sidebar Toggle */}
        <div className="lg:hidden p-3 border-b border-purple-500/10 bg-slate-950/60 backdrop-blur-md flex items-center justify-between">
          <button
            onClick={() => setSidebarOpen(true)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-purple-900/40 border border-purple-500/30 text-purple-300 text-xs font-semibold"
          >
            <Menu className="w-4 h-4" />
            <span>Configuration</span>
          </button>
          <span className="text-xs font-bold text-purple-300">RAG Agent</span>
        </div>

        {/* Main Scrollable Body */}
        <main className="flex-1 overflow-y-auto px-4 sm:px-8 lg:px-12 py-6 max-w-6xl mx-auto w-full">
          {/* Hero Section */}
          <HeroSection />

          {/* Indexing Status Banner */}
          <IndexingStatus
            status={indexingStatus}
            fileName={uploadedFile?.name}
            errorMessage={errorMessage}
          />

          {/* Chat Input */}
          <ChatInput
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            disabled={indexingStatus !== 'success'}
          />

          {/* Suggestion Chips */}
          <SuggestionChips onSelectChip={handleSendMessage} />

          {/* Chat Conversation History */}
          <div className="w-full mt-6 pb-12">
            <AnimatePresence>
              {messages.map((msg) => (
                <ChatMessage key={msg.id} message={msg} />
              ))}
            </AnimatePresence>

            {/* Loading Typing Indicator */}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center gap-3 p-4 rounded-3xl bg-slate-900/80 border border-purple-500/30 w-fit backdrop-blur-xl mb-4"
              >
                <Bot className="w-5 h-5 text-cyan-400 animate-bounce" />
                <span className="text-xs text-purple-300 font-semibold flex items-center gap-1">
                  Analyzing document & generating response...
                  <span className="animate-ping">✦</span>
                </span>
              </motion.div>
            )}
          </div>
        </main>
      </div>

      {/* Deploy Modal */}
      <AnimatePresence>
        {deployModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="w-full max-w-md p-6 rounded-3xl glass-panel-glow border border-purple-500/50 shadow-2xl relative"
            >
              <button
                onClick={() => setDeployModalOpen(false)}
                className="absolute top-4 right-4 text-slate-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 rounded-2xl bg-purple-600/30 border border-purple-400/40 text-purple-300">
                  <Sparkles className="w-6 h-6 animate-pulse" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">Deploy RAG Agent</h3>
                  <p className="text-xs text-purple-300">Publish your customized AI Chatbot</p>
                </div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed mb-6">
                Your Multi-Format RAG Chatbot is configured and ready for production deployment on Vercel, Netlify, or AWS.
              </p>

              <div className="flex items-center justify-end gap-3">
                <button
                  onClick={() => setDeployModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-xs font-semibold text-slate-300"
                >
                  Cancel
                </button>
                <button
                  onClick={() => {
                    alert('Deploying application to production environment...');
                    setDeployModalOpen(false);
                  }}
                  className="px-5 py-2 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-600 text-xs font-bold text-white shadow-lg hover:shadow-purple-500/50"
                >
                  Start Deployment 🚀
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
