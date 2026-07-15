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

const apiStatus = document.querySelector("#api-status");

fetchJson("/api/health")
  .then((payload) => {
    apiStatus.textContent = payload.status === "ok" ? "Online" : payload.status;
  })
  .catch((error) => {
    apiStatus.textContent = error.message;
  });
