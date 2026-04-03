import api from "./api"

export async function getConversations() {
    const res = await api.get("/messages/conversations/")
    return res.data
}

export async function getConversationMessages(conversationId: number) {
    const res = await api.get(`/messages/conversations/${conversationId}/messages/`)
    return res.data
}

export async function sendMessage(receiver_id: number, content: string) {
    const res = await api.post("/messages/send/", { receiver_id, content })
    return res.data
}

export async function deleteConversation(conversationId: number) {
    const res = await api.delete(`/messages/conversations/${conversationId}/`)
    return res.data
}
