# Cadastro de Alunos e Professores

Projeto Django com cadastro de alunos e professores, página HTML de listagem e uma API REST de leitura construída com Django REST Framework.

## Stack

| Ferramenta | Versão |
| --- | --- |
| Python | 3.8+ |
| Django | 4.2.30 |
| Django REST Framework | 3.15.2 |
| Banco de dados | SQLite |

## Pré-requisitos

- [Python 3.8 ou superior](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

Confira as versões instaladas:

```bash
python3 --version
git --version
```

## Como rodar

### 1. Clonar o repositório

```bash
git clone https://github.com/DelisG/one.git
cd one
```

### 2. Criar e ativar o ambiente virtual

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

Com o ambiente ativo, o prompt passa a exibir `(venv)`.

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o banco de dados

O `db.sqlite3` não vai para o repositório, então o banco começa vazio a cada clone. As migrations criam as tabelas:

```bash
python manage.py migrate
```

### 5. Criar um usuário administrador

Necessário para acessar o `/admin/` e cadastrar alunos e professores:

```bash
python manage.py createsuperuser
```

Informe usuário, e-mail e senha quando solicitado.

### 6. Subir o servidor

```bash
python manage.py runserver
```

Acesse http://127.0.0.1:8000/

Para encerrar, pressione `Ctrl+C`.

## Rotas

| Rota | Método | Descrição |
| --- | --- | --- |
| `/` | GET | Página HTML com as listas de alunos e professores |
| `/admin/` | GET | Painel administrativo do Django |
| `/api/alunos` | GET | Lista de alunos em JSON |
| `/api/professores` | GET | Lista de professores em JSON |

A API é somente leitura. Os cadastros são feitos pelo `/admin/`.

Exemplo de resposta de `/api/alunos`:

```json
[
  { "id": 1, "nome": "Delis", "idade": 26, "email": "delis@mail.com" }
]
```

## Models

**Aluno** — `nome`, `idade`, `email`

**Professor** — `nome`, `cpf`

O `ProfessorSerializer` normaliza o CPF para 11 dígitos (aceita `123.456.789-00` e grava `12345678900`) e recusa CPF duplicado. Como as rotas atuais são só de leitura, essa validação só é acionada ao usar o serializer diretamente, por exemplo no shell:

```bash
python manage.py shell
```

```python
from app.serializers import ProfessorSerializer

s = ProfessorSerializer(data={'nome': 'Carlos', 'cpf': '123.456.789-00'})
s.is_valid()   # True
s.save()
```

## Estrutura

```
one/
├── app/                    # aplicação principal
│   ├── migrations/         # migrations do banco
│   ├── admin.py            # registro dos models no /admin/
│   ├── models.py           # Aluno e Professor
│   ├── serializers.py      # serializers do DRF
│   ├── urls.py             # rotas da aplicação
│   └── views.py            # views HTML e da API
├── segunda/                # configuração do projeto
│   ├── settings.py
│   ├── urls.py             # rotas raiz
│   └── wsgi.py
├── templates/
│   ├── default.html        # layout base
│   └── home.html           # listagem de alunos e professores
├── manage.py
└── requirements.txt
```

## Comandos úteis

```bash
# Verificar problemas no projeto
python manage.py check

# Ver o status das migrations
python manage.py showmigrations

# Gerar migrations após alterar os models
python manage.py makemigrations

# Abrir o shell do Django
python manage.py shell
```

## Observações

Este projeto está configurado para desenvolvimento. Antes de publicar em produção, ajuste em `segunda/settings.py`:

- `DEBUG = False`
- preencha `ALLOWED_HOSTS`
- mova a `SECRET_KEY` para uma variável de ambiente
