# Dashboard de Vendas E-commerce

Projeto desenvolvido para análise exploratória de um dataset de e-commerce usando Python, Dash, Plotly e Pandas.

O dashboard apresenta KPIs, filtros interativos e gráficos para analisar catálogo, vendas estimadas, preços, descontos, avaliações, marcas, materiais, gênero e temporada dos produtos.

## Funcionalidades

- Filtros por gênero, temporada e marca.
- Indicadores de produtos, vendas estimadas, receita estimada, preço médio, nota média e desconto médio.
- Histogramas, rankings, gráfico de dispersão, boxplot, treemap, mapa de correlação e regressão.
- Tratamento inicial das colunas para evitar erros causados por nomes com ou sem acento.
- Estimativa numérica de vendas a partir das faixas textuais do dataset.

## Estrutura do projeto

```text
.
├── data/
│   └── ecommerce_preparados.csv
├── src/
│   └── dashboard_ecommerce/
│       ├── __init__.py
│       └── app.py
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Como executar

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o dashboard:

```bash
python run.py
```

Depois acesse:

```text
http://127.0.0.1:8050
```

## Dataset

O arquivo usado pelo dashboard está em `data/ecommerce_preparados.csv`.

A coluna `Qtd_Vendidos` contém faixas textuais, como `+100`, `+1000` e `+10mil`. Por isso, os campos `Vendas_Num` e `Receita_Estimada` são aproximações para análise exploratória, não valores oficiais de faturamento.

## Tecnologias

- Python
- Dash
- Plotly
- Pandas
- Statsmodels

