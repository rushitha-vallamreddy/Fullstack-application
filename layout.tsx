@import "tailwindcss";

:root {
  --bg: #1e1e1e;
  --bg-2: #252526;
  --bg-3: #2d2d2d;
  --bg-hover: #333334;
  --border: #3e3e3e;
  --text: #e8e8e8;
  --text-dim: #a0a0a0;
  --text-mute: #6e6e6e;
  --accent: #ff6c37;
  --accent-hover: #ff8458;
  --green: #6bdd9a;
  --blue: #4aa3df;
  --yellow: #f2c94c;
  --red: #ff6b6b;
  --purple: #b794f4;
}

@theme inline {
  --color-bg: var(--bg);
  --color-bg-2: var(--bg-2);
  --color-bg-3: var(--bg-3);
  --color-border: var(--border);
  --color-text: var(--text);
  --color-text-dim: var(--text-dim);
  --color-accent: var(--accent);
  --font-sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, "JetBrains Mono", Menlo, monospace;
}

* { box-sizing: border-box; }
html, body { height: 100%; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-sans);
  font-size: 13px;
  -webkit-font-smoothing: antialiased;
}

/* Scrollbars */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3a3a3a; border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: #4a4a4a; }

/* Method colors */
.m-GET { color: var(--green); }
.m-POST { color: var(--yellow); }
.m-PUT { color: var(--blue); }
.m-PATCH { color: var(--purple); }
.m-DELETE { color: var(--red); }
.m-HEAD, .m-OPTIONS { color: var(--text-dim); }

/* JSON syntax highlight */
.json-key { color: #9cdcfe; }
.json-string { color: #ce9178; }
.json-number { color: #b5cea8; }
.json-bool { color: #569cd6; }
.json-null { color: #569cd6; }

/* Inputs reset */
input, select, textarea, button {
  font: inherit;
  color: inherit;
  background: transparent;
  border: none;
  outline: none;
}
input::placeholder, textarea::placeholder { color: var(--text-mute); }

button { cursor: pointer; }

/* Tabs */
.tab-active { background: var(--bg); border-top: 2px solid var(--accent); }

/* Resizer */
.resizer {
  width: 4px;
  cursor: col-resize;
  background: transparent;
}
.resizer:hover { background: var(--accent); }
