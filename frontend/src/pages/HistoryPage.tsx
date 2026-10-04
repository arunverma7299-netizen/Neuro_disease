import { useEffect, useState } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { fetchHistory, type HistoryEntry } from '../services/api';

const historyData = [
  { day: 'Mon', score: 72, sleep: 6.1, screen: 8.4, exercise: 20 },
  { day: 'Tue', score: 65, sleep: 6.6, screen: 7.8, exercise: 25 },
  { day: 'Wed', score: 58, sleep: 7.1, screen: 6.4, exercise: 35 },
  { day: 'Thu', score: 61, sleep: 6.8, screen: 7.1, exercise: 30 },
  { day: 'Fri', score: 49, sleep: 7.6, screen: 5.8, exercise: 42 },
];

export function HistoryPage() {
  const [entries, setEntries] = useState<HistoryEntry[]>([]);

  useEffect(() => {
    fetchHistory()
      .then((data) => setEntries(data.entries ?? []))
      .catch(() => setEntries([]));
  }, []);

  return (
    <div className="history-page">
      <div className="section-head">
        <div className="eyebrow">NEURO JOURNEY</div>
        <h2>Previous scans</h2>
      </div>
      <div className="chart-shell">
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={historyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.15)" />
            <XAxis dataKey="day" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip contentStyle={{ background: '#08111f', border: '1px solid rgba(103,232,249,0.18)', borderRadius: 14 }} />
            <Line type="monotone" dataKey="score" stroke="#67e8f9" strokeWidth={3} dot={{ r: 3 }} />
            <Line type="monotone" dataKey="sleep" stroke="#a78bfa" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="screen" stroke="#fb7185" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="history-summary">
        <div className="history-card"><span>Mon</span><strong>72</strong></div>
        <div className="history-card"><span>Tue</span><strong>65</strong></div>
        <div className="history-card"><span>Wed</span><strong>58</strong></div>
        <div className="history-card"><span>Thu</span><strong>61</strong></div>
        <div className="history-card"><span>Fri</span><strong>49</strong></div>
      </div>
      <div className="history-feed">
        {entries.length === 0 ? (
          <p className="subtle">No saved scans yet. Run a NeuroScan to populate your history.</p>
        ) : (
          entries.map((entry) => (
            <div key={entry.id} className="history-card">
              <span>{entry.created_at}</span>
              <strong>{entry.score}</strong>
              <small>{entry.state}</small>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
