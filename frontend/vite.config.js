import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react( )],
  server: {
    // --- INÍCIO DA CORREÇÃO CRÍTICA ---
    proxy: {
      // Qualquer requisição do frontend que comece com '/api'
      // será redirecionada para o backend do SOFIA na porta 8000.
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      // Qualquer requisição do frontend que comece com '/fsmw'
      // será redirecionada para o backend do FSMW na porta 8001.
      '/fsmw': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      }
    }
    // --- FIM DA CORREÇÃO CRÍTICA ---
  }
} )

