* {
  box-sizing: border-box;
}

:root {
  --bg: #09111f;
  --bg-soft: #101c2d;
  --panel: rgba(16, 27, 40, 0.8);
  --panel-alt: #12263d;
  --border: rgba(146, 180, 208, 0.18);
  --text: #ebf3ff;
  --muted: #a9bfd9;
  --green: #64d5a6;
  --blue: #6ea8ff;
  --gold: #f5c97f;
  --purple: #b69dff;
  --danger: #ff7a7a;
}

html, body {
  margin: 0;
  min-height: 100%;
  background: linear-gradient(180deg, #07111c 0%, #0d1825 100%);
  color: var(--text);
  font-family: Inter,Segoe UI, sans-serif;
}

body {
  min-height: 100vh;
}

.app-shell {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
}

.sidebar {
  background: rgba(16, 26, 38, 0.9);
  border-right: 1px solid var(--border);
  padding: 28px 20px;
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 28px;
}

.brand-mark {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--green), var(--blue));
  display: grid;
  place-items: center;
  font-size: 22px;
  font-weight: 800;
  color: #041722;
}

.brand-block h1 {
  margin: 0;
  font-size: 1.4rem;
}

.brand-block p {
  margin: 4px 0 0;
  color: var(--muted);
  font-size: 0.75rem;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  text-decoration: none;
  color: var(--muted);
  padding: 12px 14px;
  border-radius: 10px;
  transition: 0.2s ease;
}

.nav-item.active,
.nav-item:hover {
  background: rgba(110, 168, 255, 0.14);
  color: var(--text);
}

.sidebar-card {
  margin-top: 30px;
  padding: 16px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: 16px;
}

.sidebar-card label {
  display: block;
  color: var(--muted);
  margin-bottom: 6px;
}

.main-panel {
  padding: 28px;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
}

.eyebrow {
  margin: 0 0 8px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 0.7rem;
}

.topbar h2 {
  margin: 0;
  font-size: clamp(1.5rem, 2vw, 2.2rem);
}

.primary-button {
  border: none;
  background: linear-gradient(135deg, var(--green), var(--blue));
  color: #061a2b;
  font-weight: 700;
  padding: 12px 18px;
  border-radius: 10px;
  cursor: pointer;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(180px, 1fr));
  gap: 18px;
  margin-bottom: 22px;
}

.stat-card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 18px;
  min-height: 120px;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: "";
  position: absolute;
  inset: 0 auto 0 0;
  width: 6px;
  background: currentColor;
}

.stat-card.accent-green { color: var(--green); }
.stat-card.accent-blue { color: var(--blue); }
.stat-card.accent-gold { color: var(--gold); }
.stat-card.accent-purple { color: var(--purple); }

.stat-card .label {
  display: block;
  color: var(--muted);
  margin-bottom: 18px;
  font-size: 0.82rem;
}

.stat-card strong {
  font-size: clamp(1.5rem, 3vw, 2.1rem);
}

.stat-card small {
  display: inline-block;
  margin-left: 6px;
  font-size: 0.8rem;
  color: var(--muted);
}

.content-grid {
  display: grid;
  grid-template-columns: 1.7fr 1fr;
  gap: 18px;
  margin-bottom: 18px;
}

.panel {
  background: rgba(15, 24, 35, 0.9);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 18px;
}

.large-panel {
  min-height: 340px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.05rem;
}

.chip {
  padding: 6px 10px;
  border-radius: 999px;
  color: var(--text);
  border: 1px solid var(--border);
  background: rgba(110, 168, 255, 0.08);
  font-size: 0.7rem;
}

.chip.success {
  border-color: rgba(100, 213, 166, 0.25);
  background: rgba(100, 213, 166, 0.09);
}

.forecast-bars {
  display: flex;
  align-items: end;
  gap: 8px;
  height: 245px;
  padding-top: 10px;
}

.bar-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: end;
  align-items: center;
  gap: 8px;
  min-width: 18px;
}

.bar {
  width: 100%;
  max-width: 22px;
  border-radius: 10px 10px 4px 4px;
  background: linear-gradient(180deg, var(--blue), var(--green));
  opacity: 0.95;
}

.bar-label {
  font-size: 0.6rem;
  color: var(--muted);
}

.recommendations-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recommendations-list li {
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border);
}

.recommendations-list strong {
  display: block;
  margin-bottom: 4px;
}

.recommendations-list span {
  color: var(--muted);
  font-size: 0.84rem;
}

.bottom-panel table {
  width: 100%;
  border-collapse: collapse;
}

.bottom-panel th,
.bottom-panel td {
  text-align: left;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  color: var(--muted);
}

.bottom-panel th {
  color: var(--text);
  font-weight: 600;
}

.bottom-panel tbody tr:last-child td {
  border-bottom: none;
}

@media (max-width: 980px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, minmax(140px, 1fr));
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}
