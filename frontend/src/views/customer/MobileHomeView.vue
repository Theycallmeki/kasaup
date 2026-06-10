<template>
  <div class="mobile-home-page">

    <nav class="mobile-navbar">
      <div class="nav-brand">Kasa<span>Up</span></div>
      <div class="nav-actions">
        <button class="btn btn-outline-sm" @click="goAuth">Login</button>
        <button class="btn btn-primary-sm" @click="goAuth">Get Started</button>
      </div>
    </nav>

    <section class="mobile-hero">
      <div class="mobile-hero-content">
        <span class="section-tag">Manpower Services</span>
        <h1 class="mobile-hero-title">
          Connect with <br />
          <span class="gradient-text">Trusted Pros</span> <br />
          in Your Area
        </h1>
        <p class="mobile-hero-desc">
          KasaUp is the smartest way to find, book, and manage reliable local services. From home repair to event planning, get it done right.
        </p>
        <div class="mobile-hero-actions">
          <button class="btn btn-primary-full" @click="goProviders">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            Browse Providers
          </button>
          <a href="#features" class="btn btn-outline-full" @click.prevent="scrollTo('#features')">
            Learn More
          </a>
        </div>
      </div>

      <div class="mobile-hero-card">
        <div class="infographic-card">
          <h3 class="mission-title">KasaUp</h3>
          <p class="mission-paragraph">
            KasaUp is a personal project created by <strong>Kian Jacob L. Laxamana</strong> as part of an upskilling initiative to learn modern web development. The ultimate goal of this platform is to empower and help local blue-collar workers in the Pampanga area find more job opportunities and connect them with clients seamlessly.
          </p>
        </div>
      </div>
    </section>

    <section id="features" class="mobile-features">
      <span class="section-tag">Why Choose Us</span>
      <h2 class="section-title">Everything you need<br />to get the job done</h2>
      <p class="section-subtitle">
        We've built a platform that makes finding, booking, and managing services seamless.
      </p>

      <div class="mobile-features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <h3>Verified Pros</h3>
          <p>Every provider undergoes strict background checks and skill verification.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
          </div>
          <h3>Easy Booking</h3>
          <p>Schedule services instantly with our streamlined booking system.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
          </div>
          <h3>Secure Payments</h3>
          <p>Pay safely through our platform with buyer protection guaranteed.</p>
        </div>
      </div>
    </section>

    <section id="how-it-works" class="mobile-how-it-works">
      <span class="section-tag">Process</span>
      <h2 class="section-title">How KasaUp Works</h2>
      <p class="section-subtitle">
        Getting started is as simple as 1-2-3.
      </p>

      <div class="steps-container">
        <div class="step-item">
          <div class="step-number">1</div>
          <div class="step-text">
            <h3>Search Services</h3>
            <p>Find the right professional for your specific needs in Pampanga.</p>
          </div>
        </div>
        <div class="step-connector"></div>
        <div class="step-item">
          <div class="step-number">2</div>
          <div class="step-text">
            <h3>Book & Confirm</h3>
            <p>Choose a time that works for you and get instant confirmation.</p>
          </div>
        </div>
        <div class="step-connector"></div>
        <div class="step-item">
          <div class="step-number">3</div>
          <div class="step-text">
            <h3>Get it Done</h3>
            <p>The provider completes the job. Pay only when you're satisfied.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="mobile-cta">
      <div class="cta-card">
        <h2>Ready to get started?</h2>
        <p>Join KasaUp and connect with trusted professionals near you.</p>
        <button class="btn btn-primary-full" @click="goAuth">Create an Account</button>
      </div>
    </section>

    <footer class="mobile-footer">
      <div class="footer-brand">
        <strong>KasaUp</strong> &copy; 2026. All rights reserved.
      </div>
      <div class="footer-links">
        Privacy Policy &middot; Terms of Service &middot; Contact Support
      </div>
    </footer>

  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"

const router = useRouter()

const goProviders = () => router.push("/providers")
const goAuth = () => router.push("/auth")

const scrollTo = (selector: string) => {
  const el = document.querySelector(selector)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped src="../../styles/customer/MobileHomeView.css"></style>
