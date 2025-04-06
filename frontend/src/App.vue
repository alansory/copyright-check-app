<template>
  <div id="app" class="min-h-screen bg-gray-50 text-gray-800 px-4 py-10 flex flex-col items-center">
    <h1 class="text-3xl font-bold mb-8 text-center">Copyright Image Checker</h1>

    <UploadSection />
    <ResultSection v-if="result" :result="result" />
  </div>
</template>

<script>
import UploadSection from '@/components/UploadSection.vue';
import ResultSection from '@/components/ResultSection.vue';
import { useCopyrightStore } from '@/stores/useCopyrightStore';
import { storeToRefs } from 'pinia';

export default {
  name: 'App',
  components: {
    UploadSection,
    ResultSection,
  },
  setup() {
    const store = useCopyrightStore();
    const { result } = storeToRefs(store);

    return {
      result,
    };
  },
};
</script>

<style>
body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background-color: #f9fafb;
}
</style>
