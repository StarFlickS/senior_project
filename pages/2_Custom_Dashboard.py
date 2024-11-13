import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Custom Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to read CSV files
def read_file(path):
    return pd.read_csv(path)

# Load datasets
@st.cache_data
def load_data():
    owid_df = pd.read_csv("Datasets/Main_Dashboard/Modified/owid/owid_Thailand.csv")
    owid_df['date'] = pd.to_datetime(owid_df['date'])

    death_df = pd.read_csv("Datasets/Main_Dashboard/Modified/DDC/deaths/deaths_merged.csv")
    death_df['date'] = death_df.apply(lambda row: pd.to_datetime(f"{row['year']}-{row['weeknum']}-1", format="%Y-%W-%w"), axis=1)

    report_df = pd.read_csv("Datasets/Main_Dashboard/Modified/DDC/report/report.csv")
    report_df['date'] = report_df.apply(lambda row: pd.to_datetime(f"{row['year']}-{row['weeknum']}-1", format="%Y-%W-%w"), axis=1)

    cases_df = pd.read_csv("Datasets/Main_Dashboard/Modified/DDC/cases/cases_merged.csv")

    return owid_df, death_df, report_df, cases_df

owid_df, death_df, report_df, cases_df = load_data()

# Sidebar for user selections
st.sidebar.title("ปรับแต่งแดชบอร์ด")
dataset = st.sidebar.selectbox(
    "เลือกชุดข้อมูล",
    ("owid_Thailand.csv", "deaths_merged.csv", "report.csv", "cases_merged.csv")
)

# Selecting attributes from the dataset and initializing selected_provinces
selected_provinces = []  # Initialize as an empty list to avoid NameError
if dataset == "owid_Thailand.csv":
    selected_df = owid_df
    columns = ["new_cases", "new_deaths", "new_vaccinations", "total_cases", "total_deaths", "total_vaccinations"]
    min_date = owid_df['date'].min().date()
    max_date = owid_df['date'].max().date()
elif dataset == "deaths_merged.csv":
    selected_df = death_df
    columns = ["age", "age_range", "type", "occupation", "death_cluster", "province"]
    min_date = death_df['date'].min().date()
    max_date = death_df['date'].max().date()
    
    # Filter options specific to death data
    # Filter by year
    years = sorted(selected_df['year'].unique())
    selected_year = st.sidebar.selectbox(
        "เลือกปี",
        options=["รวมทุกปี"] + years
    )

    # Filter by multiple provinces for comparison
    provinces = sorted(selected_df['province'].unique())
    selected_provinces = st.sidebar.multiselect(
        "เลือกจังหวัด (เปรียบเทียบได้หลายจังหวัด)",
        provinces,
    )

    # Filter by age range
    age_ranges = sorted(selected_df['age_range'].unique())
    selected_age_range = st.sidebar.multiselect(
        "เลือกช่วงอายุ",
        age_ranges,
        default=age_ranges  # Default to all age ranges selected
    )

    # Apply filters to the dataset
    if selected_year != "รวมทุกปี":
        selected_df = selected_df[selected_df['year'] == selected_year]
    
    # Apply additional filters for selected provinces and age ranges
    selected_df = selected_df[
        (selected_df['province'].isin(selected_provinces)) &
        (selected_df['age_range'].isin(selected_age_range))
    ]

elif dataset == "report.csv":
    selected_df = report_df
    columns = [
    "new_case",
    "total_case",
    "new_case_excludeabroad",
    "total_case_excludeabroad",
    "new_recovered",
    "total_recovered",
    "new_death",
    "total_death",
    "case_foreign",
    "case_prison",
    "case_walkin"
    ]
    min_date = report_df['date'].min().date()
    max_date = report_df['date'].max().date()
else:
    selected_df = cases_df
    columns = ["gender",
    "age_number",
    "age_range",
    "job",
    "risk",
    "patient_type",
    "province",
    "reporting_group",
    "region_odpc",
    "region"]
    min_date = None
    max_date = None

    # Filter options specific to cases data
    years = sorted(selected_df['year'].unique())
    selected_year = st.sidebar.selectbox(
        "เลือกปี",
        options=["รวมทุกปี"] + years
    )

    # Filter by multiple provinces for comparison
    provinces = sorted(selected_df['province'].unique())
    selected_provinces = st.sidebar.multiselect(
        "เลือกจังหวัด (เปรียบเทียบได้หลายจังหวัด)",
        provinces,
    )

    # Filter by age range
    age_ranges = sorted(selected_df['age_range'].unique())
    selected_age_range = st.sidebar.multiselect(
        "เลือกช่วงอายุ",
        age_ranges,
        default=age_ranges  # Default to all age ranges selected
    )

    # Apply filters to the dataset
    if selected_year != "รวมทุกปี":
        selected_df = selected_df[selected_df['year'] == selected_year]
    
    # Apply additional filters for selected provinces and age ranges
    selected_df = selected_df[
        (selected_df['province'].isin(selected_provinces)) &
        (selected_df['age_range'].isin(selected_age_range))
    ]

# Allow the user to select the attributes to plot
selected_attributes = st.sidebar.multiselect(
    "เลือก attribute ที่จะนำมาใช้",
    columns
)

# Add graph type selection with the new "Pie Chart" option
graph_type = st.sidebar.selectbox(
    "เลือกประเภทกราฟ",
    ("Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart")
)

# Check if the selected dataset has a date column before showing the date filters
if 'date' in selected_df.columns:
    # Convert date column back to datetime for filtering
    selected_df['date'] = pd.to_datetime(selected_df['date'])
    
    # User selects start and end dates
    start_date = st.sidebar.date_input(
        "เลือกวันเริ่มต้น", min_date, min_value=min_date, max_value=max_date
    )
    end_date = st.sidebar.date_input(
        "เลือกวันสิ้นสุด", max_date, min_value=min_date, max_value=max_date
    )

    # Filter the dataset based on selected dates
    selected_df = selected_df[(selected_df['date'] >= pd.to_datetime(start_date)) & (selected_df['date'] <= pd.to_datetime(end_date))]

# Check for chart compatibility
incompatible_chart = False
if graph_type == "Pie Chart" and len(selected_attributes) != 1:
    incompatible_chart = True
    st.warning("กรุณาเลือก attribute เพียงหนึ่งตัวสำหรับการแสดงผล Pie Chart")
elif graph_type in ["Line Chart", "Scatter Plot"] and any(selected_df[attr].dtype == 'object' for attr in selected_attributes):
    incompatible_chart = True
    st.warning("กราฟแบบ Line และ Scatter ใช้ได้กับข้อมูลตัวเลขเท่านั้น กรุณาเลือก attribute ที่เหมาะสม")

# Plot the graph if compatible
if not incompatible_chart and not selected_df.empty and len(selected_attributes) > 0:
    if graph_type == "Line Chart" and 'date' in selected_df.columns:
        fig = px.line(selected_df, x='date', y=selected_attributes, title=f'กราฟเส้นของ {", ".join(selected_attributes)}')
        st.plotly_chart(fig)
    elif graph_type == "Bar Chart":
        fig = px.bar(selected_df, x='date' if 'date' in selected_df.columns else 'year', y=selected_attributes, title=f'กราฟแท่งของ {", ".join(selected_attributes)}')
        st.plotly_chart(fig)
    elif graph_type == "Scatter Plot":
        fig = px.scatter(selected_df, x='date' if 'date' in selected_df.columns else 'year', y=selected_attributes, title=f'กราฟกระจายของ {", ".join(selected_attributes)}')
        st.plotly_chart(fig)
    elif graph_type == "Pie Chart" and len(selected_attributes) == 1:
        attribute = selected_attributes[0]
        for province in selected_provinces:
            province_data = selected_df[selected_df['province'] == province]
            fig = px.pie(province_data, names=attribute, title=f'กราฟวงกลมของ {attribute} สำหรับจังหวัด {province}')
            st.plotly_chart(fig)
else:
    st.write("กรุณาเลือก attribute ที่จะนำมาแสดงข้อมูล")