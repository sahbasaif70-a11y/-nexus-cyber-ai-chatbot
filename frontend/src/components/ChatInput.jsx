import React, { useState } from 'react';
import { Send, Sparkles, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

export const ChatInput = ({ onSendMessage, isLoading, disabled }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading || disabled) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative w-full mb-6">
      <div className="relative flex items-center">
        {/* Sparkle Icon */}
        <div className="absolute left-4 text-purple-400">
          <Sparkles className="w-5 h-5 animate-pulse" />
        </div>

        {/* Pill Input */}
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled || isLoading}
          placeholder={disabled ? "Please upload a document to ask questions..." : "Ask a question about your uploaded document..."}
          className={`
            w-full py-4 pl-12 pr-16 rounded-full bg-slate-900/90 border text-xs sm:text-sm text-slate-100 placeholder-slate-400
            backdrop-blur-xl transition-all shadow-[0_0_25px_rgba(168,85,247,0.15)]
            focus:outline-none focus:border-purple-400 focus:ring-4 focus:ring-purple-500/20 focus:shadow-[0_0_35px_rgba(168,85,247,0.3)]
            disabled:opacity-50 disabled:cursor-not-allowed
            ${disabled ? 'border-purple-500/20' : 'border-purple-500/40'}
          `}
        />

        {/* Circular Send Button */}
        <motion.button
          whileHover={{ scale: 1.08 }}
          whileTap={{ scale: 0.92 }}
          type="submit"
          disabled={!input.trim() || isLoading || disabled}
          className={`
            absolute right-2.5 p-3 rounded-full flex items-center justify-center transition-all cursor-pointer shadow-lg
            ${input.trim() && !isLoading && !disabled
              ? 'bg-gradient-to-r from-purple-500 via-pink-500 to-indigo-500 hover:from-purple-400 hover:to-indigo-400 text-white shadow-[0_0_20px_rgba(236,72,153,0.5)]'
              : 'bg-purple-900/30 text-purple-400/40 cursor-not-allowed border border-purple-500/20'}
          `}
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <Send className="w-4 h-4 transform rotate-45" />
          )}
        </motion.button>
      </div>
    </form>
  );
};
