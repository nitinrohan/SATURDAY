// Single source of truth for where the backend lives.
//
// - Local dev: talks to the Flask server on :10000.
// - Split deploy (Vercel frontend + Render backend): set REACT_APP_API_URL
//   in Vercel to the Render URL, e.g. https://saturday-backend.onrender.com
// - Single-service deploy (Flask serves the build): leave REACT_APP_API_URL
//   unset and it falls back to same-origin.
const isLocalhost =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1";

export const API_BASE =
  process.env.REACT_APP_API_URL ||
  (isLocalhost ? "http://localhost:10000" : window.location.origin);
