import StatCard from '@/components/dashboard/StatCard';
import ActivityFeed from '@/components/dashboard/ActivityFeed';
import { Database, Zap, HardDrive } from 'lucide-react';

export default function DashboardPage() {
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
            value="1.8M" 
            trend="+12k this week"
            icon={<Database className="text-[#00E5FF]" size={24} />} 
            delay={0.1}
          />
          <StatCard 
            title="Memory Footprint" 
            value="142 MB" 
            trend="-85% vs FP32"
            icon={<HardDrive className="text-[#B200FF]" size={24} />} 
            delay={0.2}
            glowColor="#B200FF"
          />
          <StatCard 
            title="Avg Retrieval Latency" 
            value="0.8 ms" 
            icon={<Zap className="text-amber-400" size={24} />} 
            delay={0.3}
            glowColor="#fbbf24"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 glass-panel rounded-2xl p-6 flex flex-col items-center justify-center min-h-[300px] border-slate-800">
            {/* Mock Graph Area */}
            <div className="text-center">
              <Zap className="text-slate-700 w-12 h-12 mx-auto mb-4" />
              <p className="text-slate-500 font-mono text-sm">Query Volume Chart</p>
              <p className="text-slate-600 text-xs mt-2">Awaiting sufficient live traffic data...</p>
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
