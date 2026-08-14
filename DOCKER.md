# Rodando o projeto com Docker

Guia para subir o projeto dentro de um container, sem precisar instalar Python nem criar `venv` na sua máquina.

Este documento tem duas partes:

- **Parte 1 — Primeira vez:** o que fazer uma única vez, para deixar tudo configurado.
- **Parte 2 — Uso diário:** os comandos que você vai usar todo dia, depois de configurado.

Todos os comandos são executados no **PowerShell**, dentro da pasta do projeto.

---

## Conceitos básicos

Antes de começar, três palavras que aparecem o tempo todo:

| Termo | O que é |
| --- | --- |
| **Imagem** | O "molde" do projeto: Python, as dependências e o código, tudo empacotado. Criada com `docker build`. |
| **Container** | Uma instância da imagem em execução. É onde o Django realmente roda. Criado com `docker run`. |
| **Porta** | O endereço de acesso. Aqui a porta `8000` de dentro do container é publicada como `8001` na sua máquina. |

A imagem e o container deste projeto se chamam **`virada-dev`**.

---

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e **em execução** (o ícone da baleia precisa estar ativo na barra de tarefas).

Confirme que está tudo certo:

```powershell
docker --version
```

Se aparecer algo como `Docker version 27.x.x`, pode seguir.

---

## Parte 1 — Primeira vez

### 1. Entrar na pasta do projeto

```powershell
cd C:\Users\delis\Desktop\projects\one
```

### 2. Construir a imagem

Este comando lê o `dockerfile`, baixa o Python 3.10, instala tudo do `requirements.txt` e empacota o código.

```powershell
docker build -t virada-dev .
```

O `-t virada-dev` dá um nome à imagem. O `.` no final indica que o `dockerfile` está na pasta atual.

A primeira execução demora alguns minutos, porque o Docker precisa baixar a imagem base do Python. Nas próximas vezes é bem mais rápido, pois ele reaproveita o que já baixou.

Ao terminar, confirme que a imagem existe:

```powershell
docker images virada-dev
```

### 3. Criar e subir o container

```powershell
docker run -d --name virada-dev -p 8001:8000 virada-dev
```

Entendendo cada parte:

| Trecho | Significado |
| --- | --- |
| `-d` | Roda em segundo plano (*detached*), liberando o terminal. |
| `--name virada-dev` | Dá um nome ao container, para você não precisar decorar o ID. |
| `-p 8001:8000` | Publica a porta 8000 do container como 8001 na sua máquina. |
| `virada-dev` (no final) | O nome da imagem que será usada. |

Não é preciso rodar nenhum comando para "iniciar o Django": a última linha do `dockerfile` já executa o `runserver` automaticamente quando o container sobe.

### 4. Verificar se subiu

```powershell
docker ps
```

O container deve aparecer com status `Up`. Para ver a saída do Django:

```powershell
docker logs virada-dev
```

Você deve ver algo como:

```
Starting development server at http://0.0.0.0:8000/
```

### 5. Preparar o banco de dados

O `db.sqlite3` está no `.gitignore`, então quem clona o repositório começa sem banco. Rode as migrations **dentro** do container:

```powershell
docker exec -it virada-dev python manage.py migrate
```

E crie o usuário administrador:

```powershell
docker exec -it virada-dev python manage.py createsuperuser
```

O `docker exec` executa um comando dentro de um container que já está rodando. O `-it` deixa a sessão interativa, necessário para digitar usuário e senha.

Se o seu `db.sqlite3` já existia na pasta quando você construiu a imagem, ele foi copiado junto e esses dois passos podem não ser necessários. O `migrate` é seguro de rodar mesmo assim: se já estiver tudo aplicado, ele não faz nada.

### 6. Acessar

Abra no navegador:

| Endereço | Página |
| --- | --- |
| http://localhost:8001 | Listagem de alunos e professores |
| http://localhost:8001/admin/ | Painel administrativo |
| http://localhost:8001/api/alunos | API de alunos (JSON) |
| http://localhost:8001/api/professores | API de professores (JSON) |

Pronto. A configuração inicial acabou. Você **não vai repetir esta parte** no dia a dia.

---

## Parte 2 — Uso diário

Com o container já criado, o fluxo é bem curto.

### Iniciar

```powershell
docker start virada-dev
```

Acesse http://localhost:8001

### Parar

```powershell
docker stop virada-dev
```

### Ver os logs

```powershell
docker logs -f virada-dev
```

O `-f` acompanha os logs em tempo real. Pressione `Ctrl+C` para sair da visualização — isso **não** para o container.

### Conferir se está rodando

```powershell
docker ps
```

Se o container não aparecer na lista, ele está parado. Use `docker ps -a` para ver também os parados.

---

## Entrando no container

Às vezes você precisa olhar os arquivos ou rodar um comando do Django lá dentro. Para abrir um terminal no container:

```powershell
docker exec -it virada-dev bash
```

O prompt muda, e essa mudança é a parte mais importante de entender:

```
PS C:\Users\delis\Desktop\projects\one>     <- Windows (PowerShell)
root@de0edd15e88e:/app#                      <- dentro do container (Linux)
```

Enquanto o prompt estiver como `root@...:/app#`, você **não está mais no Windows**. Está em um Linux isolado, que só enxerga o que foi copiado para dentro da imagem.

| Prompt | Onde você está | O que funciona ali |
| --- | --- | --- |
| `PS C:\...>` | Windows | `docker build`, `docker run`, `docker start`, `docker stop`, `docker logs` |
| `root@...:/app#` | Container | `ls`, `cat`, `pip list`, `python manage.py <comando>` |

Para sair e voltar ao Windows:

```
exit
```

Sair do terminal **não** para o container. Ele continua rodando normalmente.

### Dois erros comuns lá dentro

**`bash: docker: command not found`**

Esperado. O Docker não está instalado dentro do container. Comandos `docker` só existem no PowerShell. Se você precisa de um, saia com `exit` primeiro.

**Tentar subir o servidor de novo**

Não é necessário: o Django já está rodando. Ele é o processo principal do container, como mostra a coluna `COMMAND` do `docker ps`:

```
CONTAINER ID   IMAGE        COMMAND                  STATUS
de0edd15e88e   virada-dev   "python manage.py ru…"   Up 53 seconds
```

Rodar `python manage.py runserver` de novo apenas daria erro de porta em uso.

### Atalho

Para um comando pontual, não compensa entrar e sair. Passe o comando direto:

```powershell
docker exec -it virada-dev python manage.py migrate
```

É o mesmo resultado de entrar com `bash`, rodar `python manage.py migrate` e dar `exit`.

---

## Quando alterar o código

O código é copiado para dentro da imagem no momento do `build`. Portanto, editar um arquivo na sua máquina **não** altera o que está rodando no container.

Depois de mexer no código (ou no `requirements.txt`), refaça o ciclo:

```powershell
docker rm -f virada-dev
docker build -t virada-dev .
docker run -d --name virada-dev -p 8001:8000 virada-dev
```

O `docker rm -f` remove o container antigo. Sem isso, o `docker run` falha com erro de nome duplicado.

Atenção: como o banco fica dentro do container, `docker rm` **apaga os dados cadastrados**. Após recriar, rode o `migrate` e o `createsuperuser` da Parte 1 novamente.

### Alternativa: refletir alterações sem rebuildar

Para desenvolvimento, você pode espelhar a pasta do projeto dentro do container. Assim, o Django recarrega sozinho a cada arquivo salvo, e o banco fica na sua máquina (não some ao remover o container):

```powershell
docker rm -f virada-dev
docker run -d --name virada-dev -p 8001:8000 -v ${PWD}:/app virada-dev
```

O `-v ${PWD}:/app` monta a pasta atual sobre o `/app` do container. Com isso, você só precisa rebuildar quando mudar o `requirements.txt` ou o `dockerfile`.

---

## Resumo dos comandos

| Situação | Comando |
| --- | --- |
| Construir a imagem | `docker build -t virada-dev .` |
| Criar e subir o container | `docker run -d --name virada-dev -p 8001:8000 virada-dev` |
| Iniciar (já criado) | `docker start virada-dev` |
| Parar | `docker stop virada-dev` |
| Ver logs ao vivo | `docker logs -f virada-dev` |
| Listar containers ativos | `docker ps` |
| Listar todos os containers | `docker ps -a` |
| Rodar comando do Django | `docker exec -it virada-dev python manage.py <comando>` |
| Abrir um terminal no container | `docker exec -it virada-dev bash` |
| Remover o container | `docker rm -f virada-dev` |

---

## Problemas comuns

**`docker: error during connect` ou `cannot connect to the Docker daemon`**

O Docker Desktop não está aberto. Inicie-o e espere o ícone da baleia ficar estável.

**`The container name "/virada-dev" is already in use`**

Já existe um container com esse nome. Use `docker start virada-dev` para reaproveitá-lo, ou `docker rm -f virada-dev` para removê-lo antes de criar outro.

**`port is already allocated`**

A porta 8001 está ocupada por outro programa. Troque o número da esquerda, por exemplo `-p 8002:8000`, e acesse pela porta nova.

**`error: [Errno 2] No such file or directory: 'gcc'` durante o build**

Alguma dependência do `requirements.txt` não tem versão pré-compilada para o Python da imagem e está tentando compilar do zero, mas a imagem `slim` não traz compilador.

Foi o que aconteceu com o `backports.zoneinfo`, que só existe para Python inferior a 3.9. Como a imagem usa Python 3.10, a linha no `requirements.txt` recebeu uma condição para ser ignorada:

```
backports.zoneinfo==0.2.1; python_version < "3.9"
```

Se aparecer com outro pacote, a saída de erro indica qual é logo acima do `error:`.

**A página não abre em http://localhost:8001**

Confira se o container está `Up` com `docker ps` e veja o `docker logs virada-dev`. Lembre-se de usar a porta **8001**, não a 8000.

---

## Observações

- O `.dockerignore` impede que a pasta `venv/` e o `.git/` entrem na imagem. O `venv` local é do Linux/WSL e não funcionaria dentro do container.
- A imagem usa Python 3.10, enquanto o `venv` local usa Python 3.8. Por isso o `requirements.txt` precisa de dependências compatíveis com as duas versões.
- Este guia cobre apenas o ambiente de desenvolvimento. O `runserver` do Django não deve ser usado em produção.
