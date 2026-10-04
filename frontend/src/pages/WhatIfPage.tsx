import { useMemo, useState } from 'react';
import { ScanInputs, ScanResult } from '../types/neuroPulse';

type WhatIfPageProps = {
  currentInputs: ScanInputs;
  currentResult: ScanResult;
  onSimulate: (inputs: ScanInputs) => void;
};

export function WhatIfPage({ currentInputs, currentResult, onSimulate }: WhatIfPageProps) {
  const [draft, setDraft] = useState<ScanInputs>(currentInputs);
  const simulatedScore = useMemo(() => {
    return Math.min(100, Math.max(0, Math.round(100 - draft.sleep_hours * 8 + draft.screen_time * 4 + draft.stress_level * 6 - draft.exercise_minutes / 6)));
  }, [draft]);

  return (
    <div className="whatif-page">
      <div className="section-head">
        <div className="eyebrow">WHAT IF?</div>
        <h2>Simulate a change</h2>
      </div>
      <div className="whatif-grid">
        <label>
          <span>Sleep</span>
          <input type="range" min={4} max={10} step={0.1} value={draft.sleep_hours} onChange={(event) => setDraft({ ...draft, sleep_hours: Number(event.target.value) })} />
        </label>
        <label>
          <span>Screen time</span>
          <input type="range" min={0} max={14} step={0.1} value={draft.screen_time} onChange={(event) => setDraft({ ...draft, screen_time: Number(event.target.value) })} />
        </label>
        <label>
          <span>Exercise</span>
          <input type="range" min={0} max={120} step={1} value={draft.exercise_minutes} onChange={(event) => setDraft({ ...draft, exercise_minutes: Number(event.target.value) })} />
        </label>
        <label>
          <span>Stress</span>
          <input type="range" min={1} max={10} step={1} value={draft.stress_level} onChange={(event) => setDraft({ ...draft, stress_level: Number(event.target.value) })} />
        </label>
        <label>
          <span>Caffeine</span>
          <input type="range" min={0} max={6} step={1} value={draft.caffeine} onChange={(event) => setDraft({ ...draft, caffeine: Number(event.target.value) })} />
        </label>
      </div>
      <div className="whatif-result">
        <div>
          <span>CURRENT</span>
          <strong>{currentResult.score}</strong>
        </div>
        <div className="arrow-bubble">↓</div>
        <div>
          <span>SIMULATED</span>
          <strong>{simulatedScore}</strong>
        </div>
      </div>
      <button className="primary-action" onClick={() => onSimulate(draft)}>RUN SIMULATION</button>
    </div>
  );
}
