import pandas as pd
import numpy as np
import os

# Ensure data directory exists at project root level
output_path = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(output_path, exist_ok=True)

# Define nodes for Sankey: suppliers → categories → channels
suppliers = ['Supplier A', 'Supplier B', 'Supplier C']
categories = ['Electronics', 'Clothing', 'Food']
channels = ['Online', 'Retail Store']

# Seed for reproducibility
np.random.seed(42)

# Phase 1: Generate flows from suppliers to categories
data_flow = []

for supplier in suppliers:
    for category in categories:
        if supplier == 'Supplier A' and category == 'Electronics':
            volume = np.random.randint(200, 300)
        elif supplier == 'Supplier C' and category == 'Food':
            volume = np.random.randint(150, 250)
        else:
            volume = np.random.randint(50, 150)
        data_flow.append({
            'source': supplier,
            'target': category,
            'value': volume,
            'period': 'Q1-2025'
        })

# Convert to DataFrame to calculate totals
flow_df = pd.DataFrame(data_flow)
category_totals = flow_df.groupby('target')['value'].sum()

# Phase 2: Generate flows from categories to channels with adjusted proportions
for category in categories:
    total = category_totals[category]
    if category == 'Electronics':
        proportions = {'Online': 0.7, 'Retail Store': 0.3}
    elif category == 'Clothing':
        proportions = {'Online': 0.35, 'Retail Store': 0.65}
    elif category == 'Food':
        proportions = {'Online': 0.45, 'Retail Store': 0.55}
    for channel in channels:
        volume = int(total * proportions[channel])
        data_flow.append({
            'source': category,
            'target': channel,
            'value': volume,
            'period': 'Q1-2025'
        })

# Export updated flow data
flow_df = pd.DataFrame(data_flow)
flow_df.to_csv(os.path.join(output_path, "supply_chain_flow.csv"), index=False)

# Phase 3: Generate complementary sales summary by channel and category
sales_data = {
    'Channel': [],
    'Category': [],
    'Total Sales': [],
    'Period': []
}
for channel in channels:
    for category in categories:
        sales = flow_df[
            (flow_df['source'] == category) & (flow_df['target'] == channel)
        ]['value'].sum()
        sales_data['Channel'].append(channel)
        sales_data['Category'].append(category)
        sales_data['Total Sales'].append(sales)
        sales_data['Period'].append('Q1-2025')

sales_df = pd.DataFrame(sales_data)
sales_df.to_csv(os.path.join(output_path, "sales_by_channel.csv"), index=False)

# Validation: check consistency between category inputs and outputs
category_inputs = flow_df[flow_df['target'].isin(categories)].groupby('target')['value'].sum()
category_outputs = flow_df[flow_df['source'].isin(categories)].groupby('source')['value'].sum()

print("=== Sankey Flow Validation ===")
print("Inbound volumes per category:\n", category_inputs)
print("Outbound volumes per category:\n", category_outputs)

if category_inputs.equals(category_outputs):
    print("✅ Flow is consistent: input = output for all categories.")
else:
    print("⚠️ Flow inconsistency detected: input ≠ output.")

print("✅ Files generated successfully:")
print("- data/supply_chain_flow.csv")
print("- data/sales_by_channel.csv")
