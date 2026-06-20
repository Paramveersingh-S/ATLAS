'use client';
import React, { useEffect, useState } from 'react';
import StatCard from '@/components/dashboard/StatCard';
import ActivityFeed from '@/components/dashboard/ActivityFeed';
import { Database, Zap, HardDrive } from 'lucide-react';
import { motion } from 'framer-motion';

export default function DashboardPage() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('/api/v1/stats/compression');
        if (res.ok) {
          setStats(await res.json());
        }
      } catch (e) {
        console.error("Failed to fetch stats", e);
      }
    };
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-full w-full bg-[#020617] overflow-y-auto p-6 md:p-10 relative">
      <div className="absolute top-1/4 left-1/4 w-[400px] h-[400px] bg-[#00E5FF]/5 rounded-full blur-[120px] pointer-events-none"></div>
      
      <div className="max-w-6xl mx-auto space-y-8 relative z-10">
        <div>
          <h1 className="text-3xl font-bold text-slate-100 tracking-tight mb-2">Memory Analytics</h1>
          <p className="text-slate-400">Real-time health and performance of the TurboQuant Vector Engine.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <StatCard 
            title="Total Vectors Indexed" 
            value={stats ? stats.vector_index.num_vectors.toLocaleString() : "Loading..."} 
            icon={<Database className="text-[#00E5FF]" size={24} />} 
            delay={0.1}
          />
          <StatCard 
            title="Memory Footprint" 
            value={stats ? (stats.vector_index.index_size_mb < 0.01 && stats.vector_index.num_vectors > 0 ? "< 0.01 MB" : `${stats.vector_index.index_size_mb} MB`) : "Loading..."} 
            trend={stats ? `-${stats.vector_index.compression_ratio}x vs FP32` : ""}
            icon={<HardDrive className="text-[#B200FF]" size={24} />} 
            delay={0.2}
            glowColor="#B200FF"
          />
          <StatCard 
            title="Avg Retrieval Latency" 
            value={stats ? `${stats.vector_index.last_index_latency_ms} ms` : "Loading..."} 
            icon={<Zap className="text-amber-400" size={24} />} 
            delay={0.3}
            glowColor="#fbbf24"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 glass-panel rounded-2xl p-6 flex flex-col min-h-[300px] border-slate-800">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-slate-200 font-semibold flex items-center gap-2">
                <Zap className="text-[#00E5FF]" size={18} />
                Live Query Volume
              </h3>
              <div className="flex gap-4 text-xs font-mono">
                <span className="flex items-center gap-1 text-slate-400">
                  <div className="w-2 h-2 rounded-full bg-[#00E5FF]"></div> Queries / Min
                </span>
              </div>
            </div>
            
            <div className="flex-1 flex items-end justify-between gap-2 md:gap-4 mt-auto h-48">
              {[120, 230, 150, 400, 320, 500, 380, 290, 410, 460, 520, 310].map((val, i) => (
                <div key={i} className="relative flex flex-col justify-end items-center w-full group h-full">
                  <motion.div 
                    initial={{ height: 0 }}
                    animate={{ height: `${(val / 520) * 100}%` }}
                    transition={{ duration: 0.8, delay: i * 0.05, ease: "easeOut" }}
                    className="w-full bg-gradient-to-t from-[#00E5FF]/20 to-[#00E5FF]/70 rounded-t-sm transition-colors duration-300 group-hover:to-[#00E5FF]"
                  ></motion.div>
                  {/* Tooltip */}
                  <div className="absolute -top-8 bg-slate-900 border border-slate-700 text-[#00E5FF] text-xs py-1 px-2 rounded opacity-0 group-hover:opacity-100 transition-opacity font-mono pointer-events-none z-20 shadow-lg">
                    {val}
                  </div>
                </div>
              ))}
            </div>
            <div className="flex justify-between text-slate-500 text-xs mt-4 font-mono border-t border-slate-800/50 pt-2">
              <span>-60m</span>
              <span>-30m</span>
              <span className="text-[#00E5FF]">Now</span>
            </div>
          </div>
          <div className="lg:col-span-1">
            <ActivityFeed />
          </div>
        </div>
      </div>
    </div>
  );
}
