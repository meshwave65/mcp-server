// sofia/engine/frontend/src/components/StatusPanel.jsx

import React, { useState, useEffect } from 'react';
import './StatusPanel.css'; // Criaremos este arquivo de estilo a seguir

const StatusIndicator = ({ status }) => (
  <span className={`status-indicator ${status === 'ATIVO' ? 'active' : 'inactive'}`}>
    {status}
  </span>
);

function StatusPanel() {
  const [statusData, setStatusData] = useState(null);
  const [error, setError] = useState(null);

  const fetchStatus = () => {
    // O frontend chama seu próprio backend usando um caminho relativo.
    fetch('/api/v1/engine/status')
      .then(res => {
        if (!res.ok) {
          throw new Error('Falha ao buscar status do motor.');
        }
        return res.json();
      })
      .then(data => {
        setStatusData(data);
        setError(null); // Limpa erros anteriores se a chamada for bem-sucedida
      })
      .catch(err => {
        console.error(err);
        setError(err.message);
        // Mantém os dados antigos em caso de falha temporária, para não piscar a tela
      });
  };

  useEffect(() => {
    fetchStatus(); // Busca o status imediatamente ao carregar
    const intervalId = setInterval(fetchStatus, 5000); // E depois a cada 5 segundos
    return () => clearInterval(intervalId); // Limpa o intervalo ao desmontar o componente
  }, []);

  return (
    <div className="status-panel">
      <h2>Status do Motor SOFIA</h2>
      {error && <p className="error-message">Erro de comunicação com o Backend: {error}</p>}
      {!statusData && !error && <p>Carregando status...</p>}
      {statusData && (
        <div className="status-grid">
          <div className="status-item">
            <span className="service-name">Backend</span>
            <StatusIndicator status={statusData.backend.status} />
          </div>
          <div className="status-item">
            <span className="service-name">Frontend</span>
            <StatusIndicator status={statusData.frontend.status} />
          </div>
          <div className="status-item">
            <span className="service-name">NGROK</span>
            <StatusIndicator status={statusData.ngrok.status} />
          </div>
          {statusData.ngrok.url && (
            <div className="ngrok-url-container">
              <span className="service-name">URL Pública</span>
              <input type="text" readOnly value={statusData.ngrok.url} className="ngrok-url-input" />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default StatusPanel;

