'use client';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, File, FileCode, Trash2, RefreshCw } from 'lucide-react';

export default function DocumentList() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [totalChunks, setTotalChunks] = useState(0);

  const fetchDocs = async () => {
    try {
      const res = await fetch('/api/v1/documents/');
      if (res.ok) {
        const data = await res.json();
        setDocuments(data.documents);
        const chunks = data.documents.reduce((acc: number, doc: any) => acc + (doc.chunk_count || 0), 0);
        setTotalChunks(chunks);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchDocs();
    window.addEventListener('documentUploaded', fetchDocs);
    const interval = setInterval(fetchDocs, 5000);
    return () => {
      window.removeEventListener('documentUploaded', fetchDocs);
      clearInterval(interval);
    }
  }, []);

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
          Total Chunks: {totalChunks.toLocaleString()}
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
            </tr>
          </thead>
          <tbody>
            {documents.length === 0 ? (
              <tr>
                <td colSpan={4} className="p-8 text-center text-slate-500">No documents indexed yet. Upload one above!</td>
              </tr>
            ) : documents.map((doc) => (
              <tr key={doc.id} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors">
                <td className="p-4 flex items-center gap-3">
                  <div className={`p-2 rounded-lg bg-slate-900/80 border border-slate-800
                    ${doc.file_type === 'pdf' ? 'text-red-400' : doc.file_type === 'md' ? 'text-[#00E5FF]' : 'text-slate-400'}`}
                  >
                    {doc.file_type === 'pdf' ? <File size={16} /> : doc.file_type === 'md' ? <FileCode size={16} /> : <FileText size={16} />}
                  </div>
                  <span className="text-slate-200 font-medium truncate max-w-[150px] sm:max-w-xs">{doc.title}</span>
                </td>
                <td className="p-4 text-slate-400 font-mono text-sm hidden md:table-cell">{doc.chunk_count?.toLocaleString()}</td>
                <td className="p-4 text-slate-400 text-sm hidden sm:table-cell">{new Date(doc.ingested_at).toLocaleDateString()}</td>
                <td className="p-4">
                  <span className={`px-2.5 py-1 text-xs rounded-full border flex items-center gap-1.5 w-max
                    ${doc.status === 'Indexed' 
                      ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' 
                      : doc.status.toLowerCase().includes('error') ? 'bg-red-500/10 border-red-500/30 text-red-400' : 'bg-amber-500/10 border-amber-500/30 text-amber-400'}
                  `}>
                    {doc.status !== 'Indexed' && !doc.status.toLowerCase().includes('error') && <RefreshCw size={10} className="animate-spin" />}
                    {doc.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
}
