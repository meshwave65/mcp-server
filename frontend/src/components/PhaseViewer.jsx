// sofia/engine/frontend/src/components/PhaseViewer.jsx (v3.1 - Adaptado para nova arquitetura)

import React from 'react';
import './PhaseViewer.css';

function PhaseViewer({ segment }) {
  if (!segment) {
    return <div className="phase-viewer"><p>Selecione um segmento para visualizar.</p></div>;
  }

  const phases = segment.phases || [];

  return (
    <div className="phase-viewer">
      <h2 className="phase-viewer-title">Segmento: {segment.segment_name}</h2>
      <p className="phase-viewer-description">{segment.description || 'Disponível em breve.'}</p>
      <hr />
      <h3 className="phases-section-title">Fases do Desenvolvimento</h3>
      
      <div className="phases-button-container">
        {phases.length > 0 ? (
          phases.map(phase => (
            <div key={phase.phase_name} className="phase-dropdown">
              <button className="phase-button">{phase.phase_name}</button>
              <div className="module-dropdown-content">
                {phase.modules && phase.modules.length > 0 ? (
                  phase.modules.map(module => (
                    <span key={module.id} className="module-link">
                      {module.name}
                    </span>
                  ))
                ) : (
                  <span className="module-link empty">Nenhum módulo nesta fase.</span>
                )}
              </div>
            </div>
          ))
        ) : (
          <p>Nenhuma fase encontrada para este segmento.</p>
        )}
      </div>
    </div>
  );
}

export default PhaseViewer;

