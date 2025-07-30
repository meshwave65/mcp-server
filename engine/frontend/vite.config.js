import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react( )],
  server: {
    // Configuração do proxy (que já estava correta)
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
    // --- A CORREÇÃO ESTÁ AQUI ---
    // Força o servidor Vite a escutar explicitamente no endereço de localhost.
    // Isso o torna "visível" para a verificação de serviço do nosso backend.
    host: 'localhost',
    // --- FIM DA CORREÇÃO ---
  },
} );

