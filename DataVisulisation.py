import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            placeholder='Select a report type'
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in range(1980, 2024)],
            placeholder='Select a year'
        ),
    ]),
    html.Div(id='output-container', className='chart-grid', style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'space-around',  # Makes sure the charts are evenly distributed
        'gap': '20px'  # Adds space between the charts
    })
])

@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Line chart for average automobile sales during recession periods
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales fluctuation over Recession Period"))

        # Plot 2: Bar chart for average vehicles sold by vehicle type during recession periods
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Number of Vehicles Sold By Vehicle Type"))

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(id='advertising-expenditure-pie', figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title='Advertising Expenditure by Vehicle Type'))

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales during recession
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'], as_index=False)['Automobile_Sales'].mean()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type', title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div([R_chart1, R_chart2], style={'flex': '0 0 48%', 'marginBottom': '20px'}),  # First row (2 charts)
            html.Div([R_chart3, R_chart4], style={'flex': '0 0 48%'})  # Second row (2 charts)
        ]
    elif selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Line chart for yearly automobile sales
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title='Automobile Sales'))

        # Plot 2: Line chart for total monthly automobile sales
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales'))

        # Plot 3: Bar chart for average number of vehicles sold by vehicle type in the given year
        avr_vdata = yearly_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title=f'Average Vehicles Sold by Vehicle Type in the year {input_year}'))

        # Plot 4: Pie chart for total advertisement expenditure by vehicle type
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title='Advertising Expenditure by Vehicle Type'))

        return [
            html.Div([Y_chart1, Y_chart2], style={'flex': '0 0 48%', 'marginBottom': '20px'}),  # First row (2 charts)
            html.Div([Y_chart3, Y_chart4], style={'flex': '0 0 48%'})  # Second row (2 charts)
        ]
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
