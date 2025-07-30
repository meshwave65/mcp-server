# =============================================================================
# ARQUIVO COMPLETO: sofia/engine/backend/seed_database.py
# VERSÃO: 4.1 - Limpeza definitiva e roadmap completo
# =============================================================================

import sys
from pathlib import Path

# Adiciona o diretório 'app' ao path para que possamos importar 'database' e 'models'
sys.path.append(str(Path(__file__).parent / 'app'))

from app import database, models
from sqlalchemy.orm import Session

# --- ESTRUTURA DE DADOS COMPLETA DO ROADMAP ---
ROADMAP = {
    "FUNDACAO": {
        "description": "Estrutura base, arquitetura e setup inicial do projeto.",
        "phases": {
            "Arquitetura do Sistema": ["Definição da Arquitetura SOFIA", "Estrutura de Diretórios", "Controle de Versão (Git)"],
            "Configuração do Ambiente": ["Ambientes Virtuais (venv)", "Gerenciamento de Dependências", "Scripts de Inicialização"],
            "Base de Dados": ["Design do Schema", "Configuração do SQLAlchemy", "Scripts de Semeadura (Seed)"],
            "Motor Principal (Engine)": ["Backend (FastAPI)", "Frontend (React/Vite)", "Comunicação API"]
        }
    },
    "IA CENTRAL": {
        "description": "Desenvolvimento do núcleo de inteligência artificial e agentes autônomos.",
        "phases": {
            "Modelo de Agentes": ["Definição de Agente/Consultor", "Ciclo de Vida de Tarefas", "Modelo de Permissões"],
            "Processamento de Linguagem": ["Interpretação de Prompts", "Geração de Respostas", "Análise de Contexto"],
            "Gerenciamento de Tarefas": ["Alocação de Tarefas", "Monitoramento de Progresso", "Sistema de Filas (Queue)"],
            "Memória e Aprendizado": ["Vetorização de Documentos", "Mecanismos de Memória a Longo Prazo", "Fine-tuning de Modelos"]
        }
    },
    "APLICACAO": {
        "description": "Desenvolvimento do aplicativo cliente e interface.",
        "phases": {
            "Interface do Gestor": ["Dashboard de Projetos", "Visualização de Tarefas", "Criação e Edição de Tarefas"],
            "Interface do Agente": ["Listagem de Tarefas Disponíveis", "Visualização de Tarefa Única", "Mecanismo de 'Aceitar Tarefa'"],
            "Componentes Reutilizáveis": ["Sistema de Notificações", "Componentes de UI (Botões, Cards)", "Gráficos e Relatórios"],
            "Comunicação em Tempo Real": ["WebSockets para Notificações", "Atualização de Status ao Vivo", "Chat ou Comentários"]
        }
    },
    "INTERFACE": {
        "description": "Design e implementação da interface do usuário e experiência do usuário (UI/UX).",
        "phases": {
            "Design System": ["Paleta de Cores e Tipografia", "Biblioteca de Ícones", "Layouts Padrão (Grid System)"],
            "Prototipação": ["Wireframes de Baixa Fidelidade", "Mockups de Alta Fidelidade", "Prototipação Interativa (Figma)"],
            "Acessibilidade": ["Contraste de Cores (WCAG)", "Navegação por Teclado", "Leitores de Tela"],
            "Responsividade": ["Layout para Desktop", "Layout para Tablets", "Layout para Mobile"]
        }
    },
    "SEGURANCA": {
        "description": "Implementação de protocolos de segurança, autenticação e criptografia.",
        "phases": {
            "Autenticação e Autorização": ["Login de Usuário", "Gerenciamento de Sessão (Tokens)", "Controle de Acesso Baseado em Função (RBAC)"],
            "Segurança da API": ["Validação de Entradas", "Rate Limiting", "Proteção contra Injeção"],
            "Criptografia": ["Criptografia de Dados em Repouso", "Criptografia de Dados em Trânsito (HTTPS/TLS)", "Gerenciamento de Chaves"],
            "Auditoria e Logs": ["Logs de Acesso", "Monitoramento de Atividades Suspeitas", "Alertas de Segurança"]
        }
    },
    "DADOS": {
        "description": "Gerenciamento de banco de dados, pipelines de dados e análise.",
        "phases": {
            "Modelagem de Dados": ["Diagrama Entidade-Relacionamento (DER)", "Normalização de Dados", "Definição de Índices"],
            "ETL/ELT Pipelines": ["Extração de Dados de Fontes Externas", "Transformação e Limpeza de Dados", "Carga no Data Warehouse"],
            "Analytics e BI": ["Criação de Dashboards (Business Intelligence)", "Geração de Relatórios Automatizados", "Análise Preditiva"],
            "Backup e Recuperação": ["Estratégia de Backup", "Plano de Recuperação de Desastres (DRP)", "Testes de Restauração"]
        }
    },
    "INFRA": {
        "description": "Configuração de servidores, deployment, CI/CD e infraestrutura de nuvem.",
        "phases": {
            "Provisionamento de Infra": ["Infraestrutura como Código (IaC)", "Configuração de Servidores", "Redes e VPC"],
            "CI/CD": ["Integração Contínua (CI)", "Entrega Contínua (CD)", "Automação de Testes no Pipeline"],
            "Monitoramento e Observabilidade": ["Métricas de Performance (CPU, Memória)", "Coleta de Logs Centralizada", "Tracing de Aplicações"],
            "Conteinerização": ["Criação de Imagens Docker", "Orquestração de Contêineres (Kubernetes/Swarm)", "Registro de Contêineres"]
        }
    },
    "GOVERNANCA": {
        "description": "Definição de processos, documentação, conformidade e gerenciamento de projetos.",
        "phases": {
            "Documentação": ["Documentação da API (Swagger/OpenAPI)", "Guias de Contribuição", "Manuais de Usuário"],
            "Qualidade de Código": ["Padrões de Código (Linting)", "Revisão de Código (Code Review)", "Cobertura de Testes"],
            "Gerenciamento de Projeto": ["Metodologia Ágil (Scrum/Kanban)", "Ferramentas de Gestão (Jira/Trello)", "Comunicação com Stakeholders"],
            "Conformidade (Compliance)": ["Análise de Licenças de Software", "Adequação a Normas (LGPD/GDPR)", "Relatórios de Conformidade"]
        }
    }
}

def seed_data(db: Session):
    print("--- Iniciando a semeadura do banco de dados com o Roadmap Real e Completo ---")

    for seg_name, seg_data in ROADMAP.items():
        # Cria o Segmento
        segment = models.Segment(name=seg_name, description=seg_data["description"])
        db.add(segment)
        db.commit() # Commit para que o segmento tenha um ID
        print(f"✅ Segmento '{seg_name}' criado.")

        phase_order = 1
        for phase_name, modules_list in seg_data["phases"].items():
            # Cria a Fase
            phase = models.Phase(name=phase_name, order=phase_order, segment_id=segment.id)
            db.add(phase)
            db.commit() # Commit para que a fase tenha um ID
            print(f"  ✅ Fase '{phase_name}' criada.")
            phase_order += 1

            module_order = 1
            for module_name in modules_list:
                # Cria o Módulo
                module = models.Module(name=module_name, order=module_order, phase_id=phase.id)
                db.add(module)
                module_order += 1
            
            db.commit() # Commit final para salvar todos os módulos da fase
            print(f"    ✅ {len(modules_list)} módulos criados para a fase '{phase_name}'.")

    print("--- Semeadura do Roadmap Real concluída ---")


if __name__ == "__main__":
    # Passo crucial: Apagar o banco de dados antigo para garantir uma semeadura limpa
    db_file = Path(__file__).parent / 'app' / 'sofia.db'
    if db_file.exists():
        print(f"ATENÇÃO: Removendo banco de dados antigo: {db_file}")
        db_file.unlink()

    # Cria uma nova sessão e semeia os dados
    db_session = database.SessionLocal()
    try:
        print("Recriando todas as tabelas a partir de um banco de dados limpo...")
        models.Base.metadata.create_all(bind=database.engine)
        seed_data(db_session)
    finally:
        print("Fechando sessão do banco de dados.")
        db_session.close()

