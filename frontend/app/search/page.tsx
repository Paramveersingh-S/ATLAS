'use client';
import React, { useState } from 'react';
import { Search, Database, ChevronRight, Zap } from 'lucide-react';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setLoading(true);
    setSearched(true);
    try {
      const res = await fetch('/api/v1/documents/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: 5 })
      });
      if (res.ok) {
        const data = await res.json();
        setResults(data.results);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full w-full bg-[#020617] overflow-y-auto p-6 md:p-10 relative">
      <div className="absolute top-0 right-1/4 w-[500px] h-[500px] bg-[#B200FF]/5 rounded-full blur-[120px] pointer-events-none"></div>
      
      <div className="max-w-4xl mx-auto space-y-8 relative z-10">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-slate-100 tracking-tight mb-4 flex items-center justify-center gap-3">
            <Search className="text-[#00E5FF]" size={36} />
            Explore Memory
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto">
            Directly query the TurboQuant 3-bit vector space to see exactly how your data is chunked, indexed, and retrieved.
          </p>
        </div>

        <form onSubmit={handleSearch} className="relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-[#00E5FF] to-[#B200FF] rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
          <div className="relative flex items-center bg-[#0F172A] border border-slate-800 rounded-2xl overflow-hidden">
            <div className="pl-6 text-slate-400">
              <Search size={24} />
            </div>
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search your indexed documents..."
              className="w-full bg-transparent border-none text-slate-200 p-6 focus:outline-none focus:ring-0 text-lg placeholder-slate-600"
            />
            <button 
              type="submit"
              disabled={loading || !query.trim()}
              className="bg-gradient-to-r from-[#00E5FF] to-[#00B4D8] text-[#020617] font-semibold px-8 py-6 transition hover:opacity-90 disabled:opacity-50 flex items-center gap-2 whitespace-nowrap"
            >
              {loading ? 'Searching...' : 'Search Vectors'}
              {!loading && <ChevronRight size={20} />}
            </button>
          </div>
        </form>

        {searched && (
          <div className="mt-12 space-y-4">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-200 flex items-center gap-2">
                <Database className="text-[#B200FF]" size={20} />
                Raw Vector Chunks
              </h2>
              <span className="text-sm text-slate-500 font-mono bg-slate-900 px-3 py-1 rounded-full border border-slate-800 flex items-center gap-2">
                <Zap className="text-amber-400" size={14} />
                {results.length} results returned
              </span>
            </div>

            {results.length === 0 && !loading ? (
              <div className="glass-panel rounded-2xl p-12 text-center border-slate-800">
                <p className="text-slate-400">No matching chunks found in the vector space.</p>
              </div>
            ) : (
              results.map((result, idx) => (
                <div key={idx} className="glass-panel rounded-2xl p-6 border-slate-800 hover:border-slate-700 transition">
                  <div className="flex justify-between items-start mb-4">
                    <span className="text-xs font-mono text-[#00E5FF] bg-[#00E5FF]/10 px-2 py-1 rounded">
                      Score: {result.score.toFixed(4)}
                    </span>
                    <span className="text-xs font-mono text-slate-500">
                      DOC: {result.doc_id.substring(0, 12)}...
                    </span>
                  </div>
                  <p className="text-slate-300 leading-relaxed text-sm">
                    {result.text}
                  </p>
                  <div className="mt-4 pt-4 border-t border-slate-800/50 flex justify-between">
                    <span className="text-xs text-slate-600 font-mono">CHUNK_ID: {result.chunk_id}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}
