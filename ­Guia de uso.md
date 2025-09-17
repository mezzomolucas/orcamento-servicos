
1. Como Rodar o Projeto
Abra o terminal na pasta do projeto e execute os seguintes comandos:

Bash

# Ativar o ambiente virtual
source venv/bin/activate

# Executar a versão simplificada do sistema (recomendado)
python src/main_simples.py
Pronto! O sistema estará rodando em http://localhost:5000.

2. Como Testar (Usando Postman/Insomnia)
A forma mais fácil de testar é usando o Postman ou Insomnia.

a) Autenticação

Primeiro, crie um usuário e faça login para gerar a sessão (cookies).

Cadastrar Usuário:
POST http://localhost:5000/api/auth/register

JSON

{
  "nome": "Seu Nome",
  "email": "seu@email.com",
  "senha": "123456"
}
Fazer Login:
POST http://localhost:5000/api/auth/login

JSON

{
  "email": "seu@email.com",
  "senha": "123456"
}
Importante: As rotas abaixo só funcionam se você estiver logado!

b) Clientes

Cadastrar Cliente:
POST http://localhost:5000/api/clientes/

JSON

{
  "nome": "Maria Silva",
  "telefone": "11987654321",
  "email": "maria@email.com",
  "endereco": "Rua das Flores, 123"
}
Listar Clientes:
GET http://localhost:5000/api/clientes/

c) Serviços

Cadastrar Serviço:
POST http://localhost:5000/api/servicos/

JSON

{
  "nome": "Instalação de Ar-Condicionado",
  "descricao": "Instalação completa do aparelho",
  "valor": 250.00
}
Listar Serviços:
GET http://localhost:5000/api/servicos/

3. Entendendo os Arquivos
Para facilitar os estudos, criamos versões simplificadas e comentadas dos arquivos principais. Foque neles:

src/main_simples.py: Arquivo principal para rodar.

src/models/models_simples.py: Define as tabelas do banco de dados (Cliente, Serviço, etc).

src/routes/: Pasta com as rotas (APIs) de cada módulo. Use os arquivos com final _simples.py para entender a lógica.

4. Resolvendo Problemas Comuns
Erro "401 Unauthorized": Você não está logado ou esqueceu de enviar os cookies da sessão. Faça login primeiro.

Erro "400 Bad Request": Você enviou algum dado errado ou esqueceu um campo obrigatório no JSON.

Banco de dados deu problema?: Simplesmente apague o arquivo app.db dentro da pasta src/database e rode o sistema novamente. Ele será criado do zero.
