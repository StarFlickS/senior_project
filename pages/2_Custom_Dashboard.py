import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Custom Dashboard", layout="wide", initial_sidebar_state="expanded")

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
    cases_df['date'] = cases_df.apply(lambda row: pd.to_datetime(f"{row['year']}-{row['weeknum']}-1", format="%Y-%W-%w"), axis=1)

    return owid_df, death_df, report_df, cases_df

owid_df, death_df, report_df, cases_df = load_data()

# Sidebar for user selections
st.sidebar.title("ปรับแต่งแดชบอร์ด")
dataset = st.sidebar.selectbox("เลือกชุดข้อมูล", ("owid_Thailand.csv", "deaths_merged.csv", "report.csv", "cases_merged.csv"))

# Initialize selected_provinces as an empty list to avoid NameError
selected_provinces = []

# Define translations for each dataset
owid_translation = {
    "new_cases": "new_cases (ผู้ป่วยรายใหม่)",
    "new_deaths": "new_deaths (ผู้เสียชีวิตรายใหม่)",
    "new_vaccinations": "new_vaccinations (การฉีดวัคซีนใหม่)",
    "total_cases": "total_cases (ผู้ป่วยสะสมทั้งหมด)",
    "total_deaths": "total_deaths (ผู้เสียชีวิตสะสมทั้งหมด)",
    "total_vaccinations": "total_vaccinations (การฉีดวัคซีนทั้งหมด)"
}

deaths_translation = {
    "age": "age (อายุ)",
    "age_range": "age_range (ช่วงอายุ)",
    "type": "type (ประเภท)",
    "occupation": "occupation (อาชีพ)",
    "death_cluster": "death_cluster (กลุ่มผู้เสียชีวิต)",
    "province": "province (จังหวัด)"
}

report_translation = {
    "new_case": "new_case (ผู้ป่วยรายใหม่)",
    "total_case": "total_case (ผู้ป่วยสะสม)",
    "new_case_excludeabroad": "new_case_excludeabroad (ผู้ป่วยในประเทศ)",
    "total_case_excludeabroad": "total_case_excludeabroad (ผู้ป่วยสะสมในประเทศ)",
    "new_recovered": "new_recovered (ผู้ป่วยหายใหม่)",
    "total_recovered": "total_recovered (ผู้ป่วยหายสะสม)",
    "new_death": "new_death (ผู้เสียชีวิตใหม่)",
    "total_death": "total_death (ผู้เสียชีวิตสะสม)",
    "case_foreign": "case_foreign (ผู้ป่วยต่างชาติ)",
    "case_prison": "case_prison (ผู้ป่วยในเรือนจำ)",
    "case_walkin": "case_walkin (ผู้ป่วย walk-in)"
}

cases_translation = {
    "gender": "gender (เพศ)",
    "age_number": "age_number (อายุเป็นตัวเลข)",
    "age_range": "age_range (ช่วงอายุ)",
    "job": "job (อาชีพ)",
    "risk": "risk (ความเสี่ยง)",
    "patient_type": "patient_type (ประเภทผู้ป่วย)",
    "province": "province (จังหวัด)",
    "reporting_group": "reporting_group (กลุ่มการรายงาน)",
    "region_odpc": "region_odpc (เขตสุขภาพ ODPC)",
    "region": "region (ภูมิภาค)"
}

# Selecting attributes and updating the dataset name and columns
if dataset == "owid_Thailand.csv":
    selected_df = owid_df
    columns = list(owid_translation.keys())
    translated_columns = [owid_translation[col] for col in columns]
    min_date = owid_df['date'].min().date()
    max_date = owid_df['date'].max().date()
    dataset_name = "owid_Thailand.csv"
elif dataset == "deaths_merged.csv":
    selected_df = death_df
    columns = list(deaths_translation.keys())
    translated_columns = [deaths_translation[col] for col in columns]
    years = sorted(selected_df['year'].unique())
    selected_year = st.sidebar.selectbox("เลือกปี", options=["รวมทุกปี"] + years)

    # Filter by multiple provinces for comparison
    provinces = sorted(selected_df['province'].unique())
    selected_provinces = st.sidebar.multiselect("เลือกจังหวัด (เปรียบเทียบได้หลายจังหวัด)", provinces)

    # Filter by age range
    age_ranges = sorted(selected_df['age_range'].unique())
    selected_age_range = st.sidebar.multiselect("เลือกช่วงอายุ", age_ranges, default=age_ranges)

    # Apply filters to the dataset
    if selected_year != "รวมทุกปี":
        selected_df = selected_df[selected_df['year'] == selected_year]
    
    # Apply additional filters for selected provinces and age ranges
    selected_df = selected_df[
        (selected_df['province'].isin(selected_provinces)) &
        (selected_df['age_range'].isin(selected_age_range))
    ]
    min_date = death_df['date'].min().date()
    max_date = death_df['date'].max().date()
    dataset_name = "deaths_merged.csv"
elif dataset == "report.csv":
    selected_df = report_df
    columns = list(report_translation.keys())
    translated_columns = [report_translation[col] for col in columns]
    min_date = report_df['date'].min().date()
    max_date = report_df['date'].max().date()
    dataset_name = "report.csv"
else:
    selected_df = cases_df
    columns = list(cases_translation.keys())
    translated_columns = [cases_translation[col] for col in columns]
    # Year filter for cases_merged.csv
    years = sorted(selected_df['year'].unique())
    selected_year = st.sidebar.selectbox("เลือกปี", options=["รวมทุกปี"] + years)

    # Filter by multiple provinces for comparison
    provinces = sorted(selected_df['province'].unique())
    selected_provinces = st.sidebar.multiselect("เลือกจังหวัด (เปรียบเทียบได้หลายจังหวัด)", provinces)

    # Filter by age range
    age_ranges = sorted(selected_df['age_range'].unique())
    selected_age_range = st.sidebar.multiselect("เลือกช่วงอายุ", age_ranges, default=age_ranges)

    # Apply filters to the dataset
    if selected_year != "รวมทุกปี":
        selected_df = selected_df[selected_df['year'] == selected_year]
    
    # Apply additional filters for selected provinces and age ranges
    selected_df = selected_df[
        (selected_df['province'].isin(selected_provinces)) &
        (selected_df['age_range'].isin(selected_age_range))
    ]
    min_date = cases_df['date'].min().date()
    max_date = cases_df['date'].max().date()
    dataset_name = "cases_merged.csv"

# Display the selected dataset name in the sidebar
st.sidebar.write(f"ชุดข้อมูลที่เลือก: {dataset_name}")

# Allow the user to select the attributes to plot
selected_attributes = st.sidebar.multiselect("เลือก Attribute", translated_columns)

# Map selected translated attributes back to original names
attribute_mapping = {v: k for k, v in owid_translation.items()}
attribute_mapping.update({v: k for k, v in deaths_translation.items()})
attribute_mapping.update({v: k for k, v in report_translation.items()})
attribute_mapping.update({v: k for k, v in cases_translation.items()})
selected_attributes = [attribute_mapping[attr] for attr in selected_attributes]

# Add graph type selection with the new "Pie Chart" option
graph_type = st.sidebar.selectbox("เลือกประเภทกราฟ", ("Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart"))

# Check if the selected dataset has a date column before showing the date filters
if 'date' in selected_df.columns:
    selected_df['date'] = pd.to_datetime(selected_df['date'])
    start_date = st.sidebar.date_input("เลือกวันเริ่มต้น", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("เลือกวันสิ้นสุด", max_date, min_value=min_date, max_value=max_date)
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
    translated_attributes = [attribute_mapping.get(attr, attr) for attr in selected_attributes]
    if graph_type == "Line Chart" and 'date' in selected_df.columns:
        fig = px.line(selected_df, x='date', y=selected_attributes, title=f'กราฟเส้นของ {", ".join(translated_attributes)}')
        st.plotly_chart(fig)
    elif graph_type == "Bar Chart":
        fig = px.bar(selected_df, x='date' if 'date' in selected_df.columns else 'year', y=selected_attributes, title=f'กราฟแท่งของ {", ".join(translated_attributes)}')
        st.plotly_chart(fig)
    elif graph_type == "Scatter Plot":
        fig = px.scatter(selected_df, x='date' if 'date' in selected_df.columns else 'year', y=selected_attributes, title=f'กราฟกระจายของ {", ".join(translated_attributes)}')
        
        st.plotly_chart(fig)
    elif graph_type == "Pie Chart" and len(selected_attributes) == 1:
        attribute = selected_attributes[0]
        translated_attribute = attribute_mapping.get(attribute, attribute)
        for province in selected_provinces:
            province_data = selected_df[selected_df['province'] == province]
            fig = px.pie(province_data, names=attribute, title=f'กราฟวงกลมของ {translated_attribute} สำหรับจังหวัด {province}')
            st.plotly_chart(fig)
else:
    st.write("กรุณาเลือก Attribute ที่จะนำมาแสดงข้อมูล")
