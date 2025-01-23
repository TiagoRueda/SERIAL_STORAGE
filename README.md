# SERIAL_STORAGE

Este script Python realiza a leitura de dados de uma porta serial, grava essas informações em um arquivo de texto e, periodicamente, faz o upload deste arquivo para o Firebase Storage. A conexão com a porta serial é mantida, e o script tenta reconectar automaticamente caso a conexão seja perdida.

**Instruções de Uso**

1. Instale as dependências necessárias.
2. Execute o comando abaixo em seu terminal:
   ```bash
   pip install firebase-admin
3. Execute o comando abaixo em seu terminal:
   ```bash
   pip install requests
4. Execute o comando abaixo em seu terminal:
   ```bash
   pip install pyserial

**Configuração do Firebase**

Para usar o Firebase, você precisa configurar o Firebase Admin SDK com as credenciais do seu projeto:

1. No Console Firebase, crie um novo projeto ou use um existente.
2. Vá para Configurações do Projeto > Contas de Serviço e gere um novo arquivo de chave privada.
3. Salve o arquivo JSON gerado em um local seguro e forneça o caminho correto para ele no código.

```
cred = credentials.Certificate("C:/Users/seuuser/pasta/suakey.json")
```

Substitua "C:/Users/seuuser/pasta/suakey.json" pelo caminho correto do seu arquivo de chave.