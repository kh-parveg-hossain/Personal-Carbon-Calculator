import streamlit as st
import plotly.express as px

# Define emission factors (example values)
EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,  # kgCO2/km
        "Electricity": 0.82,     # kgCO2/kWh
        "Diet": 1.25,            # kgCO2/meal
        "Waste": 0.1             # kgCO2/kg
    }
}

# Configure page
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

# Title
st.title("🌿 Personal Carbon Calculator App")

# Country selection
st.subheader("🌍 Your Country")
country = st.selectbox("Select", ["India"])

# Two column layout for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Daily commute distance (in km)")
    distance = st.slider("Distance", 0.0, 100.0, key="distance_input")

    st.subheader("💡 Monthly electricity consumption (in kWh)")
    electricity = st.slider("Electricity", 0.0, 1000.0, key="electricity_input")

with col2:
    st.subheader("🗑️ Waste generated per week (in kg)")
    waste = st.slider("Waste", 0.0, 100.0, key="waste_input")

    st.subheader("🍽️ Number of meals per day")
    meals = st.number_input("Meals", 0, key="meals_input")

# Convert all inputs to yearly values
distance = distance * 365
electricity = electricity * 12
meals = meals * 365
waste = waste * 52

# Calculate emissions (kg)
transportation_emissions = EMISSION_FACTORS[country]["Transportation"] * distance
electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity
diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals
waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste

# Convert to tonnes
transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)

# Total
total_emissions = round(
    transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
)

# Button to calculate and show results
if st.button("Calculate CO2 Emissions"):

    st.header("📊 Results")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Emissions by Category (in tonnes/year)")
        st.info(f"🚗 Transportation: {transportation_emissions}")
        st.info(f"💡 Electricity: {electricity_emissions}")
        st.info(f"🍽️ Diet: {diet_emissions}")
        st.info(f"🗑️ Waste: {waste_emissions}")

    with col4:
        st.subheader("🌍 Total Carbon Footprint")
        st.success(f"Your total carbon footprint is: {total_emissions} tonnes CO2/year")
        st.warning("⚠️ India's average per capita CO2 emission was 1.9 tonnes/year in 2021.")

    # Graphs
    st.subheader("📈 Visual Representation of Your Emissions")

    emission_data = {
        "Category": ["Transportation", "Electricity", "Diet", "Waste"],
        "Emissions (tonnes)": [
            transportation_emissions,
            electricity_emissions,
            diet_emissions,
            waste_emissions
        ]
    }

    # Pie Chart
    pie_fig = px.pie(
        emission_data,
        names="Category",
        values="Emissions (tonnes)",
        title="Proportion of CO2 Emissions by Category",
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    st.plotly_chart(pie_fig, use_container_width=True)

    # Bar Chart
    bar_fig = px.bar(
        emission_data,
        x="Category",
        y="Emissions (tonnes)",
        title="Annual CO2 Emissions by Category",
        text_auto=True,
        color="Category"
    )
    st.plotly_chart(bar_fig, use_container_width=True)
    # Line Chart
    line_fig = px.line(
        emission_data,
        x="Category",
        y="Emissions (tonnes)",
        title="Trend of CO2 Emissions by Category",
        markers=True
    )
    st.plotly_chart(line_fig, use_container_width=True)