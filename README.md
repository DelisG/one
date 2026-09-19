# Cadastro de Alunos e Professores

Aplicação web em Django para cadastrar alunos e professores, com uma página de listagem e uma API REST de leitura feita com Django REST Framework.

> **EN:** Django web app to register students and teachers, with a listing page and a read-only REST API built with Django REST Framework.

<!-- Print da aplicação: salve a imagem em docs/print.png e remova este comentário -->
<!-- ![Tela inicial](docs/print.png) -->

## Funcionalidades

- Cadastro de alunos (nome, idade, e-mail) e professores (nome, CPF) pelo painel `/admin/`
- Página HTML que lista alunos e professores
- API REST de leitura: `GET /api/alunos` e `GET /api/professores`
- Validação de CPF no `ProfessorSerializer`: normaliza para 11 dígitos e recusa CPF duplicado
- Dockerfile para rodar a aplicação em contêiner

## Tecnologias

Python · Django 4.2 · Django REST Framework 3.15 · SQLite · Docker

## Rotas

| Rota | Método | Descrição |
| --- | --- | --- |
| `/` | GET | Página com as listas de alunos e professores |
| `/admin/` | GET | Painel administrativo do Django |
| `/api/alunos` | GET | Lista de alunos em JSON |
| `/api/professores` | GET | Lista de professores em JSON |

## Autora

**Delis Guerra**, Engenheira de Software Full Stack · Recife-PE
[LinkedIn](https://www.linkedin.com/in/delisguerra) · [GitHub](https://github.com/Delisg)
