import { ScanInputs, ScanResult } from '../types/neuroPulse';

export type HistoryEntry = {
  id: number;
  created_at: string;
  score: number;
  state: string;
  sleep_hours: number;
  screen_time: number;
  exercise_minutes: number;
  stress_level: number;
  model_version: string;
};

export type HistoryResponse = {
  entries: HistoryEntry[];
};

export type ModelInfoResponse = {
  model_name: string;
  model_version: string;
  status: string;
  description: string;
  best_model?: string | null;
  metrics: Record<string, number>;
  feature_names: string[];
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function predictScan(inputs: ScanInputs): Promise<ScanResult> {
  return request<ScanResult>('/predict', {
    method: 'POST',
    body: JSON.stringify(inputs),
  });
}

export function simulateScan(inputs: ScanInputs): Promise<ScanResult> {
  return request<ScanResult>('/simulate', {
    method: 'POST',
    body: JSON.stringify(inputs),
  });
}

export function fetchModelInfo() {
  return request<ModelInfoResponse>('/model-info');
}

export function fetchHistory() {
  return request<HistoryResponse>('/history');
}
