from dash import html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

def generate_top5_chart(df):
    top_df = df.sort_values("% выполнения", ascending=False).head(5)
    fig = px.bar(top_df, x="Участник", y="% выполнения", color="Группа",
                 title="Топ-5 участников по выполнению плана", height=500, width=1400)
    return dcc.Graph(figure=fig)


def generate_heatmap(df: pd.DataFrame):
    # Пример: у участников есть столбец "Регион"
    heat_df = df.groupby("Регион").agg({"% выполнения": "mean"}).reset_index()

    fig = px.density_heatmap(
        heat_df,
        x="Регион",
        y="% выполнения",
        z="% выполнения",
        color_continuous_scale="RdYlGn",
        title="Средний процент выполнения по регионам",
        height=750,
        width=750,
    )

    fig.update_layout(
        margin=dict(t=60, b=100),
        coloraxis_colorbar=dict(title="% выполнения"),
        uniformtext_minsize=10,
    )

    return dcc.Graph(figure=fig)


def generate_product_bar(df: pd.DataFrame):
    # Добавим цветовую категорию
    def get_color(proc):
        if proc >= 90:
            return "Зелёный"
        elif proc < 50:
            return "Красный"
        else:
            return "Жёлтый"

    df["Цвет"] = df["% выполнения"].apply(get_color)

    fig = px.bar(
        df,
        x="Участник",
        y="% выполнения",
        color="Цвет",
        color_discrete_map={
            "Зелёный": "green",
            "Жёлтый": "gold",
            "Красный": "red"
        },
        facet_col="Группа",
        title="Выполнение плана по участникам и группам",
        height=900
    )

    return dcc.Graph(figure=fig)

def generate_layout_groups(df: pd.DataFrame):
    fig = px.bar(df, x="Участник", y="% выполнения", color="Группа", barmode="group", title="Выполнение плана по участникам", height=800)

    return dcc.Graph(figure=fig)


def generate_group_share_pie(df):
    group_sum = df.groupby("Группа")["План"].sum().reset_index()
    fig = px.pie(group_sum, names="Группа", values="План", title="Доля групп в общем плане")
    return dcc.Graph(figure=fig)

def generate_efficiency_scatter(df):
    group_info = df.groupby("Группа").agg({
        "% выполнения": "mean",
        "Участник": "count"
    }).rename(columns={"Участник": "Количество участников"}).reset_index()

    fig = px.scatter(group_info, x="Количество участников", y="% выполнения", color="Группа",
                     size="% выполнения", title="Эффективность групп: % выполнения vs кол-во участников")
    return dcc.Graph(figure=fig)

def generate_completion_vs_score(df):
    fig = px.scatter(
        df,
        x="% выполнения (общий)",
        y="Балл за группу",
        size="Кол-во выполненных разделов",
        color="Группа",
        hover_name="Группа",
        title="Зависимость между выполнением и начисленными баллами",
        height=600
    )
    return dcc.Graph(figure=fig)

# def generate_member_plan_fact(df):
#     melted = df.melt(id_vars=["Участник", "Группа"], value_vars=["План", "Факт"], var_name="Тип", value_name="Сумма")
#     fig = px.bar(
#         melted,
#         x="Участник",
#         y="Сумма",
#         color="Тип",
#         barmode="group",
#         facet_col="Группа",
#         title="Сравнение план/факт по участникам",
#         height=700
#     )
#     return dcc.Graph(figure=fig)

def generate_single_member_plan_fact(df, member_name):
    # Фильтрация данных по имени участника
    filtered_df = df[df["Участник"] == member_name]

    # Проверка: найден ли участник
    if filtered_df.empty:
        return dcc.Markdown(f"**Участник '{member_name}' не найден в данных.**")

    # Подготовка данных в формат long-form
    melted = filtered_df.melt(
        id_vars=["Участник", "Группа"],
        value_vars=["План", "Факт"],
        var_name="Тип",
        value_name="Сумма"
    )

    # Построение графика
    fig = px.bar(
        melted,
        x="Тип",  # только "План" и "Факт"
        y="Сумма",
        color="Тип",
        barmode="group",
        title=f"Сравнение план/факт: {member_name}",
        height=500,
        width=550,
        text_auto=True
    )

    fig.update_layout(
        margin=dict(t=50, b=100),
        xaxis_title="Тип значения",
        yaxis_title="Сумма (₽)",
        # showlegend=False
    )

    return dcc.Graph(figure=fig)


def generate_plan_fact_by_group(df):
    agg_df = df.groupby("Группа")[["План", "Факт"]].sum().reset_index()
    df_melt = agg_df.melt(id_vars="Группа", value_vars=["План", "Факт"], var_name="Тип", value_name="Сумма")

    fig = px.bar(df_melt, x="Группа", y="Сумма", color="Тип", barmode="group",
                 title="Сравнение суммы плана и факта по группам", height=600)
    return dcc.Graph(figure=fig)

def generate_group_completion_pie(df):
    completed = df[df["% выполнения"] >= 100].groupby("Группа").size()
    all_groups = df.groupby("Группа").size()
    completion_rate = (completed / all_groups).fillna(0).reset_index()
    completion_rate.columns = ["Группа", "Доля завершенных"]

    fig = px.pie(
        completion_rate,
        names="Группа",
        values="Доля завершенных",
        title="Доля полностью завершенных участников по группам"
    )
    return dcc.Graph(figure=fig)


def generate_layout(df: pd.DataFrame):
    fig = px.bar(df, x="Участник", y="% выполнения", color="Группа", barmode="group", title="Выполнение плана по участникам")
        
    return html.Div(id='graph_layout',children=[
        html.H2("Дашборд выполнения плана продаж по группам"),
        generate_layout_groups(df),
        html.Hr(),
        html.H2("Аналитика выполнения плана продаж"),
        generate_product_bar(df),
        html.Hr(),
        html.H3("Региональная карта выполнения"),
        generate_heatmap(df),
        html.Hr(),
        html.H3("Топ-5 участников по выполнению"),
        generate_top5_chart(df),
        html.Hr(),
        html.H3("Сравнение планов и факта по группам"),
        generate_plan_fact_by_group(df),
        html.Hr(),
        html.H3("Доля группы в общем плане"),
        generate_group_share_pie(df),
        html.Hr(),
        html.H3("Связь между выполнением и количеством участников"),
        generate_efficiency_scatter(df),
        html.Hr(),
        html.H3("% выполнения vs Балл за группу"),
        generate_completion_vs_score(df),
        dbc.Row([
            dbc.Row([
                html.H3("Сравнение план/факт по определенному участнику"),
                dbc.Col([
                    html.Hr(),
                    generate_single_member_plan_fact(df, "Kaspersky (только B2B)"),
                ]),
                dbc.Col([
                    html.Hr(),
                    generate_single_member_plan_fact(df, "ГК «Астра» (без учета Tantor SE 1C)"),
                ]),
                dbc.Col([
                    html.Hr(),
                    generate_single_member_plan_fact(df, "Ideco"),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Hr(),
                    generate_single_member_plan_fact(df, "РедСофт"),
                ]),
                dbc.Col([
                    html.Hr(),
                    generate_single_member_plan_fact(df, "Dr.Web"),
                ]),
                dbc.Col([
                    html.Hr(),
                    generate_single_member_plan_fact(df, "МойОфис"),
                ]),
            ]),
            html.Hr(),
            html.H3("Кольцевая диаграмма долей выполненных групп"),
            generate_group_completion_pie(df),
        ])

    ])
