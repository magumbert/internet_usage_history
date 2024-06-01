# ------------------------ IMPORT LIBRARIES -------------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# ------------------------ LOAD & PREPARE DATA -------------------------------------

@st.cache_data # decorator

def load_data(path):
    df = pd.read_csv(path)
    return df

# Load geojson file
with open('./data/countries.geojson', 'r') as f:
    geojson_data = json.load(f)

# load csv file
usage_df_raw = load_data(path="./data/share-of-individuals-using-the-internet.csv")
usage_df = deepcopy(usage_df_raw) # for security, you cannot change what is cached

# ------------------------ CREATE HEADERS AND PICTURE -------------------------------------

st.title("History of Internet Usage Across the World (1990 - 2019)")


st.image("gates_jobs.jpg", caption="Bill Gates and Steve Jobs")

# Attribution text in Markdown format
attribution = """
Picture by [Leandro Agrò](https://www.flickr.com/photos/leeander/). Licensed under [CC BY-NC-ND 2.0](https://creativecommons.org/licenses/by-nc-nd/2.0/).
"""

# Display the attribution using st.markdown to handle the Markdown formatting
st.markdown(attribution)

# -------------------- INTRODUCTION -----------------------------------------
caption_text = """
The first prototype of the internet was invented in the late 1960s under the name Advanced Research Projects Agency Network (ARPANET). 
The project was funded by the U.S. Department of Defense. <br/>
In broader terms, January 1, 1983, is considered the official birthday of the internet. On this day, the transition to the new communications protocol, 
TCP/IP, was officially completed, allowing different networks to communicate with each other, which was not possible within the ARPANET network alone.<br/>
Since the early 1990s, the usage of the internet has found its way into everyday life, impacting business, science, and social life.<br/>
Let's have a brief look at how internet usage has evolved since 1990 across different countries.<br/><br/>
ALL THE GRAPHICS ARE INTERACTIVE! So feel free to click and play around with them to get an intuition of how internet usage has evolved over the years. Have fun!<br/><br/>

"""

# Display the caption using st.markdown to handle HTML formatting
st.markdown(f"<p style='font-size: 1.1em; color: gray;'>{caption_text}</p>", unsafe_allow_html=True)

# ------------------------ LINE PLOT FOR G8+ STATES  -------------------------------------

caption_text = """
First let's explore how the usage has evolved over the years 1990 to 2019 within the G8+ states.
Unfortunately, there is no data available for Great Britain.
"""

# Display the caption using st.markdown to handle HTML formatting
st.markdown(f"<p style='font-size: 1.1em; color: gray;'>{caption_text}</p>", unsafe_allow_html=True)

countries = ['USA', 'CAN', 'RUS', 'CHN', 'FRA', 'DEU', 'ITA', 'IND', 'BRA'] # there is no info for GBR

fig2 = go.Figure()
# Define traces
for c in countries:
    country_data = usage_df[usage_df['Code'] == c]
    fig2.add_trace(
        go.Scatter(
            x=country_data['Year'],
            y=country_data['Individuals using the Internet (% of population)'],
            mode='lines+markers', 
            name=c,
            text=[c] * len(country_data),
            hovertemplate=
                "Country: %{text}<br>" +
                "Internet Usage: %{y:.2f}%<br>" +
                "Year: %{x:.0f}<br>" +
                "<extra></extra>"
        )
    )

# Update layout
fig2.update_layout(
    title='Internet Usage of Population Over Time in G8+ Countries',
    xaxis_title='Year',
    yaxis_title='Internet Usage (%)',
    yaxis=dict(range=[0, 100])
)

st.plotly_chart(fig2)



# ------------------------ PLOT WORLD OVERVIEW  -------------------------------------
caption_text = """
Not suprisingly internet usage has vastly evolved over the last years. 
There seems to be a huge increase in the late 90s/early 2000s, which is probably due to the invention of systems such as Windows 95/98
and increasing internet speed.<br/><br/>
Now let's inspect how internet usage was distributed around the globe in various years. 
"""

# Display the caption using st.markdown to handle HTML formatting
st.markdown(f"<p style='font-size: 1.1em; color: gray;'>{caption_text}</p>", unsafe_allow_html=True)




# Initial year to display
initial_year = 2017

# Create the initial figure
fig = px.choropleth_mapbox(
    usage_df[usage_df['Year'] == initial_year],
    geojson=geojson_data,
    locations='Code',
    featureidkey="properties.ISO_A3",
    color='Individuals using the Internet (% of population)',
    color_continuous_scale="Reds",
    range_color=(0, 100),
    mapbox_style="carto-positron",
    zoom=.5,
    center={"lat": 0, "lon": 0},
    opacity=0.5,
    labels={'Individuals using the Internet (% of population)': 'Internet Usage (%)'}
)

# Update layout with title
fig.update_layout(
    title_text=f'Percentage of Population Using the Internet in {initial_year} by Country',
    margin={"r": 0, "t": 40, "l": 0, "b": 0}
)

fig.update_traces(hovertemplate='Internet Usage: %{z:.2f}%<br>' +
                                 '<extra></extra>')

# Create a list of years for the dropdown menu
years = usage_df['Year'].unique()
years = sorted(years)

# Add dropdown menu to update the plot based on the selected year
dropdown_buttons = [
    {
        'label': str(year),
        'method': 'update',
        'args': [
            {'z': [usage_df[usage_df['Year'] == year]['Individuals using the Internet (% of population)']],
             'locations': [usage_df[usage_df['Year'] == year]['Code']]},
            {'title': f'Percentage of Population Using the Internet in {year} by Country'}
        ]
    } for year in years
]

fig.update_layout(
    updatemenus=[
        {
            'buttons': dropdown_buttons,
            'direction': 'down',
            'showactive': True,
        }
    ]
)

st.plotly_chart(fig)


caption_text = """
As we can see a huge percentage of the population is using the internet in the Americas, Europe and Asia as well as Australia. 
However, in Africa there is minor internet usage especially in the interior countries.
"""

# Display the caption using st.markdown to handle HTML formatting
st.markdown(f"<p style='font-size: 1.1em; color: gray;'>{caption_text}</p>", unsafe_allow_html=True)
