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

      <router-link to="/appointments" class="link">
        My Appointments
      </router-link>

      <router-link to="/login" class="link">
        Login
      </router-link>

      <router-link to="/register" class="link">
        Register
      </router-link>

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
}

.link:hover{
  background:#334155;
}

</style>