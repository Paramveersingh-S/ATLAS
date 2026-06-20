import React, { useState } from 'react';
import { Send, Paperclip, Mic } from 'lucide-react';

interface ContextBarProps {
  onSendMessage: (msg: string) => void;
  isLoading: boolean;
}

export default function ContextBar({ onSendMessage, isLoading }: ContextBarProps) {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="p-4 bg-transparent w-full max-w-4xl mx-auto z-10 relative">
      <div className="glass-panel bg-slate-900/60 rounded-2xl p-2 flex items-end gap-2 border border-slate-700/60 shadow-[0_0_30px_rgba(0,0,0,0.5)]">
        
        <button className="p-3 rounded-xl text-slate-400 hover:bg-slate-800/80 hover:text-[#00E5FF] transition-all">
          <Paperclip size={20} />
        </button>
        
        <textarea
          className="flex-1 max-h-40 min-h-[44px] bg-transparent border-none focus:outline-none focus:ring-0 resize-none text-slate-200 py-3 px-2"
          placeholder="Ask ATLAS anything..."
          value={input}
          rows={1}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />

        <button className="p-3 rounded-xl text-slate-400 hover:bg-slate-800/80 transition-all hidden sm:block">
          <Mic size={20} />
        </button>

        <button 
          onClick={handleSend}
          disabled={!input.trim() || isLoading}
          className={`p-3 rounded-xl transition-all duration-300 flex items-center justify-center flex-shrink-0
            ${input.trim() && !isLoading
              ? 'bg-gradient-to-r from-[#B200FF] to-[#00E5FF] text-white shadow-[0_0_15px_rgba(0,229,255,0.5)] scale-105' 
              : 'bg-slate-800 text-slate-500 cursor-not-allowed'}
          `}
        >
          <Send size={20} className={input.trim() && !isLoading ? 'ml-1' : ''} />
        </button>
        
      </div>
      <p className="text-center text-xs text-slate-500 mt-3 font-mono tracking-wider">TurboQuant Engine Active • Infinite Context Available</p>
    </div>
  );
}
