<script setup lang="ts">
import { ref } from 'vue';
import { submitReview } from '../services/ratings';

const props = defineProps<{
  appointmentId: number;
  isOpen: boolean;
}>();

const emit = defineEmits(['close', 'success']);

const rating = ref(5);
const comment = ref('');
const loading = ref(false);
const error = ref('');

const setRating = (r: number) => {
  rating.value = r;
};

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';
  try {
    await submitReview({
      appointment_id: props.appointmentId,
      rating: rating.value,
      comment: comment.value
    });
    emit('success');
    emit('close');
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to submit review';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h2 class="modal-title">Rate Your Experience</h2>
        <button class="close-btn" @click="emit('close')" aria-label="Close modal">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="modal-body">
        <div class="appointment-pill">
          Appointment #{{ appointmentId }}
        </div>
        <p class="subtitle">How would you describe the service you received?</p>

        <div class="stars-container">
          <div class="stars">
            <button 
              v-for="i in 5" 
              :key="i"
              class="star-btn"
              :class="{ active: i <= rating }"
              @click="setRating(i)"
              type="button"
            >
              <svg width="36" height="36" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
              </svg>
            </button>
          </div>
          <span class="rating-label" v-if="rating">{{ rating }} / 5 Stars</span>
        </div>

        <div class="input-group">
          <label>Comments (Optional)</label>
          <textarea 
            v-model="comment" 
            placeholder="Share your thoughts about this provider..."
            rows="4"
          ></textarea>
        </div>

        <p v-if="error" class="error-msg">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          {{ error }}
        </p>
      </div>

      <div class="modal-footer">
        <button class="btn-secondary" @click="emit('close')" :disabled="loading">Cancel</button>
        <button class="btn-primary" @click="handleSubmit" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          <span v-else>Submit My Review</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  animation: fadeIn 0.2s ease-out;
  padding: 20px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-card {
  background: #1c1c24;
  width: 100%;
  max-width: 440px;
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  overflow: hidden;
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  font-family: 'DM Sans', sans-serif;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-header {
  padding: 24px 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.modal-title {
  margin: 0;
  font-family: 'Sora', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
}

.close-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  transform: rotate(90deg);
}

.modal-body {
  padding: 28px;
}

.appointment-pill {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #a78bfa;
  background: rgba(167, 139, 250, 0.1);
  padding: 4px 12px;
  border-radius: 100px;
  margin-bottom: 12px;
  border: 0.5px solid rgba(167, 139, 250, 0.2);
}

.subtitle {
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 24px;
  font-size: 15px;
  line-height: 1.5;
}

.stars-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 32px;
}

.stars {
  display: flex;
  gap: 10px;
}

.star-btn {
  background: none;
  border: none;
  padding: 0;
  color: rgba(255, 255, 255, 0.08);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.star-btn:hover {
  transform: scale(1.2) rotate(8deg);
  color: rgba(251, 191, 36, 0.3);
}

.star-btn.active {
  color: #fbbf24;
  filter: drop-shadow(0 0 12px rgba(251, 191, 36, 0.4));
}

.rating-label {
  font-size: 13px;
  font-weight: 600;
  color: #fbbf24;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group label {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 0.02em;
}

textarea {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 16px;
  color: #fff;
  resize: none;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.6;
  transition: all 0.2s;
}

textarea::placeholder {
  color: rgba(255, 255, 255, 0.2);
}

textarea:focus {
  outline: none;
  border-color: #a78bfa;
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 4px rgba(167, 139, 250, 0.1);
}

.error-msg {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #f87171;
  background: rgba(248, 113, 113, 0.1);
  padding: 12px;
  border-radius: 12px;
  font-size: 13px;
  margin-top: 20px;
  border: 0.5px solid rgba(248, 113, 113, 0.2);
}

.modal-footer {
  padding: 24px 28px;
  display: flex;
  gap: 14px;
  justify-content: flex-end;
  background: rgba(0, 0, 0, 0.2);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.btn-primary {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 14px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 8px 20px rgba(124, 58, 237, 0.25);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(124, 58, 237, 0.35);
  opacity: 0.95;
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.7);
  padding: 12px 24px;
  border-radius: 14px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(0.5);
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2.5px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 480px) {
  .modal-card {
    border-radius: 20px 20px 0 0;
    max-width: 100%;
    margin-bottom: -20px;
    animation: slideUpMobile 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }

  @keyframes slideUpMobile {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }

  .modal-overlay {
    align-items: flex-end;
    padding: 0;
  }
  
  .modal-footer {
    flex-direction: column;
    padding: 20px 28px 40px;
  }
  
  .btn-primary, .btn-secondary {
    width: 100%;
    justify-content: center;
    padding: 14px;
  }

  .modal-header {
    padding: 20px 24px;
  }

  .modal-body {
    padding: 24px;
  }
}
</style>
