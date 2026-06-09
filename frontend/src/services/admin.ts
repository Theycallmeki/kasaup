import api from "./api"

export async function getOverview() {
  const res = await api.get("/admin/analytics/overview")
  return res.data
}

export async function getRecentActivity() {
  const res = await api.get("/admin/analytics/recent-activity")
  return res.data
}

export async function getPendingUsers() {
  const res = await api.get("/admin/analytics/users/pending")
  return res.data
}
