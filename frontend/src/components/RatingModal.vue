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
    <div class="modal-content">
      <div class="modal-header">
        <h2>Rate Your Experience</h2>
        <button class="close-btn" @click="emit('close')">&times;</button>
      </div>

      <div class="modal-body">
        <p class="subtitle">How was the service for appointment #{{ appointmentId }}?</p>

        <div class="stars">
          <button 
            v-for="i in 5" 
            :key="i"
            class="star-btn"
            :class="{ active: i <= rating }"
            @click="setRating(i)"
          >
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
            </svg>
          </button>
        </div>

        <div class="input-group">
          <label>Comments (Optional)</label>
          <textarea 
            v-model="comment" 
            placeholder="Share your thoughts about the provider..."
            rows="4"
          ></textarea>
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>
      </div>

      <div class="modal-footer">
        <button class="secondary-btn" @click="emit('close')" :disabled="loading">Cancel</button>
        <button class="primary-btn" @click="handleSubmit" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          Submit Review
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: var(--bg);
  width: 90%;
  max-width: 480px;
  border-radius: 24px;
  border: 1px solid var(--border);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  animation: slideUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-header {
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border);
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: var(--text);
  cursor: pointer;
  transition: color 0.2s;
}

.close-btn:hover {
  color: var(--accent);
}

.modal-body {
  padding: 24px;
}

.subtitle {
  color: var(--text);
  margin-bottom: 24px;
  font-size: 15px;
}

.stars {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 32px;
}

.star-btn {
  background: none;
  border: none;
  padding: 0;
  color: #3f3f46;
  cursor: pointer;
  transition: transform 0.2s, color 0.2s;
}

.star-btn:hover {
  transform: scale(1.1);
}

.star-btn.active {
  color: #fbbf24;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-h);
}

textarea {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px;
  color: var(--text-h);
  resize: none;
  font-family: inherit;
  font-size: 15px;
}

textarea:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--accent-bg);
}

.error-msg {
  color: #ef4444;
  font-size: 13px;
  margin-top: 12px;
  text-align: center;
}

.modal-footer {
  padding: 24px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  background: rgba(255, 255, 255, 0.02);
}

.primary-btn {
  background: var(--accent);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.primary-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.secondary-btn {
  background: none;
  border: 1px solid var(--border);
  color: var(--text);
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
}

.primary-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
