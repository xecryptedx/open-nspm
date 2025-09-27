import { useEffect, useState } from 'react';

interface Finding {
  id: number;
  summary: string;
  severity: string;
}

function App() {
  const [status, setStatus] = useState<string>('Connecting...');

  useEffect(() => {
    fetch('/v1/health', { headers: { 'x-api-key': import.meta.env.VITE_API_KEY ?? '' } })
      .then((res) => (res.ok ? res.json() : Promise.reject(new Error('failed'))))
      .then((body) => setStatus(body.status ?? 'ok'))
      .catch(() => setStatus('offline'));
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      <header className="bg-slate-800 py-6 shadow">
        <div className="mx-auto max-w-5xl px-6">
          <h1 className="text-3xl font-semibold">OpenNSPM</h1>
          <p className="text-sm text-slate-300">Fortinet policy visibility & hygiene</p>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-6 py-10">
        <section className="rounded-lg bg-slate-800 p-6 shadow-lg">
          <h2 className="text-xl font-semibold">API Status</h2>
          <p className="mt-2 text-slate-300">Backend health: {status}</p>
        </section>
      </main>
    </div>
  );
}

export default App;
