<script setup lang="ts">
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import { useServiceStore } from "../../stores/serviceStore"
import { useAuthStore } from "../../stores/authStore"

const serviceStore = useServiceStore()
const authStore = useAuthStore()
const router = useRouter()

onMounted(async () => {

  if (authStore.user?.provider_id) {

    await serviceStore.fetchProviderServices(authStore.user.provider_id)

  }

})

function createService() {

  router.push("/provider/services/create")

}

function editService(id: number) {

  router.push(`/provider/services/edit/${id}`)

}

async function deleteService(id: number) {

  await serviceStore.removeService(id)

}
</script>

<template>

<div>

<h2>My Services</h2>

<button @click="createService">
Create Service
</button>

<div v-if="serviceStore.loading">
Loading...
</div>

<div v-else>

<div
v-for="service in serviceStore.services"
:key="service.id"
style="margin-bottom:12px"
>

<strong>{{ service.name }}</strong>

<div>
Price: ₱{{ service.price }}
</div>

<div>
Duration: {{ service.duration_minutes }} minutes
</div>

<div style="margin-top:6px">

<button @click="editService(service.id)">
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

</div>

</div>

</template>