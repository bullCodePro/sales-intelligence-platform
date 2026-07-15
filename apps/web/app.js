const form = document.querySelector("#company-form");
const scoresEl = document.querySelector("#scores");
const statusEl = document.querySelector("#status");
const countEl = document.querySelector("#count");

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

function renderScores(scores) {
  countEl.textContent = `${scores.length} account${scores.length === 1 ? "" : "s"}`;
  scoresEl.innerHTML = scores
    .map((item) => {
      const tierClass = item.tier === "A" ? "" : `tier-${item.tier.toLowerCase()}`;
      const reasons = item.reasons.map((reason) => `<span class="reason">${reason}</span>`).join("");
      return `
        <article class="score-card">
          <div class="score-badge ${tierClass}">${item.score}</div>
          <div>
            <h3>${item.company_name}</h3>
            <p>${item.domain} · Tier ${item.tier}</p>
            <div class="reasons">${reasons}</div>
          </div>
        </article>
      `;
    })
    .join("");
}

async function refreshScores() {
  const { scores } = await fetchJson("/api/scores");
  renderScores(scores);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());
  data.employee_count = Number(data.employee_count || 0);
  data.revenue_usd = Number(data.revenue_usd || 0);

  statusEl.textContent = "Saving...";
  try {
    await fetchJson("/api/companies", {
      method: "POST",
      body: JSON.stringify(data),
    });
    form.reset();
    statusEl.textContent = "Saved";
    await refreshScores();
  } catch (error) {
    statusEl.textContent = error.message;
  }
});

refreshScores().catch((error) => {
  statusEl.textContent = error.message;
});
