const state = {
  currentReport: null,
  currentConversationId: null,
  history: [],
  theme: localStorage.getItem("travelo_theme") || "dark",
  useTools: true,  // Toggle between tools and Groq-only
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
  renderHistory();
}

async function loadHistory() {
  try {
    const response = await fetch("/api/history");
    if (!response.ok) throw new Error(`History failed with ${response.status}`);
    const data = await response.json();
    state.history = data.history || [];
  } catch (error) {
    state.history = [];
  }
  renderHistory();
}

function renderHistory() {
  historyList.innerHTML = "";
  if (!state.history.length) {
    historyList.innerHTML = '<div class="empty-history">No saved trips yet. Your reports will appear here.</div>';
    return;
  }
  state.history.forEach((item, index) => {
    const row = document.createElement("div");
    row.className = "history-row";
    row.innerHTML = `
      <button class="history-item" type="button">
        <span>${escapeHtml(item.destination || "Trip")}</span>
        <small>${escapeHtml(item.date || "Recent")}</small>
      </button>
      <button class="history-menu" type="button" aria-label="Delete chat" title="Delete chat">⋮</button>`;
    
    row.querySelector(".history-item").addEventListener("click", () => loadHistoryItem(index));
    
    // Attach menu handler using closure to capture item.conversation_id
    row.querySelector(".history-menu").addEventListener("click", (event) => {
      showDeleteMenu(event, item.conversation_id);
    });
    
    historyList.appendChild(row);
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

async function loadHistoryItem(index) {
  const item = state.history[index];
  if (!item) return;
  
  welcomeStage.classList.add("is-hidden");
  messages.innerHTML = "";
  
  // Set current conversation ID
  state.currentConversationId = item.conversation_id;
  
  // Load all messages in this conversation
  try {
    const response = await fetch(`/api/conversation/${item.conversation_id}`);
    if (!response.ok) throw new Error(`Failed to load conversation with ${response.status}`);
    const data = await response.json();
    const conversation = data.conversation || [];
    
    // Display all messages in order
    conversation.forEach((msg) => {
      addUserMessage(msg.message || `Plan a trip to ${msg.destination || "your destination"}`);
      if (msg.type === "chat") {
        addAssistantChat(msg.answer, false);
      } else {
        addAssistantReport(msg.report, false);
        state.currentReport = msg.report;
      }
    });
  } catch (error) {
    // Fallback to single item display
    addUserMessage(item.message || `Plan a trip to ${item.destination || "your destination"}`);
    if (item.type === "chat") {
      addAssistantChat(item.answer, false);
    } else {
      addAssistantReport(item.report, false);
      state.currentReport = item.report;
    }
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
  
  if (state.useTools) {
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
  } else {
    card.innerHTML = `
      <div class="assistant-icon"><img class="slow-spin" src="${logoPath}" alt=""></div>
      <div class="report-card compact">
        <div class="tool-loader"><span></span><span></span><span></span></div>
        <h2>Travelo Thinking...</h2>
        <p>Processing your question.</p>
      </div>`;
  }
  
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
  if (persist) pushHistory(plan, report);
  scrollToBottom();
}

function addAssistantChat(answer, persist = true, plan = null) {
  const card = document.createElement("article");
  card.className = "message assistant-message";
  card.innerHTML = `
    <div class="assistant-icon"><img class="slow-spin" src="${logoPath}" alt=""></div>
    <div class="report-card compact">
      <h2>Travelo says</h2>
      <p style="line-height: 1.6; margin: 0; color: var(--text);">${escapeHtml(answer)}</p>
    </div>`;
  messages.appendChild(card);
  if (persist) pushChatHistory(answer, plan);
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
      `Budget: ${budget.budget_display || budget.input_display || formatMoney(trip.budget || budget.total_budget || 0, budget.currency)}`,
      `Estimate currency: ${budget.local_currency || budget.currency || "USD"}`,
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
          <li>Your budget: <strong>${escapeHtml(report.budget.budget_display || report.budget.input_display || formatMoney(report.budget.total_budget || 0, report.budget.currency))}</strong></li>
          <li>Expected total: <strong>${escapeHtml(report.budget.local_expected_display || formatMoney(report.budget.expected_total || 0, report.budget.currency))}</strong></li>
          <li>Lodging estimate: ${escapeHtml(report.budget.local_lodging_display || formatMoney(report.budget.lodging || 0, report.budget.currency))}</li>
          <li>Food estimate: ${escapeHtml(report.budget.local_food_display || formatMoney(report.budget.food || 0, report.budget.currency))}</li>
          <li>Transport estimate: ${escapeHtml(report.budget.local_transport_display || formatMoney(report.budget.transport || 0, report.budget.currency))}</li>
          <li>Activities estimate: ${escapeHtml(report.budget.local_activities_display || formatMoney(report.budget.activities || 0, report.budget.currency))}</li>
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
        ...(report.food.foods || []).map((item) => formatFoodItem(item, "food")),
        ...(report.food.drinks || []).map((item) => formatFoodItem(item, "drink")),
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
    <h2>Budget Snapshot</h2><ul><li>Status: ${escapeHtml(report.budget.status || "review")}</li><li>Your budget: ${escapeHtml(report.budget.budget_display || report.budget.input_display || formatMoney(report.budget.total_budget || 0, report.budget.currency))}</li><li>Expected total: ${escapeHtml(report.budget.local_expected_display || formatMoney(report.budget.expected_total || 0, report.budget.currency))}</li><li>Buffer: ${escapeHtml(report.budget.local_buffer_display || formatMoney(report.budget.buffer || 0, report.budget.currency))}</li></ul>
    <h2>Day-By-Day Itinerary</h2>${report.days.map((day) => `<div class="day"><h3>${escapeHtml(day.title || `Day ${day.day}`)}</h3><ul>${toBullets(day.activities || [])}</ul></div>`).join("")}
    <h2>Attractions</h2><ul>${toBullets(report.attractions.slice(0, 6).map((item) => `${item.name} - ${item.description || item.category || "attraction"}`))}</ul>
    <h2>Famous Food And Drinks</h2><ul>${toBullets([...(report.food.foods || []), ...(report.food.drinks || [])].map((item) => formatFoodItem(item)))}</ul>
    <h2>Weather And Crowds</h2><ul>${toBullets(report.weather.map((item, index) => `${item.date}: ${item.condition}; crowd ${report.crowds[index]?.level || "moderate"}`))}</ul>
    <h2>News Scan</h2><ul>${toBullets(report.news.slice(0, 5).map((item) => `${item.title}: ${item.summary || "Review before departure."}`))}</ul>
    </body></html>`);
  popup.document.close();
  popup.focus();
  setTimeout(() => popup.print(), 350);
}

function pushHistory(plan, report) {
  const item = {
    id: plan.history_id,
    conversation_id: plan.conversation_id,
    type: "travel_plan",
    destination: report.destination,
    date: new Date().toLocaleString(),
    message: plan.user_message,
    report: plan,
  };
  state.history = state.history.filter((historyItem) => historyItem.conversation_id !== item.conversation_id);
  state.history.unshift(item);
  state.history = state.history.slice(0, 12);
  saveHistory();
}

function pushChatHistory(answer, plan = null) {
  const item = {
    id: plan?.history_id,
    conversation_id: plan?.conversation_id || state.currentConversationId,
    type: "chat",
    destination: "Chat",
    date: new Date().toLocaleString(),
    message: plan?.user_message || $("#messageInput").dataset.lastMessage || "",
    answer,
  };
  state.history = state.history.filter((historyItem) => historyItem.conversation_id !== item.conversation_id);
  state.history.unshift(item);
  state.history = state.history.slice(0, 12);
  saveHistory();
}

function showDeleteMenu(event, conversationId) {
  event.stopPropagation();
  
  const triggerElement = event.currentTarget || event.target;
  
  // Remove any existing menus
  const existingMenu = document.querySelector(".history-menu-popup");
  if (existingMenu) existingMenu.remove();
  
  // Create menu
  const menu = document.createElement("div");
  menu.className = "history-menu-popup";
  menu.innerHTML = `<button class="menu-delete-btn" type="button">Delete</button>`;
  
  document.body.appendChild(menu);
  
  // Position menu near the button
  const rect = triggerElement.getBoundingClientRect();
  menu.style.position = "fixed";
  menu.style.top = (rect.bottom + 5) + "px";
  menu.style.left = (rect.left - 50) + "px";
  
  // Delete button handler
  menu.querySelector(".menu-delete-btn").addEventListener("click", (e) => {
    e.stopPropagation();
    menu.remove();
    showDeleteConfirmation(conversationId, triggerElement);
  });
  
  // Close menu when clicking outside
  document.addEventListener("click", function closeMenu(e) {
    if (!menu.contains(e.target) && e.target !== triggerElement) {
      menu.remove();
      document.removeEventListener("click", closeMenu);
    }
  });
}

function showDeleteConfirmation(conversationId, triggerElement) {
  // Remove any existing popovers
  const existingPopover = document.querySelector(".delete-popover");
  if (existingPopover) existingPopover.remove();

  const popover = document.createElement("div");
  popover.className = "delete-popover";
  popover.innerHTML = `
    <p>Delete this chat?</p>
    <div class="delete-popover-buttons">
      <button class="delete-cancel-btn" type="button">Cancel</button>
      <button class="delete-confirm-btn" type="button">Delete</button>
    </div>
  `;
  
  document.body.appendChild(popover);
  
  // Position popover relative to the triple dot triggerElement
  const rect = triggerElement.getBoundingClientRect();
  popover.style.position = "fixed";
  popover.style.top = (rect.bottom + 6) + "px";
  popover.style.left = (rect.right - 180) + "px";
  
  const cancelBtn = popover.querySelector(".delete-cancel-btn");
  const confirmBtn = popover.querySelector(".delete-confirm-btn");
  
  const closePopover = () => {
    popover.remove();
  };
  
  cancelBtn.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    closePopover();
  });
  
  confirmBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      const response = await fetch(`/api/conversation/${conversationId}`, { method: "DELETE" });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(`Delete failed: ${data.error || response.status}`);
      }
      if (data.deleted) {
        state.history = state.history.filter((item) => item.conversation_id !== conversationId);
        renderHistory();
        
        // Instant screen clear if we deleted the currently active conversation!
        if (state.currentConversationId === conversationId) {
          messages.innerHTML = "";
          state.currentReport = null;
          state.currentConversationId = null;
          welcomeStage.classList.remove("is-hidden");
          $("#welcomeText").textContent = "WELCOME TO TRAVELO";
          $("#subheadingText").textContent = "make every trip awesome";
          $(".hero-card h1 .caret").classList.add("is-done");
          $(".subheading .caret").classList.add("is-done");
        }
        
        closePopover();
      } else {
        throw new Error("Delete operation failed");
      }
    } catch (error) {
      closePopover();
      addErrorMessage(error.message);
    }
  });
  
  // Close popover when clicking outside
  document.addEventListener("click", function clickOutside(e) {
    if (!popover.contains(e.target) && e.target !== triggerElement) {
      popover.remove();
      document.removeEventListener("click", clickOutside);
    }
  });
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
    if (plan.conversation_id) {
      state.currentConversationId = plan.conversation_id;
    }
    if (plan.type === "chat") {
      addAssistantChat(plan.answer || "I could not generate a response.", true, plan);
    } else {
      addAssistantReport(plan);
    }
  } catch (error) {
    removeLoadingMessage();
    addErrorMessage(error.message);
  }
}

function collectPayload(message) {
  const payload = {
    message,
    use_tools: state.useTools,
    destination: $("#destinationInput").value.trim(),
    start_date: $("#startDateInput").value,
    end_date: $("#endDateInput").value,
    travelers: $("#travelersInput").value,
    budget: $("#budgetInput").value,
    interests: $("#interestsInput").value.trim(),
  };
  if (state.currentConversationId) {
    payload.conversation_id = state.currentConversationId;
  }
  return payload;
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
    .replaceAll("**", "")
    .split(/\n|\.\s+/)
    .map((item) => item.replace(/^[-*\s]+/, "").trim())
    .filter(Boolean)
    .slice(0, 8);
}

function toBullets(items) {
  const clean = (items || []).filter(Boolean);
  if (!clean.length) return "<li>Keep the plan flexible and confirm local details before departure.</li>";
  return clean.map((item) => `<li>${escapeHtml(cleanText(item))}</li>`).join("");
}

function formatMoney(value, currency = "USD") {
  const amount = Number(value || 0);
  const symbols = { USD: "$", INR: "Rs ", EUR: "EUR ", JPY: "JPY ", GBP: "GBP " };
  const maximumFractionDigits = ["INR", "JPY"].includes(currency) ? 0 : 2;
  return amount
    ? `${symbols[currency] || `${currency} `}${amount.toLocaleString(undefined, { maximumFractionDigits })}${currency === "USD" ? "" : ` ${currency}`}`
    : `${symbols[currency] || `${currency} `}0${currency === "USD" ? "" : ` ${currency}`}`;
}

function formatActivityCost(day, currency = "USD") {
  if (!Number(day.estimated_cost || 0)) {
    return escapeHtml(day.cost_note || "Free or low-cost activity.");
  }
  const note = day.cost_note ? ` (${day.cost_note})` : "";
  return `${formatMoney(day.estimated_cost, currency)}${escapeHtml(note)}`;
}

function formatFoodItem(item, fallbackType = "specialty") {
  const name = item.name || `Local ${fallbackType}`;
  const why = item.why_try || "Worth trying locally.";
  const where = item.where_to_try ? ` Try it at ${item.where_to_try}.` : "";
  const tip = item.tip ? ` Tip: ${item.tip}` : "";
  return `${name}: ${why}${where}${tip}`;
}

function cleanText(value) {
  return String(value ?? "").replaceAll("**", "");
}

function escapeHtml(value) {
  return cleanText(value)
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
  state.currentConversationId = null;
  welcomeStage.classList.remove("is-hidden");
  $("#welcomeText").textContent = "WELCOME TO TRAVELO";
  $("#subheadingText").textContent = "make every trip awesome";
  $(".hero-card h1 .caret").classList.add("is-done");
  $(".subheading .caret").classList.add("is-done");
});
$("#menuButton").addEventListener("click", () => document.body.classList.toggle("sidebar-open"));
$("#themeToggle").addEventListener("click", () => applyTheme(state.theme === "dark" ? "light" : "dark"));
$("#toolsToggle").addEventListener("click", (e) => {
  state.useTools = !state.useTools;
  const btn = e.target.closest("#toolsToggle");
  btn.setAttribute("aria-pressed", String(state.useTools));
  btn.style.opacity = state.useTools ? "1" : "0.5";
});

function exportConversationPdf() {
  const messageElements = document.querySelectorAll("#messages .message");
  if (!messageElements.length) {
    alert("No messages to export.");
    return;
  }
  
  let htmlContent = "";
  messageElements.forEach((msg) => {
    if (msg.classList.contains("loading-card")) return;
    
    if (msg.classList.contains("user-message")) {
      const bubble = msg.querySelector(".bubble");
      if (bubble) {
        htmlContent += `
          <div class="message user">
            <strong>You</strong>
            <div>${bubble.innerHTML}</div>
          </div>`;
      }
    } else if (msg.classList.contains("assistant-message")) {
      const card = msg.querySelector(".report-card");
      if (card) {
        const clonedCard = card.cloneNode(true);
        const btn = clonedCard.querySelector(".export-button");
        if (btn) btn.remove();
        
        const isCompact = card.classList.contains("compact");
        const title = isCompact ? "Travelo Chat" : "Travel Plan";
        
        htmlContent += `
          <div class="message assistant">
            <strong>${title}</strong>
            <div class="report-card ${isCompact ? 'compact' : ''}">
              ${clonedCard.innerHTML}
            </div>
          </div>`;
      }
    }
  });

  const popup = window.open("", "_blank", "width=920,height=1200");
  if (!popup) return;
  popup.document.write(`
    <!doctype html><html><head><title>Travelo Chat Export</title>
    <style>
      body{font-family:Aptos,'Segoe UI',Arial,sans-serif;color:#172033;margin:40px;line-height:1.55}
      h1{font-size:32px;margin:0 0 8px} 
      h2{font-size:20px;margin-top:28px;border-bottom:1px solid #d9e2ef;padding-bottom:8px}
      .brand{color:#246bfe;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:12px}
      .conversation{margin-top:30px}
      .message{margin-bottom:30px;padding-bottom:20px;border-bottom:1.5px solid #e8edf5;break-inside:avoid}
      .message.user{background:#f8fbff;border-left:4px solid #246bfe;padding:16px;border-radius:8px}
      .message.user strong{display:block;color:#1e40af;font-size:12px;text-transform:uppercase;margin-bottom:8px;letter-spacing:0.05em}
      .message.assistant strong{display:block;color:#0f766e;font-size:12px;text-transform:uppercase;margin-bottom:12px;letter-spacing:0.05em}
      .meta-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:15px}
      .meta-row span{display:inline-block;padding:6px 10px;border-radius:999px;background:#edf4ff;color:#315176;font-size:11px;font-weight:bold}
      .report-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:15px 0}
      .mini-panel, .report-section{border:1px solid #d9e2ef;border-radius:14px;padding:16px;margin:15px 0;background:#fafbfe}
      .mini-panel h3, .report-section h3{margin-top:0;font-size:15px;color:#1e293b;border-bottom:1px solid #e2e8f0;padding-bottom:6px}
      .day-list{display:grid;gap:12px}
      .day-card{border:1px solid #d9e2ef;border-radius:12px;padding:14px;background:#ffffff}
      .day-card h4{margin:0 0 6px;font-size:14px}
      .day-card p{font-size:12px;color:#64748b;margin:0 0 8px}
      li{margin:7px 0}
      ul{padding-left:20px}
      .tool-audit{display:none}
      @media print{button{display:none} body{margin:24px}}
    </style></head><body>
    <button onclick="window.print()">Print / Save as PDF</button>
    <p class="brand">Travelo</p>
    <h1>Travelo Travel Itinerary & Chat History</h1>
    <div class="conversation">
      ${htmlContent}
    </div>
    </body></html>`);
  popup.document.close();
  popup.focus();
  setTimeout(() => popup.print(), 350);
}

const exportChatBtn = $("#exportChatBtn");
if (exportChatBtn) {
  exportChatBtn.addEventListener("click", exportConversationPdf);
}

applyTheme(state.theme);
setDefaultDates();
loadHistory();
runIntro();

