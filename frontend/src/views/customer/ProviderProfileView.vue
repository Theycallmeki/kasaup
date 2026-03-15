<script setup lang="ts">
import { onMounted } from "vue"
import { useRoute } from "vue-router"
import { useProviderStore } from "../../stores/providerStore"
import { useAppointmentStore } from "../../stores/appointmentStore"

const route = useRoute()
const providerStore = useProviderStore()
const appointmentStore = useAppointmentStore()

const id = Number(route.params.id)

onMounted(async () => {

  await providerStore.fetchProviderProfile(id)

})

function loadSlots(serviceId: number) {

  appointmentStore.fetchAvailableSlots(serviceId)

}

function book(serviceId: number, slot: string) {

  appointmentStore.bookAppointment({
    provider_id: id,
    service_id: serviceId,
    appointment_time: slot
  })

}
</script>

<template>

<div>

<div v-if="providerStore.loading">
Loading...
</div>

<div v-else-if="providerStore.providerProfile">

<h2>
{{ providerStore.providerProfile.provider.shop_name }}
</h2>

<p>
{{ providerStore.providerProfile.provider.description }}
</p>

<div
v-for="service in providerStore.providerProfile.services"
:key="service.id"
style="margin-bottom:16px"
>

<div>
<strong>{{ service.name }}</strong>
</div>

<div>
Price: ₱{{ service.price }}
</div>

<div>
Duration: {{ service.duration_minutes }} minutes
</div>

<button
style="margin-top:6px"
@click="loadSlots(service.id)"
>
Book
</button>

<div
v-if="appointmentStore.slots.length"
style="margin-top:10px"
>

<div
v-for="slot in appointmentStore.slots"
:key="slot"
style="margin-bottom:6px"
>

{{ slot }}

<button
style="margin-left:10px"
@click="book(service.id, slot)"
>
Confirm
</button>

</div>

</div>

</div>

</div>

</div>

</template>