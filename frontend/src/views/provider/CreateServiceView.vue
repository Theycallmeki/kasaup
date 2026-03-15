<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useServiceStore } from "../../stores/serviceStore"
import LocationPickerMap from "../../components/LocationPickerMap.vue"

const router = useRouter()
const serviceStore = useServiceStore()

const name = ref("")
const description = ref("")
const price = ref(0)
const duration_minutes = ref(60)
const category_id = ref(1)

const latitude = ref<number | null>(null)
const longitude = ref<number | null>(null)

function setLocation(data: any) {

  latitude.value = data.latitude
  longitude.value = data.longitude

}

const createService = async () => {

  try {

    await serviceStore.addService({
      category_id: category_id.value,
      name: name.value,
      description: description.value,
      price: price.value,
      duration_minutes: duration_minutes.value,
      latitude: latitude.value ?? undefined,
      longitude: longitude.value ?? undefined
    })

    router.push("/provider/services")

  } catch (err: any) {

    console.log(err.response?.data)

  }

}
</script>

<template>

<div>

<h2>Create Service</h2>

<div>

<input
v-model="name"
placeholder="Service name"
/>

</div>

<div>

<textarea
v-model="description"
placeholder="Description"
/>

</div>

<div>

<input
v-model.number="price"
type="number"
placeholder="Price"
/>

</div>

<div>

<input
v-model.number="duration_minutes"
type="number"
placeholder="Duration Minutes"
/>

</div>

<div>

<select v-model.number="category_id">

<option :value="1">
General Service
</option>

<option :value="2">
Cleaning
</option>

<option :value="3">
Repair
</option>

</select>

</div>

<div style="margin-top:12px">

<LocationPickerMap
@location-selected="setLocation"
/>

</div>

<button
style="margin-top:12px"
@click="createService"
>
Create Service
</button>

</div>

</template>