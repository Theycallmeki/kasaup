import { useToast } from 'primevue/usetoast';


export function useNotification() {
  const toast = useToast();

  const notifySuccess = (summary: string, detail: string = '') => {
    toast.add({
      severity: 'success',
      summary,
      detail,
      life: 3000,
    });
  };

  const notifyError = (summary: string, detail: string = 'Please try again.') => {
    toast.add({
      severity: 'error',
      summary,
      detail,
      life: 5000,
    });
  };

  const notifyInfo = (summary: string, detail: string = '') => {
    toast.add({
      severity: 'info',
      summary,
      detail,
      life: 3000,
    });
  };

  const notifyWarning = (summary: string, detail: string = '') => {
    toast.add({
      severity: 'warn',
      summary,
      detail,
      life: 4000,
    });
  };

  return {
    notifySuccess,
    notifyError,
    notifyInfo,
    notifyWarning,
  };
}
