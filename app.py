import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import random

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=["/assets/dark-theme.css"])
app.title = "Farmer's Financial Dashboard"
server = app.server

# Sample Data Generation
farms = ['Farm 1', 'Farm 2', 'Farm 3']
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

data = {
    "Farm": [],
    "Month": [],
    "Income": [],
    "Expense": [],
    "Seeds": [],
    "Labor": [],
    "Machinery": []
}

for farm in farms:
    for month in months:
        income = random.randint(5000, 15000)
        expense = random.randint(3000, 12000)
        seeds = expense * 0.3
        labor = expense * 0.4
        machinery = expense * 0.3
        
        data["Farm"].append(farm)
        data["Month"].append(month)
        data["Income"].append(income)
        data["Expense"].append(expense)
        data["Seeds"].append(seeds)
        data["Labor"].append(labor)
        data["Machinery"].append(machinery)

# Create DataFrame
df = pd.DataFrame(data)

# Layout
app.layout = html.Div([
    html.H1("Farmer's Financial Dashboard", style={'textAlign': 'center'}),
    
    # Dropdown to select farm
    html.Label("Select a Farm:"),
    dcc.Dropdown(
        id='farm-selector',
        options=[{'label': farm, 'value': farm} for farm in farms],
        value='Farm 1'
    ),
    
    # Income vs Expense Bar Chart
    dcc.Graph(id='income-expense-bar'),
    
    # Expense Distribution Pie Chart
    dcc.Graph(id='expense-distribution'),
    
    # Data Table
    html.H3("Monthly Financial Summary"),
    html.Div(id='data-table')
], className="dark-theme")

# Callbacks
@app.callback(
    [Output('income-expense-bar', 'figure'),
     Output('expense-distribution', 'figure'),
     Output('data-table', 'children')],
    [Input('farm-selector', 'value')]
)
def update_dashboard(selected_farm):
    filtered_df = df[df['Farm'] == selected_farm]
    
    # Bar Chart for Income vs Expenses
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=filtered_df['Month'], y=filtered_df['Income'], name='Income', marker_color='#90EE90'))
    bar_fig.add_trace(go.Bar(x=filtered_df['Month'], y=filtered_df['Expense'], name='Expense', marker_color='#FFB347'))
    bar_fig.update_layout(title="Monthly Income vs Expenses", barmode='group')
    
    # Pie Chart for Expense Breakdown
    avg_seeds = filtered_df['Seeds'].mean()
    avg_labor = filtered_df['Labor'].mean()
    avg_machinery = filtered_df['Machinery'].mean()
    
    pie_fig = go.Figure()
    pie_fig.add_trace(go.Pie(labels=['Seeds', 'Labor', 'Machinery'],
                              values=[avg_seeds, avg_labor, avg_machinery],
                              hole=0.4))
    pie_fig.update_layout(title="Average Expense Distribution")
    
    # Data Table
    table_html = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in ['Month', 'Income', 'Expense']]))] +
        [html.Tr([html.Td(filtered_df.iloc[i][col]) for col in ['Month', 'Income', 'Expense']])
         for i in range(len(filtered_df))]
    )
    
    return bar_fig, pie_fig, table_html

if __name__ == '__main__':
    app.run_server(debug=True)
