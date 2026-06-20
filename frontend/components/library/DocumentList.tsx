'use client';
import React from 'react';
import { motion } from 'framer-motion';
import { FileText, File, FileCode, Trash2, RefreshCw } from 'lucide-react';

const mockDocuments = [
  { id: 1, name: 'Q3_Financial_Report.pdf', type: 'pdf', chunks: 1450, date: 'Oct 14, 2026', status: 'Indexed' },
  { id: 2, name: 'Architecture_RFC_v2.md', type: 'md', chunks: 320, date: 'Oct 12, 2026', status: 'Indexed' },
  { id: 3, name: 'Meeting_Transcript_Sales.txt', type: 'txt', chunks: 85, date: 'Oct 10, 2026', status: 'Processing' },
];

export default function DocumentList() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="glass-panel rounded-2xl overflow-hidden"
    >
      <div className="p-5 border-b border-slate-800/50 flex justify-between items-center bg-slate-900/40">
        <h3 className="font-medium text-slate-200 text-lg tracking-wide">Indexed Memory</h3>
        <span className="text-xs font-mono text-slate-500 bg-slate-950/50 px-3 py-1 rounded-full border border-slate-800">
          Total Chunks: 1,855
        </span>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800/50 text-slate-500 text-sm">
              <th className="p-4 font-medium">Document Name</th>
              <th className="p-4 font-medium hidden md:table-cell">Vector Chunks</th>
              <th className="p-4 font-medium hidden sm:table-cell">Upload Date</th>
              <th className="p-4 font-medium">Status</th>
              <th className="p-4 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {mockDocuments.map((doc, idx) => (
              <tr key={doc.id} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors">
                <td className="p-4 flex items-center gap-3">
                  <div className={`p-2 rounded-lg bg-slate-900/80 border border-slate-800
                    ${doc.type === 'pdf' ? 'text-red-400' : doc.type === 'md' ? 'text-[#00E5FF]' : 'text-slate-400'}`}
                  >
                    {doc.type === 'pdf' ? <File size={16} /> : doc.type === 'md' ? <FileCode size={16} /> : <FileText size={16} />}
                  </div>
                  <span className="text-slate-200 font-medium truncate max-w-[150px] sm:max-w-xs">{doc.name}</span>
                </td>
                <td className="p-4 text-slate-400 font-mono text-sm hidden md:table-cell">{doc.chunks.toLocaleString()}</td>
                <td className="p-4 text-slate-400 text-sm hidden sm:table-cell">{doc.date}</td>
                <td className="p-4">
                  <span className={`px-2.5 py-1 text-xs rounded-full border flex items-center gap-1.5 w-max
                    ${doc.status === 'Indexed' 
                      ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' 
                      : 'bg-amber-500/10 border-amber-500/30 text-amber-400'}
                  `}>
                    {doc.status === 'Processing' && <RefreshCw size={10} className="animate-spin" />}
                    {doc.status}
                  </span>
                </td>
                <td className="p-4 text-right">
                  <button className="text-slate-500 hover:text-red-400 transition-colors p-2 rounded-lg hover:bg-slate-800/50">
                    <Trash2 size={18} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
}
