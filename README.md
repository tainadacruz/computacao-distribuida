# Serviço de Espaço de Tuplas Tolerante a Falhas

## Visão Geral
Este projeto implementa um serviço de espaço de tuplas tolerante a falhas utilizando `Pyro4` para comunicação distribuída e `Redis` para sincronização e bloqueio distribuído. O serviço permite adicionar, ler e remover tuplas de um espaço de memória compartilhada de forma segura e confiável.

## Requisitos
- Python 3.x
- Pyro4
- Redis
- threading

## Instalação

1. **Instale as dependências necessárias:**
   ```sh
   pip install Pyro4 redis

