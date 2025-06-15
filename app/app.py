import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.title("Gapminder")
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

# 1. Load and prepare data
@st.cache_data
def load_data():
    def tidy_csv(path, value_name):
        df = pd.read_csv(path)
        df.replace(["..", "N/A", ""], pd.NA, inplace=True)
        df = df.ffill(axis=1)
        df = df.melt(id_vars=["country"], var_name="year", value_name=value_name)
        df["year"] = df["year"].astype(int)

        # Convert strings like '3.2M', '450k' to numbers
        def convert_suffix(val):
            if pd.isna(val):
                return None
            val = str(val).replace(",", "").strip()
            if val.endswith("M"):
                return float(val[:-1]) * 1_000_000
            elif val.endswith("k"):
                return float(val[:-1]) * 1_000
            else:
                try:
                    return float(val)
                except:
                    return None

        df[value_name] = df[value_name].apply(convert_suffix)
        return df

    base_path = os.path.join(os.path.dirname(__file__), "data")
    population = tidy_csv(os.path.join(base_path, "population.csv"), "population")
    life_exp = tidy_csv(os.path.join(base_path, "life_expectancy.csv"), "life_expectancy")
    gni = tidy_csv(os.path.join(base_path, "gni_per_capita.csv"), "gni_per_capita")

    df = population.merge(life_exp, on=["country", "year"]).merge(gni, on=["country", "year"])

    df["country"] = df["country"].replace({
        "USA": "United States",
        "UK": "United Kingdom",
        "Korea, Rep.": "South Korea"
    })

    df["population"] = pd.to_numeric(df["population"], errors="coerce")
    df["life_expectancy"] = pd.to_numeric(df["life_expectancy"], errors="coerce")
    df["gni_per_capita"] = pd.to_numeric(df["gni_per_capita"], errors="coerce")

    return df

df = load_data()

# 2. UI - Country selection
countries = df["country"].unique()
default_selection = [c for c in ["Germany", "United States"] if c in countries]
selected_countries = st.multiselect("Select Countries", countries, default=default_selection)

# 3. Animated Plotly Chart
if selected_countries:
    animated_df = df[df["country"].isin(selected_countries)]
    animated_df = animated_df.dropna(subset=["population", "life_expectancy", "gni_per_capita"])

    fig = px.scatter(
        animated_df,
        x="gni_per_capita",
        y="life_expectancy",
        animation_frame="year",
        animation_group="country",
        size="population",
        color="country",
        log_x=True,
        size_max=60,
        range_x=[100, 100000],
        title="Gapminder: Animated Bubble Chart"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select at least one country.")