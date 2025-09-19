# Guia de Uso - Sistema de Orçamentos de Serviços

## 1. Clonar o Repositório

```bash
git clone https://github.com/mezzomolucas/orcamento-servicos.git
```

## 2. Entrar na Pasta do Projeto

```bash
cd orcamento-servicos
```

## 3. Configurar Ambiente Virtual

Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

## 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 5. Rodar a Aplicação

Inicie o servidor:

```bash
python src/main.py
```

O servidor estará em `http://localhost:5000/`.

## 6. Testar com Postman.

### Autenticação

#### Registrar Usuário
- **Método:** `POST`
- **URL:** `http://localhost:5000/api/auth/register`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
```json
{
  "nome": "Seu Nome",
  "email": "seu.email@example.com",
  "senha": "sua_senha"
}
```

#### Fazer Login
- **Método:** `POST`
- **URL:** `http://localhost:5000/api/auth/login`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
```json
{
  "email": "seu.email@example.com",
  "senha": "sua_senha"
}
```

### Clientes

#### Cadastrar Cliente
- **Método:** `POST`
- **URL:** `http://localhost:5000/api/clientes/`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
```json
{
  "nome": "Nome do Cliente",
  "telefone": "11987654321",
  "email": "cliente@example.com",
  "endereco": "Rua Exemplo, 123"
}
```

#### Listar Clientes
- **Método:** `GET`
- **URL:** `http://localhost:5000/api/clientes/`

#### Buscar Cliente por ID
- **Método:** `GET`
- **URL:** `http://localhost:5000/api/clientes/1` (substitua `1` pelo ID)

### Serviços

#### Cadastrar Serviço
- **Método:** `POST`
- **URL:** `http://localhost:5000/api/servicos/`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
```json
{
  "nome": "Desenvolvimento Web",
  "descricao": "Criação de websites e sistemas web.",
  "preco": 1500.00
}
```

#### Listar Serviços
- **Método:** `GET`
- **URL:** `http://localhost:5000/api/servicos/`

### Orçamentos

#### Criar Orçamento
- **Método:** `POST`
- **URL:** `http://localhost:5000/api/orcamentos/`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
```json
{
  "cliente_id": 1, 
  "servicos_ids": [1, 2], 
  "data_validade": "2025-12-31",
  "observacoes": "Orçamento inicial."
}
```
*Certifique-se de que `cliente_id` e `servicos_ids` existam.*

## Observações

- O banco de dados (`app.db`) é criado na primeira execução de `main_simples.py`.
- O `index.html` é um placeholder e não faz parte da API backend.

OrcamentoServicos2025!
