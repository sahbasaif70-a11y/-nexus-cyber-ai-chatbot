import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Search, BarChart3, Sparkles } from 'lucide-react';

export const SuggestionChips = ({ onSelectChip }) => {
  const chips = [
    {
      icon: <FileText className="w-4 h-4 text-pink-400" />,
      label: 'Summarize the document',
      prompt: 'Provide a comprehensive summary of this document.',
    },
    {
      icon: <Search className="w-4 h-4 text-cyan-400" />,
      label: 'Find specific information',
      prompt: 'What are the key findings and main insights in this document?',
    },
    {
      icon: <BarChart3 className="w-4 h-4 text-purple-400" />,
      label: 'Compare data',
      prompt: 'Compare the main data points, metrics, or categories present in this file.',
    },
    {
      icon: <Sparkles className="w-4 h-4 text-amber-400" />,
      label: 'Ask anything...',
      prompt: 'List the top 5 most important details from this file.',
    },
  ];

  return (
    <div className="w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
      {chips.map((chip, idx) => (
        <motion.button
          key={idx}
          whileHover={{ scale: 1.02, y: -2 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => onSelectChip(chip.prompt)}
          className="flex items-center gap-2.5 px-4 py-3 rounded-2xl bg-purple-950/40 hover:bg-purple-900/60 border border-purple-500/30 hover:border-purple-400/70 text-slate-200 hover:text-white text-xs font-semibold shadow-md hover:shadow-[0_0_20px_rgba(168,85,247,0.3)] transition-all cursor-pointer backdrop-blur-md"
        >
          {chip.icon}
          <span className="truncate">{chip.label}</span>
        </motion.button>
      ))}
    </div>
  );
};
