<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useProviderStore } from "../../stores/providerStore"

const providerStore = useProviderStore()

const shop_name = ref("")
const description = ref("")
const phone = ref("")
const email = ref("")
const address = ref("")
const offers_home_service = ref(false)

const loading = ref(false)

onMounted(async () => {
  await providerStore.fetchMyProvider()

  if (providerStore.myProvider) {
    const p = providerStore.myProvider
    shop_name.value = p.shop_name
    description.value = p.description
    phone.value = p.phone
    email.value = p.email
    address.value = p.address
    offers_home_service.value = p.offers_home_service
  }
})

const save = async () => {
  loading.value = true

  await providerStore.updateMy({
    shop_name: shop_name.value,
    description: description.value,
    phone: phone.value,
    email: email.value,
    address: address.value,
    offers_home_service: offers_home_service.value
  })

  loading.value = false
}
</script>

<template>
  <div class="page">
    <h1 class="title">My Profile</h1>

    <div class="form">
      <input v-model="shop_name" class="input" placeholder="Shop Name" />
      <input v-model="phone" class="input" placeholder="Phone" />
      <input v-model="email" class="input" placeholder="Email" />
      <input v-model="address" class="input" placeholder="Address" />
      <textarea v-model="description" class="input" placeholder="Description" />

      <label class="checkbox">
        <input type="checkbox" v-model="offers_home_service" />
        Offers Home Service
      </label>

      <button class="btn" @click="save" :disabled="loading">
        {{ loading ? "Saving..." : "Save Changes" }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.page {
  padding: 32px;
  max-width: 500px;
}

.title {
  font-size: 20px;
  margin-bottom: 20px;
  color: #fff;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #333;
  background: #111;
  color: #fff;
}

.checkbox {
  color: #ccc;
  font-size: 14px;
}

.btn {
  padding: 12px;
  border-radius: 10px;
  background: #7c3aed;
  color: #fff;
  border: none;
  cursor: pointer;
}
</style>