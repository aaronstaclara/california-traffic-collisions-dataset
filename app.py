import json
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from urllib.request import urlopen


@st.cache
def load_data(type=None):
    # Specify location
    if type == "choropleth":
        source_file = "choropleth.csv"
    elif type == "hourly":
        source_file = "hourly.csv"
    else:
        source_file = "day_of_week.csv"

    # Load the data
    collisions = pd.read_csv(
        source_file
    )

    # Edit choropleth file
    if type == "choropleth":
        collisions["FIPS"] = "0" + collisions["FIPS"].astype(str)

    return collisions


def introduction():
    # Write the title and the subheader
    st.title("🚗 Mitigating Fatal Collisions Using California Traffic Collisions Data Set")
    st.subheader(
        "This simple web app aims to provide insights regarding the California Traffic Collisions Data Set "
        "sourced from Kaggle."
    )

    # Write details of the web app
    st.markdown(
        """
        In this web app, we aim to answer the following questions: 
        
        1. Where and when do fatal collisions occur? 
        2. Using the data, can we predict the conditions which would result to injurious collisions? 
        3. How do we mitigate these collisions?
        """
    )

    # Add image
    st.image("collision_photo.jpg")
    st.caption(
        f"Source: Forbes (https://www.forbes.com/sites/carltonreid/2020/09/28/journalists-should-stress-agency-in-reporting-on-traffic-crashes-states-new-media-guidelines).")


def generate_choropleth_map(year):
    # Load the data
    collisions = load_data(type="choropleth")

    # Apply filter
    collisions = collisions[collisions["year_option"] == str(year)]

    # Generate the choropleth map
    with urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as response:
        counties = json.load(response)

    fig = px.choropleth(
        collisions,
        geojson=counties,
        locations="FIPS",
        color="killed_victims",
        color_continuous_scale="YlOrRd",
        scope="usa",
        hover_data=["county", "FIPS", "killed_victims"],
        labels={
            'county': "county",
            'killed_victims': 'fatalities'
        },
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    # Show the choropleth map
    st.markdown("**Number of collision fatalities for each county in California**")
    st.plotly_chart(fig)


def generate_collisions_by_hour_bar_graph(year):
    # Load the data
    collisions = load_data(type="hourly")

    # Apply filter
    collisions = collisions[collisions["year_option"] == str(year)]

    # Plot the data
    fig, ax = plt.subplots(figsize=(6, 3), dpi=200)
    ax.bar(
        collisions["collision_hour"],
        collisions["killed_victims"],
    )
    ax.set_ylabel("Number of killed victims")
    ax.set_xlabel("Hour")
    st.markdown(
        "**Number of fatalities per hour due to collisions**"
    )
    st.pyplot(fig)


def generate_collisions_by_day_of_week_bar_graph(year):
    # Load the data
    collisions = load_data(type="day_of_week")

    # Apply filter
    collisions = collisions[collisions["year_option"] == str(year)]

    # Plot the data
    fig, ax = plt.subplots(figsize=(6, 3), dpi=200)
    ax.bar(
        collisions["collision_day"],
        collisions["killed_victims"],
    )
    ax.set_ylabel("Number of killed victims")
    ax.set_xlabel("Day of week")
    st.markdown(
        "**Number of fatalities per day of week due to collisions**"
    )
    st.pyplot(fig)


def descriptive_analytics():
    # Write the title and the subheader
    st.title("🚗 Analyzing Fatal Collisions")
    st.subheader(
        "This section aims to provide insights regarding the geographical and temporal aspect of fatal collisions in California."
    )

    # Generate year_options
    year_options = ["all"]
    year_list = range(2001, 2022)
    for year in year_list:
        year_options.append(year)

    # Ask for user input
    year = st.selectbox(
        "Select year",
        year_options
    )

    # Generate choropleth map
    generate_choropleth_map(year)

    # Generate temporal bar graphs
    generate_collisions_by_hour_bar_graph(year)
    generate_collisions_by_day_of_week_bar_graph(year)


def predictive_analytics():
    # Write the title and the subheader
    st.title("🚗 Predicting Injured Victims")
    st.subheader(
        "This section aims to provide a model to predict the number of injurious collisions."
    )

    # Outline steps
    st.write(
        "Using the California Traffic Collisions Data, a model was built using the following methodology. "
    )
    st.image("Slide1.PNG")
    st.caption("Access the files at https://github.com/aaronstaclara/california-traffic-collisions-dataset.")

    # Outline features
    st.write("The following features were used in the modelling: ")
    st.image("Slide2.PNG")

    # Outline model
    st.write("The model works as follows. Models used were Linear Regression and Gradient Boosting Regressor: ")
    st.image("Slide3.PNG")

    # Outline results
    st.write("The results of the modelling are as follows: ")
    st.image("Slide4.PNG")

    # Outline feature importance
    st.write("In the modelling, party_count, type_of_collision_sideswipe and distance were found to significantly affect the prediction: ")
    st.image("Slide5.PNG")


def conclusion():
    # Write the title and the subheader
    st.title("🚗 Conclusions and Recommendations")

    # Outline conclusions and recommendations
    st.subheader("What We Found")
    st.markdown(
        """
        In exploring the data, we have found that: 
        
        1. Los Angeles registers the most number of fatal collisions from 2001 to 2021.
        2. In terms of day of week, most fatal collisions usually occur during Saturdays.
        3. In terms of hour, most fatal collisions usually occur at 6 PM. 
        """
    )

    # Outline conclusions and recommendations
    st.subheader("What We Can Do")
    st.markdown(
        """
        California should monitor closely the insights extracted fromt their data. 
        Stringent traffic measures must be implemented along Los Angeles and patrol groups should be able
        to monitor roads during the evenings and the weekends. 
        
        To further improve the modelling, we can consider other variables that could potentially affect 
        the severity of collisions. This will also help us in simulating environments that could be harmful to
        motorists. These simulations, in effect, can inform the decisions of policymakers and patrol groups 
        in creating an environment that is safe for motorists. 
        """
    )

def author():
    # Detail info about the author
    st.title("🚗 Author")

    st.markdown(
        """
        This web app was created by **Rick Aaron Sta.Clara**. He is a data scientist with a degree in chemical engineering.
        He is currently improving his capacities in understanding data and algorithms. Visit his profile here: 
        linkedin.com/in/rick-aaron-sta-clara-7470b1114.
        """
    )

list_of_pages = [
    "The Data",
    "Analyzing Fatal Collisions",
    "Predicting Injured Victims",
    "Conclusions and Recommendations",
    "Author"
]

st.sidebar.title(':scroll: Main Pages')
selection = st.sidebar.radio("Go to: ", list_of_pages)

if selection == "The Data":
    introduction()

elif selection == "Analyzing Fatal Collisions":
    descriptive_analytics()

elif selection == "Predicting Injured Victims":
    predictive_analytics()

elif selection == "Conclusions and Recommendations":
    conclusion()

elif selection == "Author":
    author()