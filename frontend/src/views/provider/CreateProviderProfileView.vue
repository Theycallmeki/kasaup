<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { createProvider } from "../../services/providers"
import LocationPickerMap from "../../components/LocationPickerMap.vue"

const router = useRouter()

const shop_name = ref("")
const description = ref("")
const phone = ref("")
const email = ref("")
const address = ref("")

const latitude = ref<number | null>(null)
const longitude = ref<number | null>(null)

const offers_home_service = ref(false)

const loading = ref(false)
const error = ref("")

function setLocation(data:any){
  latitude.value = data.latitude
  longitude.value = data.longitude
}

const create = async () => {

  error.value = ""
  loading.value = true

  try {

    if(!latitude.value || !longitude.value){
      error.value = "Please select your shop location on the map"
      loading.value = false
      return
    }

    await createProvider({
      shop_name: shop_name.value,
      description: description.value,
      phone: phone.value,
      email: email.value,
      address: address.value,
      latitude: latitude.value,
      longitude: longitude.value,
      offers_home_service: offers_home_service.value
    })

    router.push("/provider/dashboard")

  } catch(err:any){

    error.value = err.response?.data?.detail || "Failed to create provider"

  } finally {

    loading.value = false

  }

}
</script>

<template>

<div class="provider-create">

<h2>Create Provider Profile</h2>

<div class="form">

<input
v-model="shop_name"
placeholder="Shop Name"
/>

<textarea
v-model="description"
placeholder="Description"
/>

<input
v-model="phone"
placeholder="Phone"
/>

<input
v-model="email"
placeholder="Email"
/>

<input
v-model="address"
placeholder="Address"
/>

<label>
<input
type="checkbox"
v-model="offers_home_service"
/>
Offers Home Service
</label>

<h3>Select Shop Location</h3>

<LocationPickerMap
@location-selected="setLocation"
/>

<button
@click="create"
:disabled="loading"
>
{{ loading ? "Creating..." : "Create Provider Profile" }}
</button>

<p v-if="error" class="error">
{{ error }}
</p>

</div>

</div>

</template>

<style scoped>

.provider-create{
max-width:700px;
margin:40px auto;
padding:20px;
}

.form{
display:flex;
flex-direction:column;
gap:12px;
}

input,textarea{
padding:10px;
border-radius:6px;
border:1px solid #cbd5e1;
}

button{
padding:12px;
background:#2563eb;
color:white;
border:none;
border-radius:6px;
cursor:pointer;
}

button:hover{
background:#1d4ed8;
}

.error{
color:#ef4444;
}

</style>