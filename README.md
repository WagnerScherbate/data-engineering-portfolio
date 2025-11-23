# data-engineering-portfolio
# 🏗️ Portfolio de Engenharia de Dados - Arquitetura Medalhão

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)
![Kafka](https://img.shields.io/badge/Apache-Kafka-black.svg)
![Spark](https://img.shields.io/badge/Apache-Spark-orange.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![DBT](https://img.shields.io/badge/DBT-Core-orange.svg)

## 📖 Sobre o Projeto

Este projeto demonstra uma implementação completa de uma arquitetura de dados moderna utilizando o padrão **Medalhão** (Bronze, Silver, Gold), com ingestão batch e streaming de dados fictícios gerados pela biblioteca Faker.

### 🎯 Objetivo

Simular um ambiente de engenharia de dados end-to-end para um e-commerce fictício, abrangendo desde a geração de dados até análises avançadas.

## 🏛️ Arquitetura Medalhão

```
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA GOLD                              │
│  (Dados Agregados e Otimizados para Análise)               │
│  • KPIs e Métricas de Negócio                               │
│  • Modelagem Dimensional (Star Schema)                      │
│  • PostgreSQL + Databricks                                  │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                    DBT + Spark Processing
                            │
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA SILVER                            │
│  (Dados Limpos, Validados e Transformados)                  │
│  • Deduplicação e Limpeza                                   │
│  • Padronização de Formatos                                 │
│  • Parquet/Delta Format                                     │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                   Python + PySpark ETL
                            │
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA BRONZE                            │
│  (Dados Brutos - Raw Data)                                  │
│  • Ingestão Batch (Python)                                  │
│  • Ingestão Streaming (Kafka)                               │
│  • Parquet Format                                           │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
                ┌───────────┴───────────┐
                │                       │
         Batch Ingestion        Streaming Ingestion
         (Python Script)         (Kafka Producer)
                │                       │
                └───────────┬───────────┘
                            │
                    ┌───────▼────────┐
                    │  Faker Library │
                    │ (Dados Ficticios)│
                    └────────────────┘
```

## 🗂️ Estrutura do Projeto

```
data-engineering-portfolio/
├── README.md
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── src/
│   ├── data_generation/
│   │   ├── __init__.py
│   │   ├── faker_generator.py
│   │   └── schemas.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── batch_ingestion.py
│   │   └── streaming_producer.py
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── bronze_to_silver.py
│   │   └── silver_to_gold_spark.py
│   └── consumers/
│       ├── __init__.py
│       └── streaming_consumer.py
├── dbt_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── bronze/
│       ├── silver/
│       └── gold/
├── sql/
│   ├── create_tables.sql
│   └── queries_analytics.sql
├── notebooks/
│   └── databricks_analysis.ipynb
├── config/
│   ├── kafka/
│   └── spark/
└── scripts/
    ├── setup.sh
    ├── start_batch.sh
    ├── start_streaming.sh
    └── run_dbt.sh
```

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**: Linguagem principal
- **Apache Kafka**: Streaming de dados em tempo real
- **Apache Spark**: Processamento distribuído
- **PostgreSQL**: Data Warehouse
- **DBT Core**: Transformações SQL e testes
- **Docker & Docker Compose**: Containerização
- **Faker**: Geração de dados fictícios
- **Pandas & PyArrow**: Manipulação de dados
- **PgAdmin**: Interface web para PostgreSQL

## 📊 Datasets Gerados

O projeto simula um e-commerce com os seguintes datasets:

1. **Clientes** (10.000 registros)
   - ID, Nome, Email, Telefone, Endereço, Data de Cadastro

2. **Produtos** (1.000 registros)
   - ID, Nome, Categoria, Preço, Estoque, Fornecedor

3. **Pedidos** (50.000 registros)
   - ID, ID Cliente, Data, Valor Total, Status

4. **Itens de Pedido** (150.000 registros)
   - ID, ID Pedido, ID Produto, Quantidade, Valor Unitário

5. **Eventos de Website** (500.000+ registros - streaming)
   - ID Cliente, Timestamp, Tipo de Evento, Página, Session ID

## 🔧 Pré-requisitos

- Docker Desktop instalado
- Docker Compose
- Git
- 8GB+ de RAM disponível
- 10GB+ de espaço em disco

## ⚙️ Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/WagnerScherbate/data-engineering-portfolio.git
cd data-engineering-portfolio
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 3. Inicie os serviços com Docker

```bash
docker-compose up -d
```

Aguarde alguns minutos para todos os serviços iniciarem. Você pode verificar o status:

```bash
docker-compose ps
```

### 4. Instale as dependências Python (opcional, para desenvolvimento local)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🎮 Como Usar

### 1️⃣ Ingestão Batch (Bronze Layer)

Execute o script de ingestão batch para gerar dados iniciais:

```bash
./scripts/start_batch.sh
```

Ou manualmente:

```bash
python src/ingestion/batch_ingestion.py
```

### 2️⃣ Ingestão Streaming (Bronze Layer)

Inicie o producer Kafka em um terminal:

```bash
python src/ingestion/streaming_producer.py
```

Inicie o consumer Kafka em outro terminal:

```bash
python src/consumers/streaming_consumer.py
```

### 3️⃣ Transformação Bronze → Silver

```bash
python src/processing/bronze_to_silver.py
```

### 4️⃣ Transformação Silver → Gold (Spark)

```bash
./scripts/start_spark_job.sh
```

Ou:

```bash
spark-submit src/processing/silver_to_gold_spark.py
```

### 5️⃣ Transformações DBT

```bash
cd dbt_project
dbt run
dbt test
dbt docs generate
dbt docs serve
```

### 6️⃣ Acessar Interfaces Web

- **PgAdmin**: http://localhost:5050
  - Email: admin@admin.com
  - Senha: admin

- **Spark Master UI**: http://localhost:8080

- **Kafka UI** (opcional): http://localhost:9000

## 📈 Análises no Databricks Community

1. Acesse [Databricks Community Edition](https://community.cloud.databricks.com/)
2. Importe o notebook: `notebooks/databricks_analysis.ipynb`
3. Faça upload dos arquivos Parquet da camada Gold
4. Execute as análises e visualizações

## 🔍 Exemplos de Queries

### Top 10 Produtos Mais Vendidos

```sql
SELECT 
    p.nome_produto,
    SUM(ip.quantidade) as total_vendido,
    SUM(ip.quantidade * ip.valor_unitario) as receita_total
FROM gold.itens_pedido ip
JOIN gold.produtos p ON ip.id_produto = p.id_produto
GROUP BY p.nome_produto
ORDER BY total_vendido DESC
LIMIT 10;
```

### Receita Mensal

```sql
SELECT 
    DATE_TRUNC('month', data_pedido) as mes,
    COUNT(*) as total_pedidos,
    SUM(valor_total) as receita_mensal
FROM gold.pedidos
WHERE status = 'concluido'
GROUP BY mes
ORDER BY mes DESC;
```

## 📚 Conceitos Demonstrados

- ✅ Arquitetura Medalhão (Bronze, Silver, Gold)
- ✅ Ingestão Batch e Streaming
- ✅ ETL/ELT com Python e Spark
- ✅ Modelagem de Data Warehouse
- ✅ Containerização com Docker
- ✅ Message Broker com Kafka
- ✅ Transformações SQL com DBT
- ✅ Testes de Qualidade de Dados
- ✅ Documentação Técnica
- ✅ Processamento Distribuído

## 🐛 Troubleshooting

### Problema: Kafka não inicia

```bash
docker-compose down -v
docker-compose up -d zookeeper
# Aguarde 30 segundos
docker-compose up -d kafka
```

### Problema: Spark sem memória

Ajuste no `docker-compose.yml`:

```yaml
environment:
  - SPARK_WORKER_MEMORY=2g
  - SPARK_DRIVER_MEMORY=1g
```

### Problema: PostgreSQL connection refused

Verifique se o container está rodando:

```bash
docker-compose logs postgres
```

## 📝 Próximos Passos

- [ ] Implementar Apache Airflow para orquestração
- [ ] Adicionar Great Expectations para validação de dados
- [ ] Implementar CDC (Change Data Capture)
- [ ] Adicionar Monitoring com Prometheus + Grafana
- [ ] Implementar Data Lineage
- [ ] Adicionar testes de integração
- [ ] Implementar CI/CD com GitHub Actions

## 👤 Autor

**Wagner Scherbate**

- GitHub: [@WagnerScherbate](https://github.com/WagnerScherbate)
- LinkedIn: [Seu LinkedIn]

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- Biblioteca Faker pela geração de dados
- Comunidade Apache por Kafka e Spark
- DBT Labs pelo DBT Core
- Databricks Community Edition

---

⭐ Se este projeto foi útil, considere dar uma estrela!