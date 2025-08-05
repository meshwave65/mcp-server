Relatório de Migração para Arquitetura SOFIA (v1.0)
1. O Problema Original (O Estado Anterior)
Nossa estrutura inicial misturava as responsabilidades do Motor (o sistema que gerencia tudo) e do Projeto (o aplicativo que está sendo desenvolvido). O diretório MeshWave-Core continha tanto o código do aplicativo quanto os scripts do motor (backend, frontend, trinity_sentinel), além de pastas de teste de outras arquiteturas (clients/). Isso tornava o sistema difícil de manter, escalar e entender.
2. A Solução: A Arquitetura SOFIA
Projetamos e implementamos uma nova arquitetura chamada SOFIA, baseada em dois princípios fundamentais:
Separação de Responsabilidades: O Motor (engine) é uma coisa, os Projetos dos Clientes (clients) são outra. Eles são completamente separados.
Encapsulamento: Cada projeto é autocontido. Ele vive em sua própria pasta e contém tudo o que precisa para funcionar, incluindo seu próprio código, tarefas (tasks/) e relatórios (reports/).
3. O Que Acabamos de Fazer (Nossas Realizações)
Executamos com sucesso a Fase de Migração Física. Isso significa que reorganizamos todos os arquivos e pastas para se alinharem à nova arquitetura.
Estado Atual e Definitivo da Estrutura de Arquivos:
~/home/mesh/home/
└── sofia/
    │
    ├── engine/                 <-- O MOTOR SOFIA (Cérebro do Sistema)
    │   │
    │   ├── backend/            <-- A API e lógica do motor (permanece aqui)
    │   │   ├── app/
    │   │   ├── seed_database.py
    │   │   ├── test_env.py
    │   │   └── .env
    │   │
    │   ├── frontend/           <-- A interface web do motor (permanece aqui)
    │   │
    │   ├── trinity_sentinel.py <-- O SCRIPT PARA LIGAR O MOTOR
    │   └── trinity_stop.py     <-- O SCRIPT PARA DESLIGAR O MOTOR
    │
    └── clients/                <-- O DIRETÓRIO DE CLIENTES
        │
        └── meshwave/           <-- A "GARAGEM" DO NOSSO CLIENTE
            │
            ├── project_AppMWC/ <-- O PROJETO, AGORA LIMPO E AUTOCONTIDO
            │   └── (código fonte do antigo MeshWave-Core, .git, etc.)
            │
            └── config_sofia.json <-- A "CHAVE MESTRA" que descreve os projetos do cliente
Em resumo: a "cirurgia" nos arquivos foi concluída com sucesso. A base da nossa nova casa está construída e é sólida.
4. Próximos Passos (O Caminho à Frente)
Agora que a estrutura física está correta, precisamos fazer a "instalação elétrica e hidráulica". Ou seja, precisamos atualizar o código do motor para que ele entenda e funcione com essa nova estrutura.
Esta é a Fase de Adaptação Lógica.
Nosso Foco Imediato: O Backend do Motor (sofia/engine/backend/)
O cérebro do motor precisa aprender a:
Parar de procurar arquivos "ao seu lado": Ele não pode mais assumir que um projeto ou uma tarefa está em ../ ou algo parecido.
Aprender a Ler o Mapa: Ele deve primeiro ler o config_sofia.json para descobrir quais projetos existem e onde eles estão localizados no sistema de arquivos.
Usar o Mapa para Agir: Todos os comandos (listar tarefas, iniciar NGROK, etc.) devem usar as informações do config_sofia.json para construir os caminhos corretos para os arquivos do projeto (ex: /home/mesh/home/sofia/clients/meshwave/project_AppMWC/tasks/).
Ação Concreta Imediata:
Vamos começar a modificar o arquivo principal do backend (provavelmente sofia/engine/backend/app/main.py). Vou fornecer um código de exemplo claro para iniciarmos esta adaptação. Este código irá implementar a nova lógica de "ler o mapa antes de agir".
