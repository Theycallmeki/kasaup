<template>
  <div class="home-page">

<nav class="navbar animate-fade-in">
      <div class="nav-brand">Kasa<span>Up</span></div>
      <div class="nav-links">
        <a href="#features" class="nav-link" @click.prevent="scrollTo('#features')">Features</a>
        <a href="#how-it-works" class="nav-link" @click.prevent="scrollTo('#how-it-works')">How it Works</a>
      </div>
      <div class="nav-actions">
        <button class="btn btn-outline" @click="goAuth">Login</button>
        <button class="btn btn-primary" @click="goAuth">Get Started</button>
      </div>
    </nav>

<section class="hero">
      <div class="hero-content animate-fade-in delay-1">
        <span class="section-tag">Manpower Services</span>
        <h1 class="hero-title">
          Connect with <br/>
          <span class="gradient-text">Trusted Pros</span> <br/>
          in Your Area
        </h1>
        <p class="hero-desc">
          KasaUp is the smartest way to find, book, and manage reliable local services. From home repair to event planning, get it done right.
        </p>
        <div class="hero-actions">
          <button class="btn btn-primary" @click="goProviders">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            Browse Providers
          </button>
          <a href="#how-it-works" class="btn btn-outline">
            Learn More
          </a>
        </div>
      </div>
      
      <div class="hero-visual animate-fade-in delay-2">
        <div class="infographic-orb"></div>
        <div class="infographic-card">
          <div class="info-item">
            <div class="info-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="info-text">
              <h4>Active Providers</h4>
              <p>Ready to help</p>
            </div>
            <div class="info-value">12.5k+</div>
          </div>
          <div class="info-item">
            <div class="info-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
            </div>
            <div class="info-text">
              <h4>Average Rating</h4>
              <p>Across all services</p>
            </div>
            <div class="info-value">4.9/5</div>
          </div>
          <div class="info-item">
            <div class="info-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                <line x1="8" y1="21" x2="16" y2="21"></line>
                <line x1="12" y1="17" x2="12" y2="21"></line>
              </svg>
            </div>
            <div class="info-text">
              <h4>Jobs Completed</h4>
              <p>Successfully delivered</p>
            </div>
            <div class="info-value">850k+</div>
          </div>
        </div>
      </div>
    </section>

<section id="features" class="features">
      <span class="section-tag">Why Choose Us</span>
      <h2 class="section-title">Everything you need <br/> to get the job done</h2>
      <p class="section-subtitle">
        We've built a comprehensive platform that makes finding, booking, and managing services seamless for both customers and providers.
      </p>

      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <h3>Verified Professionals</h3>
          <p>Every provider on our platform undergoes a strict verification process to ensure quality and reliability.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
          </div>
          <h3>Smart Scheduling</h3>
          <p>Book appointments effortlessly with our intelligent calendar system that syncs in real-time.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
          </div>
          <h3>Secure Payments</h3>
          <p>Your transactions are protected with enterprise-grade security and escrow services.</p>
        </div>
      </div>
    </section>

<section id="how-it-works" class="how-it-works">
      <span class="section-tag">Process</span>
      <h2 class="section-title">How it works</h2>
      <p class="section-subtitle">
        Getting started with KasaUp is as simple as 1-2-3. We've streamlined the entire process.
      </p>

      <div class="workflow">
        <div class="workflow-step">
          <div class="workflow-marker">1</div>
          <div class="workflow-content">
            <h3>Search & Compare</h3>
            <p>Browse through our extensive list of verified service providers, compare their ratings, prices, and past work portfolios.</p>
          </div>
        </div>
        <div class="workflow-step">
          <div class="workflow-marker">2</div>
          <div class="workflow-content">
            <h3>Book Instantly</h3>
            <p>Select your preferred time slot and book the service directly through our platform with transparent upfront pricing.</p>
          </div>
        </div>
        <div class="workflow-step">
          <div class="workflow-marker">3</div>
          <div class="workflow-content">
            <h3>Get it Done</h3>
            <p>The provider arrives at your location, completes the job to your satisfaction, and payment is released securely.</p>
          </div>
        </div>
      </div>
    </section>

<section class="cta-section">
      <div class="cta-box">
        <div class="cta-content">
          <h2 class="cta-title">Ready to elevate your experience?</h2>
          <p class="cta-desc">
            Join thousands of satisfied customers and top-rated professionals on the fastest growing service platform.
          </p>
          <div class="hero-actions" style="justify-content: center;">
            <button class="btn btn-primary" @click="goAuth">Create an Account</button>
            <button class="btn btn-outline" @click="goProviders">Explore Services</button>
          </div>
        </div>
      </div>
    </section>

<footer class="footer">
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

<style scoped src="../../styles/customer/HomeView.css"></style>