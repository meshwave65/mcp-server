// sofia/engine/frontend/src/App.jsx (v2.3 - Ajustes de Design)

import React from 'react';
import './App.css';
import meshwaveLogo from '/meshwave_logo.png'; // Usando o caminho absoluto da pasta /public
import StatusPanel from './components/StatusPanel';

function App() {
  return (
    <div className="sofia-app">
      <aside className="sidebar">
        <div className="sidebar-header">
          <img src={meshwaveLogo} alt="MeshWave Logo" className="logo" />
        </div>
        <div className="sidebar-block">
          <h3 className="block-title">Segmentos</h3>
          <div className="button-grid">
            <button className="segment-button">Fundação</button>
            <button className="segment-button">IA Central</button>
            <button className="segment-button">Aplicações</button>
            <button className="segment-button">Interface</button>
            <button className="segment-button">Segurança</button>
            <button className="segment-button">Dados</button>
            <button className="segment-button">Infra</button>
            <button className="segment-button">Governança</button>
          </div>
        </div>
        <div className="sidebar-footer">
          <div className="sidebar-block">
            <h3 className="block-title">Acesso</h3>
            <div className="login-placeholder">Login/Usuário</div>
          </div>
          {/* --- A CORREÇÃO ESTÁ AQUI --- */}
          <div className="sidebar-block">
            <h3 className="block-title">Sistema</h3>
            <div className="settings-placeholder">Settings</div>
          </div>
          {/* --- FIM DA CORREÇÃO --- */}
        </div>
      </aside>

      <main className="main-content">
        <StatusPanel />
      </main>
    </div>
  );
}

export default App;

