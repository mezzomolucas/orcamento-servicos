🚀 Como Rodar e Testar no Postman
1. Executar o Sistema

No terminal:

cd orcamentos_servicos
source venv/bin/activate
python src/main.py


O servidor vai rodar em:
👉 http://localhost:5000

2. Testando com Postman
Usuários

Cadastrar Usuário
POST http://localhost:5000/api/auth/register

{
  "nome": "Seu Nome",
  "email": "seu@email.com",
  "senha": "123456"
}


Login
POST http://localhost:5000/api/auth/login

{
  "email": "seu@email.com",
  "senha": "123456"
}


🔑 O login gera a sessão (cookies).

Clientes

Cadastrar Cliente
POST http://localhost:5000/api/clientes/

{
  "nome": "João Silva",
  "telefone": "11999999999",
  "email": "joao@email.com",
  "endereco": "Rua A, 123"
}


Listar Clientes
GET http://localhost:5000/api/clientes/

Serviços

Cadastrar Serviço
POST http://localhost:5000/api/servicos/

{
  "descricao": "Dedetização",
  "valor": 500
}


Listar Serviços
GET http://localhost:5000/api/servicos/
