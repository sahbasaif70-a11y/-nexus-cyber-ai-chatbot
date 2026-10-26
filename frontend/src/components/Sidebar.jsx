import React, { useState } from 'react';
import {
  Settings, Key, Eye, EyeOff, Bot, Sliders, Layers, FileUp,
  FileText, FileSpreadsheet, Code2, X, Sparkles, CheckCircle2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const Sidebar = ({
  apiKey, setApiKey,
  model, setModel,
  chunkSize, setChunkSize,
  chunkOverlap, setChunkOverlap,
  topK, setTopK,
  uploadedFile, setUploadedFile,
  onFileUpload, onRemoveFile,
  isOpen, setIsOpen
}) => {
  const [showApiKey, setShowApiKey] = useState(false);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileUpload(e.dataTransfer.files[0]);
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return '0 KB';
    const kb = bytes / 1024;
    return kb > 1024 ? `${(kb / 1024).toFixed(1)} MB` : `${kb.toFixed(1)} KB`;
  };

  const getFileIcon = (fileName) => {
    if (!fileName) return <FileText className="w-5 h-5 text-purple-400" />;
    const ext = fileName.split('.').pop().toLowerCase();
    if (ext === 'pdf') return <FileText className="w-5 h-5 text-pink-400" />;
    if (['xlsx', 'xls', 'csv'].includes(ext)) return <FileSpreadsheet className="w-5 h-5 text-emerald-400" />;
    if (ext === 'json') return <Code2 className="w-5 h-5 text-cyan-400" />;
    return <FileText className="w-5 h-5 text-purple-400" />;
  };

  return (
    <aside className={`
      fixed lg:static top-0 left-0 z-40 h-full w-[310px] sm:w-[330px] lg:w-[28%] xl:w-[25%]
      glass-sidebar p-5 flex flex-col gap-6 overflow-y-auto transition-transform duration-300
      ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
    `}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-purple-900/40 border border-purple-500/30 text-purple-300 shadow-[0_0_15px_rgba(168,85,247,0.3)]">
            <Settings className="w-5 h-5 animate-[spin_10s_linear_infinite]" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-tight">Configuration</h2>
            <p className="text-[11px] text-slate-400">Fine-tune your RAG Agent</p>
          </div>
        </div>

        {/* Mobile close button */}
        <button
          onClick={() => setIsOpen(false)}
          className="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-purple-900/30"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* API Key Input */}
      <div className="flex flex-col gap-2">
        <label className="text-xs font-semibold text-purple-200 flex items-center gap-1.5">
          <Key className="w-3.5 h-3.5 text-purple-400" />
          <span>OpenAI API Key</span>
        </label>
        <div className="relative">
          <input
            type={showApiKey ? 'text' : 'password'}
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="sk-..."
            className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-purple-500/30 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-500/30 transition-all pr-10"
          />
          <button
            type="button"
            onClick={() => setShowApiKey(!showApiKey)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-purple-300 transition-colors"
          >
            {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Model Selection */}
      <div className="flex flex-col gap-2">
        <label className="text-xs font-semibold text-purple-200 flex items-center gap-1.5">
          <Bot className="w-3.5 h-3.5 text-purple-400" />
          <span>Chat model</span>
        </label>
        <select
          value={model}
          onChange={(e) => setModel(e.target.value)}
          className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-purple-500/30 text-xs text-slate-100 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-500/30 transition-all cursor-pointer"
        >
          <option value="gpt-4o-mini">gpt-4o-mini</option>
          <option value="gpt-4o">gpt-4o</option>
          <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
        </select>
      </div>

      {/* Chunk Size Slider */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between text-xs font-semibold">
          <span className="text-purple-200 flex items-center gap-1.5">
            <Sliders className="w-3.5 h-3.5 text-purple-400" /> Chunk size
          </span>
          <span className="px-2 py-0.5 rounded-md bg-purple-900/50 border border-purple-500/30 text-purple-300 font-mono text-[11px]">
            {chunkSize}
          </span>
        </div>
        <input
          type="range"
          min="500"
          max="2000"
          step="100"
          value={chunkSize}
          onChange={(e) => setChunkSize(Number(e.target.value))}
          className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-purple-400"
        />
      </div>

      {/* Chunk Overlap Slider */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between text-xs font-semibold">
          <span className="text-purple-200 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-purple-400" /> Chunk overlap
          </span>
          <span className="px-2 py-0.5 rounded-md bg-purple-900/50 border border-purple-500/30 text-purple-300 font-mono text-[11px]">
            {chunkOverlap}
          </span>
        </div>
        <input
          type="range"
          min="0"
          max="400"
          step="50"
          value={chunkOverlap}
          onChange={(e) => setChunkOverlap(Number(e.target.value))}
          className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-purple-400"
        />
      </div>

      {/* Retrieved Chunks (k) Slider */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between text-xs font-semibold">
          <span className="text-purple-200 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-purple-400" /> Retrieved chunks (k)
          </span>
          <span className="px-2 py-0.5 rounded-md bg-purple-900/50 border border-purple-500/30 text-purple-300 font-mono text-[11px]">
            {topK}
          </span>
        </div>
        <input
          type="range"
          min="2"
          max="10"
          step="1"
          value={topK}
          onChange={(e) => setTopK(Number(e.target.value))}
          className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-purple-400"
        />
      </div>

      {/* File Upload Area */}
      <div className="flex flex-col gap-2 mt-2">
        <label className="text-xs font-semibold text-purple-200 flex items-center gap-1.5">
          <FileUp className="w-3.5 h-3.5 text-purple-400" />
          <span>Upload Document (PDF, JSON, Excel, CSV)</span>
        </label>

        <AnimatePresence mode="wait">
          {uploadedFile ? (
            /* Uploaded File Card */
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="p-3 rounded-2xl bg-purple-950/60 border border-purple-500/40 backdrop-blur-md flex items-center justify-between shadow-[0_0_20px_rgba(168,85,247,0.2)]"
            >
              <div className="flex items-center gap-3 overflow-hidden">
                <div className="p-2 rounded-xl bg-purple-900/60 border border-purple-400/30">
                  {getFileIcon(uploadedFile.name)}
                </div>
                <div className="flex flex-col min-w-0">
                  <span className="text-xs font-semibold text-white truncate max-w-[160px]">
                    {uploadedFile.name}
                  </span>
                  <span className="text-[10px] text-purple-300 font-mono">
                    {formatFileSize(uploadedFile.size)}
                  </span>
                </div>
              </div>

              <button
                type="button"
                onClick={onRemoveFile}
                className="p-1.5 rounded-full hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition-colors cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </motion.div>
          ) : (
            /* Dropzone */
            <label
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={`
                relative flex flex-col items-center justify-center p-5 rounded-2xl border-2 border-dashed
                transition-all cursor-pointer text-center
                ${isDragging
                  ? 'border-pink-400 bg-purple-900/40 shadow-[0_0_30px_rgba(236,72,153,0.3)] scale-102'
                  : 'border-purple-500/30 bg-slate-900/50 hover:border-purple-400/60 hover:bg-purple-950/30'}
              `}
            >
              <input
                type="file"
                accept=".pdf,.json,.xlsx,.xls,.csv"
                onChange={(e) => e.target.files && onFileUpload(e.target.files[0])}
                className="hidden"
              />
              <div className="p-3 rounded-full bg-purple-900/40 border border-purple-400/30 mb-2 text-purple-300 shadow-[0_0_15px_rgba(168,85,247,0.3)]">
                <FileUp className="w-5 h-5 animate-bounce" />
              </div>
              <span className="text-xs font-medium text-slate-200">
                Drop file or <span className="text-purple-400 underline">click to upload</span>
              </span>
              <span className="text-[10px] text-slate-400 mt-1">
                Supports PDF, JSON, XLSX, XLS, CSV
              </span>
            </label>
          )}
        </AnimatePresence>
      </div>
    </aside>
  );
};
