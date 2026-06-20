'use client';
import React, { useState } from 'react';
import { UploadCloud, FileText } from 'lucide-react';
import { motion } from 'framer-motion';

export default function UploadZone() {
  const [isDragging, setIsDragging] = useState(false);

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`glass-panel rounded-2xl p-8 border-2 border-dashed transition-all duration-300 flex flex-col items-center justify-center min-h-[200px] cursor-pointer
        ${isDragging ? 'border-[#00E5FF] bg-[#00E5FF]/5 shadow-[0_0_30px_rgba(0,229,255,0.2)]' : 'border-slate-700 hover:border-[#B200FF]/50 hover:bg-slate-800/40'}
      `}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => { e.preventDefault(); setIsDragging(false); }}
    >
      <div className="w-16 h-16 rounded-full bg-slate-800/80 flex items-center justify-center mb-4 shadow-inner border border-slate-700/50">
        <UploadCloud className="w-8 h-8 text-[#00E5FF]" />
      </div>
      <h3 className="text-xl font-medium text-slate-200 mb-2">Drag & Drop Documents</h3>
      <p className="text-slate-500 text-sm text-center max-w-sm mb-6">
        Upload PDF, TXT, or Markdown files. The TurboQuant engine will instantly chunk, embed, and map them to the vector space.
      </p>
      
      <button className="glass-button px-6 py-2 rounded-xl text-[#00E5FF] font-medium flex items-center gap-2 border-[#00E5FF]/30 hover:border-[#00E5FF]/80 hover:shadow-[0_0_15px_rgba(0,229,255,0.3)]">
        <FileText size={18} /> Browse Files
      </button>
    </motion.div>
  );
}
