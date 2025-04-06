import { defineStore } from 'pinia';

export const useCopyrightStore = defineStore('copyright', {
  state: () => ({
    result: null,
  }),
  actions: {
    clearResult() {
      this.result = null
    },
    async checkCopyright(file) {
      const formData = new FormData();
      formData.append('image', file);

      try {
        const response = await fetch('http://localhost:5001/check_copyright', {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();
        this.result = data;
      } catch (error) {
        console.error('Error:', error);
        this.result = { verdict: 'Error', confidence: 0, file_id: 'N/A' };
      }
    },
  },
});