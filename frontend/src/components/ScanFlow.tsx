import { useMemo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, Activity, Droplets, MoonStar, Cpu, Shield, Smile } from 'lucide-react';
import { ScanInputs } from '../types/neuroPulse';

type ScanFlowProps = {
  inputs: ScanInputs;
  onComplete: (inputs: ScanInputs) => void;
  onPreviewChange: (inputs: ScanInputs) => void;
};

const questions: Array<{ key: keyof ScanInputs; title: string; subtitle: string; type: 'range' | 'choice'; min?: number; max?: number; step?: number; choices?: number[] }> = [
  { key: 'sleep_hours', title: 'How long did you sleep last night?', subtitle: 'A little more rest often moves the needle.', type: 'choice', choices: [4, 5, 6, 7, 8, 9] },
  { key: 'sleep_quality', title: 'How restorative did sleep feel?', subtitle: 'This is your personal quality signal.', type: 'choice', choices: [1, 3, 5, 7, 9] },
  { key: 'screen_time', title: 'How much screen time did you have?', subtitle: 'We keep this smooth and touch-friendly.', type: 'range', min: 0, max: 14, step: 0.1 },
  { key: 'work_hours', title: 'How mentally demanding was the day?', subtitle: 'Work or study load is a strong context signal.', type: 'range', min: 0, max: 14, step: 0.1 },
  { key: 'exercise_minutes', title: 'How much movement did you get?', subtitle: 'Even small movement matters to the model.', type: 'range', min: 0, max: 120, step: 1 },
  { key: 'caffeine', title: 'How much caffeine did you have?', subtitle: 'A simple input with a visible effect.', type: 'choice', choices: [0, 1, 2, 3, 4, 5] },
  { key: 'water_intake', title: 'How much water did you drink?', subtitle: 'Hydration helps frame the lifestyle pattern.', type: 'range', min: 0.5, max: 5, step: 0.1 },
  { key: 'stress_level', title: 'How stressed did today feel?', subtitle: 'Self-reported stress is a major signal.', type: 'choice', choices: [1, 3, 5, 7, 9] },
  { key: 'social_activity', title: 'How socially active was the day?', subtitle: 'Social context changes the scan story.', type: 'range', min: 0, max: 10, step: 0.1 },
  { key: 'resting_heart_rate', title: 'What was your resting heart rate?', subtitle: 'Used here as a wellness context input only.', type: 'range', min: 48, max: 95, step: 1 },
];

export function ScanFlow({ inputs, onComplete, onPreviewChange }: ScanFlowProps) {
  const [index, setIndex] = useState(0);
  const [localInputs, setLocalInputs] = useState<ScanInputs>(inputs);

  const question = questions[index];
  const progress = ((index + 1) / questions.length) * 100;

  const helperIcon = useMemo(() => {
    switch (question.key) {
      case 'sleep_hours': return <MoonStar size={18} />;
      case 'exercise_minutes': return <Activity size={18} />;
      case 'water_intake': return <Droplets size={18} />;
      case 'resting_heart_rate': return <Shield size={18} />;
      case 'stress_level': return <Cpu size={18} />;
      default: return <Smile size={18} />;
    }
  }, [question.key]);

  const updateValue = (value: number) => {
    const next = { ...localInputs, [question.key]: value } as ScanInputs;
    setLocalInputs(next);
    onPreviewChange(next);
  };

  const next = () => {
    if (index === questions.length - 1) {
      onComplete(localInputs);
      return;
    }
    setIndex((current) => current + 1);
  };

  const back = () => setIndex((current) => Math.max(0, current - 1));

  return (
    <div className="scan-flow">
      <div className="scan-header">
        <div>
          <div className="eyebrow">NEUROSCAN</div>
          <h2>Question {index + 1} / {questions.length}</h2>
        </div>
        <div className="scan-progress-ring" aria-hidden="true">
          <div className="scan-progress-fill" style={{ width: `${progress}%` }} />
          <span>{Math.round(progress)}%</span>
        </div>
      </div>

      <div className="scan-progress-bar" aria-hidden="true">
        <div style={{ width: `${progress}%` }} />
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={question.key}
          initial={{ opacity: 0, x: 24, filter: 'blur(6px)' }}
          animate={{ opacity: 1, x: 0, filter: 'blur(0px)' }}
          exit={{ opacity: 0, x: -24, filter: 'blur(6px)' }}
          transition={{ duration: 0.35 }}
          className="question-card"
        >
          <div className="question-icon">{helperIcon}</div>
          <h3>{question.title}</h3>
          <p>{question.subtitle}</p>

          {question.type === 'range' && (
            <div className="range-block">
              <input
                type="range"
                min={question.min}
                max={question.max}
                step={question.step}
                value={localInputs[question.key]}
                onChange={(event) => updateValue(Number(event.target.value))}
                aria-label={question.title}
              />
              <div className="range-meta">
                <span>{question.min}</span>
                <strong>{Number(localInputs[question.key]).toFixed(question.step && question.step < 1 ? 1 : 0)}</strong>
                <span>{question.max}</span>
              </div>
            </div>
          )}

          {question.type === 'choice' && question.choices && (
            <div className="choice-grid" role="group" aria-label={question.title}>
              {question.choices.map((choice) => (
                <button
                  key={choice}
                  type="button"
                  className={`choice-chip ${localInputs[question.key] === choice ? 'active' : ''}`}
                  onClick={() => updateValue(choice)}
                >
                  {choice}{question.key === 'sleep_hours' ? 'h' : question.key === 'stress_level' ? '/10' : ''}
                </button>
              ))}
            </div>
          )}
        </motion.div>
      </AnimatePresence>

      <div className="scan-footer">
        <button type="button" className="ghost-action" onClick={back} disabled={index === 0}>
          <ChevronLeft size={16} /> Back
        </button>
        <button type="button" className="primary-action" onClick={next}>
          {index === questions.length - 1 ? 'ANALYZE' : 'NEXT'} <ChevronRight size={16} />
        </button>
      </div>
    </div>
  );
}
