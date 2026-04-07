import { reactive, readonly } from 'vue'

const state = reactive({
  isActive: false,
  message: ''
})

export function useLoading() {
  const startLoading = (msg = 'Loading...') => {
    state.message = msg
    state.isActive = true
  }

  const stopLoading = () => {
    state.isActive = false
    state.message = ''
  }

  return {
    loadingState: readonly(state),
    startLoading,
    stopLoading
  }
}
