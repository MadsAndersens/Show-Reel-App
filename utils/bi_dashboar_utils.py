import streamlit as st
import pandas as pd
import json
import plotly.express as px

def get_data():
    df = pd.read_csv('data_files/Superstore.csv', encoding='ISO-8859-1')
    df['year'] = pd.to_datetime(df['Order Date']).dt.year
    return df

def load_json(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data

def apply_filters(data):
    #Apply filters
    if st.session_state['segment'] != 'All':
        data = data[data['Segment'] == st.session_state['segment']]

    if st.session_state['category'] != 'All':
        data = data[data['Category'] == st.session_state['category']]

    # Apply time filter
    data = data[(data['Order Year'] >= st.session_state['selected_range'][0]) &
                    (data['Order Year'] <= st.session_state['selected_range'][1])]

    return data
def get_map(df):
    state_code_map = load_json('data_files/state_code.json')
    df['Code'] = df['State'].map(state_code_map)

    df = apply_filters(df)

    if st.session_state['state'] == 'All':
        sub_df = df.groupby('Code')['Profit'].mean().reset_index()

        #Plot map
        fig = px.choropleth(sub_df,
                            locations='Code',
                            color='Profit',
                            color_continuous_scale='blues',
                            hover_name='Code',
                            locationmode='USA-states',
                            scope='usa')

        #Add title
        fig.update_layout(
            title={'text': 'Profit by state',
                   'xanchor': 'center',
                   'yanchor': 'top',
                   'x': 0.5})

        #Increase width
        fig.update_layout({'width': 800, 'height': 500})

        #Remove the legend
        fig.update_layout(showlegend=False)

    else:

        df = df[df['State'] == st.session_state['state']]
        st.write(df)

        # Plot map
        fig = px.scatter_mapbox(df,
                                locations = 'Postal Code',
                                color='Profit',
                                color_continuous_scale='blues',
                                hover_name='Code',
                                locationmode='USA-states',
                                scope='usa')

        # Add title
        fig.update_layout(
            title={'text': 'Profit by state',
                   'xanchor': 'center',
                   'yanchor': 'top',
                   'x': 0.5})

        # Increase width
        fig.update_layout({'width': 800, 'height': 500})

        # Remove the legend
        fig.update_layout(showlegend=False)

    return fig

def get_top_10_states(data, state = 'All'):

    #Apply filters
    data = apply_filters(data)

    #state has to be handled differently
    if state == 'All':
        #Top ten states based on profits
        sub_df = data.groupby('State')['Profit'].mean().reset_index()
        sub_df = sub_df.sort_values('Profit', ascending=True).tail(10)
        # vertical bar chart
        fig = px.bar(sub_df.reset_index(),
                     x='Profit',
                     y='State',
                     orientation='h',
                     text=sub_df['Profit'].round(2))

        # Customizing the text on the bars
        fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

        # Customizing the layout
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        #removing the axes
        fig.update_xaxes(showticklabels=False)

        #Remove the x and y axis headers
        fig.update_layout(xaxis_title='Top 10 states (avg. profit)', yaxis_title=None)

        # Increase width
        fig.update_layout({'width': 750, 'height': 500})

    else:
        #Top ten states based on profits
        sub_df = data[data['State'] == state]
        sub_df = sub_df.groupby('City')['Profit'].mean().reset_index()
        sub_df = sub_df.sort_values('Profit', ascending=True).tail(10)
        # vertical bar chart
        fig = px.bar(sub_df.reset_index(),
                     x='Profit',
                     y='City',
                     orientation='h',
                     text=sub_df['Profit'].round(2))

        # Customizing the text on the bars
        fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

        # Customizing the layout
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        #removing the axes
        fig.update_xaxes(showticklabels=False)

        #Remove the x and y axis headers
        fig.update_layout(xaxis_title='Top 10 cities (avg. profit)', yaxis_title=None)

        # Increase width
        fig.update_layout({'width': 750, 'height': 500})

    return fig

# Writing functions

def write_kpi_row(data):
    data = apply_filters(data)
    # Write KPI row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        sales = '$' + str("{:,}".format(int(data['Sales'].sum())))
        st.metric(label='Total Sales', value=sales)

    with col2:
        profit = '$' + str("{:,}".format(int(data['Profit'].sum())))
        st.metric(label='Total Profit', value=profit)

    with col3:
        # Most sold product
        most_sold_product = data.groupby('Product Name')['Quantity'].sum().reset_index()
        most_sold_product = most_sold_product.sort_values('Quantity', ascending=False).head(1)
        st.metric(label='Most sold product', value=most_sold_product['Product Name'].values[0])

    with col4:
        # Best performing state
        best_state = data.groupby('State')['Profit'].sum().reset_index()
        best_state = best_state.sort_values('Profit', ascending=False).head(1)
        st.metric(label='Best performing state', value=best_state['State'].values[0])
def write_filter_row(data):
    # First set interactive elements in top row
    col1, col2, col3, col4 = st.columns(4)

    # State
    with col1:
        states_list = data['State'].unique().tolist()
        states_list.insert(0, 'All')
        state = st.selectbox('Select State', states_list, index = 0 )
        st.session_state['state'] = state

    # Segment
    with (col2):
        segment_list = data['Segment'].unique().tolist()
        segment_list.insert(0, 'All')
        segment = st.selectbox('Select Segment', segment_list, index = 0)
        st.session_state['segment'] = segment

    # Category
    with (col3):
        category_list = data['Category'].unique().tolist()
        category_list.insert(0, 'All')
        category = st.selectbox('Select Category', category_list, index = 0)
        st.session_state['category'] = category

    # date range
    with col4:
        data['Order Year'] = pd.to_datetime(data['Order Date']).dt.year
        min_date = data['Order Year'].min()
        max_date = data['Order Year'].max()
        # Creating the slider
        selected_range = st.slider(
            "Select Date Range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date)
        )
        st.session_state['selected_range'] = selected_range

def get_time_series_plot(data):
    #Apply time filter
    data = data[(data['Order Year'] >= st.session_state['selected_range'][0]) &
                (data['Order Year'] <= st.session_state['selected_range'][1])]
    #Get the top ten best seeling products
    top_10_products = data.groupby('Sub-Category')['Quantity'].sum().reset_index()
    top_10_products = top_10_products.sort_values('Quantity', ascending=False).head(5)['Sub-Category'].tolist()

    #Filter data
    filtered_data = data[data['Sub-Category'].isin(top_10_products)]

    #Get time series data
    time_series_data = filtered_data.groupby(['year','Sub-Category'])['Quantity'].sum().reset_index()

    #Plot
    fig = px.line(time_series_data,
                  x='year',
                  y='Quantity',
                  color='Sub-Category')
    #add the title
    fig.update_layout(title='Top 5 sub-categories sold over time')
    st.plotly_chart(fig, use_container_width=True)

def get_revenue_plot(data):
    #Apply filters
    data = apply_filters(data)

    #Sort out the by the state
    if st.session_state['state'] != 'All':
        data = data[data['State'] == st.session_state['state']]

    #Get time series data
    time_series_data = data.groupby('year')['Profit'].sum().reset_index()

    #Plot
    fig = px.line(time_series_data,
                  x='year',
                  y='Profit')
    #add the title
    fig.update_layout(title='Revenue over time')
    st.plotly_chart(fig, use_container_width=True)