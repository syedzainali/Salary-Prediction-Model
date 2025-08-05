import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to shorten categories based on cutoff
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

# Function to clean the 'YearsCodePro' column
def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

# Function to clean the 'EdLevel' column
def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or 'Associate degree' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

# Load data
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "cleaned_data.csv")
    df = pd.read_csv(file_path)

    # Map numeric country codes to names
    country_map = {
        0: "USA",
        1: "Germany",
        2: "UK and Northern Ireland",
        3: "Canada",
        4: "India",
        5: "France",
        6: "Netherlands",
        7: "Australia",
        8: "Brazil",
        9: "Spain",
        10: "Sweden",
        11: "Italy",
        12: "Poland",
        13: "Switzerland",
        14: "Denmark",
        15: "Norway",
        16: "Israel"
    }

    # Replace numeric codes with country names (fallback to code if not found)
    df["Country"] = df["Country"].map(country_map).fillna(df["Country"])
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write("### Stack Overflow Developer Survey 2024")

    # Pie chart: Number of data points from each country
    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(
        data,
        labels=data.index.astype(str),
        autopct="%1.1f%%",
        startangle=90,
        rotatelabels=270
    )
    ax1.axis("equal")  # Equal aspect ratio makes the pie chart a circle

    st.write("#### Number of Data from different countries")
    st.pyplot(fig1)

    # Bar chart: Mean salary by country
    st.write("#### Mean Salary Based On Country")
    mean_salary_country = df.groupby("Country")["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(mean_salary_country)

    # Line chart: Mean salary by experience
    st.write("#### Mean Salary Based On Experience")
    mean_salary_experience = df.groupby("YearsCodePro")["Salary"].mean().sort_values(ascending=True)
    st.line_chart(mean_salary_experience)
