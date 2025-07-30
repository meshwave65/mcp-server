// sofia/engine/frontend/src/components/StatusPanel.jsx (v3.1 - Painel de Boas-Vindas)

import React from 'react';
import './StatusPanel.css';

function StatusPanel() {
  return (
    <div className="status-panel">
      <h2>Painel de Controle SOFIA</h2>
      <div className="status-grid">
        <p className="welcome-message">
          Bem-vindo ao painel de gerenciamento do Projeto MeshWave.
        </p>
        <p className="instructions">
          Selecione um dos <strong>Segmentos</strong> na barra lateral esquerda para visualizar as fases de desenvolvimento e seus respectivos módulos.
        </p>
      </div>
    </div>
  );
}

export default StatusPanel;

