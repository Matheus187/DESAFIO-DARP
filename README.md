# Projeto: API Marketplace Agro (DESAFIO-DARP)

API RESTful para um marketplace agro, desenvolvida em Python com FastAPI. O projeto permite a gestão de produtores, compradores e administradores, incluindo criação de produtos, gestão de stock e processamento de pedidos.

---

## 1. Informações Técnicas

* **Versão do Python:** `Python 3.11`
* **SGBD (Banco de Dados):** `PostgreSQL` (versão 16, a correr em Docker)
* **Principais Bibliotecas:**
    * `FastAPI`: O framework principal da API.
    * `SQLAlchemy`: O ORM para a comunicação com o banco de dados.
    * `Alembic`: Para gerir as migrações (as "versões" da estrutura) do banco.
    * `Pydantic`: Para validação de dados (Schemas).
    * `python-jose[cryptography]`: Para geração e validação de tokens de Acesso (JWT).
    * `argon2-cffi`: Para o hashing (criptografia) de senhas.
    * `uvicorn`: O servidor ASGI para executar a API.
    * `psycopg2-binary`: O "driver" que permite ao Python comunicar com o PostgreSQL.

---

## 2. Instruções de Instalação e Execução (com Docker)

Este projeto é 100% "dockerizado". A sua execução é gerida pelo Docker Compose, que orquestra a API e o Banco de Dados.

**Pré-requisitos:**
* Docker
* Docker Compose (normalmente já vem com o Docker Desktop)

### Passo 1: Iniciar os Serviços

Na raiz do projeto (onde está o `docker-compose.yml`), execute o seguinte comando no terminal. Ele irá construir a imagem da API e iniciar os contentores da API (`web`) e do Banco de Dados (`db`).

```bash
docker compose up --build