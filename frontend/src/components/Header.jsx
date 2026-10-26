import React from 'react';
import { Rocket, MoreVertical, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

export const Header = ({ onDeploy }) => {
  return (
    <header className="w-full h-16 px-6 flex items-center justify-between border-b border-purple-500/10 bg-slate-950/40 backdrop-blur-md sticky top-0 z-30">
      <div className="flex items-center gap-2">
        <Sparkles className="w-5 h-5 text-purple-400 animate-pulse" />
        <span className="text-xs font-semibold tracking-wider text-purple-300 uppercase">AI RAG Workspace</span>
      </div>

      <div className="flex items-center gap-3">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onDeploy}
          className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-semibold text-xs tracking-wide shadow-[0_0_20px_rgba(168,85,247,0.4)] border border-purple-400/30 transition-all cursor-pointer"
        >
          <Rocket className="w-3.5 h-3.5" />
          <span>Deploy</span>
        </motion.button>

        <button className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-purple-900/30 transition-colors cursor-pointer">
          <MoreVertical className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
};
