import api from "./api"

export async function submitReview(data: { 
    appointment_id: number, 
    rating: number, 
    comment: string 
}) {
    const res = await api.post("/ratings/", data)
    return res.data
}

export async function getProviderReviews(providerId: number) {
    const res = await api.get(`/ratings/provider/${providerId}`)
    return res.data
}

export async function getMyReviews() {
    const res = await api.get("/ratings/me")
    return res.data
}
