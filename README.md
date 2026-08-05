# Store - Plataforma de Comércio Eletrônico

## Descrição do Projeto

A Store é uma plataforma de comércio eletrônico desenvolvida para comercialização de camisetas pela internet.

O sistema permite que clientes realizem cadastro, autenticação, pesquisa de produtos, gerenciamento do carrinho de compras e finalização de pedidos. Além disso, disponibiliza um painel administrativo para gerenciamento dos produtos cadastrados.

A aplicação foi desenvolvida utilizando Python com o framework Flask e banco de dados SQLite.

Nesta etapa do projeto, a aplicação encontra-se em processo de homologação e será submetida à validação pela equipe de Qualidade de Software (QA) antes da publicação em ambiente de produção.

---

# Objetivo da Homologação

Validar as funcionalidades implementadas na aplicação, identificando possíveis falhas, inconsistências e não conformidades em relação aos requisitos do projeto, garantindo que o sistema esteja apto para publicação.

---

# Tecnologias Utilizadas

- Python 3
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap

---

# Estrutura do Projeto

```text
app/
static/
templates/
instance/
docs/
requirements.txt
README.md
```

---

# Configuração do Ambiente

## 1. Clonar o repositório

```bash
git clone https://github.com/iamabiel/loja-mcs.git
```

---

## 2. Acessar a pasta

```bash
cd loja-mcs
```

---

## 3. Criar ambiente virtual

Windows

```bash
python -m venv .venv
```

Linux

```bash
python3 -m venv .venv
```

---

## 4. Ativar ambiente virtual

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

---

## 5. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 6. Executar a aplicação

```bash
python run.py
```

ou

```bash
py run.py
```

---

## Endereço da aplicação

```
http://localhost:5000
```

---

# Credenciais para Homologação

## Cliente

E-mail

```
cliente@teste.com
```

Senha

```
123456
```

---

## Administrador

E-mail

```
testando@gmail.com
```

Senha

```
123456
```

---

# Funcionalidades Disponíveis

- Cadastro de usuários
- Login
- Pesquisa de produtos
- Visualização de produtos
- Carrinho de compras
- Atualização de quantidades
- Remoção de produtos do carrinho
- Finalização de pedidos
- Área administrativa

---

# Documentação do Projeto

A documentação necessária para execução da homologação encontra-se na pasta:

```text
docs/
```

Antes de iniciar os testes, recomenda-se a leitura dos seguintes documentos:

- Documento de Requisitos Funcionais
- Regras de Negócio
- Fluxo da Aplicação
- Manual do Sistema

---

# Orientações para a Equipe de QA

Antes da execução dos testes, a equipe deverá:

- Configurar o ambiente local.
- Executar a aplicação em localhost.
- Estudar a documentação do projeto.
- Compreender as funcionalidades implementadas.
- Elaborar o Plano de Testes.
- Desenvolver os Casos de Teste.
- Executar os testes planejados.
- Registrar os defeitos encontrados.
- Emitir o Relatório Final de Homologação.

---

# Observações

Esta aplicação foi disponibilizada exclusivamente para fins de homologação e treinamento da equipe técnica de Qualidade de Software.

Durante a homologação poderão existir defeitos conhecidos ou não conhecidos que deverão ser identificados e documentados pela equipe responsável pelos testes.
