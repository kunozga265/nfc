import os

import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
import numpy as np
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
# file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "REGISTERED FARM HOUSEHOLDS.xlsx")
file_path = "https://card.droluanar.com/uploads/nfc-data.xlsx"
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
        dcc.Graph(figure=fig1,style={'width': '100%', 'height': '500px'})
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
    dcc.Graph(figure=fig2, style={'width': '100%', 'height': '500px'})
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
    dcc.Graph(figure=fig3, style={'width': '100%', 'height': '500px'})
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
    dcc.Graph(figure=fig4, style={'width': '100%', 'height': '500px'})
])


# Plot 5

# Data
completed_blocks_percent = [66.45, 65.78,75.5, 69.50, 85.30, 82.26, 93.75, 77.68, 74.29, 58.53, 81.71, 64.31]

# average percentage
average_percent = np.mean(completed_blocks_percent)

# donut plot
labels = ['Completed', 'Remaining']
sizes = [average_percent, 100 - average_percent]
colors = ['green', 'lightgray']


fig5 = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.7, marker_colors=colors, textinfo='percent+label', textfont_size=20)])


fig5.update_layout(
    title_text='National Percentage of Completed Blocks',
    annotations=[dict(text=f'{average_percent:.1f}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
)

# Show the figure
completedBlocksGraph = DjangoDash('CompletedBlocksGraph')  # replaces dash.Dash

completedBlocksGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig5, style={'width': '100%', 'height': '500px'})
])

# data_table.DataTable(df, include_index=False, num_rows_per_page=10)

# Show the figure
dataTableGraph = DjangoDash('DataTableGraph')  # replaces dash.Dash

dataTableGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dash_table.DataTable(data=df.to_dict('records'), page_count=10)
])

# Plot 6

# Plotting the percentage differences
fig6 = px.bar(comparison_data, x='District', y='Percentage Difference (%)',
              title='Percentage Differences in Mean Land Holding Sizes between Household Reported and GPS Collected Data',
              labels={'Percentage Difference (%)': 'Percentage Difference (%)'},
              color='Percentage Difference (%)', color_continuous_scale='Greys')

fig6.update_layout(
    xaxis_title='District',
    yaxis_title='Percentage Difference (%)',
    coloraxis_colorbar=dict(title="Percentage Difference (%)")
)

# Show the figure
meanLandDifferenceGraph = DjangoDash('MeanLandDifferenceGraph')  # replaces dash.Dash

meanLandDifferenceGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig6, style={'width': '100%', 'height': '500px'})
])

# Plot 7
# Data
labels = ['Customary', 'Freehold', 'Leasehold']
values = [78, 21, 1]
colors = ['green', 'grey', 'red']

# Create a donut chart
fig7 = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    textinfo='label+percent',
    insidetextorientation='radial',
    hole=0.7  # this creates the donut hole
)])

fig7.update_layout(
    title='Land Tenure Type by Percentage'
)

# Show the figure
landTenureDifferenceGraph = DjangoDash('LandTenureGraph')  # replaces dash.Dash

landTenureDifferenceGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig7, style={'width': '100%', 'height': '500px'})
])

# Plot 8
# Data
data = {
    "ADD": ["BLANTYRE ADD", "KARONGA ADD", "KASUNGU ADD", "LILONGWE ADD", "MACHINGA ADD", "MZUZU ADD", "SALIMA ADD", "SHIRE VALLEY ADD"],
    "Customary": [16.09, 13.01, 15.50, 14.00, 10.97, 13.29, 13.42, 10.56],
    "Land Certificate": [6.60, 8.49, 7.36, 8.49, 9.36, 9.18, 8.22, 8.03],
    "Lease": [0.59, 1.74, 0.96, 0.95, 0.65, 0.69, 0.58, 0.63],
    "None": [70.32, 64.17, 69.98, 69.26, 72.94, 71.32, 72.37, 75.04],
    "Other": [6.40, 12.60, 6.20, 7.30, 6.08, 5.52, 5.42, 5.74]
}

df = pd.DataFrame(data)

# Melt the DataFrame for plotting
df_melted = df.melt(id_vars="ADD", var_name="Ownership Type", value_name="Percentage")


fig8 = px.bar(df_melted, x='ADD', y='Percentage', color='Ownership Type', barmode='group',
             title='Percentage of Farmers with Ownership Documents by ADD',
             labels={'Percentage':'Percentage (%)', 'ADD':'Agricultural Development Division (ADD)'},
             color_discrete_map={
                 'Customary': 'grey',
                 'Land Certificate': 'green',
                 'Lease': 'orange',
                 'None': 'darkred',
                 'Other': 'black'
             })


# Show the figure
famersOwnershipGraph = DjangoDash('FarmersOwnershipGraph')  # replaces dash.Dash

famersOwnershipGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig8, style={'width': '100%', 'height': '500px'})
])

# Plot 9
# Data
data = {
    "ADD": ["BLANTYRE ADD", "KARONGA ADD", "KASUNGU ADD", "LILONGWE ADD", "MACHINGA ADD", "MZUZU ADD", "SALIMA ADD", "SHIRE VALLEY ADD"],
    "Irrigation Participants": [81394, 9986, 86012, 153165, 64808, 26586, 7456, 9034],
    "Percent": [25.4, 16.4, 35.0, 36.3, 19.8, 21.2, 10.5, 13.6]
}

df = pd.DataFrame(data)

df_sorted = df.sort_values(by='Percent', ascending=True)

fig9 = px.bar(df_sorted, y='ADD', x='Percent', text='Percent', title='Participation in Irrigation by ADD',
             labels={'Percent':'Percent (%)', 'ADD':'Agricultural Development Division (ADD)'}, orientation='h',
             color_discrete_sequence=['grey'])
fig9.update_traces(texttemplate='%{text}%', textposition='outside')
fig9.update_layout(xaxis=dict(range=[0, 40]), xaxis_title="Percentage (%)", yaxis_title="ADD")

# Show the figure
participationIrrigationGraph = DjangoDash('ParticipationIrrigationGraph')  # replaces dash.Dash

participationIrrigationGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig9, style={'width': '100%', 'height': '500px'})
])

# Plot 10
# Data
data = {
    "ADD": ["SHIRE VALLEY ADD", "SALIMA ADD", "MZUZU ADD", "MACHINGA ADD", "LILONGWE ADD", "KASUNGU ADD", "KARONGA ADD", "BLANTYRE ADD"],
    "Both Crop & Livestock (%)": [24, 33, 34, 23, 30, 35, 41, 23],
    "Crop only (%)": [75, 67, 66, 75, 69, 64, 57, 76]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Melt the DataFrame for plotting
df_melted = df.melt(id_vars="ADD", var_name="Type", value_name="Percentage")

# Plotting
fig10 = px.bar(df_melted, x='ADD', y='Percentage', color='Type', barmode='group',
             title='Agricultural Enterprises Practised by Registered Household (%)',
             labels={'Percentage':'Percentage (%)', 'ADD':'Agricultural Development Division (ADD)'},
             color_discrete_map={
                 'Both Crop & Livestock (%)': 'grey',
                 'Crop only (%)': 'green'
             })

# Show the figure
agriculturalEnterprisesGraph = DjangoDash('AgriculturalEnterprisesGraph')  # replaces dash.Dash

agriculturalEnterprisesGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig10, style={'width': '100%', 'height': '500px'})
])

# Plot 11
# Data
data = {
    "Crop": ["Macadamia", "Sunflower", "Sesema", "Cowpea", "Bean", "Soybean", "Pigeon peas", "Groundnut"],
    "Percentage": [0, 0.50, 0.60, 2.10, 7.10, 14.50, 21, 22.50]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Plotting
fig11 = px.bar(df, x='Percentage', y='Crop', orientation='h',
             title='Registered Farm Households Reporting Cultivating Legumes (%)',
             labels={'Percentage':'Percentage (%)', 'Crop':'Crop'},
             text='Percentage',
             color_discrete_sequence=['#1f77b4'])

fig11.update_traces(texttemplate='%{text}%', textposition='outside')
fig11.update_layout(xaxis=dict(range=[0, 25]), yaxis_title="Crop", xaxis_title="Percentage (%)")

# Show the figure
cultivatingLegumesGraph = DjangoDash('CultivatingLegumesGraph')  # replaces dash.Dash

cultivatingLegumesGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig11, style={'width': '100%', 'height': '500px'})
])

# Plot 12
# Fertilizer data
fertilizer_data = {
    "ADD": ["SHIRE VALLEY ADD", "SALIMA ADD", "MZUZU ADD", "MACHINGA ADD", "LILONGWE ADD", "KASUNGU ADD", "KARONGA ADD", "BLANTYRE ADD"],
    "Fertilizer Percentage": [13, 18, 17, 27, 26, 23, 9, 26]
}

# Manure data
manure_data = {
    "ADD": ["SHIRE VALLEY ADD", "SALIMA ADD", "MZUZU ADD", "MACHINGA ADD", "LILONGWE ADD", "KASUNGU ADD", "KARONGA ADD", "BLANTYRE ADD"],
    "Manure Percentage": [30, 64, 69, 56, 66, 67, 61, 60]
}

# Create DataFrames
df_fertilizer = pd.DataFrame(fertilizer_data)
df_manure = pd.DataFrame(manure_data)

# Merge DataFrames on ADD
df_combined = pd.merge(df_fertilizer, df_manure, on="ADD")

# Melt the DataFrame for plotting
df_melted = df_combined.melt(id_vars="ADD", var_name="Type", value_name="Percentage")

# Plotting
fig12 = px.bar(df_melted, x='ADD', y='Percentage', color='Type', barmode='group',
             title='Comparison of Fertilizer and Manure Use by ADD',
             labels={'Percentage':'Percentage (%)', 'ADD':'Agricultural Development Division (ADD)'},
             color_discrete_map={
                 'Fertilizer Percentage': 'grey',
                 'Manure Percentage': 'green'
             })

# Show the figure
manureUseGraph = DjangoDash('ManureUseGraph')  # replaces dash.Dash

manureUseGraph.layout = html.Div([
    # html.Div(children='My First App with Data and a Graph'),
    dcc.Graph(figure=fig12, style={'width': '100%', 'height': '500px'})
])