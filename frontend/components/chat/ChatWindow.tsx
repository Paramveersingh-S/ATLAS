'use client';
import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import ContextBar from './ContextBar';

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    { id: '1', role: 'assistant', content: 'Hello! I am **ATLAS**, powered by the TurboQuant engine. My mathematically compressed KV Cache allows me to process near-infinite document contexts seamlessly.\n\nWhat would you like to research today?' }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    const newUserMsg = { id: Date.now().toString(), role: 'user', content };
    setMessages(prev => [...prev, newUserMsg]);
    setIsLoading(true);

    const botMsgId = (Date.now() + 1).toString();
    setMessages(prev => [...prev, { id: botMsgId, role: 'assistant', content: '' }]);

    try {
      const response = await fetch('/api/v1/chat/sessions/123/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [...messages, newUserMsg]
        })
      });

      if (!response.body) throw new Error("No response body");
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6).trim();
            if (!dataStr) continue;
            
            try {
              const data = JSON.parse(dataStr);
              if (data.event === 'llm_token') {
                setMessages(prev => prev.map(msg => 
                  msg.id === botMsgId ? { ...msg, content: msg.content + data.data.token } : msg
                ));
              } else if (data.event === 'done') {
                setIsLoading(false);
              }
            } catch (e) {
              console.error("Error parsing SSE data", e);
            }
          }
        }
      }
    } catch (error) {
      console.error("Chat error:", error);
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full relative bg-[#020617] overflow-hidden">
      {/* Background ambient glow */}
      <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-[#B200FF]/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-[#00E5FF]/10 rounded-full blur-[120px] pointer-events-none"></div>

      <div className="flex-1 overflow-y-auto px-4 md:px-8 pt-8 pb-40 z-10" ref={scrollRef}>
        <div className="max-w-4xl mx-auto">
          {messages.map((msg: any) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          {isLoading && (
            <div className="flex gap-2 items-center text-[#00E5FF] neon-text p-4">
              <span className="animate-pulse">●</span>
              <span className="animate-pulse delay-100">●</span>
              <span className="animate-pulse delay-200">●</span>
            </div>
          )}
        </div>
      </div>

      <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-[#020617] via-[#020617]/90 to-transparent pt-12 pb-4 z-20 pointer-events-none">
        <div className="pointer-events-auto">
          <ContextBar onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}
