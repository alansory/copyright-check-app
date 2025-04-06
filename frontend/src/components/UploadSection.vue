<template>
  <div class="max-w-md mx-auto shadow-lg transition-all duration-300 rounded-lg bg-white">
    <div class="p-6 space-y-6 mb-4">
      <div
        :class="[
          'relative border-2 border-dashed rounded-xl p-6 transition-all duration-200 flex flex-col items-center justify-center gap-4',
          isDragging ? 'border-primary bg-primary/5' : 'border-muted-foreground/20',
          previewUrl ? 'bg-muted/10' : 'bg-muted/5 hover:bg-muted/10',
        ]"
        @dragover.prevent="isDragging = true"
        @dragleave="isDragging = false"
        @drop.prevent="handleDrop"
      >
        <input
          type="file"
          ref="fileInputRef"
          accept="image/*"
          @change="handleFileChange"
          class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
        />

        <div v-if="previewUrl" class="relative w-full">
          <div class="absolute -top-3 -right-3 z-20">
            <button
              class="h-7 w-7 rounded-full bg-red-500 text-white hover:bg-red-600 flex items-center justify-center shadow-md"
              @click.stop="clearFile"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
              </svg>
            </button>
          </div>
          <div class="relative w-full flex justify-center">
            <img
              :src="previewUrl || '/placeholder.svg'"
              alt="Preview"
              class="max-w-full max-h-64 rounded-lg object-contain shadow-md transition-all duration-300"
            />
          </div>
        </div>
        <template v-else>
          <div class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-8 w-8 text-blue-500">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
          </div>
          <div class="text-center space-y-1">
            <p class="font-medium text-base">Drag and drop your image here</p>
            <p class="text-sm text-gray-500">or click to browse files</p>
            <p class="text-xs text-gray-400 mt-2">Supports: JPG & PNG</p>
          </div>
        </template>
      </div>

      <button
        @click="handleSubmit"
        :disabled="!file || isUploading"
        :class="[
          'w-full h-12 font-medium transition-all duration-300 rounded-md shadow-md',
          'flex items-center justify-center gap-2',
          !file || isUploading 
            ? 'bg-gray-300 text-gray-600 cursor-not-allowed' 
            : 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800',
          'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
          'disabled:opacity-75 disabled:hover:bg-gray-300'
        ]"
      >
        <span v-if="isUploading" class="flex items-center gap-2">
          <svg
            class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          Processing...
        </span>
        <span v-else-if="file" class="flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          Check Copyright
        </span>
        <span v-else>Check Copyright</span>
      </button>
    </div>
  </div>
</template>

<script>
import { useCopyrightStore } from '@/stores/useCopyrightStore';

export default {
  data() {
    return {
      file: null,
      previewUrl: null,
      isDragging: false,
      isUploading: false
    }
  },
  setup() {
    const store = useCopyrightStore();
    
    return {
      store
    }
  },
  methods: {
    handleFileChange(e) {
      const selectedFile = e.target.files?.[0] || null
      this.handleFile(selectedFile)
    },
    handleFile(selectedFile) {
      if (selectedFile) {
        this.file = selectedFile

        // Create preview URL
        const url = URL.createObjectURL(selectedFile)
        this.previewUrl = url
      }
    },
    handleDrop(e) {
      this.isDragging = false

      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        this.handleFile(e.dataTransfer.files[0])
      }
    },
    clearFile() {
      if (this.previewUrl) {
        URL.revokeObjectURL(this.previewUrl)
      }
      this.file = null
      this.previewUrl = null
      if (this.$refs.fileInputRef) {
        this.$refs.fileInputRef.value = ""
      }

      this.store.clearResult()
    },
    handleSubmit() {
      if (this.file) {
        this.isUploading = true
        
        // Call the Pinia store action to check copyright
        this.store.checkCopyright(this.file)
          .finally(() => {
            this.isUploading = false
          });
      }
    }
  },
  beforeUnmount() {
    // Clean up preview URL when component is unmounted
    if (this.previewUrl) {
      URL.revokeObjectURL(this.previewUrl)
    }
  }
}
</script>