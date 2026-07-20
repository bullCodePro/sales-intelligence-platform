const storageKey = "sales-intelligence-ui-state-v2";

const defaultState = {
  clientName: "New client",
  workspaceName: "Prospecting workspace",
  targetCountry: "",
  icpName: "Custom ICP",
  minEmployees: 200,
  maxEmployees: "",
  targetSectors: "Retail, Logistics, Healthcare",
  positiveSignals: "Multiple locations, shift work, operational staff, frequent hiring",
  targetRoles: "HR Manager, People Operations, CFO, Benefits Manager",
  companies: [],
  filter: "all",
};

const demoCompanies = [
  {
    name: "Northstar Operations",
    sector: "Retail",
    country: "Uruguay",
    employees: 420,
    signals: "Multiple locations, shift work, operational staff",
  },
  {
    name: "Atlas Fulfillment",
    sector: "Logistics",
    country: "Uruguay",
    employees: 310,
    signals: "Warehouse teams, shift work, frequent hiring",
  },
  {
    name: "Bluebird Services",
    sector: "Cleaning",
    country: "Uruguay",
    employees: 190,
    signals: "Operational staff, multiple client sites",
  },
  {
    name: "Meridian Health Group",
    sector: "Healthcare",
    country: "Argentina",
    employees: 860,
    signals: "Operational staff, HR team visible",
  },
];

let state = loadState();

const fields = {
  clientName: document.querySelector("#client-name"),
  workspaceName: document.querySelector("#workspace-name"),
  targetCountry: document.querySelector("#target-country"),
  icpName: document.querySelector("#icp-name"),
  minEmployees: document.querySelector("#min-employees"),
  maxEmployees: document.querySelector("#max-employees"),
  targetSectors: document.querySelector("#target-sectors"),
  positiveSignals: document.querySelector("#positive-signals"),
  targetRoles: document.querySelector("#target-roles"),
};

const companyForm = document.querySelector("#company-form");
const companyTable = document.querySelector("#company-table");
const searchBrief = document.querySelector("#search-brief");
const segmented = document.querySelector(".segmented");
const apiStatus = document.querySelector("#api-status");

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "Request failed");
  }
  return payload;
}

function loadState() {
  const saved = localStorage.getItem(storageKey);
  return saved ? { ...defaultState, ...JSON.parse(saved) } : { ...defaultState };
}

function saveState() {
  localStorage.setItem(storageKey, JSON.stringify(state));
}

function toList(value) {
  return String(value || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function normalize(value) {
  return String(value || "").trim().toLowerCase();
}

function scoreCompany(company) {
  const sectors = toList(state.targetSectors).map(normalize);
  const signals = toList(state.positiveSignals).map(normalize);
  const minEmployees = Number(state.minEmployees || 0);
  const maxEmployees = Number(state.maxEmployees || 0);

  let score = 20;
  const reasons = [];

  if (normalize(company.country) === normalize(state.targetCountry)) {
    score += 25;
    reasons.push("country");
  }

  if (sectors.includes(normalize(company.sector))) {
    score += 25;
    reasons.push("sector");
  }

  if (Number(company.employees) >= minEmployees) {
    score += 20;
    reasons.push("size");
  }

  if (!maxEmployees || Number(company.employees) <= maxEmployees) {
    score += 5;
  }

  const companySignals = normalize(company.signals);
  const matchedSignals = signals.filter((signal) => companySignals.includes(signal));
  if (matchedSignals.length > 0) {
    score += Math.min(25, matchedSignals.length * 8);
    reasons.push("signals");
  }

  score = Math.min(score, 100);
  const tier = score >= 80 ? "A" : score >= 60 ? "B" : "C";
  return { ...company, score, tier, reasons };
}

function filteredCompanies() {
  const scored = state.companies.map(scoreCompany).sort((a, b) => b.score - a.score);
  if (state.filter === "A") {
    return scored.filter((company) => company.tier === "A");
  }
  if (state.filter === "review") {
    return scored.filter((company) => company.tier !== "A");
  }
  return scored;
}

function syncInputs() {
  Object.entries(fields).forEach(([key, input]) => {
    input.value = state[key] ?? "";
  });
}

function renderMetrics() {
  const scored = state.companies.map(scoreCompany);
  document.querySelector("#metric-client").textContent = state.clientName || "New client";
  document.querySelector("#metric-market").textContent = state.targetCountry
    ? `${state.workspaceName || "Workspace"} · ${state.targetCountry}`
    : "No market configured";
  document.querySelector("#metric-companies").textContent = String(state.companies.length);
  document.querySelector("#metric-tier-a").textContent = String(
    scored.filter((company) => company.tier === "A").length,
  );
  document.querySelector("#metric-roles").textContent = String(toList(state.targetRoles).length);
}

function renderTable() {
  const rows = filteredCompanies();

  companyTable.innerHTML = `
    <div class="table-row table-head">
      <span>Company</span>
      <span>Fit</span>
      <span>Why</span>
      <span></span>
    </div>
    ${
      rows.length
        ? rows
            .map(
              (company) => `
                <div class="table-row">
                  <span>
                    <strong>${company.name}</strong>
                    <small>${company.sector} · ${company.country} · ${company.employees} employees</small>
                  </span>
                  <span>
                    <span class="score ${company.tier === "A" ? "good" : "warn"}">${company.score}</span>
                    <small>Tier ${company.tier}</small>
                  </span>
                  <span>${company.reasons.length ? company.reasons.join(", ") : "Needs more data"}</span>
                  <button class="text-button" data-remove="${company.name}" type="button">Remove</button>
                </div>
              `,
            )
            .join("")
        : `<div class="empty-state">Add companies above or load the demo to see scoring.</div>`
    }
  `;
}

function renderBrief() {
  const sectors = toList(state.targetSectors);
  const roles = toList(state.targetRoles);
  const signals = toList(state.positiveSignals);

  searchBrief.innerHTML = `
    <div class="brief-row">
      <span>Client</span>
      <strong>${state.clientName || "Not set"}</strong>
    </div>
    <div class="brief-row">
      <span>ICP</span>
      <strong>${state.icpName || "Not set"}</strong>
    </div>
    <div class="brief-row">
      <span>Market</span>
      <strong>${state.targetCountry || "Any country"}</strong>
    </div>
    <div class="brief-row">
      <span>Employee range</span>
      <strong>${state.minEmployees || 0}+${state.maxEmployees ? ` to ${state.maxEmployees}` : ""}</strong>
    </div>
    <div class="brief-block">
      <span>Sectors</span>
      <div class="chips">${sectors.map((sector) => `<span>${sector}</span>`).join("") || "<em>None</em>"}</div>
    </div>
    <div class="brief-block">
      <span>Signals</span>
      <div class="chips">${signals.map((signal) => `<span>${signal}</span>`).join("") || "<em>None</em>"}</div>
    </div>
    <div class="brief-block">
      <span>Contacts</span>
      <div class="chips">${roles.map((role) => `<span>${role}</span>`).join("") || "<em>None</em>"}</div>
    </div>
  `;
}

function renderFilters() {
  segmented.querySelectorAll("button").forEach((button) => {
    button.classList.toggle("selected", button.dataset.filter === state.filter);
  });
}

function render() {
  syncInputs();
  renderMetrics();
  renderFilters();
  renderTable();
  renderBrief();
  saveState();
}

Object.entries(fields).forEach(([key, input]) => {
  input.addEventListener("input", () => {
    state[key] = input.type === "number" ? input.value : input.value;
    render();
  });
});

companyForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(companyForm).entries());
  state.companies = [
    ...state.companies,
    {
      name: data.name,
      sector: data.sector,
      country: data.country,
      employees: Number(data.employees || 0),
      signals: data.signals,
    },
  ];
  companyForm.reset();
  render();
});

companyTable.addEventListener("click", (event) => {
  const button = event.target.closest("[data-remove]");
  if (!button) return;
  state.companies = state.companies.filter((company) => company.name !== button.dataset.remove);
  render();
});

segmented.addEventListener("click", (event) => {
  const button = event.target.closest("[data-filter]");
  if (!button) return;
  state.filter = button.dataset.filter;
  render();
});

document.querySelector("#load-demo").addEventListener("click", () => {
  state = {
    ...defaultState,
    clientName: "Demo Client",
    workspaceName: "Operational workforce search",
    targetCountry: "Uruguay",
    icpName: "Operational workforce 200+",
    targetSectors: "Retail, Logistics, Healthcare, Cleaning",
    companies: demoCompanies,
  };
  render();
});

document.querySelector("#reset-workspace").addEventListener("click", () => {
  state = { ...defaultState };
  localStorage.removeItem(storageKey);
  render();
});

fetchJson("/api/health")
  .then((payload) => {
    apiStatus.textContent = payload.status === "ok" ? "Online" : payload.status;
  })
  .catch((error) => {
    apiStatus.textContent = error.message;
  });

render();
