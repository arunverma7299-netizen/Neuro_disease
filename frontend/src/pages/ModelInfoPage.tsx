import { useEffect, useState } from 'react';
import { fetchModelInfo, type ModelInfoResponse } from '../services/api';

const modelItems = [
  {
    title: 'What is a Decision Tree?',
    text: 'A model that splits data into understandable branches based on feature thresholds.',
  },
  {
    title: 'What is Random Forest?',
    text: 'A collection of trees that vote together to improve stability and reduce overfitting.',
  },
  {
    title: 'What is cross-validation?',
    text: 'A repeated train-test process that checks how well the model generalizes across folds.',
  },
];

export function ModelInfoPage() {
  const [modelInfo, setModelInfo] = useState<Partial<ModelInfoResponse>>({});

  useEffect(() => {
    fetchModelInfo()
      .then((data) => setModelInfo(data))
      .catch(() => setModelInfo({ status: 'unavailable', description: 'The backend is not reachable right now.' }));
  }, []);

  return (
    <div className="model-page">
      <div className="section-head">
        <div className="eyebrow">INSIDE THE AI</div>
        <h2>Model transparency</h2>
      </div>
      <div className="model-grid">
        {modelItems.map((item) => (
          <article key={item.title} className="info-card">
            <h3>{item.title}</h3>
            <p>{item.text}</p>
          </article>
        ))}
      </div>
      <section className="info-card highlight-card">
        <h3>Best model</h3>
        <p>{modelInfo.best_model ?? 'The final selected model will be shown here after Phase 4 training and comparison are complete.'}</p>
        <p className="subtle">Status: {modelInfo.status ?? 'unknown'}</p>
        {modelInfo.description ? <p>{modelInfo.description}</p> : null}
      </section>
    </div>
  );
}
