'use client';
import React from 'react';
import { motion } from 'framer-motion';

interface StatCardProps {
  title: string;
  value: string;
  trend?: string;
  icon: React.ReactNode;
  delay?: number;
  glowColor?: string;
}

export default function StatCard({ title, value, trend, icon, delay = 0, glowColor = '#00E5FF' }: StatCardProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay }}
      className="glass-panel rounded-2xl p-6 relative overflow-hidden group hover:border-slate-600 transition-colors"
    >
      <div 
        className="absolute -right-6 -top-6 w-24 h-24 rounded-full blur-2xl opacity-20 group-hover:opacity-40 transition-opacity"
        style={{ backgroundColor: glowColor }}
      ></div>
      
      <div className="flex justify-between items-start mb-4">
        <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 shadow-inner">
          {icon}
        </div>
        {trend && (
          <span className="text-xs font-medium text-emerald-400 bg-emerald-400/10 px-2.5 py-1 rounded-full border border-emerald-400/20">
            {trend}
          </span>
        )}
      </div>
      
      <div>
        <h3 className="text-3xl font-bold text-slate-100 tracking-tight mb-1">{value}</h3>
        <p className="text-slate-400 text-sm font-medium">{title}</p>
      </div>
    </motion.div>
  );
}
