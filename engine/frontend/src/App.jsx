// sofia/engine/frontend/src/App.jsx (v3.7 - Correção Final para Ngrok)

import React, { useState, useEffect } from 'react';
import './App.css';
import StatusPanel from './components/StatusPanel'; 
import PhaseViewer from './components/PhaseViewer';

function App() {
  const [roadmapData, setRoadmapData] = useState([]);
  const [activeSegment, setActiveSegment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchConfig = async () => {
      const sources = [
        'http://meshwave.com.br/sofia/config.json',
        '/config.json' // Vite serve a pasta /public na raiz
      ];

      for (const source of sources  ) {
        try {
          console.log(`Tentando buscar configuração de: ${source}`);
          const response = await fetch(source);
          if (!response.ok) throw new Error(`HTTP ${response.status}`);
          const config = await response.json();
          console.log(`✅ Configuração carregada com sucesso de: ${source}`);
          return config;
        } catch (error) {
          console.warn(`❌ Falha ao carregar de ${source}:`, error.message);
        }
      }
      throw new Error('Não foi possível carregar a configuração de nenhuma fonte disponível.');
    };

    const initializeApp = async () => {
      try {
        const config = await fetchConfig();
        const backendUrl = config.backend_url;
        if (!backendUrl) throw new Error('URL do backend não encontrada no config.json.');
        
        console.log("URL do Backend descoberta:", backendUrl);
        
        // --- CORREÇÃO DEFINITIVA ---
        // Adicionamos o cabeçalho 'ngrok-skip-browser-warning' para instruir o Ngrok
        // a não mostrar sua página de aviso HTML, indo direto para a nossa API.
        const fetchOptions = {
          headers: {
            'ngrok-skip-browser-warning': 'true'
          }
        };

        const roadmapResponse = await fetch(`${backendUrl}/api/v1/roadmap/`, fetchOptions);
        
        if (!roadmapResponse.ok) {
          throw new Error(`A resposta da API do roadmap não foi bem-sucedida (status: ${roadmapResponse.status}).`);
        }
        
        const data = await roadmapResponse.json();
        setRoadmapData(data);
        if (data && data.length > 0) setActiveSegment(data[0]);
        
      } catch (err) {
        console.error("Erro no processo de inicialização:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    initializeApp();
  }, []);

  const handleSegmentClick = (segment) => {
    setActiveSegment(segment);
  };

  const showStatusPanel = () => {
    setActiveSegment(null); 
  }

  if (loading) {
    return <div className="loading-screen">Carregando Configuração do Sistema...</div>;
  }

  if (error) {
    return <div className="error-screen">
      <h1>Erro Crítico</h1>
      <p>{error}</p>
      <p>Verifique se o backend está online e se o arquivo de configuração está acessível.</p>
    </div>;
  }

  return (
    <div className="sofia-app">
      <aside className="sidebar">
        <div className="sidebar-header" onClick={showStatusPanel} style={{ cursor: 'pointer' }} title="Voltar ao Painel de Controle">
          <img src="/meshwave_logo.png" alt="MeshWave Logo" className="logo" />
        </div>
        <div className="sidebar-block">
          <h3 className="block-title">Segmentos</h3>
          <div className="button-grid">
            {roadmapData.map(segment => (
              <button
                key={segment.segment_name}
                className={activeSegment?.segment_name === segment.segment_name ? 'segment-button active' : 'segment-button'}
                onClick={() => handleSegmentClick(segment)}
              >
                {segment.segment_name}
              </button>
            ))}
          </div>
        </div>
        <div className="sidebar-footer">
          <div className="sidebar-block">
            <h3 className="block-title">Acesso</h3>
            <div className="login-placeholder">Login/Usuário</div>
          </div>
          <div className="sidebar-block">
            <h3 className="block-title">Sistema</h3>
            <div className="settings-placeholder" onClick={showStatusPanel} style={{ cursor: 'pointer' }}>
                Painel de Controle
            </div>
          </div>
        </div>
      </aside>
      <main className="main-content">
        {activeSegment ? (
          <PhaseViewer segment={activeSegment} />
        ) : (
          <StatusPanel /> 
        )}
      </main>
    </div>
  );
}

export default App;

