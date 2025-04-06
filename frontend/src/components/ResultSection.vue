<template>
  <div
    v-if="result"
    class="max-w-md mx-auto mt-6 bg-white p-6 rounded-2xl shadow-md space-y-4"
  >
    <h2 class="text-xl font-semibold text-gray-800">Result</h2>
    <div class="space-y-2">
      <p><span class="font-medium text-gray-600">Verdict:</span> <span :class="verdictClass">{{ result.verdict }}</span></p>
      <p><span class="font-medium text-gray-600">Confidence:</span> {{ result.confidence }}%</p>
      <p><span class="font-medium text-gray-600">File ID:</span> {{ result.file_id }}</p>
      
      <div class="w-full bg-gray-200 rounded-full h-2.5 mt-2">
        <div class="h-2.5 rounded-full" 
             :class="result.verdict === 'Copyright Infringed' ? 'bg-red-500' : 'bg-green-500'"
             :style="{ width: `${result.confidence}%` }"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResultSection',
  props: {
    result: Object,
  },
  computed: {
    verdictClass() {
      const results = ["Copyright Infringed", "Error"];
      return results.includes(this.result.verdict)
        ? 'text-red-600 font-bold'
        : 'text-green-600 font-bold';
    },
  },
};
</script>