// ~/home/sofia/engine/frontend/src/App.jsx
// Versão com lógica de login para alternar entre visão pública e painel de gestor.

import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:8000/api/v1';

// --- Componente da Barra Lateral (Sidebar ) ---
// Agora inclui um botão de Login/Logout funcional
const Sidebar = ({ segments, onSelectSegment, selectedSegmentName, isLoading, isLoggedIn, onLogin, onLogout }) => (
  <aside className="sidebar">
    <div className="logo">
      <img src="/meshwave-logo.png" alt="MeshWave Logo" />
      <span>MeshWave</span>
    </div>
    <nav>
      <p className="nav-title">SEGMENTOS</p>
      {isLoading ? (
        <p>Carregando...</p>
      ) : (
        segments.map(segment => (
          <button
            key={segment.segment_name}
            className={selectedSegmentName === segment.segment_name ? 'active' : ''}
            onClick={() => onSelectSegment(segment)}
          >
            {segment.segment_name}
          </button>
        ))
      )}
    </nav>
    <div className="sidebar-footer">
      <p className="nav-title">ACESSO</p>
      {isLoggedIn ? (
        <button onClick={onLogout}>Logout</button>
      ) : (
        <button onClick={onLogin}>Login/Usuário</button>
      )}
      <p className="nav-title">SISTEMA</p>
      {/* O Painel de Controle só é "ativo" se estiver logado */}
      <button className={isLoggedIn ? 'active' : ''}>Painel de Controle</button>
    </div>
  </aside>
);

// --- Componente da Visão Pública ---
// Exibe o roadmap informativo.
const PublicRoadmapView = ({ selectedSegment }) => {
  if (!selectedSegment) {
    return (
      <div className="content-placeholder">
        <h1>Bem-vindo ao Projeto MeshWave</h1>
        <p>Selecione um segmento na barra lateral para explorar o progresso do nosso projeto.</p>
      </div>
    );
  }
  return (
    <div className="segment-view">
      <header className="segment-header">
        <h2>Segmento: {selectedSegment.segment_name}</h2>
        <p>Passe o mouse sobre uma fase para ver seus módulos.</p>
      </header>
      <section className="phases-section">
        <h3>Fases do Desenvolvimento</h3>
        <div className="phases-grid">
          {selectedSegment.phases.map(phase => (
            <div key={phase.phase_name} className="phase-card">
              <div className="phase-name">{phase.phase_name}</div>
              <div className="modules-on-hover">
                <h4>Módulos:</h4>
                {phase.modules.length > 0 ? (
                  <ul>{phase.modules.map(module => <li key={module.id}>{module.name}</li>)}</ul>
                ) : (
                  <p>Nenhum módulo nesta fase.</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

// --- Componente do Painel do Gestor (Dashboard) ---
// Por enquanto, é um placeholder. Aqui entrará a interatividade.
const ManagerDashboard = () => {
    return (
        <div className="content-placeholder">
            <h1>Painel do Gestor</h1>
            <p>Área interativa para gerenciamento de tarefas, agentes e sistema.</p>
            <p>(Funcionalidades futuras serão implementadas aqui)</p>
        </div>
    );
};


// --- Componente Principal da Aplicação ---
function App() {
  const [roadmap, setRoadmap] = useState([]);
  const [selectedSegment, setSelectedSegment] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Novo estado para controlar o login

  // Função para simular o login
  const handleLogin = () => {
    // Em um sistema real, isso abriria um modal de login e faria uma chamada à API.
    // Por agora, apenas alternamos o estado.
    const password = prompt("Para acessar o modo de gestão, por favor, insira a senha:");
    // A senha aqui é apenas para demonstração no frontend. A segurança real está no backend.
    if (password === "a_sua_senha_segura_aqui") {
        setIsLoggedIn(true);
        setSelectedSegment(null); // Reseta a seleção para mostrar o dashboard
    } else {
        alert("Senha incorreta.");
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  useEffect(() => {
    const fetchRoadmapData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await axios.get(`${API_URL}/roadmap`);
        setRoadmap(response.data);
      } catch (err) {
        setError("Não foi possível carregar os dados do roadmap.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchRoadmapData();
  }, []);

  return (
    <div className="main-layout">
      <Sidebar 
        segments={roadmap}
        onSelectSegment={setSelectedSegment}
        selectedSegmentName={selectedSegment?.segment_name}
        isLoading={isLoading}
        isLoggedIn={isLoggedIn}
        onLogin={handleLogin}
        onLogout={handleLogout}
      />
      <main className="content-area">
        {error ? (
          <p className="error-message">{error}</p>
        ) : (
          // Renderiza um componente ou outro com base no estado de login
          isLoggedIn ? <ManagerDashboard /> : <PublicRoadmapView selectedSegment={selectedSegment} />
        )}
      </main>
    </div>
  );
}

export default App;

