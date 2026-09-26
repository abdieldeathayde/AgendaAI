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

## ☁️ Deploy no PythonAnywhere

O projeto já foi preparado para funcionar no PythonAnywhere com `gunicorn` e `whitenoise`.

### 1. Configurar o projeto no PythonAnywhere

- Crie um novo app web e escolha `Manual configuration`.
- Defina o caminho do projeto para a pasta raiz do repositório.
- Configure o WSGI para apontar para `AgendaAI.wsgi.application`.
- Em `Settings`, configure:

```env
DEBUG=False
SECRET_KEY=sua-chave-secreta-forte
ALLOWED_HOSTS=seu_usuario.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://seu_usuario.pythonanywhere.com
CORS_ALLOWED_ORIGINS=https://seu_usuario.pythonanywhere.com
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
SECURE_SSL_REDIRECT=True
DATABASE_URL=mysql://usuario:senha@seu_host:3306/seu_banco
```

### 2. Criar o banco MySQL no PythonAnywhere

- Acesse o painel de banco de dados do PythonAnywhere.
- Crie um banco MySQL ou use o serviço oferecido pela plataforma.
- Ajuste a `DATABASE_URL` com os dados reais do banco.

### 3. Coletar arquivos estáticos

```bash
python manage.py collectstatic --noinput
```

### 4. Rodar as migrações

```bash
python manage.py migrate
```

### 5. Criar superusuário

```bash
python manage.py createsuperuser
```

### 6. Opcional: popular dados de demonstração

```bash
python manage.py seed_data
```

> Se o projeto estiver em domínio do PythonAnywhere, o host deve ser adicionado em `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` para que admin + formulários funcionem corretamente.

## ♻️ Recriar a base de demonstração

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
