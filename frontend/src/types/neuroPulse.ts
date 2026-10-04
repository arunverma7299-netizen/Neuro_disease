export type AppView = 'scan' | 'result' | 'history' | 'model' | 'whatif';

export type ScanInputs = {
  sleep_hours: number;
  sleep_quality: number;
  screen_time: number;
  work_hours: number;
  exercise_minutes: number;
  caffeine: number;
  water_intake: number;
  stress_level: number;
  social_activity: number;
  resting_heart_rate: number;
};

export type FactorImpact = {
  feature: string;
  value: number;
  impact: 'positive' | 'negative' | 'contextual';
};

export type ScanResult = {
  score: number;
  state: 'Calm' | 'Balanced' | 'Strained' | 'Overloaded';
  confidence: number;
  top_factors: FactorImpact[];
  decision_path: string[];
  model_version: string;
  message?: string | null;
};
