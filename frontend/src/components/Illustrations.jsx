import React from 'react';
import { motion } from 'framer-motion';

export const FolderIllustration = () => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8 }}
      className="relative w-52 h-44 flex items-center justify-center select-none"
    >
      {/* Glow background */}
      <div className="absolute inset-0 bg-gradient-to-r from-purple-600/30 via-pink-500/20 to-cyan-500/30 rounded-full blur-2xl -z-10 animate-pulse" />

      {/* Main Glowing Folder */}
      <motion.div
        animate={{ y: [-4, 4, -4] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        className="relative z-10 w-44 h-32 bg-gradient-to-br from-purple-900/80 via-purple-950/90 to-indigo-950/90 rounded-2xl border border-purple-500/40 backdrop-blur-xl shadow-[0_10px_30px_rgba(168,85,247,0.3)] p-3 flex flex-col justify-end"
      >
        <div className="absolute -top-3 left-4 w-16 h-5 bg-purple-800/80 rounded-t-lg border-t border-l border-r border-purple-400/30" />

        {/* Floating File Badges */}
        <motion.div
          animate={{ y: [-6, 2, -6], rotate: [-8, -4, -8] }}
          transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: 0.2 }}
          className="absolute -top-6 -left-2 bg-gradient-to-br from-rose-500 to-pink-600 text-white font-extrabold text-xs px-2.5 py-1.5 rounded-lg shadow-lg border border-pink-300/40 flex items-center gap-1"
        >
          <span className="text-[10px]">📄</span> PDF
        </motion.div>

        <motion.div
          animate={{ y: [-2, -8, -2], rotate: [6, 10, 6] }}
          transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
          className="absolute -top-8 left-14 bg-gradient-to-br from-emerald-500 to-teal-600 text-white font-extrabold text-xs px-2.5 py-1.5 rounded-lg shadow-lg border border-emerald-300/40 flex items-center gap-1"
        >
          <span className="text-[10px]">📊</span> XLSX
        </motion.div>

        <motion.div
          animate={{ y: [-5, 3, -5], rotate: [12, 6, 12] }}
          transition={{ duration: 4.2, repeat: Infinity, ease: "easeInOut", delay: 0.8 }}
          className="absolute -top-5 right-0 bg-gradient-to-br from-purple-500 to-indigo-600 text-white font-extrabold text-xs px-2.5 py-1.5 rounded-lg shadow-lg border border-purple-300/40 flex items-center gap-1"
        >
          <span className="text-[10px]">⚙️</span> JSON
        </motion.div>

        <motion.div
          animate={{ y: [2, -6, 2], rotate: [-4, 2, -4] }}
          transition={{ duration: 4.8, repeat: Infinity, ease: "easeInOut", delay: 0.1 }}
          className="absolute bottom-2 right-2 bg-gradient-to-br from-cyan-500 to-blue-600 text-white font-extrabold text-[11px] px-2.5 py-1 rounded-lg shadow-lg border border-cyan-300/40"
        >
          CSV
        </motion.div>

        {/* Folder Label */}
        <div className="w-full bg-purple-900/40 border border-purple-400/20 rounded-xl p-2 backdrop-blur-md">
          <div className="w-12 h-1.5 bg-purple-400/50 rounded-full mb-1" />
          <div className="w-20 h-1.5 bg-purple-400/30 rounded-full" />
        </div>
      </motion.div>
    </motion.div>
  );
};

export const RobotIllustration = () => {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.8 }}
      className="relative flex flex-col items-center select-none"
    >
      {/* Speech Bubble */}
      <motion.div
        animate={{ y: [-3, 3, -3] }}
        transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        className="mb-2 relative bg-gradient-to-r from-blue-900/80 via-indigo-900/80 to-purple-900/80 border border-cyan-400/50 px-4 py-2 rounded-2xl shadow-[0_0_20px_rgba(6,182,212,0.3)] backdrop-blur-md"
      >
        <p className="text-xs font-semibold text-cyan-200 tracking-wide flex items-center gap-1.5">
          <span>💖</span> Let's find answers together!
        </p>
        <div className="absolute -bottom-2 right-6 w-3 h-3 bg-indigo-900 border-r border-b border-cyan-400/50 transform rotate-45" />
      </motion.div>

      {/* Floating Robot Body */}
      <motion.div
        animate={{ y: [-6, 6, -6] }}
        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
        className="relative w-40 h-40 flex items-center justify-center"
      >
        {/* Glow Halo */}
        <div className="absolute inset-0 bg-gradient-to-tr from-cyan-500/30 via-purple-500/20 to-pink-500/30 rounded-full blur-xl -z-10 animate-pulse" />

        {/* Robot Head */}
        <div className="relative w-32 h-28 bg-gradient-to-b from-slate-200 via-slate-100 to-slate-300 rounded-3xl p-2 border-2 border-cyan-300 shadow-[0_0_25px_rgba(6,182,212,0.4)] flex flex-col items-center justify-center">
          {/* Antennas */}
          <div className="absolute -top-4 w-2 h-4 bg-slate-300 rounded-t-full flex items-center justify-center">
            <div className="absolute -top-2 w-3.5 h-3.5 bg-cyan-400 rounded-full shadow-[0_0_10px_#06b6d4] animate-ping" />
            <div className="absolute -top-2 w-3.5 h-3.5 bg-cyan-400 rounded-full shadow-[0_0_10px_#06b6d4]" />
          </div>

          {/* Ears */}
          <div className="absolute -left-3 w-3 h-6 bg-slate-400 rounded-l-md border border-slate-300" />
          <div className="absolute -right-3 w-3 h-6 bg-slate-400 rounded-r-md border border-slate-300" />

          {/* Face Screen */}
          <div className="w-28 h-20 bg-slate-950 rounded-2xl p-2 border border-slate-800 flex flex-col items-center justify-center relative overflow-hidden shadow-inner">
            {/* Cyan Glowing Eyes */}
            <div className="flex items-center gap-5">
              <motion.div
                animate={{ scaleY: [1, 0.1, 1] }}
                transition={{ duration: 4, repeat: Infinity, times: [0, 0.95, 1] }}
                className="w-5 h-5 bg-cyan-400 rounded-full shadow-[0_0_12px_#06b6d4] border border-cyan-200 flex items-center justify-center"
              >
                <div className="w-1.5 h-1.5 bg-white rounded-full" />
              </motion.div>
              <motion.div
                animate={{ scaleY: [1, 0.1, 1] }}
                transition={{ duration: 4, repeat: Infinity, times: [0, 0.95, 1] }}
                className="w-5 h-5 bg-cyan-400 rounded-full shadow-[0_0_12px_#06b6d4] border border-cyan-200 flex items-center justify-center"
              >
                <div className="w-1.5 h-1.5 bg-white rounded-full" />
              </motion.div>
            </div>

            {/* Smile / Mouth Line */}
            <div className="mt-2 w-8 h-1.5 bg-cyan-400/80 rounded-full shadow-[0_0_8px_#06b6d4]" />
          </div>

          {/* Small OpenAI / AI emblem on chest/laptop */}
          <div className="absolute bottom-1 w-6 h-6 bg-purple-600 rounded-full flex items-center justify-center text-[10px] text-white font-bold shadow-md">
            ✨
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};
