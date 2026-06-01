const state = {
  currentReport: null,
  history: JSON.parse(localStorage.getItem("travelo_history") || "[]"),
  theme: localStorage.getItem("travelo_theme") || "dark",
};

const $ = (selector) => document.querySelector(selector);
const logoPath = "/static/images/travelo-logo.png";
const messages = $("#messages");
const historyList = $("#historyList");
const welcomeStage = $("#welcomeStage");

function typeText(element, text, speed = 42, cursor = null) {
  element.textContent = "";
  if (cursor) cursor.classList.remove("is-done");
  return new Promise((resolve) => {
    let index = 0;
    const timer = setInterval(() => {
      element.textContent += text[index] || "";
      index += 1;
      if (index > text.length) {
        clearInterval(timer);
        if (cursor) cursor.classList.add("is-done");
        resolve();
      }
    }, speed);
  });
}

async function runIntro() {
  await typeText($("#welcomeText"), "WELCOME TO TRAVELO", 48, $(".hero-card h1 .caret"));
  await new Promise((resolve) => setTimeout(resolve, 260));
  await typeText($("#subheadingText"), "make every trip awesome", 36, $(".subheading .caret"));
}

function saveHistory() {
  localStorage.setItem("travelo_history", JSON.stringify(state.history.slice(0, 12)));
}

function renderHistory() {
  historyList.innerHTML = "";
  if (!state.history.length) {
    historyList.innerHTML = '<div class="empty-history">No saved trips yet. Your reports will appear here.</div>';
    return;
  }
  state.history.forEach((item, index) => {
    const button = document.createElement("button");
    button.className = "history-item";
    button.type = "button";
    button.innerHTML = `<span>${escapeHtml(item.destination || "Trip")}</span><small>${escapeHtml(item.date || "Recent")}</small>`;
    button.addEventListener("click", () => loadHistoryItem(index));
    historyList.appendChild(button);
  });
}

function applyTheme(theme) {
  const safeTheme = theme === "dark" ? "dark" : "light";
  state.theme = safeTheme;
  document.body.dataset.theme = safeTheme;
  localStorage.setItem("travelo_theme", safeTheme);
  const toggle = $("#themeToggle");
  if (!toggle) return;
  const isDark = safeTheme === "dark";
  toggle.setAttribute("aria-pressed", String(isDark));
  toggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
  const label = toggle.querySelector(".theme-label");
  if (label) label.textContent = isDark ? "Light" : "Dark";
}

function loadHistoryItem(index) {
  const item = state.history[index];
  if (!item) return;
  welcomeStage.classList.add("is-hidden");
  messages.innerHTML = "";
  addUserMessage(item.message || `Plan a trip to ${item.destination || "your destination"}`);
  if (item.type === "chat") {
    addAssistantChat(item.answer, false);
  } else {
    addAssistantReport(item.report, false);
    state.currentReport = item.report;
  }
  document.body.classList.remove("sidebar-open");
}

function addUserMessage(text) {
  const bubble = document.createElement("article");
  bubble.className = "message user-message";
  bubble.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
  messages.appendChild(bubble);
  scrollToBottom();
}

function addLoadingMessage() {
  const card = document.createElement("article");
  card.className = "message assistant-message loading-card";
  card.id = "loadingCard";
  card.innerHTML = `
    <div class="assistant-icon"><img class="slow-spin" src="${logoPath}" alt=""></div>
    <div class="report-card compact">
      <div class="tool-loader"><span></span><span></span><span></span></div>
      <h2>Travelo is using tools...</h2>
      <p>Checking weather, news, routes, attractions, budget, crowds, and itinerary agents.</p>
      <div class="tool-steps">
        <span>Attractions</span><span>Budget</span><span>Weather</span><span>News</span><span>Routes</span><span>Crowds</span><span>Itinerary</span>
      </div>
    </div>`;
  messages.appendChild(card);
  scrollToBottom();
}

function removeLoadingMessage() {
  const loading = $("#loadingCard");
  if (loading) loading.remove();
}

function addAssistantReport(plan, persist = true) {
  const report = buildReport(plan);
  state.currentReport = report;
  const card = document.createElement("article");
  card.className = "message assistant-message";
  card.innerHTML = `
    <div class="assistant-icon"><img class="slow-spin" src="${logoPath}" alt=""></div>
    <div class="report-card" id="travelReport">
      ${renderReport(report)}
    </div>`;
  messages.appendChild(card);
  bindExportButton(card, report);
  if (persist) pushHistory(plan, report);
  scrollToBottom();
}

function addAssistantChat(answer, persist = true) {
  const card = document.createElement("article");
  card.className = "message assistant-message";
  card.innerHTML = `
    <div class="assistant-icon"><img class="slow-spin" src="${logoPath}" alt=""></div>
    <div class="report-card compact">
      <h2>Travelo says</h2>
      <ul>${toBullets(splitSummary(answer))}</ul>
    </div>`;
  messages.appendChild(card);
  if (persist) pushChatHistory(answer);
  scrollToBottom();
}

function buildReport(plan) {
  const context = plan.context || {};
  const trip = plan.trip || {};
  const itinerary = context.itinerary || {};
  const days = itinerary.days || [];
  const budget = context.budget || {};
  const weather = context.weather || [];
  const news = context.news || [];
  const route = context.route || {};
  const attractions = context.attractions || [];
  const crowds = context.crowds || [];
  const food = context.food || {};

  return {
    title: `${trip.destination || itinerary.destination || "Your"} Travel Report`,
    destination: trip.destination || itinerary.destination || "Trip",
    summary: plan.manager_summary || itinerary.summary || "Here is your detailed travel plan.",
    meta: [
      `${trip.travelers || 1} traveler(s)`,
      `${trip.start_date || "Start date"} to ${trip.end_date || "End date"}`,
      `Budget: ${budget.input_display || formatMoney(trip.budget || budget.total_budget || 0, budget.currency)}`,
      `Destination currency: ${budget.local_display || formatMoney(budget.local_amount || 0, budget.local_currency)}`,
      `Interests: ${trip.interests || "culture, food, landmarks"}`,
    ],
    budget,
    weather,
    news,
    route,
    attractions,
    crowds,
    food,
    days,
    tools: (plan.pipeline || []).map((step) => step.agent).filter(Boolean),
  };
}

function renderReport(report) {
  return `
    <div class="report-header">
      <div>
        <p class="eyebrow">Generated travel intelligence</p>
        <h2>${escapeHtml(report.title)}</h2>
        <div class="meta-row">${report.meta.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</div>
      </div>
      <button class="export-button" type="button">Export PDF</button>
    </div>

    <section class="report-section">
      <h3>Executive Summary</h3>
      <ul>${toBullets(splitSummary(report.summary))}</ul>
    </section>

    <section class="report-grid">
      <div class="mini-panel">
        <h3>Budget Snapshot</h3>
        <ul>
          <li>Status: <strong>${escapeHtml(report.budget.status || "review")}</strong></li>
          <li>Your budget: <strong>${escapeHtml(report.budget.input_display || formatMoney(report.budget.total_budget || 0, report.budget.currency))}</strong></li>
          <li>Destination value: <strong>${escapeHtml(report.budget.local_display || formatMoney(report.budget.local_amount || 0, report.budget.local_currency))}</strong></li>
          <li>Expected total: <strong>${escapeHtml(report.budget.local_expected_display || formatMoney(report.budget.expected_total || 0, report.budget.currency))}</strong></li>
          <li>Lodging estimate: ${formatMoney(report.budget.lodging || 0, report.budget.currency)} base</li>
          <li>Food estimate: ${formatMoney(report.budget.food || 0, report.budget.currency)} base</li>
          <li>Transport estimate: ${formatMoney(report.budget.transport || 0, report.budget.currency)} base</li>
          <li>Activities estimate: ${formatMoney(report.budget.activities || 0, report.budget.currency)} base</li>
          <li>Buffer: ${escapeHtml(report.budget.local_buffer_display || formatMoney(report.budget.buffer || 0, report.budget.currency))}</li>
          <li>${escapeHtml(report.budget.conversion_note || "Currency conversion is approximate.")}</li>
        </ul>
      </div>
      <div class="mini-panel">
        <h3>Route Intelligence</h3>
        <ul>
          <li>Mode: ${escapeHtml(report.route.recommended_mode || "public transport + walking")}</li>
          <li>Estimated time: ${escapeHtml(report.route.estimated_transfer_time || "30-60 minutes")}</li>
          <li>Distance: ${report.route.distance_km ? `${report.route.distance_km} km` : "Flexible by neighborhood"}</li>
          ${(report.route.notes || []).map((note) => `<li>${escapeHtml(note)}</li>`).join("")}
        </ul>
      </div>
    </section>

    <section class="report-section">
      <h3>Recommended Attractions</h3>
      <ul>${toBullets(report.attractions.slice(0, 6).map((item) => `${item.name} - ${item.category || "attraction"}: ${item.description || "Worth adding to your route."}`))}</ul>
    </section>

    <section class="report-section">
      <h3>Famous Food And Drinks</h3>
      <ul>${toBullets([
        ...(report.food.foods || []).map((item) => `${item.name}: ${item.why_try || "A famous local food to try."}`),
        ...(report.food.drinks || []).map((item) => `${item.name}: ${item.why_try || "A famous local drink to try."}`),
      ])}</ul>
    </section>

    <section class="report-section">
      <h3>Weather And Crowd Notes</h3>
      <ul>${toBullets(report.weather.map((item, index) => {
        const crowd = report.crowds[index] || {};
        return `${item.date}: ${item.condition}, ${item.high_c || "?"}C. Crowd level: ${crowd.level || "moderate"}. ${item.tip || "Keep plans flexible."}`;
      }))}</ul>
    </section>

    <section class="report-section">
      <h3>Day-By-Day Itinerary</h3>
      <div class="day-list">
        ${report.days.map((day) => `
          <div class="day-card">
            <h4>${escapeHtml(day.title || `Day ${day.day}`)}</h4>
            <p>Weather: ${escapeHtml(day.weather?.condition || "mixed")} | Crowd: ${escapeHtml(day.crowd_level || "moderate")} | Activity cost: ${formatActivityCost(day, report.budget.currency)}</p>
            <ul>${toBullets(day.activities || [])}</ul>
          </div>
        `).join("")}
      </div>
    </section>

    <section class="report-section">
      <h3>Live News And Safety Scan</h3>
      <ul>${toBullets(report.news.slice(0, 5).map((item) => `${item.title}: ${item.summary || "Review before departure."}`))}</ul>
    </section>

    <section class="report-section tool-audit">
      <h3>Tools Used</h3>
      <div>${report.tools.map((tool) => `<span>${escapeHtml(tool.replaceAll("_", " "))}</span>`).join("")}</div>
    </section>`;
}

function bindExportButton(root, report) {
  const button = root.querySelector(".export-button");
  if (button) button.addEventListener("click", () => exportReportPdf(report));
}

function exportReportPdf(report) {
  const popup = window.open("", "_blank", "width=920,height=1200");
  if (!popup) return;
  popup.document.write(`
    <!doctype html><html><head><title>${escapeHtml(report.title)}</title>
    <style>
      body{font-family:Aptos,'Segoe UI',Arial,sans-serif;color:#172033;margin:40px;line-height:1.55}
      h1{font-size:32px;margin:0 0 8px} h2{font-size:20px;margin-top:28px;border-bottom:1px solid #d9e2ef;padding-bottom:8px}
      .meta span{display:inline-block;margin:0 8px 8px 0;padding:6px 10px;border-radius:999px;background:#edf4ff;color:#315176}
      li{margin:7px 0}.day{break-inside:avoid;border:1px solid #d9e2ef;border-radius:14px;padding:14px;margin:12px 0}.brand{color:#246bfe;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:12px}
      @media print{button{display:none} body{margin:24px}}
    </style></head><body>
    <button onclick="window.print()">Print / Save as PDF</button>
    <p class="brand">Travelo</p>
    <h1>${escapeHtml(report.title)}</h1>
    <div class="meta">${report.meta.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</div>
    <h2>Executive Summary</h2><ul>${toBullets(splitSummary(report.summary))}</ul>
    <h2>Budget Snapshot</h2><ul><li>Status: ${escapeHtml(report.budget.status || "review")}</li><li>Your budget: ${escapeHtml(report.budget.input_display || formatMoney(report.budget.total_budget || 0, report.budget.currency))}</li><li>Destination value: ${escapeHtml(report.budget.local_display || formatMoney(report.budget.local_amount || 0, report.budget.local_currency))}</li><li>Expected total: ${escapeHtml(report.budget.local_expected_display || formatMoney(report.budget.expected_total || 0, report.budget.currency))}</li><li>Buffer: ${escapeHtml(report.budget.local_buffer_display || formatMoney(report.budget.buffer || 0, report.budget.currency))}</li></ul>
    <h2>Day-By-Day Itinerary</h2>${report.days.map((day) => `<div class="day"><h3>${escapeHtml(day.title || `Day ${day.day}`)}</h3><ul>${toBullets(day.activities || [])}</ul></div>`).join("")}
    <h2>Attractions</h2><ul>${toBullets(report.attractions.slice(0, 6).map((item) => `${item.name} - ${item.description || item.category || "attraction"}`))}</ul>
    <h2>Famous Food And Drinks</h2><ul>${toBullets([...(report.food.foods || []), ...(report.food.drinks || [])].map((item) => `${item.name}: ${item.why_try || "Worth trying locally."}`))}</ul>
    <h2>Weather And Crowds</h2><ul>${toBullets(report.weather.map((item, index) => `${item.date}: ${item.condition}; crowd ${report.crowds[index]?.level || "moderate"}`))}</ul>
    <h2>News Scan</h2><ul>${toBullets(report.news.slice(0, 5).map((item) => `${item.title}: ${item.summary || "Review before departure."}`))}</ul>
    </body></html>`);
  popup.document.close();
  popup.focus();
  setTimeout(() => popup.print(), 350);
}

function pushHistory(plan, report) {
  state.history.unshift({
    type: "travel_plan",
    destination: report.destination,
    date: new Date().toLocaleString(),
    message: plan.user_message,
    report,
  });
  state.history = state.history.slice(0, 12);
  saveHistory();
  renderHistory();
}

function pushChatHistory(answer) {
  state.history.unshift({
    type: "chat",
    destination: "Chat",
    date: new Date().toLocaleString(),
    message: $("#messageInput").dataset.lastMessage || "",
    answer,
  });
  state.history = state.history.slice(0, 12);
  saveHistory();
  renderHistory();
}

async function submitChat(event) {
  event.preventDefault();
  const messageInput = $("#messageInput");
  const message = messageInput.value.trim();
  if (!message) return;

  welcomeStage.classList.add("is-hidden");
  addUserMessage(message);
  messageInput.dataset.lastMessage = message;
  addLoadingMessage();
  messageInput.value = "";
  resizeTextarea(messageInput);

  const payload = collectPayload(message);
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error(`Request failed with ${response.status}`);
    const plan = await response.json();
    removeLoadingMessage();
    if (plan.type === "chat") {
      addAssistantChat(plan.answer || "I could not generate a response.");
    } else {
      addAssistantReport(plan);
    }
  } catch (error) {
    removeLoadingMessage();
    addErrorMessage(error.message);
  }
}

function collectPayload(message) {
  return {
    message,
    destination: $("#destinationInput").value.trim(),
    start_date: $("#startDateInput").value,
    end_date: $("#endDateInput").value,
    travelers: $("#travelersInput").value,
    budget: $("#budgetInput").value,
    interests: $("#interestsInput").value.trim(),
  };
}

function addErrorMessage(text) {
  const card = document.createElement("article");
  card.className = "message assistant-message";
  card.innerHTML = `<div class="assistant-icon">!</div><div class="report-card compact"><h2>Travelo hit a snag</h2><p>${escapeHtml(text)}</p></div>`;
  messages.appendChild(card);
}

function resizeTextarea(textarea) {
  textarea.style.height = "auto";
  textarea.style.height = `${Math.min(textarea.scrollHeight, 180)}px`;
}

function splitSummary(summary) {
  return String(summary || "")
    .split(/\n|\.\s+/)
    .map((item) => item.replace(/^[-*\s]+/, "").trim())
    .filter(Boolean)
    .slice(0, 8);
}

function toBullets(items) {
  const clean = (items || []).filter(Boolean);
  if (!clean.length) return "<li>Keep the plan flexible and confirm local details before departure.</li>";
  return clean.map((item) => `<li>${escapeHtml(String(item))}</li>`).join("");
}

function formatMoney(value, currency = "USD") {
  const amount = Number(value || 0);
  const symbols = { USD: "$", INR: "₹", EUR: "€", JPY: "¥", GBP: "£" };
  const maximumFractionDigits = ["INR", "JPY"].includes(currency) ? 0 : 2;
  return amount
    ? `${symbols[currency] || `${currency} `}${amount.toLocaleString(undefined, { maximumFractionDigits })}`
    : `${symbols[currency] || `${currency} `}0`;
}

function formatActivityCost(day, currency = "USD") {
  if (!Number(day.estimated_cost || 0)) {
    return escapeHtml(day.cost_note || "Free or low-cost activity.");
  }
  const note = day.cost_note ? ` (${day.cost_note})` : "";
  return `${formatMoney(day.estimated_cost, currency)}${escapeHtml(note)}`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function scrollToBottom() {
  setTimeout(() => messages.scrollIntoView({ block: "end", behavior: "smooth" }), 60);
}

function setDefaultDates() {
  const start = new Date();
  start.setDate(start.getDate() + 30);
  const end = new Date(start);
  end.setDate(end.getDate() + 2);
  $("#startDateInput").value = start.toISOString().slice(0, 10);
  $("#endDateInput").value = end.toISOString().slice(0, 10);
}

$("#chatForm").addEventListener("submit", submitChat);
$("#messageInput").addEventListener("input", (event) => resizeTextarea(event.target));
$("#newChatButton").addEventListener("click", () => {
  messages.innerHTML = "";
  state.currentReport = null;
  welcomeStage.classList.remove("is-hidden");
  $("#welcomeText").textContent = "WELCOME TO TRAVELO";
  $("#subheadingText").textContent = "make every trip awesome";
  $(".hero-card h1 .caret").classList.add("is-done");
  $(".subheading .caret").classList.add("is-done");
});
$("#menuButton").addEventListener("click", () => document.body.classList.toggle("sidebar-open"));
$("#themeToggle").addEventListener("click", () => applyTheme(state.theme === "dark" ? "light" : "dark"));

applyTheme(state.theme);
setDefaultDates();
renderHistory();
runIntro();

