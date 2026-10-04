import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ScanResult } from '../types/neuroPulse';

type ResultPanelProps = {
  result: ScanResult;
};

const secondaryScores = (score: number) => ({
  focus: Math.max(20, Math.round(100 - score * 0.35)),
  recovery: Math.max(10, Math.round(100 - score * 0.7)),
  stress: Math.min(100, Math.round(score)),
  energy: Math.max(15, Math.round(100 - score * 0.45)),
  balance: Math.max(20, Math.round(100 - Math.abs(50 - score) * 1.2)),
});

export function ResultPanel({ result }: ResultPanelProps) {
  const metrics = secondaryScores(result.score);
  const [missionProgress, setMissionProgress] = useState(0);
  const [missionStarted, setMissionStarted] = useState(false);
  const [missionDone, setMissionDone] = useState(false);

  useEffect(() => {
    if (!missionStarted || missionDone) {
      return;
    }

    const timer = window.setInterval(() => {
      setMissionProgress((current) => {
        if (current >= 100) {
          window.clearInterval(timer);
          setMissionDone(true);
          return 100;
        }
        return Math.min(100, current + 4);
      });
    }, 120);

    return () => window.clearInterval(timer);
  }, [missionStarted, missionDone]);

  const startMission = () => {
    setMissionStarted(true);
    setMissionDone(false);
    setMissionProgress(0);
  };

  return (
    <div className="result-panel">
      <div className="result-hero">
        <div>
          <div className="eyebrow">YOUR NEUROPULSE</div>
          <h2>{result.score} / 100</h2>
          <h3>{result.state.toUpperCase()}</h3>
          <p>“Your current lifestyle pattern suggests a moderately elevated mental-load state.”</p>
        </div>
        <motion.div
          className="score-ring"
          initial={{ scale: 0.92, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.45 }}
        >
          <span>{result.score}</span>
          <small>/ 100</small>
        </motion.div>
      </div>

      <div className="result-grid">
        {Object.entries(metrics).map(([label, value]) => (
          <div key={label} className="result-card">
            <span>{label.toUpperCase()}</span>
            <strong>{value}%</strong>
          </div>
        ))}
      </div>

      <section className="insight-section">
        <h4>WHY THIS RESULT?</h4>
        <div className="decision-path">
          {result.decision_path.map((step, index) => (
            <motion.div
              key={step}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.15 }}
              className="path-step"
            >
              {step}
            </motion.div>
          ))}
        </div>
      </section>

      <section className="insight-section">
        <h4>Key contributors to this prediction</h4>
        <div className="factor-grid">
          {result.top_factors.map((factor) => (
            <div key={factor.feature} className="factor-card">
              <span>{factor.feature.replace('_', ' ')}</span>
              <strong>{factor.value}</strong>
              <small>{factor.impact}</small>
            </div>
          ))}
        </div>
      </section>

      <section className="mission-card">
        <div>
          <div className="eyebrow">TODAY'S NEURO MISSION</div>
          <p>Try a 15-minute screen-free break and move a little earlier than usual tonight.</p>
          <div className="mission-meter" aria-live="polite">
            <div className="mission-meter-fill" style={{ width: `${missionProgress}%` }} />
          </div>
          <small className="subtle">
            {missionDone
              ? 'Mission complete. Small routines like this help you track consistent recovery habits.'
              : missionStarted
                ? `Mission in progress: ${missionProgress}%`
                : 'Start the mission to launch a small guided recovery goal.'}
          </small>
        </div>
        <button className="secondary-action" onClick={startMission}>
          {missionDone ? 'START AGAIN' : missionStarted ? 'RESTART MISSION' : 'START MISSION'}
        </button>
      </section>
    </div>
  );
}
