# Serviço de Espaço de Tuplas Tolerante a Falhas com Kazoo/Zookeeper

Este projeto implementa um espaço de tuplas usando Kazoo/Zookeeper com um backend Flask e um frontend React. A API do backend se comunica com o servidor Zookeeper para realizar operações nas tuplas, enquanto o frontend React fornece uma interface de usuário para interagir com o espaço de tuplas.

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Instruções de Configuração](#instruções-de-configuração)
  - [Instalar Apache Zookeeper](#instalar-apache-zookeeper)
  - [Configuração do Backend](#configuração-do-backend)
  - [Configuração do Frontend](#configuração-do-frontend)
- [Uso](#uso)

## Pré-requisitos

- Python 3.7+
- Node.js 12+
- npm ou yarn
- Apache Zookeeper
- Kazoo (biblioteca Python para Zookeeper)

## Instruções de Configuração

### Instalar Apache Zookeeper

1. **Baixar e Instalar o Zookeeper:**

   - Baixe a versão estável mais recente do Zookeeper no [site do Apache Zookeeper](https://zookeeper.apache.org/releases.html).

   - Extraia o arquivo tar.gz baixado:

     ```sh
     tar -zxf zookeeper-x.y.z.tar.gz
     cd zookeeper-x.y.z
     ```

   - Execute o seguinte comando:

     ```
     cp conf/zoo_sample.cfg conf/zoo.cfg 
     ``` 

   - Inicie o Zookeeper:

     ```sh
     bin/zkServer.sh start
     ```

   - Verifique se o Zookeeper está em execução verificando o status:

     ```sh
     bin/zkServer.sh status
     ```

### Configuração do Backend

1. **Clone o repositório:**

   ```sh
   git clone https://github.com/tainadacruz/computacao-distribuida.git
   cd computacao-distribuida/backend
   ```


2. **Crie um ambiente virtual e ative-o:**

   ```sh
   python -m venv venv
   source venv/bin/activate # No Windows, use `venv\Scripts\activate`
   ```

3. **Instale as dependências necessárias:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Inicie o servidor Flask:**

   ```sh
   python app.py
   ```

### Configuração do Frontend

1. **Navegue até o diretório do frontend:**

   ```sh
   cd ../frontend
   ```

2. **Instale as dependências:**

   ```sh
   npm install
   ```

3. **Inicie a aplicação React:**

   ```sh
   npm start
   ```

Sua aplicação React deve estar em execução em http://localhost:3000.

### Uso

Abra o seu navegador e navegue até http://localhost:3000. 
Use o formulário na página para escrever, obter e listar tuplas no espaço de tuplas.
