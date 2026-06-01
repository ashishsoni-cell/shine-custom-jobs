import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

const container = document.getElementById('root');
if (!container) {
  throw new Error('Root container not found. Add <div id="root"></div> to index.html.');
}

const root = createRoot(container);
root.render(<App />);
