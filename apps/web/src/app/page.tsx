"use client";

import React, { useState, useEffect, useRef } from "react";

export default function Home() {
  const [logs, setLogs] = useState<string[]>([]);
  const [input, setInput] = useState("");
  const wsRef = useRef<WebSocket | null>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Connect to backend WebSocket API
    const ws = new WebSocket("ws://localhost:8000/api/v1/stream/events");
    wsRef.current = ws;

    ws.onopen = () => {
      setLogs((prev) => [...prev, "[SYSTEM] WebSocket connection established."]);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLogs((prev) => [...prev, data.message]);
    };

    ws.onclose = () => {
      setLogs((prev) => [...prev, "[SYSTEM] WebSocket disconnected. Attempting to reconnect..."]);
    };

    return () => {
      ws.close();
    };
  }, []);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const handleCommandSubmit = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && input.trim() !== "") {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(input);
        setInput("");
      }
    }
  };

  const getLogColor = (log: string) => {
    if (log.includes("[SYSTEM]")) return "text-green-500";
    if (log.includes("[WS]")) return "text-gray-400";
    if (log.includes("[AGENT")) return "text-purple-400";
    if (log.includes("[SUCCESS]")) return "text-green-400 glow-text";
    if (log.includes("[ERROR]")) return "text-red-500 font-bold";
    if (log.startsWith(">")) return "text-white font-bold";
    return "text-blue-400";
  };

  return (
    <main className="min-h-screen cyber-grid p-8 flex flex-col relative overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/20 rounded-full blur-[120px] -z-10" />

      <header className="flex justify-between items-center mb-8 glass-panel p-4 rounded-xl">
        <h1 className="text-3xl font-bold glow-text tracking-wider">
          NEURAL<span className="text-secondary">OPS</span>
        </h1>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${wsRef.current?.readyState === WebSocket.OPEN ? "bg-green-500 animate-pulse" : "bg-red-500"}`} />
            <span className={`text-sm font-mono ${wsRef.current?.readyState === WebSocket.OPEN ? "text-green-500" : "text-red-500"}`}>
              {wsRef.current?.readyState === WebSocket.OPEN ? "SYSTEM ONLINE" : "OFFLINE"}
            </span>
          </div>
          <button className="px-4 py-2 bg-white/10 hover:bg-white/20 transition-all rounded font-mono text-sm border border-white/10">
            SETTINGS
          </button>
        </div>
      </header>

      <div className="grid grid-cols-12 gap-6 flex-1 max-h-[calc(100vh-140px)]">
        <section className="col-span-3 glass-panel rounded-xl p-4 flex flex-col gap-4">
          <h2 className="text-xl font-semibold border-b border-white/10 pb-2">Active Agents</h2>
          <div className="flex-1 overflow-y-auto font-mono text-sm space-y-2">
            <div className="p-3 bg-white/5 rounded border border-white/5 flex items-center justify-between hover:bg-white/10 transition-colors cursor-pointer">
              <span>PlannerAgent</span>
              <span className="text-green-400">IDLE</span>
            </div>
            <div className="p-3 bg-white/5 rounded border border-white/5 flex items-center justify-between hover:bg-white/10 transition-colors cursor-pointer">
              <span>ResearchAgent</span>
              <span className="text-blue-400">THINKING</span>
            </div>
            <div className="p-3 bg-white/5 rounded border border-white/5 flex items-center justify-between hover:bg-white/10 transition-colors cursor-pointer">
              <span>MemoryAgent</span>
              <span className="text-purple-400">INDEXING</span>
            </div>
          </div>
        </section>

        <section className="col-span-6 glass-panel rounded-xl p-4 flex flex-col relative">
          <h2 className="text-xl font-semibold border-b border-white/10 pb-2 mb-4">Live Orchestration</h2>
          <div className="flex-1 border border-white/10 rounded-lg flex items-center justify-center bg-black/20">
            <span className="text-white/30 font-mono animate-pulse">React Flow Graph Awaiting Initialization...</span>
          </div>
        </section>

        <section className="col-span-3 glass-panel rounded-xl p-4 flex flex-col gap-4">
          <h2 className="text-xl font-semibold border-b border-white/10 pb-2">Terminal Logs</h2>
          <div className="flex-1 bg-black/60 rounded p-3 font-mono text-xs overflow-y-auto flex flex-col gap-1">
            {logs.map((log, i) => (
              <div key={i} className={`whitespace-pre-wrap ${getLogColor(log)}`}>
                {log}
              </div>
            ))}
            <div ref={logsEndRef} />
          </div>
          <div className="mt-2 relative">
            <span className="absolute left-3 top-2.5 text-primary text-sm font-bold">&gt;</span>
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleCommandSubmit}
              placeholder="cmd / prompt..."
              className="w-full bg-black/50 border border-white/20 rounded py-2 pl-7 pr-3 text-sm font-mono focus:outline-none focus:border-primary transition-colors text-white"
            />
          </div>
        </section>
      </div>
    </main>
  );
}