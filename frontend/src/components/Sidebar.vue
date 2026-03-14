<script setup lang="ts">
import { useAuthStore } from "../stores/authStore"
import { useRouter } from "vue-router"

const auth = useAuthStore()
const router = useRouter()

const logout = async () => {
  await auth.logout()
  router.push("/")
}
</script>

<template>
  <div class="sidebar">

    <h2 class="logo">Kasaup</h2>

    <nav>

      <router-link to="/" class="link">
        Home
      </router-link>

      <router-link to="/providers" class="link">
        Providers
      </router-link>

      <router-link 
        v-if="auth.user"
        to="/appointments"
        class="link"
      >
        My Appointments
      </router-link>

      <!-- Not logged in -->
      <router-link 
        v-if="!auth.user"
        to="/login"
        class="link"
      >
        Login
      </router-link>

      <router-link 
        v-if="!auth.user"
        to="/register"
        class="link"
      >
        Register
      </router-link>

      <!-- Logged in -->
      <button 
        v-if="auth.user"
        class="link logout"
        @click="logout"
      >
        Logout
      </button>

    </nav>

  </div>
</template>

<style scoped>

.sidebar{
  width:220px;
  height:100vh;
  background:#1e293b;
  color:white;
  padding:20px;
  position:fixed;
}

.logo{
  margin-bottom:30px;
}

nav{
  display:flex;
  flex-direction:column;
}

.link{
  color:white;
  text-decoration:none;
  margin:10px 0;
  padding:8px;
  border-radius:6px;
  background:none;
  border:none;
  text-align:left;
  cursor:pointer;
}

.link:hover{
  background:#334155;
}

.logout{
  color:#f87171;
}

</style>
