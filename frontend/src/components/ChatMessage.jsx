import React, { useState } from 'react';
import { Bot, User, Copy, Check, ChevronDown, ChevronUp, FileText, Sparkles, RefreshCw } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';

export const ChatMessage = ({ message, onRetry }) => {
  const isUser = message.role === 'user';
  const [copied, setCopied] = useState(false);
  const [showSources, setShowSources] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`w-full flex gap-3.5 mb-5 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      {!isUser && (
        <div className="w-9 h-9 rounded-2xl bg-gradient-to-br from-purple-600 via-pink-600 to-cyan-500 p-0.5 shadow-[0_0_15px_rgba(168,85,247,0.4)] shrink-0 mt-1">
          <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center text-cyan-300">
            <Bot className="w-5 h-5" />
          </div>
        </div>
      )}

      <div className={`flex flex-col max-w-[85%] sm:max-w-[75%] ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Chat Card */}
        <div className={`
          p-4 sm:p-5 rounded-3xl backdrop-blur-xl border shadow-xl relative text-xs sm:text-sm leading-relaxed
          ${isUser
            ? 'bg-gradient-to-r from-purple-900/80 via-purple-950/90 to-indigo-950/90 border-purple-500/40 text-slate-100 rounded-tr-none shadow-[0_0_25px_rgba(168,85,247,0.2)]'
            : 'bg-slate-900/80 border-purple-500/30 text-slate-200 rounded-tl-none shadow-[0_0_30px_rgba(15,12,34,0.5)]'}
        `}>
          {isUser ? (
            <p className="whitespace-pre-wrap font-medium">{message.content}</p>
          ) : (
            <div className="prose prose-invert prose-purple max-w-none text-slate-100 text-xs sm:text-sm">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}

          {/* Action Footer for Assistant */}
          {!isUser && (
            <div className="mt-3 pt-3 border-t border-purple-500/20 flex items-center justify-between gap-3 text-slate-400 text-xs">
              <div className="flex items-center gap-2">
                <button
                  onClick={handleCopy}
                  className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-purple-950/50 hover:bg-purple-900/80 hover:text-purple-200 border border-purple-500/30 transition-colors cursor-pointer"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>

                {onRetry && (
                  <button
                    onClick={() => onRetry(message.id)}
                    className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-purple-950/50 hover:bg-purple-900/80 hover:text-purple-200 border border-purple-500/30 transition-colors cursor-pointer"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>Retry</span>
                  </button>
                )}
              </div>

              {message.sources && message.sources.length > 0 && (
                <button
                  onClick={() => setShowSources(!showSources)}
                  className="flex items-center gap-1 text-purple-300 hover:text-purple-100 font-medium transition-colors cursor-pointer"
                >
                  <FileText className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Sources ({message.sources.length})</span>
                  {showSources ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                </button>
              )}
            </div>
          )}
        </div>

        {/* Source Chunks Expander */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <AnimatePresence>
            {showSources && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="w-full mt-2 p-3 rounded-2xl bg-purple-950/40 border border-purple-500/30 backdrop-blur-md overflow-hidden text-xs text-slate-300"
              >
                <div className="font-semibold text-purple-300 mb-2 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Retrieved Reference Chunks:</span>
                </div>
                <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                  {message.sources.map((src, idx) => (
                    <div key={idx} className="p-2 rounded-xl bg-slate-900/80 border border-purple-500/20 font-mono text-[11px] text-slate-300">
                      <div className="text-cyan-400 font-bold mb-1">
                        Ref #{idx + 1} {src.metadata?.page !== undefined ? `(Page ${src.metadata.page + 1})` : src.metadata?.row ? `(Row ${src.metadata.row})` : ''}
                      </div>
                      <p className="line-clamp-3 text-slate-400 whitespace-pre-wrap">{src.page_content}</p>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        )}
      </div>

      {isUser && (
        <div className="w-9 h-9 rounded-2xl bg-gradient-to-br from-pink-500 to-rose-600 p-0.5 shadow-[0_0_15px_rgba(236,72,153,0.4)] shrink-0 mt-1">
          <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center text-pink-300">
            <User className="w-5 h-5" />
          </div>
        </div>
      )}
    </motion.div>
  );
};
