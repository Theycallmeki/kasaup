<template>
  <div>

    <h2>Get Started</h2>

    <router-link to="/login">
      <button>Login</button>
    </router-link>

    <router-link to="/register?role=customer">
      <button>Create Customer Account</button>
    </router-link>

    <router-link to="/register?role=provider">
      <button>Create Provider Account</button>
    </router-link>

  </div>
</template>
