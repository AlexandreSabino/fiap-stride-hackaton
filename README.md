# fiap-stride-hackaton

---
### Desafio: Modelagem de ameaças utilizando IA
A FIAP Software Security, empresa de Segurança de Sistemas, está analisando a viabilidade de uma nova funcionalidade para otimizar seu
software de análise de vulnerabilidades em arquitetura de sistemas. O objetivo da empresa é usar novas tecnologias para identificar e tratar
vulnerabilidades que possam colocar em risco a segurança dos sistemas criados por arquitetos(as) e desenvolvedores(as).
Um dos desafios é utilizar Inteligência Artificial para realizar automaticamente a modelagem de ameaças, baseado na metodologia STRIDE
de um sistema a partir de um diagrama de arquitetura de software em imagem. A empresa tem o objetivo de validar a viabilidade dessa feature, e para isso,
será necessário fazer um MVP para detecção supervisionada de ameaças.

---
### Arquitetura da Solução: Multi-Agent Orchestration
A solução foi construída utilizando uma arquitetura de múltiplos agentes que operam em um Self-Correction Loop (Loop de Auto-Correção). 
Essa abordagem garante que a IA não apenas "descreva" a imagem, mas realize uma auditoria técnica rigorosa antes de gerar o relatório de segurança.
``` mermaid
flowchart TD
    software_architecture_vision_analyst --> cloud_architecture_quality_auditor
    cloud_architecture_quality_auditor -->  software_architecture_vision_analyst
    cloud_architecture_quality_auditor --> senior_security_researcher
```
---
### Tecnologia e frameworks.
- Para orquestração dos agentes foi utilizado o framework [CrewAi](https://www.crewai.com/).
- O Modelo de LLM escolhido foi o gpt-4o da open-ai, configurado nessa função: [config.py](utils/config.py)
- Para o front-end do projeto optei por utilizar: [Streamlit](https://streamlit.io/)
---
### Agentes e Responsabilidades
---
- ### Software Architecture Vision Analyst: ### 
    Responsável pela extração primária de dados. 
    Utiliza técnicas de Recursive Scanning para decompor containers e identificar cada ícone e rótulo de texto individualmente.
    - [Prompt](prompts/vision.md) 
    - [Agent](agents/vision_agent.py)
    
    ***Fluxo de Execução do Agente.***
    O agente faz uma varredura no diagrama, garantindo que nenhum componente seja omitido.
    
    ***Passo 1: Reconhecimento Periférico***
  
    Antes de entrar no "coração" da arquitetura, o agente foca nas bordas da imagem.
    - Margens e Bordas: Ele escaneia as extremidades direita, esquerda e superior em busca de serviços globais ou transversais que não possuem setas de fluxo direto.
    - Contexto Global: Esses itens são classificados imediatamente com a trust_zone como "Global", servindo de base para análises de conformidade e log.
    
    ***Passo 2: Mapeamento do Núcleo***
  
    O agente inicia o rastreamento lógico seguindo o caminho do dado.
    - Ponto de Gatilho: A análise começa obrigatoriamente no ícone do Usuário ou da Internet.
    - Explosão de Clusters: Ao identificar redundância (como três colunas de zonas de disponibilidade), o agente não cria uma entrada genérica; ele "explode" o cluster, gerando IDs únicos para cada recurso em cada zona (ex: alb_a, alb_b, alb_c).
    - Extração de Rótulos Internos: Ele busca por labels específicos, para garantir que o inventário reflita a tecnologia exata.
    
    ***Passo 3: Inspeção Recursiva e Decomposição***
  
    Esta é a camada de "zoom" do agente para evitar o agrupamento indevido de tecnologias.
    - Deep Box Inspection: Ao encontrar um container (como um "Resource Group" ou "Backend Box"), o agente ignora o título do box e foca nos ícones internos.
    - Diferenciação Tecnológica: Se houver dois ícones de web services com protocolos distintos (SOAP vs REST), ele é instruído a gerar duas entradas separadas no JSON para que o STRIDE possa avaliar os riscos específicos de cada protocolo.
    
    ***Exemplo do json gerado no output:***
    ```json
    {
      "components": [
        {
          "id": "ses_service",
          "name": "Amazon SES",
          "type": "Email Service",
          "category": "Messaging",
          "parent_id": null,
          "trust_zone": "AWS Global",
          "notes": "Sidebar item, no direct flow arrows"
        }
      ],
      "flows": [
        {
          "id": "flow_1",
          "source_id": "user",
          "target_id": "shield",
          "interaction_type": "HTTPS",
          "direction": "Uni-directional"
        }
      ]
    }
    ```
---
- ### Cloud Architecture Quality Auditor: ###

    Realiza uma reconciliação quantitativa entre os pixels da imagem e o JSON gerado. 
    Se houver discrepâncias (como componentes faltantes ou fluxos incompletos), ele delega a tarefa de volta ao Analista com instruções espaciais precisas.
    - [Prompt](prompts/auditor.md)
    - [Agent](agents/auditor_agent.py)

    O Auditor opera através de uma mentalidade de desconfiança técnica, seguindo um pipeline de verificação em três camadas:
  
    ***1. Reconciliação Quantitativa e de Margens***

    O primeiro passo é garantir que nenhum componente foi "esquecido" nas extremidades do diagrama.
    - Marginal Scan: Ele verifica se todos os serviços transversais nas bordas (como CloudTrail, KMS ou SES) foram capturados.
    O Auditor realiza uma contagem manual de cada ícone único na imagem e compara com o total de entradas no JSON. Se os números não baterem, o processo é interrompido imediatamente por ser considerado incompleto.
    
    ***2. Decomposição de Blocos***
  
    O Auditor combate o comportamento "lazy" de agrupamento, garantindo a granularidade necessária para a análise STRIDE.    
    - Regra de decomposição: Se o Auditor identifica um box genérico (como "Backend Systems") contendo ícones distintos (SaaS, REST, SOAP), ele exige que cada um seja um componente individual no JSON. Ele proíbe terminantemente o agrupamento de tecnologias heterogêneas.    
    - Regra intermediária: O Auditor verifica se existe uma camada de processamento (EC2, Lambda) entre a rede e os dados. Se o Analyst reportar um fluxo direto do Load Balancer para o Banco de Dados pulando a aplicação, o Auditor sinaliza uma falha crítica.
    
    ***3. Auditoria de Fluxo e Sequenciamento***
  
    O agente verifica o caminho dos dados, e rejeita caso não esteja de acordo com o diagrama.
    - Entry-Point: Ele exige que a análise comece no gatilho inicial e rastreie cada salto até o núcleo.    
    - Sequence Check: Ele valida se os fluxos seguem a ordem lógica da operação desenhada pelo arquiteto.

     ***Resumo das principais atividades:***
    | Passo | Foco Principal | Critério de Sucesso |
    |-------|---------------|---------------------|
    | Pass 1: Marginal | Margens e Contagem Total | 100% dos ícones periféricos identificados |
    | Pass 2: Estrutural | Simetria e Anomalias | Redundâncias de zonas e componentes únicos validados |
    | Pass 3: Integridade | Rótulos Literais e Hierarquia | Nomes no JSON idênticos aos rótulos da imagem e parent_id geograficamente corretos |

    ***Diretrizes de Delegação e Correção***
    Se o Auditor encontrar uma discrepância, ele não apenas "falha" a tarefa; ele fornece um guia de correção espacial para o Analyst:
    - Identificação Regional: Ele aponta onde o erro está (ex: "Margem Inferior Direita").
    - Âncora Visual: Ele dá uma referência (ex: "O ícone verde ao lado do RDS").
    - Comando de Reexecução: Ele ordena explicitamente que o Analyst re-escaneie aquela área e atualize o inventário.
      
---
- ### Senior Security Researcher (STRIDE Specialist): ###
    Especialista em modelagem de ameaças que consome o inventário validado para inferir riscos de segurança e sugerir mitigações 
    baseadas nas melhores práticas de nuvem (AWS, Azure ou GCP).
    - [Prompt](prompts/stride.md)
    - [Agent](agents/stride_agent.py)

  O agente opera como um arquiteto de segurança sênior, seguindo um processo de dedução lógica e priorização de riscos.

  ***1. Ingestão (Vínculo Estrito)***
    O primeiro passo é o mais crítico para a confiabilidade do sistema:
    - Fidelidade ao Inventário: O agente é terminantemente proibido de assumir a existência de componentes que não estejam no JSON validado pelo Auditor.
    - Neutralidade de Visão: Mesmo que o modelo de linguagem tenha "visto" um componente na imagem original, se ele não passou pelo crivo do Auditor, o Pesquisador o ignora para evitar alucinações no relatório final.

   ***2. Mapeamento de Ameaças (Framework STRIDE)***

    Para cada componente e cada fluxo de dados, o agente realiza uma varredura mental através dos seis pilares do STRIDE:
  
    - ***S (Spoofing):*** Falsificação de Identidade - Analisa pontos de entrada e identidades (IAM/Endpoint).
    - ***T (Tampering):*** Violação / Alteração de Dados (Alterar parâmetros de uma requisição) - Avalia a integridade dos dados em trânsito (protocolos como HTTP vs HTTPS) e em repouso.
    - ***R (Repudiation):*** Alguém nega ter feito uma ação e não há como provar o contrário. - Verifica se há serviços de log e rastreabilidade (como CloudTrail) para evitar a negação de ações.
    - ***I (Information Disclosure):*** Divulgação de Informação - Foca em exposição de sub-redes públicas e sensibilidade de dados.
    - ***D (Denial of Service):*** Ataque de sobrecarga - Examina limites de infraestrutura e proteções de borda (WAF/Shield).
    - ***E (Elevation of Privilege)***: Usuário ganha mais permissões do que deveria - Revisa permissões de acesso e políticas de menor privilégio.

    ***3. Inferência Contextual e Risco Transversal***
  
    Como diagramas raramente detalham todas as configurações, o agente utiliza padrões de design para inferir vulnerabilidades:
    - Padrões de Exposição: Se um componente está em uma Public Zone, o agente automaticamente eleva o risco para DoS e Spoofing.
    - Análise de Salto (Flow Analysis): O agente analisa a relação entre componentes.
 
    ***Estrutura e Entrega do Relatório***
    O agente finaliza seu trabalho consolidando as descobertas em um relatório estruturado em Português, garantindo que a comunicação técnica seja clara para os stakeholders locais.
    | Campo do Relatório        | Descrição Técnica |
    |--------------------------|------------------|
    | Categoria de Ameaça      | Identificação clara dentro do acrônimo STRIDE |
    | Descrição do Risco       | Explicação detalhada de como a ameaça se aplica àquele componente ou fluxo específico |
    | Impacto                  | Classificação entre Alto, Médio ou Baixo para auxiliar na priorização |
    | Mitigação Recomendada    | Guia passo a passo com as melhores práticas (ex: "Habilitar Criptografia KMS") |

---
### Como rodar o projeto.

1. Utilize o python na versão: 3.11.9
2. Sugestão: crie um ambiente virtual:
```sh
  python -m venv .venv  
  \.venv\Scripts\Activate.ps1 # Windows (PowerShell)
  .\.venv\Scripts\activate.bat # Windows (CMD)
  source .venv/bin/activate # Linux / macOS
```
3. Instale as depedências:
```sh
  pip install -r requirements.txt
```
4. Crie o arquivo .env na raiz do projeto e configure a variavel de ambiente: OPENAI_API_KEY com a sua chave da openai. 
5. Rodar o projeto:
```sh
  .venv/bin/python3.11 .venv/bin/streamlit run main.py  
```
