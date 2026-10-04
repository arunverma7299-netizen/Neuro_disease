import { useMemo, useState } from 'react';
import { Brain, History, Sparkles, FileText, Settings2, ArrowRight, ShieldAlert } from 'lucide-react';
import { motion } from 'framer-motion';
import { BrainGlow } from './components/BrainGlow';
import { ScanFlow } from './components/ScanFlow';
import { ResultPanel } from './components/ResultPanel';
import { HistoryPage } from './pages/HistoryPage';
import { ModelInfoPage } from './pages/ModelInfoPage';
import { WhatIfPage } from './pages/WhatIfPage';
import { predictScan } from './services/api';
import { AppView, ScanResult, ScanInputs } from './types/neuroPulse';

const initialInputs: ScanInputs = {
  sleep_hours: 7,
  sleep_quality: 7,
  screen_time: 6.2,
  work_hours: 7.5,
  exercise_minutes: 30,
  caffeine: 2,
  water_intake: 2.5,
  stress_level: 5,
  social_activity: 2.5,
  resting_heart_rate: 68,
};

const navItems: { key: AppView; label: string; icon: typeof Brain }[] = [
  { key: 'scan', label: 'NeuroScan', icon: Sparkles },
  { key: 'result', label: 'Result', icon: Brain },
  { key: 'history', label: 'Journey', icon: History },
  { key: 'model', label: 'Inside the AI', icon: FileText },
  { key: 'whatif', label: 'What-If', icon: Settings2 },
];

const demoResult: ScanResult = {
  score: 68,
  state: 'Strained',
  confidence: 0.84,
  top_factors: [
    { feature: 'sleep_hours', value: 5.5, impact: 'negative' },
    { feature: 'screen_time', value: 8.1, impact: 'negative' },
    { feature: 'stress_level', value: 7, impact: 'negative' },
  ],
  decision_path: ['Sleep duration is below the learned threshold', 'Screen time is relatively high', 'Stress level is elevated'],
  model_version: 'v0.1.0',
  message: 'This is a local preview until the trained model artifact is connected.',
};

export default function App() {
  const [view, setView] = useState<AppView>('scan');
  const [inputs, setInputs] = useState<ScanInputs>(initialInputs);
  const [result, setResult] = useState<ScanResult>(demoResult);
  const [scanStarted, setScanStarted] = useState(false);

  const scoreTone = useMemo(() => {
    if (result.score <= 30) return 'calm';
    if (result.score <= 50) return 'balanced';
    if (result.score <= 70) return 'strained';
    return 'overloaded';
  }, [result.score]);

  const localEstimate = (payload: ScanInputs): ScanResult => {
    const score = Math.min(100, Math.max(0, Math.round(100 - payload.sleep_hours * 8 + payload.screen_time * 4 + payload.stress_level * 6 - payload.exercise_minutes / 6)));
    const state = score <= 30 ? 'Calm' : score <= 50 ? 'Balanced' : score <= 70 ? 'Strained' : 'Overloaded';
    return {
      ...demoResult,
      score,
      state,
      confidence: 0.82,
      top_factors: [
        { feature: 'sleep_hours', value: payload.sleep_hours, impact: payload.sleep_hours >= 7 ? 'positive' : 'negative' },
        { feature: 'screen_time', value: payload.screen_time, impact: payload.screen_time >= 7 ? 'negative' : 'positive' },
        { feature: 'stress_level', value: payload.stress_level, impact: payload.stress_level >= 6 ? 'negative' : 'positive' },
      ],
      decision_path: [
        payload.sleep_hours < 6 ? 'Sleep duration is below the learned threshold' : 'Sleep duration is in the learned range',
        payload.screen_time > 7 ? 'Screen time is relatively high' : 'Screen time is within a lower range',
        payload.stress_level > 6 ? 'Stress level is elevated' : 'Stress level is moderate',
      ],
      message: 'Generated locally while the trained model artifact is unavailable.',
    };
  };

  const handleCompleteScan = async (payload: ScanInputs) => {
    setInputs(payload);
    setScanStarted(true);
    try {
      const apiResult = await predictScan(payload);
      setResult(apiResult);
    } catch {
      setResult(localEstimate(payload));
    }
    setView('result');
  };

  return (
    <div className={`app-shell tone-${scoreTone}`}>
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />
      <header className="topbar">
        <div className="brand-lockup">
          <div className="brand-mark">
            <Brain size={18} />
          </div>
          <div>
            <div className="eyebrow">NEUROPULSE</div>
            <div className="subtle">Understand your mind. One day at a time.</div>
          </div>
        </div>
        <nav className="topnav" aria-label="Primary navigation">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button key={item.key} className={`nav-pill ${view === item.key ? 'active' : ''}`} onClick={() => setView(item.key)}>
                <Icon size={14} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </header>

      <main className="layout">
        <section className="hero-panel glass-panel">
          <div className="hero-copy">
            <span className="badge">
              <ShieldAlert size={14} /> Educational lifestyle insights only
            </span>
            <h1>
              NEUROPULSE
              <span>Understand your mind.</span>
              <span>One day at a time.</span>
            </h1>
            <p>
              An interactive AI-powered snapshot of how your daily habits may be influencing your current mental load.
              Not a diagnosis. Not a medical decision engine.
            </p>
            <div className="hero-actions">
              <button className="primary-action" onClick={() => setView('scan')}>
                START NEUROSCAN <ArrowRight size={16} />
              </button>
              <button className="secondary-action" onClick={() => setView('model')}>
                HOW IT WORKS
              </button>
            </div>
            <div className="hero-stats">
              <div>
                <strong>{result.score} / 100</strong>
                <span>Current mental-load estimate</span>
              </div>
              <div>
                <strong>{result.state.toUpperCase()}</strong>
                <span>Educational state</span>
              </div>
              <div>
                <strong>{Math.round(result.confidence * 100)}%</strong>
                <span>Model confidence</span>
              </div>
            </div>
          </div>
          <motion.div
            className="hero-brain-wrap"
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
          >
            <BrainGlow score={result.score} scanStarted={scanStarted} />
          </motion.div>
        </section>

        <section className="workspace glass-panel">
          {view === 'scan' && <ScanFlow inputs={inputs} onComplete={handleCompleteScan} onPreviewChange={setInputs} />}
          {view === 'result' && <ResultPanel result={result} />}
          {view === 'history' && <HistoryPage />}
          {view === 'model' && <ModelInfoPage />}
          {view === 'whatif' && <WhatIfPage currentInputs={inputs} onSimulate={handleCompleteScan} currentResult={result} />}
        </section>
      </main>
    </div>
  );
}
