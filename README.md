# AgendaAI — Sistema de Agendamento

Sistema web completo de gestão de agendamentos desenvolvido com **Python + Django + Django REST Framework + MySQL/SQLite + JWT + Docker**.

O projeto foi preparado para demonstração, testes locais e deploy. A versão inclui uma rotina de **dados fictícios realistas**, dashboard, gestão de clientes, profissionais, serviços, disponibilidade, agendamentos, relatórios, financeiro e API REST com Swagger/OpenAPI.

## ✨ Principais recursos

- Dashboard administrativo com indicadores.
- Cadastro, edição e exclusão de clientes.
- Cadastro de profissionais e especialidades.
- Cadastro de serviços com duração e preço.
- Agenda semanal de disponibilidade por profissional.
- Criação, edição, exclusão e filtro de agendamentos.
- Status: Agendado, Confirmado, Concluído e Cancelado.
- Validação de duração do serviço.
- Validação de disponibilidade do profissional.
- Bloqueio de conflitos de horário.
- Snapshot do preço no momento do agendamento.
- Relatórios operacionais.
- Financeiro com faturamento histórico e previsto.
- Exportação de agendamentos em CSV.
- API REST protegida por JWT.
- Swagger UI / ReDoc.
- Custom User do Django.
- Django Admin.
- Docker + MySQL.
- SQLite automático para desenvolvimento local sem configuração de banco.
- WhiteNoise para arquivos estáticos em produção.
- Configuração por variáveis de ambiente.
- Comando de seed com base de demonstração completa.

## 🧰 Stack

| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| Django | Backend e aplicação web |
| Django REST Framework | API REST |
| SimpleJWT | Autenticação JWT |
| drf-spectacular | OpenAPI / Swagger / ReDoc |
| MySQL 8.4 | Banco recomendado em produção/Docker |
| SQLite | Banco simples para desenvolvimento |
| Docker | Containerização |
| Gunicorn | Servidor WSGI |
| WhiteNoise | Arquivos estáticos |
| HTML/CSS/JavaScript | Interface web |

## 📁 Estrutura

```text
AgendaAI/
├── AgendaAI/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py
│   ├── migrations/
│   ├── services/
│   │   └── slots.py
│   ├── api_views.py
│   ├── crud_views.py
│   ├── models.py
│   ├── serializers.py
│   ├── forms.py
│   ├── admin.py
│   └── tests.py
├── users/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── templates/
├── mysql-init/
├── docker-compose.yml
├── dockerfile
├── entrypoint.sh
├── requirements.txt
└── manage.py
```

## 🚀 Execução local — Windows

### 1. Criar ambiente virtual

```powershell
python -m venv .venv
```

### 2. Ativar

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Criar `.env`

Copie:

```text
.env.example
```

para:

```text
.env
```

Para execução local com SQLite, uma configuração mínima é:

```env
SECRET_KEY=agendaai-chave-local
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

Não é necessário configurar MySQL para o modo local com SQLite.

### 5. Migrar

```powershell
python manage.py migrate
```

### 6. Criar dados fictícios completos

```powershell
python manage.py seed_data
```

A base de demonstração cria:

- 1 administrador;
- 5 profissionais;
- 15 serviços;
- 12 clientes;
- disponibilidades de segunda a sábado;
- histórico de atendimentos;
- agendamentos de hoje;
- agenda futura;
- diferentes status;
- faturamento para o dashboard;
- dados suficientes para testar filtros, relatórios e financeiro.

### 7. Iniciar

```powershell
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## 🔐 Usuários de demonstração

### Administrador

```text
Usuário: agenda.admin
Senha: Admin@12345
```

### Profissionais/clientes

Por padrão:

```text
Senha: Demo@12345
```

Exemplos:

```text
lucas.barber
amanda.silva
rodrigo.visagista
juliana.estetica
marcos.terapeuta

carlos.silva
beatriz.souza
fernando.lima
mariana.alves
```

**Importante:** são credenciais fictícias destinadas somente à demonstração. Troque as senhas em qualquer ambiente público.

## ☁️ Deploy na Oracle OCI (Always Free)

O projeto já está preparado para rodar em uma VM Ubuntu gratuita da OCI com `gunicorn`, `nginx` e `whitenoise`.

### 1. Preparar a VM Ubuntu na OCI

- Crie uma instância Ubuntu na OCI Always Free.
- Abra as portas `80`, `443` e `22` no Security List / NSG.
- Conecte-se via SSH e instale dependências:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx git mysql-client
```

### 2. Clonar o projeto

```bash
cd ~/ && git clone https://github.com/seu-usuario/AgendaAI.git
cd AgendaAI
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` com algo parecido com:

```env
SECRET_KEY=sua-chave-secreta-forte
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,meu-dominio.com,123.45.67.89
CSRF_TRUSTED_ORIGINS=https://meu-dominio.com,https://www.meu-dominio.com,https://123.45.67.89
CORS_ALLOWED_ORIGINS=https://meu-dominio.com,https://www.meu-dominio.com,https://123.45.67.89
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
SECURE_SSL_REDIRECT=True
DATABASE_URL=mysql://usuario:senha@host:3306/banco
DEFAULT_FROM_EMAIL=no-reply@meu-dominio.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

> Se você utilizar um banco MySQL Gratuito da OCI ou um serviço externo, ajuste a `DATABASE_URL` com os dados reais.

### 4. Rodar migrações e coletar arquivos estáticos

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 5. Criar administrador

```bash
python manage.py createsuperuser
```

### 6. Popular dados de demonstração (opcional)

```bash
python manage.py seed_data
```

### 7. Iniciar o Gunicorn

O projeto já usa Gunicorn via `requirements.txt` e suporta o comando:

```bash
gunicorn AgendaAI.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Para manter em execução em background, use `systemd` ou `nohup`.

### 8. Configurar Nginx como proxy reverso

Crie um arquivo no Nginx:

```nginx
server {
    listen 80;
    server_name meu-dominio.com 123.45.67.89;

    location /static/ {
        alias /home/ubuntu/AgendaAI/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/AgendaAI/media/;
    }

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Ative o site:

```bash
sudo ln -s /etc/nginx/sites-available/agendaai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. SSL com Let's Encrypt (recomendado)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d meu-dominio.com
```

> Em ambientes com TLS concluído no Nginx, o Django precisa receber o header `X-Forwarded-Proto=https`, por isso a variável `SECURE_PROXY_SSL_HEADER` foi adicionada no projeto.

### 10. Dicas para OCI grátis

- Use uma VM Ubuntu pequena e deixe o `gunicorn` rodando em background.
- No OCI, o domínio público geralmente é configurado por DNS externo, então o `ALLOWED_HOSTS` deve incluir o domínio e o IP público.
- Para evitar problemas com CSRF e cookies em HTTPS, inclua o domínio real em `CSRF_TRUSTED_ORIGINS`.

## ☁️ Deploy na Hostinger

A Hostinger aceita a publicação de apps Python com Gunicorn, normalmente usando uma variável de ambiente `PORT` e um comando de inicialização. Para o projeto AgendaAI, o preparo mínimo é:

### 1. Variáveis de ambiente na Hostinger

No painel da Hostinger, configure estas variáveis no app Python:

```env
SECRET_KEY=sua-chave-secreta-forte
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.hostingerapp.com,meu-dominio.com,www.meu-dominio.com
CSRF_TRUSTED_ORIGINS=https://meu-dominio.com,https://www.meu-dominio.com,https://*.hostingerapp.com
CORS_ALLOWED_ORIGINS=https://meu-dominio.com,https://www.meu-dominio.com,https://*.hostingerapp.com
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
SECURE_SSL_REDIRECT=True
DATABASE_URL=mysql://usuario:senha@host:3306/banco
```

> Se a aplicação estiver em um domínio personalizado, inclua o domínio real em `ALLOWED_HOSTS` e em `CSRF_TRUSTED_ORIGINS`.

### 2. Comando de inicialização

Use esse comando de startup no painel da Hostinger ou em um arquivo de execução:

```bash
bash startup.sh
```

O script executa automaticamente:

- `python manage.py migrate --noinput`
- `python manage.py collectstatic --noinput`
- `gunicorn app:app --bind 0.0.0.0:${PORT:-80} --workers 2 --timeout 120`

### 3. Dicas para domínio e HTTPS

- Se o app estiver usando o subdomínio da Hostinger, inclua `.hostingerapp.com` em `ALLOWED_HOSTS`.
- Se estiver em domínio próprio, adicione `meu-dominio.com` e `www.meu-dominio.com`.
- O `SECURE_PROXY_SSL_HEADER` é importante porque a Hostinger termina o TLS antes de enviar a requisição para o app.
- Se o painel exigir um comando direto em vez de `bash startup.sh`, use:

```bash
gunicorn app:app --bind 0.0.0.0:${PORT:-80} --workers 2 --timeout 120
```

## ☁️ Deploy no Render

O projeto já está preparado para funcionar no Render com um serviço web em Python e banco externo.

### 1. Variáveis de ambiente no Render

Configure no painel do Render:

```env
SECRET_KEY=sua-chave-secreta-forte
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
CORS_ALLOWED_ORIGINS=https://*.onrender.com
DATABASE_URL=postgres://usuario:senha@host:5432/banco
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
```

### 2. Build e start do serviço

No Render, use:

- Build Command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

- Start Command:

```bash
gunicorn AgendaAI.wsgi:application --bind 0.0.0.0:$PORT --workers 2
```

### 3. Banco de dados

Use um banco externo do Render ou de outro provedor e informe a URL em `DATABASE_URL`.

### 4. Migrações

Antes de testar a aplicação, rode no shell do Render ou em um job de deploy:

```bash
python manage.py migrate
```

### 5. Dados de demonstração

Opcionalmente, você pode popular o banco com os dados de exemplo:

```bash
python manage.py seed_data
```

> O domínio do Render geralmente é do tipo `https://nome-do-servico.onrender.com`; por isso o host `*.onrender.com` deve estar em `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.

## ♻️ Recriar a base de demonstração

Para apagar os registros de demonstração e gerar tudo novamente:

```powershell
python manage.py seed_data --reset
```

Para usar outra senha nos usuários comuns:

Para apagar os registros de demonstração e gerar tudo novamente:

```powershell
python manage.py seed_data --reset
```

Para usar outra senha nos usuários comuns:

```powershell
python manage.py seed_data --password "Demo@45678"
```

Para alterar a senha do administrador:

```powershell
python manage.py seed_data --admin-password "Admin@45678"
```

## 🐳 Docker + MySQL

Crie `.env`:

```env
SECRET_KEY=agendaai-docker-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

DB_NAME=agendaai
DB_USER=agendaai
DB_PASSWORD=agendaai_password
DB_HOST=db
DB_PORT=3306
MYSQL_ROOT_PASSWORD=change-root-password
```

Suba os containers:

```powershell
docker compose up --build
```

O sistema ficará disponível em:

```text
http://localhost:8000
```

O MySQL ficará exposto localmente na porta:

```text
3308
```

O Django dentro do container usa:

```text
db:3306
```

### Popular o Docker com dados fictícios

Depois que os containers estiverem funcionando:

```powershell
docker compose exec web python manage.py seed_data
```

Para recriar:

```powershell
docker compose exec web python manage.py seed_data --reset
```

## 🧪 Testes

Local:

```powershell
python manage.py test
```

Docker:

```powershell
docker compose exec web python manage.py test
```

## 📚 API

A documentação está disponível em:

```text
http://127.0.0.1:8000/api/docs/
```

ReDoc:

```text
http://127.0.0.1:8000/api/redoc/
```

Schema OpenAPI:

```text
http://127.0.0.1:8000/api/schema/
```

### JWT

Obter token:

```http
POST /api/token/
```

Exemplo:

```json
{
  "username": "agenda.admin",
  "password": "Admin@12345"
}
```

Renovar:

```http
POST /api/refresh/
```

Verificar:

```http
POST /api/token/verify/
```

Enviar o access token:

```http
Authorization: Bearer SEU_TOKEN
```

## 📊 Funcionalidades para testar

### Dashboard

Teste:

- total de clientes;
- total de profissionais;
- serviços;
- agendamentos;
- faturamento;
- atendimentos de hoje;
- próximos atendimentos;
- serviços mais utilizados;
- profissionais em destaque;
- tendência diária;
- filtros de período.

### Clientes

Teste:

- criação;
- edição;
- exclusão;
- relacionamento com usuário.

### Profissionais

Teste:

- especialidade;
- biografia;
- status ativo;
- serviços;
- horários de atendimento.

### Serviços

Teste:

- duração;
- preço;
- profissional;
- ativação/desativação.

### Horários

Teste:

- disponibilidade semanal;
- filtro por profissional;
- exclusão de disponibilidade.

### Agendamentos

Teste:

- criação;
- alteração;
- exclusão;
- filtros por status;
- filtros por profissional;
- alteração rápida de status;
- exportação CSV;
- validação de duração;
- validação de disponibilidade;
- prevenção de conflito.

### Financeiro

Teste:

- faturamento mensal;
- faturamento previsto;
- atendimentos concluídos.

## 🔒 Regras de negócio

O modelo `Appointment` protege algumas regras importantes:

1. O serviço precisa existir.
2. O horário final precisa ser posterior ao inicial.
3. A duração precisa corresponder ao serviço.
4. Serviços inativos não podem ser agendados.
5. Profissionais inativos não podem receber novos agendamentos.
6. O horário precisa respeitar a disponibilidade cadastrada quando houver disponibilidade configurada.
7. Agendamentos ativos não podem ocupar o mesmo período do profissional.
8. Cancelamentos não bloqueiam outro horário.
9. O preço é copiado para o agendamento no momento da criação, preservando o histórico mesmo se o preço do serviço mudar depois.

## ☁️ Deploy no Render

### Banco

Recomenda-se utilizar um banco PostgreSQL gerenciado no ambiente de produção caso o plano/infraestrutura do Render utilizado seja PostgreSQL.

O projeto aceita `DATABASE_URL` diretamente:

```env
DATABASE_URL=postgresql://...
```

Quando `DATABASE_URL` estiver definida, ela tem prioridade sobre SQLite.

### Build Command

```text
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Start Command

Se o Render executar diretamente o Python:

```text
gunicorn AgendaAI.wsgi:application --bind 0.0.0.0:$PORT
```

Variáveis importantes:

```env
SECRET_KEY=<uma-chave-forte>
DEBUG=False
ALLOWED_HOSTS=<seu-dominio-do-render>
CSRF_TRUSTED_ORIGINS=https://<seu-dominio-do-render>
DATABASE_URL=<url-do-banco>
SECURE_SSL_REDIRECT=True
```

O `entrypoint.sh` também está preparado para execução em Docker.

## 🛠️ Comandos úteis

```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py test
python manage.py collectstatic --noinput
```

## 🧑‍💻 Django Admin

Acesse:

```text
http://127.0.0.1:8000/admin/
```

Use:

```text
agenda.admin
Admin@12345
```

## ⚠️ Produção

Antes de colocar o sistema na internet:

- altere as senhas de demonstração;
- gere uma `SECRET_KEY` nova;
- defina `DEBUG=False`;
- configure `ALLOWED_HOSTS`;
- configure `CSRF_TRUSTED_ORIGINS`;
- configure banco de produção;
- não publique `.env`;
- configure SMTP real se for enviar e-mails;
- revise CORS;
- configure backup do banco;
- configure HTTPS;
- remova dados fictícios se não forem necessários.

## 📌 Próximas evoluções recomendadas

- Frontend React separado.
- Perfis e permissões granulares.
- Multiempresa/tenant.
- Bloqueio de férias e feriados.
- Reagendamento com histórico.
- Notificações por e-mail/WhatsApp.
- Pagamentos online.
- Integração com Google Calendar.
- Auditoria de alterações.
- Testes de integração da API.
- CI/CD com GitHub Actions.
- Observabilidade e logs estruturados.
- Rate limiting da API.
- OpenAPI com exemplos completos.
- PostgreSQL como banco principal de produção.

## 👨‍💻 Autor

**Abdiel de Athayde**

GitHub: https://github.com/abdieldeathayde

Projeto: https://github.com/abdieldeathayde/AgendaAI
