const API_BASE = "/api";

window._lastMode = null;

async function loadRisk(criticalZone) {
  window._lastMode = criticalZone;
  const container = document.getElementById("zone-cards");
  container.innerHTML = '<div class="loading-msg">Scanning zones...</div>';

  const url = criticalZone
    ? `${API_BASE}/risk-scan?inject_critical=${encodeURIComponent(criticalZone)}`
    : `${API_BASE}/risk-scan`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    renderZoneCards(data);
    updateSummary(data);
  } catch (err) {
    container.innerHTML = '<div class="loading-msg">Could not reach backend. Make sure Flask is running on port 5000.</div>';
  }
}

function renderZoneCards(results) {
  const container = document.getElementById("zone-cards");
  container.innerHTML = "";

  results.forEach(zone => {
    const card = document.createElement("div");
    card.className = `zone-card ${zone.risk_level}`;

    const reading = zone.sensor_reading;
    const alertText = zone.ai_alert?.alert || "";
    const triggers = zone.compound_triggers || [];

    const triggerTags = triggers.map(t =>
      `<span class="compound-tag">${t.type.replace(/_/g, " ")}</span>`
    ).join("");

    card.innerHTML = `
      <div class="zone-card-header">
        <span class="zone-name">${zone.zone}</span>
        <span class="risk-badge badge-${zone.risk_level}">${zone.risk_level}</span>
      </div>
      <div class="zone-readings">
        <span>Gas LEL <strong>${reading.gas_lel_percent}%</strong></span>
        <span>O₂ <strong>${reading.oxygen_percent}%</strong></span>
        <span>CO <strong>${reading.co_ppm} ppm</strong></span>
        <span>Temp <strong>${reading.temperature_celsius}°C</strong></span>
      </div>
      ${triggerTags ? `<div style="margin-top:6px">${triggerTags}</div>` : ""}
      ${alertText && alertText !== "Safe" ? `<div class="zone-alert">${alertText}</div>` : ""}
    `;

    container.appendChild(card);
  });
}

function updateSummary(results) {
  const counts = { CRITICAL: 0, WARNING: 0, SAFE: 0 };
  results.forEach(z => {
    counts[z.risk_level] = (counts[z.risk_level] || 0) + 1;
  });

  document.getElementById("count-critical").textContent = counts.CRITICAL || 0;
  document.getElementById("count-warning").textContent = counts.WARNING || 0;
  document.getElementById("count-safe").textContent = counts.SAFE || 0;

  const now = new Date();
  document.getElementById("last-scan").textContent =
    now.getHours().toString().padStart(2, "0") + ":" +
    now.getMinutes().toString().padStart(2, "0");
}

async function sendQuery() {
  const input = document.getElementById("chat-input");
  const question = input.value.trim();
  if (!question) return;

  const chatWindow = document.getElementById("chat-window");

  const userBubble = document.createElement("div");
  userBubble.className = "chat-msg user-msg";
  userBubble.textContent = question;
  chatWindow.appendChild(userBubble);
  input.value = "";

  const thinkingBubble = document.createElement("div");
  thinkingBubble.className = "chat-msg bot-msg";
  thinkingBubble.textContent = "Searching regulations...";
  chatWindow.appendChild(thinkingBubble);
  chatWindow.scrollTop = chatWindow.scrollHeight;

  try {
    const res = await fetch(`${API_BASE}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });
    const data = await res.json();
    thinkingBubble.textContent = data.answer || "No answer found.";
    if (data.source) {
      const src = document.createElement("div");
      src.style.cssText = "font-size:11px;color:#6b7280;margin-top:6px";
      src.textContent = "Source: " + data.source;
      thinkingBubble.appendChild(src);
    }
  } catch (err) {
    thinkingBubble.textContent = "Could not connect to Safety Copilot. Check backend connection.";
  }

  chatWindow.scrollTop = chatWindow.scrollHeight;
}
