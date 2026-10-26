import React from 'react';
import { motion } from 'framer-motion';
import { FolderIllustration, RobotIllustration } from './Illustrations';

export const HeroSection = () => {
  return (
    <section className="relative w-full glass-panel rounded-3xl p-6 lg:p-8 overflow-hidden mb-6">
      {/* Background ambient lighting */}
      <div className="absolute -top-20 -left-20 w-64 h-64 bg-purple-600/20 rounded-full blur-3xl -z-10" />
      <div className="absolute -bottom-20 -right-20 w-64 h-64 bg-cyan-500/20 rounded-full blur-3xl -z-10" />

      <div className="flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Left Folder Graphic */}
        <div className="hidden sm:flex items-center justify-center">
          <FolderIllustration />
        </div>

        {/* Center Title & Description */}
        <div className="flex-1 text-center md:text-left flex flex-col items-center md:items-start max-w-xl">
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center gap-2 px-3 py-1 rounded-full bg-purple-900/40 border border-purple-400/30 text-purple-300 text-xs font-semibold mb-3 backdrop-blur-md"
          >
            <span className="animate-spin text-sm">✦</span> Powered by Advanced RAG & OpenAI
          </motion.div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight neon-gradient-text mb-2">
            Multi-Format RAG
          </h1>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-100 tracking-tight mb-3">
            Question-Answering Agent
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 leading-relaxed max-w-lg">
            Upload PDF, JSON, Excel (.xlsx/.xls), or CSV files and ask questions based on their content in real time with high accuracy.
          </p>
        </div>

        {/* Right AI Robot Graphic */}
        <div className="flex items-center justify-center">
          <RobotIllustration />
        </div>
      </div>
    </section>
  );
};
