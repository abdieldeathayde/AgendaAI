# Guia rápido de demonstração

## 1. Instalar

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## 2. Preparar banco

```bash
python manage.py migrate
python manage.py seed_data
```

## 3. Abrir

http://127.0.0.1:8000/

## Credenciais

**Administrador**
- usuário: `agenda.admin`
- senha: `Admin@12345`

**Usuários de demonstração**
- senha padrão: `Demo@12345`

## API

- Swagger: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI: `/api/schema/`

## Reset da demonstração

```bash
python manage.py seed_data --reset
```

Todos os dados criados pelo comando são fictícios.
