<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useAuthStore } from "../../stores/authStore"
import {
  getAvailability,
  createAvailability,
  updateAvailability,
  deleteAvailability
} from "../../services/availability"

const authStore = useAuthStore()

const availability = ref<any[]>([])
const loading = ref(false)

const form = ref({
  day_of_week: 0,
  start_time: "09:00",
  end_time: "17:00"
})

const editingId = ref<number | null>(null)

onMounted(fetchAvailability)

async function fetchAvailability() {

  if (!authStore.user?.provider_id) return

  loading.value = true

  try {

    availability.value = await getAvailability(authStore.user.provider_id)

  } finally {

    loading.value = false

  }

}

async function submit() {

  const provider_id = authStore.user?.provider_id

  if (!provider_id) return

  if (editingId.value) {

    await updateAvailability(editingId.value, form.value)

  } else {

    await createAvailability({
      provider_id,
      ...form.value
    })

  }

  resetForm()
  fetchAvailability()

}

function edit(a: any) {

  editingId.value = a.id

  form.value = {
    day_of_week: a.day_of_week,
    start_time: a.start_time,
    end_time: a.end_time
  }

}

async function remove(id: number) {

  await deleteAvailability(id)

  fetchAvailability()

}

function resetForm() {

  editingId.value = null

  form.value = {
    day_of_week: 0,
    start_time: "09:00",
    end_time: "17:00"
  }

}
</script>

<template>

<div class="availability">

<h2>Provider Availability</h2>

<form class="availability-form" @submit.prevent="submit">

<select v-model.number="form.day_of_week">

<option :value="0">Monday</option>
<option :value="1">Tuesday</option>
<option :value="2">Wednesday</option>
<option :value="3">Thursday</option>
<option :value="4">Friday</option>
<option :value="5">Saturday</option>
<option :value="6">Sunday</option>

</select>

<input
type="time"
v-model="form.start_time"
/>

<input
type="time"
v-model="form.end_time"
/>

<button type="submit">
{{ editingId ? "Update Availability" : "Add Availability" }}
</button>

</form>

<hr>

<div v-if="loading">
Loading...
</div>

<div v-else>

<div
v-for="slot in availability"
:key="slot.id"
class="slot"
>

<div>
<strong>Day:</strong> {{ slot.day_of_week }}
</div>

<div>
{{ slot.start_time }} - {{ slot.end_time }}
</div>

<div class="actions">

<button @click="edit(slot)">
Edit
</button>

<button class="delete" @click="remove(slot.id)">
Delete
</button>

</div>

</div>

</div>

</div>

</template>

<style scoped>

.availability{
padding:20px;
max-width:600px;
}

.availability-form{
display:flex;
gap:10px;
margin-bottom:20px;
}

select,input{
padding:8px;
border-radius:6px;
border:1px solid #cbd5e1;
}

button{
padding:8px 12px;
border:none;
border-radius:6px;
background:#2563eb;
color:white;
cursor:pointer;
}

button:hover{
background:#1d4ed8;
}

.delete{
background:#ef4444;
}

.delete:hover{
background:#dc2626;
}

.slot{
padding:12px;
background:#f1f5f9;
border-radius:6px;
margin-bottom:10px;
}

.actions{
margin-top:6px;
display:flex;
gap:10px;
}

</style>