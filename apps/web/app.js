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

fetchJson("/api/health").then((payload) => {
  document.querySelector("#api-status").textContent = payload.status;
}).catch((error) => {
  document.querySelector("#api-status").textContent = error.message;
});
