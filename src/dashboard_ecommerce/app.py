from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from pathlib import Path

# ==============================================================================
# DASHBOARD E-COMMERCE — VERSÃO APRIMORADA
# ===============================================================================
# Objetivo:
# - Criar uma análise visual completa do dataset ecommerce_preparados.csv
# - Usar filtros interativos
# - Separar análise de catálogo, vendas, distribuição e correlação
# - Evitar gráficos com interpretação enganosa
# ===============================================================================

# ==============================================================================
# 1. CARGA E PADRONIZAÇÃO DOS DADOS
# ===============================================================================

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_CSV = RAIZ_PROJETO / "data" / "ecommerce_preparados.csv"

if not CAMINHO_CSV.exists():
    raise FileNotFoundError(
        "Arquivo ecommerce_preparados.csv não encontrado. "
        "Confira se ele está na pasta data/ do projeto."
    )

df = pd.read_csv(CAMINHO_CSV)

# Remove espaços invisíveis nos nomes das colunas
df.columns = df.columns.str.strip()

# Remove coluna de índice exportada pelo pandas, se existir
for coluna in ["Unnamed: 0", "unnamed", "Unnamed"]:
    if coluna in df.columns:
        df = df.drop(columns=[coluna])

# Padroniza nomes com e sem acento para evitar erros de coluna ausente.
df = df.rename(
    columns={
        "Titulo": "Título",
        "Genero": "Gênero",
        "N_Avaliacoes": "N_Avaliações",
        "Preco": "Preço",
        "Preco_MinMax": "Preço_MinMax",
        "Qtd Vendidos": "Qtd_Vendidos",
        "Quantidade_Vendida": "Qtd_Vendidos",
    }
)

# Colunas mínimas necessárias para este dashboard
colunas_necessarias = [
    "Título",
    "Nota",
    "N_Avaliações",
    "Desconto",
    "Marca",
    "Material",
    "Gênero",
    "Temporada",
    "Qtd_Vendidos",
    "Preço",
]

faltando = [col for col in colunas_necessarias if col not in df.columns]
if faltando:
    raise ValueError(
        "As seguintes colunas necessárias não foram encontradas no CSV: "
        + ", ".join(faltando)
    )

# Converte colunas numéricas de forma segura
colunas_numericas = ["Nota", "N_Avaliações", "Desconto", "Preço"]
for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

# ==============================================================================
# 2. FEATURE ENGINEERING PARA ANÁLISE
# ===============================================================================

# Mapeia faixas textuais de venda para número estimado
mapa_vendas = {
    "Nenhum": 0,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "+5": 5,
    "+25": 25,
    "+50": 50,
    "+100": 100,
    "+500": 500,
    "+1000": 1000,
    "+5mil": 5000,
    "+10mil": 10000,
    "+50mil": 50000,
}

df["Qtd_Vendidos"] = df["Qtd_Vendidos"].astype(str).str.strip()
df["Vendas_Num"] = df["Qtd_Vendidos"].map(mapa_vendas).fillna(0).astype(int)


# Agrupamento de gênero para evitar pizza com 300 fatias do inferno
def agrupar_genero(valor):
    valor = str(valor).strip()
    mapa = {
        "Feminino": "Feminino",
        "Masculino": "Masculino",
        "Bebês": "Bebês",
        "Sem gênero": "Sem gênero",
        "Meninas": "Infantil",
        "Meninos": "Infantil",
        "Sem gênero infantil": "Infantil",
    }
    return mapa.get(valor, "Outros")


df["Genero_Agrupado"] = df["Gênero"].apply(agrupar_genero)


# Agrupamento de temporada
def agrupar_temporada(valor):
    valor = str(valor).strip().lower()
    mapa = {
        "não definido": "Não definido",
        "nao definido": "Não definido",
        "primavera/verão": "Primavera/Verão",
        "primavera/verao": "Primavera/Verão",
        "outono/inverno": "Outono/Inverno",
    }
    return mapa.get(valor, "Mista/Outros")


df["Temporada_Agrupada"] = df["Temporada"].apply(agrupar_temporada)

# Receita estimada: como Qtd_Vendidos é faixa aproximada, isso é uma estimativa
# Não é faturamento oficial. É uma aproximação útil para análise exploratória.
df["Receita_Estimada"] = df["Preço"] * df["Vendas_Num"]

# ==============================================================================
# 3. TEMA VISUAL
# ===============================================================================

CORES = {
    "fundo": "#0f0f1a",
    "card": "#1a1a2e",
    "card_borda": "#2a2a4a",
    "texto": "#e8e8f0",
    "texto_secundario": "#9a9ab8",
    "destaque1": "#6c63ff",
    "destaque2": "#00d4aa",
    "destaque3": "#ff6b9d",
    "destaque4": "#ffa726",
    "azul": "#42a5f5",
    "vermelho": "#ef5350",
}

PLOTLY_COLORS = [
    "#6c63ff",
    "#00d4aa",
    "#ff6b9d",
    "#ffa726",
    "#42a5f5",
    "#ab47bc",
    "#26c6da",
    "#ef5350",
    "#66bb6a",
    "#ffca28",
]


def aplicar_tema(fig, **kwargs):
    """Aplica tema escuro personalizado a qualquer figura Plotly."""
    defaults = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=CORES["texto"], size=13),
        title_font=dict(size=18, color=CORES["texto"]),
        margin=dict(l=50, r=30, t=65, b=50),
        hoverlabel=dict(
            bgcolor=CORES["card"],
            font_size=12,
            font_family="Inter, Arial, sans-serif",
        ),
    )
    defaults.update(kwargs)
    fig.update_layout(**defaults)
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.12)",
        linecolor="rgba(255,255,255,0.12)",
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.12)",
        linecolor="rgba(255,255,255,0.12)",
    )
    return fig


ESTILO_CARD = {
    "backgroundColor": CORES["card"],
    "borderRadius": "18px",
    "border": f"1px solid {CORES['card_borda']}",
    "padding": "22px",
    "boxShadow": "0 8px 32px rgba(0,0,0,0.32)",
}

ESTILO_FILTRO = {
    "backgroundColor": CORES["card"],
    "borderRadius": "18px",
    "border": f"1px solid {CORES['card_borda']}",
    "padding": "22px",
    "marginBottom": "30px",
    "boxShadow": "0 8px 32px rgba(0,0,0,0.32)",
}

# ==============================================================================
# 4. FUNÇÕES AUXILIARES
# ===============================================================================


def formatar_numero(valor):
    if pd.isna(valor):
        return "0"
    if abs(valor) >= 1_000_000:
        return f"{valor / 1_000_000:.1f} mi"
    if abs(valor) >= 1_000:
        return f"{valor / 1_000:.1f} mil"
    return f"{valor:,.0f}".replace(",", ".")


def formatar_moeda(valor):
    if pd.isna(valor):
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def figura_vazia(
    titulo, mensagem="Nenhum dado encontrado para os filtros selecionados."
):
    fig = go.Figure()
    fig.add_annotation(
        text=mensagem,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=16, color=CORES["texto_secundario"]),
    )
    aplicar_tema(fig, title=titulo)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def criar_kpi(titulo, valor, cor, subtitulo=None):
    return html.Div(
        style={
            "backgroundColor": CORES["card"],
            "borderRadius": "18px",
            "border": f"1px solid {CORES['card_borda']}",
            "borderTop": f"3px solid {cor}",
            "padding": "24px 22px",
            "textAlign": "center",
            "boxShadow": "0 8px 32px rgba(0,0,0,0.32)",
            "flex": "1",
            "minWidth": "185px",
        },
        children=[
            html.P(
                titulo,
                style={
                    "color": CORES["texto_secundario"],
                    "fontSize": "13px",
                    "margin": "0 0 8px",
                },
            ),
            html.H2(
                valor,
                style={
                    "margin": "0",
                    "fontSize": "31px",
                    "fontWeight": "800",
                    "color": cor,
                },
            ),
            html.P(
                subtitulo or "",
                style={
                    "color": CORES["texto_secundario"],
                    "fontSize": "11px",
                    "margin": "8px 0 0",
                },
            ),
        ],
    )


def secao(titulo, cor):
    return html.H2(
        titulo,
        style={
            "fontSize": "22px",
            "fontWeight": "700",
            "marginBottom": "20px",
            "marginTop": "14px",
            "color": CORES["texto"],
            "borderLeft": f"4px solid {cor}",
            "paddingLeft": "16px",
        },
    )


def card_grafico(graph_id, altura="410px"):
    return html.Div(
        style=ESTILO_CARD,
        children=[
            dcc.Graph(
                id=graph_id,
                config={"displayModeBar": False},
                style={"height": altura},
            )
        ],
    )


# ==============================================================================
# 5. FUNÇÕES DOS GRÁFICOS
# ===============================================================================


def grafico_distribuicao_precos(dff):
    dff = dff.dropna(subset=["Preço"])
    if dff.empty:
        return figura_vazia("Distribuição de Preços")

    fig = px.histogram(
        dff,
        x="Preço",
        nbins=40,
        color_discrete_sequence=[CORES["destaque1"]],
        labels={"Preço": "Preço (R$)", "count": "Quantidade"},
    )
    aplicar_tema(
        fig,
        title="Distribuição de Preços dos Produtos",
        bargap=0.05,
        yaxis_title="Quantidade de Produtos",
        xaxis_title="Faixa de Preço (R$)",
    )
    fig.update_traces(
        marker_line_color=CORES["fundo"], marker_line_width=1, opacity=0.86
    )
    return fig


def grafico_distribuicao_notas(dff):
    dff = dff.dropna(subset=["Nota"])
    if dff.empty:
        return figura_vazia("Distribuição das Notas")

    notas_contagem = dff["Nota"].value_counts().sort_index()
    fig = go.Figure(
        go.Bar(
            x=notas_contagem.index,
            y=notas_contagem.values,
            marker=dict(
                color=notas_contagem.values,
                colorscale=[
                    [0, CORES["destaque3"]],
                    [0.5, CORES["destaque1"]],
                    [1, CORES["destaque2"]],
                ],
                line=dict(color=CORES["fundo"], width=1),
            ),
            text=notas_contagem.values,
            textposition="outside",
            textfont=dict(color=CORES["texto"], size=11),
        )
    )
    aplicar_tema(
        fig,
        title="Distribuição das Notas dos Produtos",
        xaxis_title="Nota",
        yaxis_title="Quantidade de Produtos",
    )
    fig.update_xaxes(dtick=0.2)
    return fig


def grafico_genero(dff):
    if dff.empty:
        return figura_vazia("Produtos por Gênero")

    genero_contagem = dff["Genero_Agrupado"].value_counts()
    fig = go.Figure(
        go.Pie(
            labels=genero_contagem.index,
            values=genero_contagem.values,
            hole=0.55,
            marker=dict(colors=PLOTLY_COLORS, line=dict(color=CORES["fundo"], width=2)),
            textinfo="label+percent",
            textposition="outside",
            textfont=dict(size=12),
        )
    )
    aplicar_tema(fig, title="Composição dos Produtos por Gênero", showlegend=False)
    return fig


def grafico_marcas_vendas(dff):
    dff = dff.dropna(subset=["Marca"])
    if dff.empty:
        return figura_vazia("Top Marcas por Vendas")

    top = (
        dff.groupby("Marca")["Vendas_Num"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )
    fig = go.Figure(
        go.Bar(
            x=top.values,
            y=top.index,
            orientation="h",
            marker=dict(
                color=top.values,
                colorscale=[[0, "#2a2a4a"], [1, CORES["destaque1"]]],
                line=dict(color=CORES["fundo"], width=1),
            ),
            text=[formatar_numero(v) for v in top.values],
            textposition="outside",
            textfont=dict(color=CORES["texto"], size=11),
        )
    )
    aplicar_tema(
        fig,
        title="Top 10 Marcas por Volume de Vendas",
        xaxis_title="Vendas estimadas",
        yaxis_title="",
        margin=dict(l=150, r=60, t=65, b=50),
    )
    return fig


def grafico_top_produtos(dff):
    dff = dff.dropna(subset=["Título"])
    if dff.empty:
        return figura_vazia("Top Produtos por Vendas")

    top = (
        dff.groupby("Título")["Vendas_Num"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )
    fig = go.Figure(
        go.Bar(
            x=top.values,
            y=top.index,
            orientation="h",
            marker=dict(
                color=top.values,
                colorscale=[[0, "#2a2a4a"], [1, CORES["destaque2"]]],
                line=dict(color=CORES["fundo"], width=1),
            ),
            text=[formatar_numero(v) for v in top.values],
            textposition="outside",
            textfont=dict(color=CORES["texto"], size=11),
        )
    )
    aplicar_tema(
        fig,
        title="Top 10 Produtos por Vendas Estimadas",
        xaxis_title="Vendas estimadas",
        yaxis_title="",
        margin=dict(l=230, r=60, t=65, b=50),
    )
    return fig


def grafico_preco_por_faixa_vendas(dff):
    dff = dff.dropna(subset=["Preço"])
    if dff.empty:
        return figura_vazia("Preço Médio por Faixa de Vendas")

    ordem_vendas = [
        "Nenhum",
        "1",
        "2",
        "3",
        "4",
        "+5",
        "+25",
        "+50",
        "+100",
        "+500",
        "+1000",
        "+5mil",
        "+10mil",
        "+50mil",
    ]

    temp = dff.groupby("Qtd_Vendidos")["Preço"].agg(["mean", "count"]).reset_index()
    temp.columns = ["Faixa", "Preço_Médio", "Qtd"]
    temp["Ordem"] = temp["Faixa"].map({v: i for i, v in enumerate(ordem_vendas)})
    temp = temp.dropna(subset=["Ordem"]).sort_values("Ordem")

    if temp.empty:
        return figura_vazia("Preço Médio por Faixa de Vendas")

    fig = go.Figure(
        go.Bar(
            x=temp["Faixa"],
            y=temp["Preço_Médio"],
            marker=dict(
                color=temp["Preço_Médio"],
                colorscale=[[0, CORES["destaque2"]], [1, CORES["destaque4"]]],
                line=dict(color=CORES["fundo"], width=1),
            ),
            text=[formatar_moeda(v) for v in temp["Preço_Médio"]],
            textposition="outside",
            textfont=dict(color=CORES["texto"], size=10),
            customdata=temp[["Qtd"]],
            hovertemplate="Faixa: %{x}<br>Preço médio: R$ %{y:.2f}<br>Produtos na faixa: %{customdata[0]}<extra></extra>",
        )
    )
    aplicar_tema(
        fig,
        title="Preço Médio por Faixa de Vendas",
        xaxis_title="Faixa de venda",
        yaxis_title="Preço médio (R$)",
    )
    return fig


def grafico_temporada(dff):
    if dff.empty:
        return figura_vazia("Produtos por Temporada")

    contagem = dff["Temporada_Agrupada"].value_counts()
    fig = go.Figure(
        go.Bar(
            x=contagem.index,
            y=contagem.values,
            marker=dict(
                color=PLOTLY_COLORS[: len(contagem)],
                line=dict(color=CORES["fundo"], width=1),
            ),
            text=contagem.values,
            textposition="outside",
            textfont=dict(color=CORES["texto"], size=12),
        )
    )
    aplicar_tema(
        fig,
        title="Produtos por Temporada",
        xaxis_title="Temporada",
        yaxis_title="Quantidade de Produtos",
    )
    return fig


def grafico_box_nota_genero(dff):
    dff = dff.dropna(subset=["Nota"])
    if dff.empty:
        return figura_vazia("Notas por Gênero")

    fig = px.box(
        dff,
        x="Genero_Agrupado",
        y="Nota",
        color="Genero_Agrupado",
        points="outliers",
        color_discrete_sequence=PLOTLY_COLORS,
        labels={"Genero_Agrupado": "Gênero", "Nota": "Nota"},
    )
    aplicar_tema(
        fig,
        title="Distribuição de Notas por Gênero",
        showlegend=False,
        xaxis_title="Gênero",
        yaxis_title="Nota",
    )
    return fig


def grafico_materiais(dff):
    dff = dff.dropna(subset=["Material"])
    if dff.empty:
        return figura_vazia("Materiais Mais Utilizados")

    top = dff["Material"].value_counts().head(10)
    fig = go.Figure(
        go.Treemap(
            labels=top.index,
            parents=[""] * len(top),
            values=top.values,
            marker=dict(
                colors=PLOTLY_COLORS[: len(top)],
                line=dict(color=CORES["fundo"], width=2),
            ),
            textinfo="label+value+percent root",
            textfont=dict(size=14),
        )
    )
    aplicar_tema(
        fig,
        title="Top 10 Materiais Mais Utilizados",
        margin=dict(l=10, r=10, t=65, b=10),
    )
    return fig


def grafico_correlacao(dff):
    cols = [
        "Nota",
        "N_Avaliações",
        "Desconto",
        "Preço",
        "Vendas_Num",
        "Receita_Estimada",
    ]
    dff = dff[cols].dropna(how="all")
    if len(dff) < 2:
        return figura_vazia("Mapa de Correlação")

    corr = dff.corr(numeric_only=True)
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        labels=dict(color="Correlação"),
    )
    aplicar_tema(
        fig,
        title="Mapa de Correlação entre Variáveis Numéricas",
        margin=dict(l=70, r=35, t=65, b=80),
    )
    return fig


def grafico_scatter_preco_vendas(dff):
    dff = dff.dropna(subset=["Preço", "Vendas_Num", "N_Avaliações"])
    dff = dff[(dff["Vendas_Num"] >= 0) & (dff["N_Avaliações"] > 0)]
    if dff.empty:
        return figura_vazia("Preço x Vendas")

    fig = px.scatter(
        dff,
        x="Preço",
        y="Vendas_Num",
        color="Genero_Agrupado",
        size="N_Avaliações",
        hover_data={
            "Título": True,
            "Marca": True,
            "Nota": True,
            "Desconto": True,
            "Genero_Agrupado": True,
            "N_Avaliações": True,
        },
        labels={
            "Preço": "Preço (R$)",
            "Vendas_Num": "Vendas estimadas",
            "Genero_Agrupado": "Gênero",
            "N_Avaliações": "Nº de avaliações",
        },
        color_discrete_sequence=PLOTLY_COLORS,
    )
    aplicar_tema(
        fig,
        title="Relação entre Preço e Vendas",
        xaxis_title="Preço (R$)",
        yaxis_title="Vendas estimadas",
    )
    return fig


def grafico_regressao_desconto_vendas(dff):
    dff = dff.dropna(subset=["Desconto", "Vendas_Num"])
    dff = dff[dff["Vendas_Num"] >= 0]
    if len(dff) < 3:
        return figura_vazia(
            "Regressão: Desconto x Vendas", "Dados insuficientes para regressão."
        )

    try:
        fig = px.scatter(
            dff,
            x="Desconto",
            y="Vendas_Num",
            trendline="ols",
            hover_data=["Título", "Marca", "Preço", "Nota"],
            labels={"Desconto": "Desconto (%)", "Vendas_Num": "Vendas estimadas"},
            color_discrete_sequence=[CORES["destaque2"]],
        )
    except Exception:
        # Fallback caso statsmodels não esteja instalado
        fig = px.scatter(
            dff,
            x="Desconto",
            y="Vendas_Num",
            hover_data=["Título", "Marca", "Preço", "Nota"],
            labels={"Desconto": "Desconto (%)", "Vendas_Num": "Vendas estimadas"},
            color_discrete_sequence=[CORES["destaque2"]],
        )
        fig.add_annotation(
            text="Para exibir linha de regressão: pip install statsmodels",
            x=0.5,
            y=1.08,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=12, color=CORES["texto_secundario"]),
        )

    aplicar_tema(
        fig,
        title="Tendência entre Desconto e Vendas",
        xaxis_title="Desconto (%)",
        yaxis_title="Vendas estimadas",
    )
    return fig


# ==============================================================================
# 6. APP DASH
# ===============================================================================

app = Dash(__name__)
app.title = "Dashboard E-commerce — Análise de Vendas"
server = app.server

# Opções dos filtros
opcoes_genero = sorted(df["Genero_Agrupado"].dropna().unique())
opcoes_temporada = sorted(df["Temporada_Agrupada"].dropna().unique())
opcoes_marca = sorted(df["Marca"].dropna().unique())

app.layout = html.Div(
    style={
        "backgroundColor": CORES["fundo"],
        "minHeight": "100vh",
        "fontFamily": "Inter, -apple-system, BlinkMacSystemFont, Arial, sans-serif",
        "color": CORES["texto"],
        "padding": "0",
        "margin": "0",
    },
    children=[
        # Cabeçalho
        html.Div(
            style={
                "background": "linear-gradient(135deg, #1a1a2e 0%, #16213e 55%, #0f3460 100%)",
                "padding": "42px 48px 34px",
                "borderBottom": f"1px solid {CORES['card_borda']}",
                "marginBottom": "32px",
            },
            children=[
                html.H1(
                    "Dashboard de Vendas — E-commerce",
                    style={
                        "margin": "0 0 8px 0",
                        "fontSize": "34px",
                        "fontWeight": "800",
                        "background": "linear-gradient(135deg, #6c63ff, #00d4aa)",
                        "WebkitBackgroundClip": "text",
                        "WebkitTextFillColor": "transparent",
                        "letterSpacing": "-0.7px",
                    },
                ),
                html.P(
                    "Análise exploratória com filtros, KPIs, distribuições, rankings, correlação e regressão.",
                    style={
                        "margin": "0",
                        "color": CORES["texto_secundario"],
                        "fontSize": "15px",
                    },
                ),
            ],
        ),
        # Conteúdo
        html.Div(
            style={"padding": "0 48px 48px", "maxWidth": "1480px", "margin": "0 auto"},
            children=[
                # Filtros
                html.Div(
                    style=ESTILO_FILTRO,
                    children=[
                        html.H3(
                            "Filtros interativos",
                            style={
                                "margin": "0 0 18px",
                                "fontSize": "18px",
                                "fontWeight": "700",
                            },
                        ),
                        html.Div(
                            style={
                                "display": "grid",
                                "gridTemplateColumns": "1fr 1fr 1fr",
                                "gap": "18px",
                            },
                            children=[
                                html.Div(
                                    children=[
                                        html.Label(
                                            "Gênero",
                                            style={
                                                "fontSize": "13px",
                                                "color": CORES["texto_secundario"],
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="filtro-genero",
                                            options=[
                                                {"label": g, "value": g}
                                                for g in opcoes_genero
                                            ],
                                            multi=True,
                                            placeholder="Todos os gêneros",
                                            style={"color": "#111", "marginTop": "6px"},
                                        ),
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label(
                                            "Temporada",
                                            style={
                                                "fontSize": "13px",
                                                "color": CORES["texto_secundario"],
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="filtro-temporada",
                                            options=[
                                                {"label": t, "value": t}
                                                for t in opcoes_temporada
                                            ],
                                            multi=True,
                                            placeholder="Todas as temporadas",
                                            style={"color": "#111", "marginTop": "6px"},
                                        ),
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.Label(
                                            "Marca",
                                            style={
                                                "fontSize": "13px",
                                                "color": CORES["texto_secundario"],
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="filtro-marca",
                                            options=[
                                                {"label": m, "value": m}
                                                for m in opcoes_marca
                                            ],
                                            multi=True,
                                            placeholder="Todas as marcas",
                                            style={"color": "#111", "marginTop": "6px"},
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
                # KPIs
                html.Div(
                    id="kpi-container",
                    style={
                        "display": "flex",
                        "gap": "20px",
                        "marginBottom": "36px",
                        "flexWrap": "wrap",
                    },
                ),
                # Distribuições
                secao("Distribuições", CORES["destaque1"]),
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "24px",
                        "marginBottom": "36px",
                    },
                    children=[
                        card_grafico("grafico-precos"),
                        card_grafico("grafico-notas"),
                    ],
                ),
                # Composição
                secao("Composição do Catálogo", CORES["destaque2"]),
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "24px",
                        "marginBottom": "36px",
                    },
                    children=[
                        card_grafico("grafico-genero"),
                        card_grafico("grafico-temporada"),
                    ],
                ),
                # Rankings
                secao("Rankings de Vendas", CORES["destaque4"]),
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "24px",
                        "marginBottom": "36px",
                    },
                    children=[
                        card_grafico("grafico-marcas", "460px"),
                        card_grafico("grafico-produtos", "460px"),
                    ],
                ),
                # Vendas e preço
                secao("Relações de Preço, Desconto e Vendas", CORES["destaque3"]),
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "24px",
                        "marginBottom": "36px",
                    },
                    children=[
                        card_grafico("grafico-preco-faixa"),
                        card_grafico("grafico-scatter"),
                    ],
                ),
                # Análises avançadas
                secao("Análises Detalhadas", CORES["azul"]),
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "24px",
                        "marginBottom": "36px",
                    },
                    children=[
                        card_grafico("grafico-correlacao"),
                        card_grafico("grafico-regressao"),
                    ],
                ),
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "24px",
                        "marginBottom": "36px",
                    },
                    children=[
                        card_grafico("grafico-box-nota"),
                        card_grafico("grafico-materiais", "430px"),
                    ],
                ),
                # Observação metodológica
                html.Div(
                    style={
                        "backgroundColor": CORES["card"],
                        "borderRadius": "18px",
                        "border": f"1px solid {CORES['card_borda']}",
                        "padding": "22px",
                        "marginTop": "10px",
                        "color": CORES["texto_secundario"],
                        "fontSize": "13px",
                    },
                    children=[
                        html.Strong(
                            "Nota metodológica: ", style={"color": CORES["texto"]}
                        ),
                        "a coluna Qtd_Vendidos representa faixas textuais de venda. Por isso, Vendas_Num e Receita_Estimada são aproximações úteis para análise exploratória, não valores financeiros oficiais.",
                    ],
                ),
                # Rodapé
                html.Div(
                    style={
                        "textAlign": "center",
                        "padding": "32px 0 16px",
                        "borderTop": f"1px solid {CORES['card_borda']}",
                        "marginTop": "28px",
                    },
                    children=[
                        html.P(
                            "Dashboard desenvolvido com Dash & Plotly · Projeto de Ciência de Dados · 2026",
                            style={
                                "color": CORES["texto_secundario"],
                                "fontSize": "13px",
                                "margin": "0",
                            },
                        )
                    ],
                ),
            ],
        ),
    ],
)

# ==============================================================================
# 7. CALLBACKS
# ===============================================================================


@app.callback(
    [
        Output("kpi-container", "children"),
        Output("grafico-precos", "figure"),
        Output("grafico-notas", "figure"),
        Output("grafico-genero", "figure"),
        Output("grafico-temporada", "figure"),
        Output("grafico-marcas", "figure"),
        Output("grafico-produtos", "figure"),
        Output("grafico-preco-faixa", "figure"),
        Output("grafico-scatter", "figure"),
        Output("grafico-correlacao", "figure"),
        Output("grafico-regressao", "figure"),
        Output("grafico-box-nota", "figure"),
        Output("grafico-materiais", "figure"),
    ],
    [
        Input("filtro-genero", "value"),
        Input("filtro-temporada", "value"),
        Input("filtro-marca", "value"),
    ],
)
def atualizar_dashboard(generos, temporadas, marcas):
    dff = df.copy()

    if generos:
        dff = dff[dff["Genero_Agrupado"].isin(generos)]
    if temporadas:
        dff = dff[dff["Temporada_Agrupada"].isin(temporadas)]
    if marcas:
        dff = dff[dff["Marca"].isin(marcas)]

    total_produtos = len(dff)
    total_vendas = dff["Vendas_Num"].sum()
    receita_estimada = dff["Receita_Estimada"].sum()
    preco_medio = dff["Preço"].mean()
    nota_media = dff["Nota"].mean()
    desconto_medio = dff["Desconto"].mean()

    kpis = [
        criar_kpi("Produtos", formatar_numero(total_produtos), CORES["destaque1"]),
        criar_kpi(
            "Vendas Estimadas",
            formatar_numero(total_vendas),
            CORES["destaque2"],
            "baseado nas faixas do dataset",
        ),
        criar_kpi(
            "Receita Estimada",
            formatar_moeda(receita_estimada),
            CORES["destaque3"],
            "preço × vendas estimadas",
        ),
        criar_kpi("Preço Médio", formatar_moeda(preco_medio), CORES["destaque4"]),
        criar_kpi(
            "Nota Média",
            f"{nota_media:.2f}" if pd.notna(nota_media) else "0",
            CORES["azul"],
        ),
        criar_kpi(
            "Desconto Médio",
            f"{desconto_medio:.1f}%" if pd.notna(desconto_medio) else "0%",
            CORES["vermelho"],
        ),
    ]

    return (
        kpis,
        grafico_distribuicao_precos(dff),
        grafico_distribuicao_notas(dff),
        grafico_genero(dff),
        grafico_temporada(dff),
        grafico_marcas_vendas(dff),
        grafico_top_produtos(dff),
        grafico_preco_por_faixa_vendas(dff),
        grafico_scatter_preco_vendas(dff),
        grafico_correlacao(dff),
        grafico_regressao_desconto_vendas(dff),
        grafico_box_nota_genero(dff),
        grafico_materiais(dff),
    )


# ==============================================================================
# 8. EXECUÇÃO
# ===============================================================================

if __name__ == "__main__":
    porta = int(os.getenv("PORT", "8050"))
    modo_debug = os.getenv("DASH_DEBUG", "true").lower() == "true"

    print("\nDashboard iniciando...")
    print(f"Acesse: http://127.0.0.1:{porta}")
    print("Pressione Ctrl+C para encerrar\n")
    app.run(host="0.0.0.0", port=porta, debug=modo_debug)
