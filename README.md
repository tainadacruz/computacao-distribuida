# Serviço de Espaço de Tuplas Tolerante a Falhas com Kazoo/Zookeeper

Este projeto implementa um espaço de tuplas usando Kazoo/Zookeeper com um backend Flask e um frontend React. A API do backend se comunica com o servidor Zookeeper para realizar operações nas tuplas, enquanto o frontend React fornece uma interface de usuário para interagir com o espaço de tuplas.

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Instruções de Configuração](#instruções-de-configuração)
  - [Instalação do Apache Zookeeper](#instação-do-apache-zookeeper)
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

### Instalação do Apache Zookeeper

1. **Baixe a versão estável mais recente do Zookeeper no [site do Apache Zookeeper](https://zookeeper.apache.org/releases.html).**


2. **Extraia o arquivo tar.gz baixado 3 vezes cada um em seu próprio diretório (a aplicação está programada para funcionar com no máximo 3 servidores):**

    ```sh
    mkdir Zookeeper
    mkdir Zookeeper2
    mkdir Zoopkeeper3
    tar -zxf zookeeper-x.y.z.tar.gz -C ./Zookeeper
    tar -zxf zookeeper-x.y.z.tar.gz -C ./Zookeeper2
    tar -zxf zookeeper-x.y.z.tar.gz -C ./Zookeeper3
    ```

3. **Dentro de cada pasta extraída, execute os seguintes comandos:**

    ```
    cp conf/zoo_sample.cfg conf/zoo.cfg
    mkdir data
    ``` 
   
4. **Modifique o arquivo zoo.cfg em cada pasta extraída para que fique com o seguinte texto:**
     
    ```
    tickTime=2000
    initLimit=5
    syncLimit=2
    dataDir=/path/para/data
    clientPort=XXXX
    server.1=localhost:2888:3888
    server.2=localhost:2889:3889
    server.3=localhost:2890:3890
    ```

    A clientPort deve ter um valor diferent em cada arquivo zoo.cfg, esses sendo 2181, 2182 e 2183.
    Substituir /path/para/data em dataDir do arquivo zoo.cfg pelo caminho de home ao diretório data do servidor que está sendo configurado.
   
6. **Dentro do diretório data/ de cada instância do zookeeper, crie um arquivo chamado myid com o seguinte comando:**
   
   - Em Zookeeper  
     ```
     echo "1" >> myid
     ```
   - Em Zookeeper2
     ```
     echo "2" >> myid
     ```
   - Em Zookeeper3
     ```
     echo "3" >> myid
     ```

7. **Inicie o Zookeeper com esse comando em terminais diferentes uma vez para cada servidor:**

     ```sh
     bin/zkServer.sh start
     ```

8. **Verifique se o Zookeeper está em execução através do status:**

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
