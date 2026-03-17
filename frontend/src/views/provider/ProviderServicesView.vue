<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useServiceStore } from "../../stores/serviceStore"
import { useAuthStore } from "../../stores/authStore"
import api from "../../services/api"

const serviceStore = useServiceStore()
const authStore = useAuthStore()

const providerId = ref<number | null>(null)

const editingId = ref<number | null>(null)

const form = ref({
  name: "",
  description: "",
  price: 0,
  duration_minutes: 60,
  category_id: 1
})

onMounted(async () => {
  await resolveProvider()
  await fetchServices()
})

async function resolveProvider() {
  const res = await api.get("/providers")

  const provider = res.data.find(
    (p: any) => p.owner_id === authStore.user.id
  )

  providerId.value = provider?.id || null
}

async function fetchServices() {
  if (!providerId.value) return
  await serviceStore.fetchProviderServices(providerId.value)
}

function startEdit(service: any) {
  editingId.value = service.id

  form.value = {
    name: service.name,
    description: service.description,
    price: service.price,
    duration_minutes: service.duration_minutes,
    category_id: service.category_id
  }
}

async function saveEdit() {
  if (!editingId.value) return

  await serviceStore.editService(editingId.value, form.value)

  editingId.value = null
  resetForm()
  await fetchServices()
}

async function deleteService(id: number) {
  await serviceStore.removeService(id)
  await fetchServices()
}

function resetForm() {
  form.value = {
    name: "",
    description: "",
    price: 0,
    duration_minutes: 60,
    category_id: 1
  }
}
</script>

<template>

<div>

<h2>My Services</h2>

<div v-if="serviceStore.loading">
Loading...
</div>

<div v-else>

<div
v-for="service in serviceStore.services"
:key="service.id"
style="margin-bottom:12px; border:1px solid #ddd; padding:10px; border-radius:8px"
>

<div v-if="editingId !== service.id">

<strong>{{ service.name }}</strong>

<div>
Price: ₱{{ service.price }}
</div>

<div>
Duration: {{ service.duration_minutes }} minutes
</div>

<div style="margin-top:6px">

<button @click="startEdit(service)">
Edit
</button>

<button
style="margin-left:10px"
@click="deleteService(service.id)"
>
Delete
</button>

</div>

</div>

<div v-else>

<input v-model="form.name" placeholder="Name" />
<input v-model="form.description" placeholder="Description" />
<input v-model.number="form.price" type="number" placeholder="Price" />
<input v-model.number="form.duration_minutes" type="number" placeholder="Duration" />

<div style="margin-top:6px">

<button @click="saveEdit">
Save
</button>

<button
style="margin-left:10px"
@click="editingId = null"
>
Cancel
</button>

</div>

</div>

</div>

</div>

</div>

</template>