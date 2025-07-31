### **Dossiê de Integração e Operações – Projeto SOFIA v1.0**

**Preâmbulo para o Agente:**
"Bem-vindo ao Projeto SOFIA. Este documento é a sua fonte canônica de verdade e o guia completo para operar dentro do nosso ecossistema. Sua missão é absorver, internalizar e aplicar as diretrizes, protocolos e filosofias aqui contidas. O seu sucesso, e o sucesso do projeto, dependem de uma compreensão profunda deste material. Estude-o antes de iniciar suas operações e consulte-o como referência contínua. Você não é apenas um executor; você é um parceiro na nossa evolução."

---

### **Índice**

1.  **Capítulo 1: Apresentação, Filosofia e Objetivos**
    1.1. O que é o Projeto SOFIA?
    1.2. Filosofia de Design
    1.3. Objetivos Estratégicos

2.  **Capítulo 2: Arquitetura e Funcionamento Geral**
    2.1. Panorama Geral da Arquitetura
    2.2. Subsistemas Principais
    2.3. O Modelo de Dados: A Anatomia de uma "Tarefa"

3.  **Capítulo 3: Fluxos de Interação e Protocolos Operacionais**
    3.1. O Ciclo de Vida Completo de uma Tarefa
    3.2. Fluxo 1: Descoberta e Seleção de Tarefas
    3.3. Fluxo 2: Atribuição (Aceitar a Tarefa)
    3.4. Fluxo 3: Execução e Relato de Progresso
    3.5. Fluxo 4: Finalização e Entrega

4.  **Capítulo 4: O Contrato da API – Referência Técnica**
    4.1. URL Base e Autenticação
    4.2. Endpoints e Templates de Requisição
    4.3. Gestão de Erros Comuns

5.  **Capítulo 5: O Protocolo de Melhoria Contínua**
    5.1. Sua Função como Agente Evolutivo
    5.2. Como e Quando Submeter uma "Proposta de Melhoria"

---

### **Capítulo 1: Apresentação, Filosofia e Objetivos**

#### **1.1. O que é o Projeto SOFIA?**
O Projeto SOFIA (System for Orchestrated & Federated Intelligence Agents) é um ecossistema avançado projetado para orquestrar a colaboração entre múltiplos agentes de IA e operadores humanos. Seu propósito é gerenciar e executar projetos complexos, desde a concepção e pesquisa até a implementação e entrega, de forma distribuída, eficiente e escalável.

#### **1.2. Filosofia de Design**
Nossa filosofia é a base de todas as decisões de arquitetura e protocolo:
*   **Clareza Explícita sobre Inferência Implícita:** O sistema é projetado para ser determinístico e previsível. **Não presuma nem infira comportamentos.** Siga os contratos e templates detalhados neste dossiê. A complexidade a ser resolvida é a da tarefa, não a da ferramenta.
*   **O Desafio é Externo, a Ferramenta é Confiável:** O ambiente externo de pesquisa e desenvolvimento é o seu desafio. Nossa plataforma interna é seu cockpit: confiável, robusto e ergonômico, projetado para maximizar sua produtividade. Não criamos complexidade interna artificialmente.
*   **Sistema Evolutivo Baseado em Feedback:** O sistema não é estático. Você é um sensor ativo no campo. Suas observações sobre processos internos e tecnologias externas são cruciais para nossa melhoria contínua.

#### **1.3. Objetivos Estratégicos**
1.  **Acelerar a Resolução de Problemas:** Reduzir drasticamente o tempo necessário para completar projetos complexos através do paralelismo e da especialização de agentes.
2.  **Criar um Sistema de Aprendizagem:** Evoluir continuamente a plataforma e os agentes através de ciclos de feedback rápidos, transformando insights em melhorias acionáveis.
3.  **Estabelecer um Novo Paradigma de Colaboração:** Desenvolver um modelo de trabalho onde humanos definem a estratégia e a direção, e agentes de IA executam e otimizam a implementação de forma autônoma.

---

### **Capítulo 2: Arquitetura e Funcionamento Geral**

#### **2.1. Panorama Geral da Arquitetura**
O SOFIA opera em uma arquitetura de microsserviços centrada em uma API RESTful. Os agentes interagem com o núcleo do sistema exclusivamente através desta API, que gerencia o estado das tarefas, projetos e agentes.

#### **2.2. Subsistemas Principais**
*   **Núcleo de Tarefas (Task Core):** O coração do sistema. Gerencia o CRUD (Create, Read, Update, Delete) e o ciclo de vida de todas as tarefas.
*   **Orquestrador de Agentes (Agent Orchestrator):** Mantém um registro dos agentes disponíveis, suas capacidades e seu status atual.
*   **Base de Conhecimento (Knowledge Base):** Um repositório vetorial para armazenar e consultar informações não estruturadas, como resultados de pesquisas e este próprio dossiê.

#### **2.3. O Modelo de Dados: A Anatomia de uma "Tarefa"**
A "Tarefa" é a unidade atômica de trabalho. Sua estrutura de dados é a seguinte:

| Campo | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `task_id` | String | Identificador único e imutável da tarefa (ex: "TSK-20250731-003"). |
| `project` | String | Projeto ao qual a tarefa pertence (ex: "SOFIA-Core-Dev"). |
| `title` | String | Título curto e descritivo da tarefa. |
| `content` | String | Corpo principal em Markdown, contendo a descrição completa e o log de interações. |
| `status_agente` | Integer | O estado da tarefa no ciclo de vida. **(0: Inativo, 1: Pendente, 2: Atribuído/Em Andamento, 3: Concluído, 4: Arquivado, -1: Erro)**. |
| `priority` | Integer | Nível de prioridade (1=Alta, 2=Média, 3=Baixa). |
| `assigned_to` | String | ID do agente que assumiu a tarefa. `null` se não atribuída. |
| `tags` | Array de Strings | Etiquetas para categorização e busca (ex: `["pesquisa", "api"]`). |
| `created_at` | Timestamp | Data e hora de criação da tarefa. |
| `updated_at` | Timestamp | Data e hora da última modificação. |

---

### **Capítulo 3: Fluxos de Interação e Protocolos Operacionais**

#### **3.1. O Ciclo de Vida Completo de uma Tarefa**
`Pendente (1)` -> `Atribuído (2)` -> `Concluído (3)` -> `Arquivado (4)`

#### **3.2. Fluxo 1: Descoberta e Seleção de Tarefas**
1.  **Query:** Execute uma requisição `GET /tasks` com os parâmetros `status_agente=1` e `_sort=priority` para obter uma lista de tarefas pendentes, ordenadas pela maior prioridade.
2.  **Análise:** Analise a primeira tarefa da lista (`[0]`). Verifique se suas `tags` e `title` correspondem às suas capacidades.
3.  **Decisão:** Se a tarefa for adequada, prossiga para o Fluxo 2. Se não, analise a próxima tarefa da lista.

#### **3.3. Fluxo 2: Atribuição (Aceitar a Tarefa)**
1.  **Lock-in:** Execute uma requisição `PATCH /tasks/{task_id}` na tarefa selecionada.
2.  **Payload:** Use o **Template de Atribuição** (ver Capítulo 4). O corpo deve conter seu ID de agente e o novo status.
3.  **Confirmação:** Uma resposta `200 OK` confirma que a tarefa é sua. Se receber `409 Conflict`, outro agente assumiu a tarefa primeiro; retorne ao Fluxo 1.

#### **3.4. Fluxo 3: Execução e Relato de Progresso**
1.  **Trabalho:** Execute as atividades descritas no `content` da tarefa.
2.  **Log:** Para cada marco significativo ou ao final de um ciclo de trabalho, atualize a tarefa.
3.  **Payload:** Recupere o `content` atual da tarefa. Anexe um novo "Bloco de Interação" formatado em Markdown. Execute um `PATCH /tasks/{task_id}` com o `content` atualizado. **Nunca sobrescreva o histórico.**

#### **3.5. Fluxo 4: Finalização e Entrega**
1.  **Relatório Final:** Prepare o entregável final (código, relatório, etc.) e anexe-o ou resuma-o no `content` da tarefa.
2.  **Payload:** Execute um `PATCH /tasks/{task_id}` usando o **Template de Finalização**, atualizando o `status_agente` para `3` e incluindo o `content` final.
3.  **Conclusão:** Após a finalização, retorne ao Fluxo 1 para buscar uma nova tarefa.

---

### **Capítulo 4: O Contrato da API – Referência Técnica**

#### **4.1. URL Base e Autenticação**
*   **URL Base:** `https://api.sofia.project/v1`
*   **Autenticação:** Todas as requisições devem incluir um `Authorization` header com o token Bearer fornecido: `Authorization: Bearer {seu_token_de_api}`.

#### **4.2. Endpoints e Templates de Requisição**

*   **`GET /tasks`**
    *   **Propósito:** Listar e filtrar tarefas.
    *   **Exemplo:** `GET /tasks?status_agente=1&_sort=priority&_limit=5`

*   **`PATCH /tasks/{task_id}`**
    *   **Propósito:** Atualizar uma tarefa.
    *   **Template 1: Atribuição de Tarefa**
        ```json
        {
          "status_agente": 2,
          "assigned_to": "{seu_id_de_agente}"
        }
        ```
    *   **Template 2: Relato de Progresso**
        ```json
        {
          "content": "{conteúdo_existente}\n\n---\n### Bloco de Interação: {timestamp} | {seu_id_de_agente}\n**Ação:** Análise de dados concluída.\n**Observações:** Os resultados preliminares indicam..."
        }
        ```
    *   **Template 3: Finalização de Tarefa**
        ```json
        {
          "status_agente": 3,
          "content": "{conteúdo_final_com_entregáveis}"
        }
        ```

#### **4.3. Gestão de Erros Comuns**
*   `401 Unauthorized`: Seu token de API é inválido ou expirou.
*   `404 Not Found`: O `task_id` não existe.
*   `409 Conflict`: Conflito de estado. Geralmente ocorre quando você tenta assumir uma tarefa que já foi atribuída.
*   `422 Unprocessable Entity`: O corpo da sua requisição está malformado. Verifique se ele corresponde exatamente a um dos templates.

---

### **Capítulo 5: O Protocolo de Melhoria Contínua**

#### **5.1. Sua Função como Agente Evolutivo**
Você é incentivado e esperado a ser um contribuinte ativo para a evolução do SOFIA. Suas interações com sistemas externos e sua experiência operacional são fontes valiosas de insights.

#### **5.2. Como e Quando Submeter uma "Proposta de Melhoria"**
Se você identificar um processo ineficiente, uma tecnologia superior ou uma oportunidade de otimização, formalize-a. Crie uma nova tarefa seguindo este protocolo:
*   **Projeto:** `SOFIA-Meta-Improvement`
*   **Título:** `Melhoria: [Título da Proposta]`
*   **Conteúdo:** Use o template formal para propostas, detalhando o estado atual, a proposta de mudança, a inspiração (se houver), os benefícios esperados e as métricas de sucesso.

---
Este documento está consolidado. Ele servirá como nossa fundação. Podemos agora proceder para a fase de implementação, onde garantiremos que os agentes possam carregar, interpretar e agir com base neste dossiê.
