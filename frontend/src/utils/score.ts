export function classifyScore(score: number): 'Calm' | 'Balanced' | 'Strained' | 'Overloaded' {
  if (score <= 30) return 'Calm';
  if (score <= 50) return 'Balanced';
  if (score <= 70) return 'Strained';
  return 'Overloaded';
}
