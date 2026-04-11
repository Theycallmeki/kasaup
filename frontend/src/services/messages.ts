import api from "./api"

export async function getConversations() {
    const res = await api.get("/messages/conversations/")
    return res.data
}

export async function getConversationMessages(conversationId: number) {
    const res = await api.get(`/messages/conversations/${conversationId}/messages/`)
    return res.data
}

export async function sendMessage(receiver_id: number, content: string | null = null, image_url: string | null = null) {
    const payload: any = { receiver_id }
    if (content) payload.content = content
    if (image_url) payload.image_url = image_url
    const res = await api.post("/messages/send/", payload)
    return res.data
}

export async function deleteConversation(conversationId: number) {
    const res = await api.delete(`/messages/conversations/${conversationId}/`)
    return res.data
}

export async function uploadMessageImage(file: File) {
    const formData = new FormData()
    formData.append("file", file)
    const res = await api.post("/messages/upload-image/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
    })
    return res.data.url
}
