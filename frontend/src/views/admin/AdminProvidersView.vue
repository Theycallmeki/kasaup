<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useProviderStore } from "../../stores/providerStore"

const providerStore = useProviderStore()

const form = ref({
  shop_name: "",
  description: "",
  phone: "",
  email: "",
  address: "",
  latitude: 0,
  longitude: 0,
  offers_home_service: false
})

const editingId = ref<number | null>(null)

onMounted(() => {
  providerStore.fetchProviders()
})

async function submit() {

  if (editingId.value) {

    await providerStore.editProvider(editingId.value, form.value)

  } else {

    await providerStore.addProvider(form.value)

  }

  resetForm()
}

function edit(provider: any) {

  editingId.value = provider.id

  form.value = {
    shop_name: provider.shop_name,
    description: provider.description,
    phone: provider.phone,
    email: provider.email,
    address: provider.address,
    latitude: provider.latitude,
    longitude: provider.longitude,
    offers_home_service: provider.offers_home_service
  }

}

async function remove(id: number) {

  await providerStore.removeProvider(id)

}

function resetForm() {

  editingId.value = null

  form.value = {
    shop_name: "",
    description: "",
    phone: "",
    email: "",
    address: "",
    latitude: 0,
    longitude: 0,
    offers_home_service: false
  }

}
</script>

<template>

<div>

<h2>Providers</h2>

<form @submit.prevent="submit">

<input v-model="form.shop_name" placeholder="Shop Name" />

<input v-model="form.description" placeholder="Description" />

<input v-model="form.phone" placeholder="Phone" />

<input v-model="form.email" placeholder="Email" />

<input v-model="form.address" placeholder="Address" />

<input v-model.number="form.latitude" placeholder="Latitude" />

<input v-model.number="form.longitude" placeholder="Longitude" />

<label>
<input type="checkbox" v-model="form.offers_home_service" />
Offers Home Service
</label>

<button type="submit">
{{ editingId ? "Update Provider" : "Create Provider" }}
</button>

<button
type="button"
@click="resetForm"
v-if="editingId"
>
Cancel
</button>

</form>

<hr />

<div v-if="providerStore.loading">
Loading...
</div>

<div v-else>

<div
v-for="provider in providerStore.providers"
:key="provider.id"
style="margin-bottom:10px"
>

<strong>{{ provider.shop_name }}</strong>

<div>

<button @click="edit(provider)">
Edit
</button>

<button @click="remove(provider.id)">
Delete
</button>

</div>

</div>

</div>

</div>

</template>