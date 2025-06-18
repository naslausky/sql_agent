# SQL Agent
> SQL Agent Inteligente utilizando Langflow e modelos de IA generativa.

### Como rodar:
 - Vá para a raiz do projeto.
 - Instale os requisitos:
   ```pip install -r requirements.txt```
 - Adicione o seu arquivo oculto ```.env```. Segue o formato dele abaixo:
   ```
   OPENAI_API_KEY= {APIKEY da OpenAI}
   POSTGRES_HOST={Endereço IP do servidor POSTGRESQL}
   POSTGRES_PORT={Porta do servidor POSTGRESQL}
   POSTGRES_USER={Usuario para acessar o BD}
   POSTGRES_PASSWORD={Senha do usuario acima}
   POSTGRES_DB={Nome do BD}
    ```
 - Lembre-se de adicionar suas próprias informações ao arquivo mencionado acima.
 - Para correta segurança da orquestração, certifique-se que o usuário do POSTGRESQL tenha permissões de **somente leitura**.
 - Certifique-se que o banco de dados contenha as tabelas corretas:
   ```sql
    -- Tabela de clientes
    CREATE TABLE clientes (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        saldo NUMERIC(10, 2) DEFAULT 0.00  -- Saldo disponível do cliente
    );
    
    -- Tabela de produtos
    CREATE TABLE produtos (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        preco NUMERIC(10, 2) NOT NULL
    );
    
    -- Tabela de transações (compra de produtos por clientes)
    CREATE TABLE transacoes (
        id SERIAL PRIMARY KEY,
        cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
        produto_id INTEGER NOT NULL REFERENCES produtos(id) ON DELETE SET NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
   ```
 - Certifique-se que o banco de dados esteja populado:
   ```sql
      INSERT INTO clientes (nome, email, saldo) VALUES
      ('Alice Martins', 'alice@example.com', 1500.00),
      ('Bruno Lima', 'bruno@example.com', 300.00),
      ('Carla Souza', 'carla@example.com', 2200.00),
      ('Daniel Rocha', 'daniel@example.com', 850.00),
      ('Eduarda Ramos', 'eduarda@example.com', 120.00);
      INSERT INTO produtos (nome, preco) VALUES
      ('Notebook', 2000.00),
      ('Smartphone', 900.00),
      ('Fone de Ouvido', 150.00),
      ('Teclado Mecânico', 350.00),
      ('Mouse Gamer', 200.00);
      INSERT INTO transacoes (cliente_id, produto_id, data) VALUES
      (1, 2, '2024-05-01 10:30:00'),  -- Alice comprou um Smartphone
      (2, 5, '2024-05-02 12:00:00'),  -- Bruno comprou um Mouse Gamer
      (3, 1, '2024-05-03 09:45:00'),  -- Carla comprou um Notebook
      (4, 4, '2024-05-04 14:20:00'),  -- Daniel comprou um Teclado
      (1, 3, '2024-05-05 11:10:00'),  -- Alice comprou um Fone
      (3, 5, '2024-05-06 16:30:00'),  -- Carla comprou um Mouse
      (1, 5, '2024-05-07 08:20:00');  -- Alice comprou outro Mouse
   ```
- Rode o script principal: ```python3 main.py```

## 💻 Imagens da utilização
