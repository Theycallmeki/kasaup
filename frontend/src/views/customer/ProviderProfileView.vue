<script setup lang="ts">
import { onMounted } from "vue"
import { useRoute } from "vue-router"
import { useProviderStore } from "../../stores/providerStore"
import { useAppointmentStore } from "../../stores/appointmentStore"

const route = useRoute()
const providerStore = useProviderStore()
const appointmentStore = useAppointmentStore()

const id = Number(route.params.id)

onMounted(() => {
  providerStore.fetchProviderProfile(id)
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
        {{ providerStore.providerProfile.shop_name }}
      </h2>

      <div
        v-for="service in providerStore.providerProfile.services"
        :key="service.id"
      >

        <div>
          {{ service.name }} - {{ service.price }}
        </div>

        <button @click="loadSlots(service.id)">
          Book
        </button>

        <div v-if="appointmentStore.slots.length">

          <div
            v-for="slot in appointmentStore.slots"
            :key="slot"
          >
            {{ slot }}
            <button @click="book(service.id, slot)">
              Confirm
            </button>
          </div>

        </div>

      </div>

    </div>

  </div>
</template>