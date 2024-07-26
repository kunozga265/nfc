import os

import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
# import matplotlib.pyplot as plt

app = DjangoDash('SimpleExample')  # replaces dash.Dash

app.layout = html.Div([
    dcc.RadioItems(
        id='dropdown-color',
        options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
        value='red'
    ),
    html.Div(id='output-color'),
    dcc.RadioItems(
        id='dropdown-size',
        options=[{'label': i,
                  'value': j} for i, j in [('L', 'large'), ('M', 'medium'), ('S', 'small')]],
        value='medium'
    ),
    html.Div(id='output-size')

])


@app.callback(
    dash.dependencies.Output('output-color', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value')])
def callback_color(dropdown_value):
    return "The selected color is %s." % dropdown_value


@app.callback(
    dash.dependencies.Output('output-size', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value'),
     dash.dependencies.Input('dropdown-size', 'value')])
def callback_size(dropdown_color, dropdown_size):
    return "The chosen T-shirt is a %s %s one." % (dropdown_size,
                                                   dropdown_color)


# Main Graph
# NFC data
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "REGISTERED FARM HOUSEHOLDS.xlsx")
# file_path = "https://card.droluanar.com/uploads/nfc-data.xlsx"
print(file_path)
df = pd.read_excel(file_path)

# Data transformation
# df['Date'] = pd.to_datetime(df['Date'])

# Plots/Visuals

# Plot 1: Actual vs Target Cumulative Numbers
fig1 = go.Figure()

fig1.add_trace(go.Bar(
    x=df['Date'],
    y=df['Actual_Cumulative'],
    name='Actual Cumulative',
    marker_color='green'
))

fig1.add_trace(go.Bar(
    x=df['Date'],
    y=df['Target_Cumulative'],
    name='Target Cumulative',
    marker_color='gray'
))

# Layout
fig1.update_layout(
    title='NUMBER OF REGISTERED FARM HOUSEHOLDS BY JULY 22, 2024',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Cumulative Numbers (Millions)'),
    barmode='group',
    legend=dict(title='Legend')
)

# Annotations
for i in range(len(df)):
    fig1.add_annotation(
        x=df['Date'][i],
        y=df['Actual_Cumulative'][i],
        text=f"{df['Actual_Cumulative'][i]:,}",
        showarrow=False,
        yshift=10
    )
    fig1.add_annotation(
        x=df['Date'][i],
        y=df['Target_Cumulative'][i],
        text=f"{df['Target_Cumulative'][i]:,}",
        showarrow=False,
        yshift=-10
    )

    mainGraph = DjangoDash('MainGraph')  # replaces dash.Dash

    mainGraph.layout = html.Div([
        # html.Div(children='My First App with Data and a Graph'),
        dcc.Graph(figure=fig1,style={'width': '100%', 'height': '350px'})
    ])



# Plot 2: Registered Farm Households at ADD Level

# Sorting data
sorted_df = df.sort_values(by='Registered Farm Households')

# bar plot
fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=sorted_df['Registered Farm Households'],
    y=sorted_df['ADD'],
    orientation='h',
    marker_color='lightgreen'
))

for i in range(len(sorted_df)):
    fig2.add_annotation(
        x=sorted_df['Registered Farm Households'][i],
        y=sorted_df['ADD'][i],
        text=f"{sorted_df['Registered Farm Households'][i]:,}",
        showarrow=False,
        xanchor='left',
        yanchor='middle'
    )

# Top 4 ADDs
top_4_bars = sorted_df[-4:]
x_min = 0
x_max = top_4_bars['Registered Farm Households'].max()
y_min = top_4_bars.iloc[0]['ADD']
y_max = top_4_bars.iloc[-1]['ADD']

fig2.add_shape(
    type="rect",
    x0=x_min, y0=y_min, x1=x_max, y1=y_max,
    line=dict(color="red", width=2),
)

# Layout
fig2.update_layout(
    title='Number of Registered Farm Households at ADD Level',
    xaxis=dict(title='Number of Registered Farm Households'),
    yaxis=dict(title='ADD')
)

householdGraph = DjangoDash('HouseholdGraph')  # replaces dash.Dash

householdGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig2, style={'width': '100%', 'height': '350px'})
])

# Plot 3
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "REGISTERED FARM HOUSEHOLDS.xlsx")
# file_path = "https://card.droluanar.com/uploads/nfc-data.xlsx"
print(file_path)
df = pd.read_excel(file_path)

# Extract relevant columns for comparison
comparison_data = df[['District.1', 'Mean1 (Ha)', 'Mean2 (Ha)']]
comparison_data.columns = ['District', 'Mean1 (Ha)', 'Mean2 (Ha)']

# Calculate percentage differences
comparison_data['Percentage Difference (%)'] = ((comparison_data['Mean1 (Ha)'] - comparison_data['Mean2 (Ha)']) / comparison_data['Mean2 (Ha)']) * 100

# Plotting the comparison bar chart using Plotly
fig3 = go.Figure(data=[
    go.Bar(name='Mean1 (Ha)', x=comparison_data['District'], y=comparison_data['Mean1 (Ha)'], marker_color='orange'),
    go.Bar(name='Mean2 (Ha)', x=comparison_data['District'], y=comparison_data['Mean2 (Ha)'], marker_color='red')
])

fig3.update_layout(
    title='Comparison of Mean Land Holding Sizes Reported and Collected via GPS',
    xaxis_title='District',
    yaxis_title='Mean Land Holding Size (Ha)',
    barmode='group'
)

# Show the figure

districtGraph = DjangoDash('DistrictGraph')  # replaces dash.Dash

districtGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig3, style={'width': '100%', 'height': '350px'})
])

# Plotting the percentage differences using Plotly
fig4 = px.bar(comparison_data, x='District', y='Percentage Difference (%)',
              title='Percentage Differences in Mean Land Holding Sizes between Household Reported and GPS Collected Data',
              labels={'Percentage Difference (%)': 'Percentage Difference (%)'},
              color='Percentage Difference (%)', color_continuous_scale='Viridis')

fig4.update_layout(
    xaxis_title='District',
    yaxis_title='Percentage Difference (%)',
    coloraxis_colorbar=dict(title="Percentage Difference (%)")
)

# Show the figure
districtDifferenceGraph = DjangoDash('DistrictDifferenceGraph')  # replaces dash.Dash

districtDifferenceGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig4, style={'width': '100%', 'height': '350px'})
])


