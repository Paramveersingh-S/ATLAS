import Link from 'next/link';
import { MessageSquare, Library, LayoutDashboard, Settings, Compass } from 'lucide-react';
import React from 'react';

export default function Sidebar() {
  return (
    <div className="w-20 md:w-64 h-full glass-panel flex flex-col border-r border-slate-800/50 transition-all duration-300 z-50 relative">
      <div className="p-4 flex items-center justify-center md:justify-start gap-3 border-b border-slate-800/50 mb-4 h-20">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#B200FF] to-[#00E5FF] flex items-center justify-center shadow-[0_0_15px_rgba(0,229,255,0.4)] flex-shrink-0">
          <Compass className="text-white w-6 h-6" />
        </div>
        <h1 className="hidden md:block font-bold text-xl tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">ATLAS</h1>
      </div>
      
      <nav className="flex flex-col gap-2 p-2 flex-grow">
        <SidebarItem href="/chat" icon={<MessageSquare size={20} />} label="Chat" active />
        <SidebarItem href="/library" icon={<Library size={20} />} label="Library" />
        <SidebarItem href="/dashboard" icon={<LayoutDashboard size={20} />} label="Memory" />
        <SidebarItem href="/search" icon={<Compass size={20} />} label="Explore" />
      </nav>

      <div className="p-2 border-t border-slate-800/50 mt-auto h-20 flex items-center">
        <SidebarItem href="/settings" icon={<Settings size={20} />} label="Settings" />
      </div>
    </div>
  );
}

function SidebarItem({ href, icon, label, active = false }: { href: string, icon: React.ReactNode, label: string, active?: boolean }) {
  return (
    <Link 
      href={href}
      className={`flex items-center gap-4 p-3 rounded-xl transition-all duration-300 group overflow-hidden whitespace-nowrap
        ${active 
          ? 'bg-gradient-to-r from-[#B200FF]/20 to-transparent border-l-2 border-[#B200FF] text-white' 
          : 'text-slate-400 hover:bg-slate-800/50 hover:text-white'
        }
      `}
    >
      <div className={`flex items-center justify-center ${active ? 'text-[#00E5FF] neon-text' : 'group-hover:text-[#00E5FF]'}`}>
        {icon}
      </div>
      <span className="hidden md:block font-medium tracking-wide">{label}</span>
    </Link>
  );
}
