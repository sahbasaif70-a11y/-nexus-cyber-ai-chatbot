import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, Loader2, AlertCircle, Sparkles } from 'lucide-react';

export const IndexingStatus = ({ status, fileName, errorMessage }) => {
  if (!status) return null;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={status}
        initial={{ opacity: 0, y: -10, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 10, scale: 0.98 }}
        transition={{ duration: 0.4 }}
        className="w-full mb-6"
      >
        {status === 'indexing' && (
          <div className="w-full px-5 py-3.5 rounded-2xl bg-cyan-950/40 border border-cyan-500/40 text-cyan-300 flex items-center justify-between shadow-[0_0_20px_rgba(6,182,212,0.2)] backdrop-blur-md">
            <div className="flex items-center gap-3">
              <Loader2 className="w-5 h-5 text-cyan-400 animate-spin" />
              <span className="text-xs sm:text-sm font-semibold">
                Parsing & Indexing <strong className="text-white">{fileName}</strong>...
              </span>
            </div>
            <Sparkles className="w-4 h-4 text-cyan-300 animate-pulse hidden sm:block" />
          </div>
        )}

        {status === 'success' && (
          <div className="w-full px-5 py-3.5 rounded-2xl bg-emerald-950/40 border border-emerald-500/50 text-emerald-300 flex items-center justify-between shadow-[0_0_25px_rgba(16,185,129,0.25)] backdrop-blur-md">
            <div className="flex items-center gap-3">
              <div className="p-1 rounded-full bg-emerald-500/20 text-emerald-400">
                <CheckCircle2 className="w-5 h-5" />
              </div>
              <span className="text-xs sm:text-sm font-semibold">
                Indexed <strong className="text-white">{fileName}</strong> — ask away!
              </span>
            </div>
            <span className="text-xs text-emerald-400 font-mono flex items-center gap-1">
              ✨ Ready
            </span>
          </div>
        )}

        {status === 'error' && (
          <div className="w-full px-5 py-3.5 rounded-2xl bg-rose-950/40 border border-rose-500/50 text-rose-300 flex items-center justify-between shadow-[0_0_20px_rgba(244,63,94,0.2)] backdrop-blur-md">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
              <span className="text-xs sm:text-sm font-semibold">
                {errorMessage || 'Failed to index file. Please check your API key.'}
              </span>
            </div>
          </div>
        )}
      </motion.div>
    </AnimatePresence>
  );
};
