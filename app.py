import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output

# 1. 读取 Excel
df = pd.read_excel("Workbook1.xlsx", sheet_name=0)

# 2. 定义指标
metrics = ["企业法人单位", "从业人员数量", "资产", "营收", "负债", "R&D经费支出", "R&D经费与营业收入之比"]

# 3. 启动 Dash 应用
app = Dash(__name__)

app.layout = html.Div([
    html.H1("纺织产业数据 Dashboard", style={"textAlign": "center"}),

    # 下拉选择指标
    dcc.Dropdown(
        id="metric_selector",
        options=[{"label": m, "value": m} for m in metrics],
        value="资产",
        clearable=False
    ),

    # 柱状图
    dcc.Graph(id="bar_chart"),

    # 饼状图
    dcc.Graph(id="pie_chart"),

    # 折线图
    dcc.Graph(id="line_chart"),

    # 表格
    dash_table.DataTable(
        id="data_table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        page_size=10
    )
])

# 4. 回调更新图表
@app.callback(
    [Output("bar_chart", "figure"),
     Output("pie_chart", "figure"),
     Output("line_chart", "figure")],
    [Input("metric_selector", "value")]
)
def update_charts(metric):
    # 柱状图
    bar_fig = px.bar(df, x="省份", y=metric, color="行业", barmode="group")

    # 饼图（按行业汇总）
    pie_fig = px.pie(df, names="行业", values=metric, title=f"{metric} 行业占比")

    # 折线图（用省份排序代替时间序列）
    line_fig = px.line(df, x="省份", y=metric, color="行业", markers=True)

    return bar_fig, pie_fig, line_fig

if __name__ == "__main__":
    app.run(debug=True)
