# Trabalho 1 - Python NoteBot

Python NoteBot é uma aplicação web desenvolvida como parte do projeto da disciplina de Redes de Computadores da Universidade de Brasília (UnB). A plataforma permite que usuários criem notas sobre a linguagem de programação Python e recebam um complemento gerado por inteligência artificial, que aprofunda e exemplifica o conteúdo da anotação.

-----

## Autores

Este projeto foi desenvolvido por:

- **Angel Flavius Alves Negri** - Matrícula: 24/1038110
- **Matheus De Melo Fellet** - Matrícula: 22/2015201
- **Matheus Duarte Da Silva** - Matrícula: 21/1062277

---

## Visão Geral do Projeto

O objetivo principal do projeto é aplicar em um cenário prático os conceitos de desenvolvimento de aplicações cliente-servidor e a análise de protocolos de rede. 
A aplicação foi concebida como um chatbot educacional que utiliza a API da Perplexity, integrada a um backend construído com o microframework Flask, para fornecer respostas em linguagem natural.

Toda a comunicação entre o cliente (navegador web) e o servidor (aplicação Flask) foi monitorada e analisada com a ferramenta Wireshark para verificar o correto funcionamento dos protocolos das camadas de aplicação, transporte e rede.

### Principais Funcionalidades

  * **Autenticação de Usuários:** Sistema de cadastro e login.
  * **Criação de Notas:** Os usuários podem criar anotações sobre dúvidas ou conceitos da linguagem Python.
  * **Enriquecimento com IA:** Cada nota submetida é processada por um assistente de IA que fornece uma explicação detalhada, com exemplos de código e formatação em Markdown.
  * **Gerenciamento de Notas:** Os usuários podem visualizar, editar e apagar suas notas.

---

## Arquitetura e Tecnologias Utilizadas

A aplicação segue uma arquitetura cliente-servidor e foi desenvolvida com as seguintes tecnologias:

  * **Backend:** Python 3.12 ou superior
  * **Framework Web:** Flask
  * **Banco de Dados:** SQLite com ORM SQLAlchemy
  * **Inteligência Artificial:** API da Perplexity (acessada via cliente OpenAI)
  * **Frontend:** HTML, CSS e Jinja2

---

## Como Executar o Projeto

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

**1. Clone o Repositório**

```bash
git clone git@github.com:smmstakes/redes-trabalho-1.git
cd redes-trabalho-1
```

**2. Crie um Ambiente Virtual**
Se estiver usando um sistema Unix (Linux ou macOS), você pode criar e ativar um ambiente virtual com os seguintes comandos:

```bash
python -m venv venv
source venv/bin/activate
```

Se você estiver usando o Windows, o comando para ativar o ambiente virtual é:

```bash
venv\Scripts\activate
```

**3. Instale as Dependências**

```bash
pip install -r requirements.txt
```

**4. Configure as Variáveis de Ambiente**

Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes chaves. A `APP_SECRET_KEY` pode ser qualquer string segura e a `OPEN_AI_KEY` deve ser sua chave da API da Perplexity.

```
APP_SECRET_KEY='sua-chave-secreta-aqui'
OPEN_AI_KEY='sua-chave-da-api-perplexity'
```

**5. Execute a Aplicação**

O comando abaixo irá criar o banco de dados `python-notebot.sqlite3` (caso não exista) e iniciar o servidor de desenvolvimento.

```bash
python app.py
```

A aplicação estará disponível em `http://127.0.0.1:5000`.

-----
