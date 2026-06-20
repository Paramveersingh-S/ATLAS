import React from 'react';
import { Settings2, Cpu, HardDrive, Shield } from 'lucide-react';

export default function SettingsPage() {
  return (
    <div className="h-full w-full bg-[#020617] overflow-y-auto p-6 md:p-10 relative">
      <div className="absolute bottom-0 right-0 w-[400px] h-[400px] bg-[#00E5FF]/5 rounded-full blur-[120px] pointer-events-none"></div>
      
      <div className="max-w-4xl mx-auto space-y-8 relative z-10">
        <div>
          <h1 className="text-3xl font-bold text-slate-100 tracking-tight mb-2">Engine Settings</h1>
          <p className="text-slate-400">Configure ATLAS backend behavior and vector space optimizations.</p>
        </div>

        <div className="grid grid-cols-1 gap-6">
          <div className="glass-panel rounded-2xl p-8 border-slate-800">
            <h2 className="text-xl font-semibold text-slate-200 mb-6 flex items-center gap-2">
              <Cpu className="text-[#00E5FF]" size={20} />
              TurboQuant Compression
            </h2>
            
            <div className="space-y-6">
              <div className="flex items-center justify-between p-4 bg-[#0F172A] rounded-xl border border-slate-800/50">
                <div>
                  <h3 className="font-medium text-slate-200">Quantization Bits</h3>
                  <p className="text-sm text-slate-500">The number of bits used per component in Polar Quantization.</p>
                </div>
                <div className="bg-slate-900 px-4 py-2 rounded-lg border border-slate-800 text-[#00E5FF] font-mono">
                  3 Bits (Aggressive)
                </div>
              </div>

              <div className="flex items-center justify-between p-4 bg-[#0F172A] rounded-xl border border-slate-800/50">
                <div>
                  <h3 className="font-medium text-slate-200">Jointly Localized Sketching (QJL)</h3>
                  <p className="text-sm text-slate-500">Enable inner product estimation without full decompression.</p>
                </div>
                <div className="w-12 h-6 bg-[#00E5FF] rounded-full relative cursor-pointer opacity-80">
                  <div className="absolute right-1 top-1 bg-slate-900 w-4 h-4 rounded-full"></div>
                </div>
              </div>
            </div>
          </div>

          <div className="glass-panel rounded-2xl p-8 border-slate-800 opacity-60">
            <h2 className="text-xl font-semibold text-slate-200 mb-6 flex items-center gap-2">
              <HardDrive className="text-[#B200FF]" size={20} />
              Model Settings
            </h2>
            <p className="text-slate-500 mb-4 text-sm">Advanced embedding models are managed via environment variables.</p>
            <div className="p-4 bg-[#0F172A] rounded-xl border border-slate-800/50 font-mono text-sm text-slate-400">
              EMBEDDING_MODEL = "all-MiniLM-L6-v2"<br />
              DIMENSION = 384
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
