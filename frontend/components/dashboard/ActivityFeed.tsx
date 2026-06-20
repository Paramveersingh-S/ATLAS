'use client';
import React from 'react';
import { motion } from 'framer-motion';
import { Zap, Database, Search } from 'lucide-react';

const activities = [
  { id: 1, type: 'search', message: 'Executed 3-bit TurboQuant search in 0.8ms', time: 'Just now', icon: <Search size={14} className="text-[#00E5FF]" /> },
  { id: 2, type: 'index', message: 'Indexed 1,450 chunks from Q3_Financial_Report.pdf', time: '2 hours ago', icon: <Database size={14} className="text-[#B200FF]" /> },
  { id: 3, type: 'system', message: 'Background KV cache compression completed (Saved 1.2GB)', time: '5 hours ago', icon: <Zap size={14} className="text-amber-400" /> },
];

export default function ActivityFeed() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="glass-panel rounded-2xl p-6"
    >
      <h3 className="font-medium text-slate-200 text-lg mb-6 tracking-wide">System Activity</h3>
      
      <div className="space-y-6">
        {activities.map((activity, idx) => (
          <div key={activity.id} className="flex gap-4 relative">
            {/* Timeline line */}
            {idx !== activities.length - 1 && (
              <div className="absolute top-8 left-[15px] bottom-[-24px] w-px bg-slate-800"></div>
            )}
            
            <div className="w-8 h-8 rounded-full bg-slate-900/80 border border-slate-700/50 flex items-center justify-center flex-shrink-0 z-10 shadow-inner">
              {activity.icon}
            </div>
            
            <div className="pt-1.5">
              <p className="text-slate-200 text-sm">{activity.message}</p>
              <p className="text-slate-500 text-xs mt-1 font-mono">{activity.time}</p>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
