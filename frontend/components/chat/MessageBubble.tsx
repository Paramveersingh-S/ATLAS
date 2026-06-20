import React from 'react';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';
import { Bot, User } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant' | string;
  content: string;
}

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';
  
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`flex gap-4 max-w-[85%] md:max-w-[75%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        
        {/* Avatar */}
        <div className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 ${
          isUser 
            ? 'bg-slate-800 border border-slate-700/50' 
            : 'bg-gradient-to-br from-[#B200FF] to-[#00E5FF] shadow-[0_0_15px_rgba(0,229,255,0.3)]'
        }`}>
          {isUser ? <User size={16} className="text-slate-300" /> : <Bot size={18} className="text-white" />}
        </div>
        
        {/* Bubble Content */}
        <div className={`px-5 py-4 rounded-2xl ${
          isUser 
            ? 'glass-panel rounded-tr-sm bg-[#B200FF]/10 border-[#B200FF]/30' 
            : 'glass-panel rounded-tl-sm bg-slate-900/60 border-slate-700/50'
        }`}>
          <div className="prose prose-invert prose-p:leading-relaxed prose-p:my-1 max-w-none prose-pre:bg-slate-950/80 prose-pre:border prose-pre:border-slate-800 prose-pre:shadow-inner prose-code:text-[#00E5FF]">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        </div>
        
      </div>
    </motion.div>
  );
}
