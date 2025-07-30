Relatório Mestre: Arquitetura e Funcionamento do Sistema SOFIA
ID do Documento: SOFIA-BLUEPRINT-V1.0
Nome do Sistema: SOFIA (Sistema Orquestrador Federado de Inteligência Artificial)
Data: 2025-07-29
1. Sumário Executivo
SOFIA é uma plataforma de software projetada para atuar como um "cérebro" na gestão de projetos complexos de pesquisa e desenvolvimento. Ele funciona como um servidor MCP (Model Context Protocol) avançado, orquestrando o fluxo de trabalho entre gestores humanos, uma IA central (Manus) e agentes consultores (humanos ou IA).
Sua arquitetura "Headless" e Federada foi projetada com três princípios fundamentais: Automação, Segurança e Escalabilidade, permitindo desde o desenvolvimento de projetos internos até a oferta como um produto SaaS (Software as a Service) com soberania de dados para clientes corporativos.
2. Módulos Detalhados do Sistema
O ecossistema SOFIA é composto por três módulos principais e um componente de automação.
Módulo 1: O "Project C3" (Centro de Comando e Controle)
Descrição: É o coração do sistema, a interface de gerenciamento e o motor da API.
Componentes:
Backend (O Cérebro): Uma API em Python/FastAPI, conectada a um banco de dados MySQL. Contém toda a lógica de negócios, gerenciamento de tarefas, estados e a API RESTful que serve como única fonte da verdade.
Frontend (A Interface): Uma aplicação web em React/Vite, projetada para ser implantada em um servidor web (como a Locaweb). Ela oferece a interface visual para os gestores, com navegação hierárquica (Segmento -> Fase -> Módulo) e dashboards contextuais.
Ponte de Configuração: Um arquivo config.json desacoplado, hospedado em um local de fácil atualização (como o próprio site do cliente), que permite ao frontend descobrir dinamicamente a URL do backend, garantindo flexibilidade e resiliência.
Módulo 2: O "Agente Sentinela"
Descrição: Um serviço de automação e monitoramento que garante a saúde e a conformidade do ambiente de desenvolvimento.
Componentes:
Monitor de Processos ("Trinity Sentinel"): Um script Python que verifica continuamente se os três processos essenciais (Backend, Frontend e o túnel Ngrok) estão ativos, reiniciando-os automaticamente em caso de falha.
Controlador de SLA: Mantém uma base de dados própria para rastrear os prazos de cada tarefa, atualizando o status_sla (Aberta, Em Andamento, Atrasada, etc.) que determina a cor da tarefa na UI.
Orquestrador de Deploy: Interage com o Git (via SSH) para atualizar automaticamente o config.json e acionar o pipeline de CI/CD no GitHub Actions, garantindo que as mudanças sejam publicadas sem intervenção manual.
Módulo 3: O Pipeline de CI/CD (A "Esteira" de Produção)
Descrição: O fluxo automatizado que compila e publica o frontend na web.
Componentes:
GitHub Actions: O motor de automação do GitHub.
Workflow de Deploy: Um arquivo .yml que define os passos: a cada push no branch main, o GitHub Actions irá automaticamente compilar o projeto React (npm run build) e enviar os arquivos resultantes para o servidor de hospedagem (Locaweb) via FTP, usando credenciais armazenadas de forma segura nos "Secrets" do repositório.
3. Como o Sistema Funciona: Uma Sessão Passo a Passo
Vamos simular uma sessão completa, desde a criação de uma tarefa até a sua conclusão.
Personagens:
O Gestor: Você, operando a interface do SOFIA.
SOFIA: Todo o sistema automatizado.
Agente Consultor: Um especialista (humano ou IA) que executará a pesquisa.
Cenário: O Gestor precisa de uma análise sobre "Protocolos de Criptografia Pós-Quântica".
Passo 1: O Gestor Cria a Tarefa
O Gestor acessa https://meshwave.com.br/mcp/meshwave/project_c3.
Ele navega pela UI: clica no segmento SEGURANCA, depois na Fase 3: Descentralização, e no módulo Criptografia Avançada.
Ele clica em "Nova Tarefa" e preenche os detalhes:
Título: "Análise de Algoritmos Pós-Quânticos para Redes Mesh"
Descrição: "Pesquisar e comparar os algoritmos finalistas do NIST (Kyber, Dilithium, etc. ), focando em sua aplicabilidade para comunicação P2P em dispositivos móveis..."
Prazo: Define um prazo de 3 dias.
Ao salvar, a UI envia os dados para a API do Backend.
Passo 2: SOFIA Entra em Ação (Nos Bastidores)
Backend: Recebe a requisição, cria um novo arquivo TASK-006.md no diretório /tasks e faz o git push para o GitHub.
Agente Sentinela: Detecta a nova tarefa, a registra em sua base de dados de SLA com status_sla: 0 (Aberta, 🔵 Azul) e calcula o timestamp_deadline (agora + 3 dias).
Passo 3: O Agente Aceita a Tarefa
O Agente Consultor vê a nova tarefa Azul na UI.
Ele a "pega", e o sistema atualiza o status_agente para 2 (In_Progress).
O Sentinela detecta a mudança e atualiza o status_sla para 1 (Em Andamento, 🟢 Verde).
Passo 4: O Agente Tem uma Dúvida
O Agente não tem certeza se deve focar em performance ou em tamanho da chave.
Ele paralisa a pesquisa, edita o arquivo TASK-006.md, adiciona o bloco ### Dúvida do Agente... e muda o status_agente para 3 (On_Hold).
O Sentinela vê que a tarefa está On_Hold, mas como ainda está dentro do prazo, a cor permanece 🟢 Verde.
Passo 5: O Gestor Responde
O Gestor vê a tarefa em espera, lê a dúvida e edita o arquivo, adicionando o bloco ### Esclarecimento do Orquestrador... com a resposta: "Foque em performance."
O Agente vê que o arquivo foi atualizado, lê a resposta, muda o status_agente de volta para 2 e retoma o trabalho.
Passo 6: O Sentinela Detecta um Atraso
Passam-se 3 dias. O Agente ainda não terminou.
O Sentinela, em sua verificação periódica, compara o tempo atual com o timestamp_deadline. Como o prazo foi ultrapassado, ele atualiza o status_sla para 2 (Atenção, 🟡 Amarelo).
O Gestor, ao olhar o dashboard, vê imediatamente a tarefa amarela e sabe que precisa de atenção.
Passo 7: O Agente Conclui a Tarefa
O Agente finaliza a pesquisa, edita o TASK-006.md pela última vez, adicionando o bloco ### Relatório de Conclusão... com toda a análise.
Ele muda o status_agente para 4 (Done).
O Sentinela detecta a conclusão. Como foi depois do prazo, ele define o status_sla final como 5 (Concluída com Atraso, ⚫️ Preto).
O ciclo está completo. Todo o histórico da tarefa, desde sua criação até as dúvidas e a conclusão, está registrado em um único arquivo, e seu ciclo de vida temporal foi monitorado e visualizado de forma automática pelo SOFIA.
