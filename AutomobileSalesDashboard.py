import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Initialize app layout
app.layout = html.Div([
    # App name
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center'}),

    # Division for selecting yearly statistics or recession period statistics drop down 
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            placeholder='Select a report type' #Temp untill year is selected
        )
    ]),

    # Division for selecting the year of statistics to view
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in range(1980, 2024)], #All years we have data for
            placeholder='Select a year' #Temp untill year is selected
        ),
    ]),

    # Division for output style to be in a 2X2 format
    html.Div(id='output-container', className='chart-grid', style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'space-around', 
        'gap': '20px'  
    })
])

# Callback to make dashboard interactive and chose which data to display
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics' #Returns false if recession statistics are chosen

# Callback to generate graphs according to user input changes
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Line chart for average automobile sales during recession periods
        # Filter to average automobile sales during recession periods
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
                figure=px.line(
                    yearly_rec, 
                    x='Year', 
                    y='Automobile_Sales', 
                    title="Average Automobile Sales fluctuation over Recession Period"
                )
            )

        # Plot 2: Bar chart for average vehicles sold by vehicle type during recession periods
        # Filter data for sales during recession by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
                figure=px.bar(
                    average_sales, 
                    x='Vehicle_Type', 
                    y='Automobile_Sales', 
                    title="Average Number of Vehicles Sold By Vehicle Type"
                )
            )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        # Filter data to advertising expenditure by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
                figure=px.pie(
                    exp_rec, 
                    values='Advertising_Expenditure', 
                    names='Vehicle_Type', 
                    title='Advertising Expenditure by Vehicle Type'
                )
            )

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales during recession
        # Filter data to combine unemployment rates and vehicle types and average their sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'], as_index=False)['Automobile_Sales'].mean()
        R_chart4 = dcc.Graph(
                figure=px.bar(
                    unemp_data, 
                    x='unemployment_rate', 
                    y='Automobile_Sales', 
                    color='Vehicle_Type', 
                    title='Effect of Unemployment Rate on Vehicle Type and Sales'
                )
            )
        # Retrun all charts for display
        return [
            html.Div([R_chart1, R_chart2], style={'flex': '0 0 48%', 'marginBottom': '20px'}),  # First row with 2 charts
            html.Div([R_chart3, R_chart4], style={'flex': '0 0 48%'})  # Second row 2 charts
        ]
    
    # If user wants data for a selected year
    elif selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year] #Data filtered for a certain year 

        # Plot 1: Line chart for yearly automobile sales
        # Filter data to group average automobile sales for a selected year 
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas, 
                x='Year', 
                y='Automobile_Sales', 
                title='Automobile Sales'
                )
            )

        # Plot 2: Line chart for total monthly automobile sales
        # filter data to total sales for a month
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
                figure=px.line(
                    mas, 
                    x='Month', 
                    y='Automobile_Sales', 
                    title='Total Monthly Automobile Sales'
                )
            )

        # Plot 3: Bar chart for average number of vehicles sold by vehicle type in the given year
        # Filter data for sales by year and vehicle type
        avr_vdata = yearly_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
                figure=px.bar(
                    avr_vdata, 
                    x='Vehicle_Type', 
                    y='Automobile_Sales', 
                    title=f'Average Vehicles Sold by Vehicle Type in the year {input_year}'
                    )
                )

        # Plot 4: Pie chart for total advertisement expenditure by vehicle type
        # Filter data to years advertising expediture by vehicle
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data, 
                values='Advertising_Expenditure', 
                names='Vehicle_Type', 
                title='Advertising Expenditure by Vehicle Type'
                )
            )

        # Retrun all charts for display
        return [
            html.Div([Y_chart1, Y_chart2], style={'flex': '0 0 48%', 'marginBottom': '20px'}),  # First row (2 charts)
            html.Div([Y_chart3, Y_chart4], style={'flex': '0 0 48%'})  # Second row (2 charts)
        ]
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
