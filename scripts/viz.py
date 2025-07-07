import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Ensure output directory exists
os.makedirs("../outputs", exist_ok=True)

# Load datasets
flow_df = pd.read_csv("../data/supply_chain_flow.csv")
sales_df = pd.read_csv("../data/sales_by_channel.csv")

# Color palette (original corporate palette you liked)
colors = {
    'Supplier A': '#264653',
    'Supplier B': '#2A9D8F',
    'Supplier C': '#E76F51',
    'Electronics': '#F4A261',
    'Clothing': '#E9C46A',
    'Food': '#A8DADC',
    'Online': '#457B9D',
    'Retail Store': '#1D3557'
}

# Build nodes and assign colors
nodes = pd.concat([flow_df["source"], flow_df["target"]]).unique().tolist()
node_colors = [colors.get(node, '#999999') for node in nodes]

# Sankey diagram
sankey = go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes,
        color=node_colors
    ),
    link=dict(
        source=flow_df["source"].map({name: idx for idx, name in enumerate(nodes)}),
        target=flow_df["target"].map({name: idx for idx, name in enumerate(nodes)}),
        value=flow_df["value"],
        color=[colors.get(src, '#999999') for src in flow_df["source"]],
        hovertemplate="%{source.label} → %{target.label}: %{value} units<extra></extra>"
    )
)

# Highlight max sales in table
max_sales = sales_df["Total Sales"].max()
highlight_colors = [
    ['#FFE5D9' if val == max_sales else '#F5F6F5' for val in sales_df["Total Sales"]]
]

# Table
table = go.Table(
    header=dict(
        values=["<b>Channel</b>", "<b>Category</b>", "<b>Total Sales</b>", "<b>Period</b>"],
        fill_color='#264653',
        font=dict(color="white", size=12),
        align="left"
    ),
    cells=dict(
        values=[
            sales_df["Channel"],
            sales_df["Category"],
            sales_df["Total Sales"],
            sales_df["Period"]
        ],
        fill_color=['#F5F6F5', '#F5F6F5', highlight_colors[0], '#F5F6F5'],
        font=dict(color='#333333', size=11),
        align="left"
    )
)

# Layout
fig = make_subplots(
    rows=2, cols=1,
    specs=[[{'type': 'sankey'}], [{'type': 'table'}]],
    subplot_titles=[
        "<b>Supply Chain Flow</b>",
        "<b>Sales by Channel and Category</b>"
    ],
    vertical_spacing=0.12
)

fig.add_trace(sankey, row=1, col=1)
fig.add_trace(table, row=2, col=1)

fig.update_layout(
    title_text="<b>Supply Chain Dashboard – Q1 2025</b><br><span style='font-size:14px;'>This dashboard tracks product flow from suppliers to sales channels in Q1 2025.</span>",
    title_font=dict(size=24, color='#1A1A1A', family='Arial, sans-serif'),
    font=dict(family='Arial, sans-serif', color='#333333'),
    paper_bgcolor='#FFFFFF',
    height=850,
    margin=dict(l=30, r=30, t=120, b=30)
)

# Export to HTML
fig.write_html("../outputs/golden_image.html")
print("✅ Dashboard saved to: outputs/golden_image.html")
