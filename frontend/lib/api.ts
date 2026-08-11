const API_BASE_URL = "/api";

export async function fetchExecutiveDashboard() {
  const response = await fetch(`${API_BASE_URL}/executive`);

  if (!response.ok) {
    throw new Error("Failed to fetch Executive Dashboard");
  }

  return response.json();
}

export async function fetchSalesDashboard() {
  const response = await fetch(`${API_BASE_URL}/sales`);

  if (!response.ok) {
    throw new Error("Failed to fetch Sales Dashboard");
  }

  return response.json();
}