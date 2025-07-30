Relatório Mestre: Arquitetura e Funcionamento do Sistema SOFIA (v2.0)
ID do Documento: SOFIA-BLUEPRINT-V2.0
Nome do Sistema: SOFIA (Sistema Orquestrador Federado de Inteligência Artificial)
Data: 2025-07-29
Status: FINALIZADO. Blueprint Oficial para Implementação.
(Nota: As seções 1, 2 e 5 permanecem as mesmas do relatório anterior. A mudança principal está na seção 3, que descreve o fluxo de trabalho.)
3. Gerenciamento de Tarefas e Fluxo de Trabalho (Modelo "Turn-Based")
O sistema evoluiu para um modelo de "documento vivo" com um sistema de turnos explícito, garantindo que a responsabilidade pela próxima ação seja sempre clara.
3.1. Estrutura do Arquivo de Tarefa
Localização: Um único diretório /tasks.
Estrutura Interna: Um arquivo Markdown que acumula blocos de conteúdo cronologicamente. Cada bloco (Dúvida, Esclarecimento, Relatório) deve ter seu próprio cabeçalho com um timestamp UTC para fins de auditoria.
Metadados Essenciais (Cabeçalho YAML):
task_id, title, assigned_to.
status_agente: O estado do trabalho (1-Open, 2-In_Progress, 3-On_Hold, 4-Done, 5-Canceled).
turn_holder: O novo metadado crucial. Indica quem deve agir.
0: Ação requerida do Agente/Consultor.
1: Ação requerida do Gestor/Orquestrador.
3.2. O Fluxo de Trabalho "Turn-Based"
Este novo fluxo elimina a necessidade de monitorar timestamps de arquivos, focando apenas no status_agente e no turn_holder.
Criação da Tarefa:
O Gestor cria a tarefa.
Estado Inicial: status_agente: 1 (Open), turn_holder: 0 (A bola está com qualquer Agente disponível).
Agente Aceita a Tarefa:
O Agente encontra uma tarefa com status_agente: 1.
Ele a aceita, mudando o estado para: status_agente: 2 (In_Progress), turn_holder: 0 (A bola continua com o Agente para que ele execute a pesquisa).
Agente Tem uma Dúvida (Passando o Turno):
O Agente paralisa a pesquisa.
Ele adiciona o bloco ### Dúvida do Agente... ao arquivo.
Ele muda o estado para: status_agente: 3 (On_Hold), turn_holder: 1 (A bola agora é do Gestor).
Lógica do Agente: "Eu não faço mais nada nesta tarefa até que o turn_holder volte a ser 0."
Gestor Responde à Dúvida (Devolvendo o Turno):
O Gestor (nós) escaneia o sistema procurando por tarefas com status_agente: 3 E turn_holder: 1.
Ele encontra a tarefa, lê a dúvida e adiciona o bloco ### Esclarecimento do Orquestrador....
Ele muda o estado para: status_agente: 3 (On_Hold), turn_holder: 0 (A bola foi devolvida ao Agente).
Lógica do Gestor: "Eu não olho mais para esta tarefa On_Hold porque o turn_holder é 0."
Agente Retoma o Trabalho:
O Agente, em seu monitoramento, vê uma tarefa que é sua, com status_agente: 3 e turn_holder: 0.
Ele entende que sua dúvida foi respondida.
Ele lê a resposta e muda o estado para: status_agente: 2 (In_Progress), turn_holder: 0 (A bola continua com ele para finalizar a pesquisa).
Agente Conclui a Tarefa:
O Agente adiciona o bloco ### Relatório de Conclusão....
Ele muda o estado para: status_agente: 4 (Done), turn_holder: 1 (A bola volta para o Gestor para aprovação final e arquivamento).
3.3. Vantagens do Novo Modelo
Clareza Absoluta: Nunca há dúvida sobre quem é o responsável pela próxima ação.
Eficiência: Elimina a necessidade de verificações constantes do mesmo arquivo. Se o turn_holder não é seu, você ignora a tarefa.
Simplicidade Lógica: O sistema se torna mais fácil de programar e automatizar, pois as regras são binárias e explícitas.
Auditoria Completa: O histórico de "passagem de bola" fica implicitamente registrado na sequência de blocos e na mudança do turn_holder ao longo do tempo.
