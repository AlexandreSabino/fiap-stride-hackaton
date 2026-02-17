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

- ***Software Architecture Vision Analyst:*** 
Responsável pela extração primária de dados. 
Utiliza técnicas de Recursive Scanning para decompor containers e identificar cada ícone e rótulo de texto individualmente.
    - [Prompt](prompts/vision.md) 
    - [Agent](agents/vision_agent.py)

- ***Cloud Architecture Quality Auditor:*** 
Realiza uma reconciliação quantitativa entre os pixels da imagem e o JSON gerado. 
Se houver discrepâncias (como componentes faltantes ou fluxos incompletos), ele delega a tarefa de volta ao Analista com instruções espaciais precisas.
    - [Prompt](prompts/auditor.md)
    - [Agent](agents/auditor_agent.py)

- ***Senior Security Researcher (STRIDE Specialist):*** 
Especialista em modelagem de ameaças que consome o inventário validado para inferir riscos de segurança e sugerir mitigações 
baseadas nas melhores práticas de nuvem (AWS, Azure ou GCP).
    - [Prompt](prompts/stride.md)
    - [Agent](agents/stride_agent.py)
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
