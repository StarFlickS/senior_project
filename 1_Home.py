import streamlit as st
import pandas as pd
import plotly.express as px
from Codes.Other import regions

def read_file(path):
    return pd.read_csv(path)

owid_df = read_file("Datasets/Main_Dashboard/Modified/owid/owid_Thailand.csv")
owid_df['date'] = pd.to_datetime(owid_df['date'])
total_cases = owid_df['total_cases'].max()
owid_df_weekly = owid_df.resample('W-Mon', on='date').sum().reset_index().sort_values(by='date')
owid_df_weekly['month_year'] = owid_df_weekly['date'].dt.strftime('%b %Y')

total_vac = owid_df['people_vaccinated'].max()

death_df = read_file("Datasets/Main_Dashboard/Modified/DDC/deaths/deaths_merged.csv")
report_df = read_file("Datasets/Main_Dashboard/Modified/DDC/report/report.csv")
report_df['date'] = report_df.apply(lambda row: pd.to_datetime(f"{row['year']}-{row['weeknum']}-1", format="%Y-%W-%w"), axis=1)
total_recovered = report_df['total_recovered'].max()
total_deaths = len(death_df)

death_age_range_count = death_df['age_range'].value_counts().reset_index()
death_age_range_count.columns = ['age_range', 'count']

cases_df = read_file("Datasets/Main_Dashboard/Modified/DDC/cases/cases_merged.csv")
cases_age_range_count = cases_df['age_range'].value_counts().reset_index()
cases_age_range_count.columns = ['age_range', 'count']

st.set_page_config(
    page_title="Dashboard Covid-19 in Thailand",
    layout="wide",
    initial_sidebar_state="expanded")

col1_row1, col2_row1, col3_row1 = st.columns(3)
col1_row2, col2_row2, col3_row2 = st.columns(3)

with col1_row1:
    container = st.container(border=True)
    container.subheader("จำนวนผู้ติดเชื้อทั้งหมดในประเทศไทย")
    container.metric("จำนวนผู้ติดเชื้อ", f"{total_cases:,} ราย")
    
    fig = px.line(owid_df_weekly, x='date', y='new_cases', title='จำนวนผู้ติดเชื้อในแต่ละปี')
    
    fig.update_xaxes(
        dtick="M12",
        tickformat="%Y",
        title_text="ปีที่ระบาด"
    )

    fig.update_yaxes(
        title_text="จำนวนผู้ติดเชื้อ",
    )
    
    container.plotly_chart(fig)
    container.write("ข้อมูลจาก owid (https://ourworldindata.org)")

with col2_row1:
    container = st.container(border=True)
    def get_region(province):
        if province in north_region:
            return 'ภาคเหนือ'
        elif province in northeast_region:
            return 'ภาคตะวันออกเฉียงเหนือ'
        elif province in central_region:
            return 'ภาคกลาง'
        elif province in eastern_region:
            return 'ภาคตะวันออก'
        elif province in western_region:
            return 'ภาคตะวันตก'
        elif province in southern_region:
            return 'ภาคใต้'
        else:
            return 'ไม่สามารถระบุได้'
        
    north_region = regions.north_region
    northeast_region = regions.northeast_region
    central_region = regions.central_region
    eastern_region = regions.eastern_region
    western_region = regions.western_region
    southern_region = regions.southern_region

    death_df['region'] = death_df['province'].apply(get_region)
    deaths_by_region = death_df['region'].value_counts().reset_index()
    deaths_by_region.columns = ['Region', 'Number of Deaths']

    fig_pie = px.pie(deaths_by_region, names='Region', values='Number of Deaths', title='สัดส่วนจำนวนผู้เสียชีวิตในแต่ละภูมิภาค')

    fig_pie.update_layout(
        legend_title_text='ภาค',
        xaxis_title='จำนวนผู้เสียชีวิต',
        yaxis_title='จำนวนผู้เสียชีวิต'
    )
    
    container.subheader("จำนวนผู้เสียชีวิตในประเทศไทย")
    container.metric("จำนวนผู้เสียชีวิต", f"{total_deaths:,} ราย")
    container.plotly_chart(fig_pie)
    container.write("ข้อมูลจาก กรมควบคุมโรค (https://covid19.ddc.moph.go.th)")

with col3_row1:
    container = st.container(border=True)
    container.subheader("จำนวนผู้ป่วยที่รักษาหาย")
    container.metric("จำนวนผู้ที่หายป่วย", f"{total_recovered:,} ราย")  

    fig = px.line(report_df, x='date', y='new_recovered', title='จำนวนผู้ป่วยที่รักษาหายในแต่ละปี')

    fig.update_xaxes(
        dtick="M12",
        tickformat="%Y",
        title_text="ปีที่ระบาด"
    )

    fig.update_yaxes(
        title_text="จำนวนผู้ติดเชื้อ",
    )

    container.plotly_chart(fig)
    container.write("ข้อมูลจาก กรมควบคุมโรค (https://covid19.ddc.moph.go.th)")

with col1_row2:
    container = st.container(border=True)
    container.subheader("ช่วงอายุของผู้เสียชีวิต")

    fig = px.bar(death_age_range_count, x='age_range', y='count',
                 title='การกระจายอายุของผู้เสียชีวิต',
                 labels={'age_range': 'ช่วงอายุ', 'death_count': 'จำนวนผู้เสียชีวิต'})

    container.plotly_chart(fig)
    container.write("ข้อมูลจาก กรมควบคุมโรค (https://covid19.ddc.moph.go.th)")

with col2_row2:
    container = st.container(border=True)
    container.subheader("ช่วงอายุของผู้ติดเชื้อ")

    fig = px.bar(cases_age_range_count, x='age_range', y='count',
                 title='การกระจายอายุของผู้ติดเชื้อ',
                 labels={'age_range': 'ช่วงอายุ', 'count': 'จำนวนผู้ติดเชื้อ'})

    container.plotly_chart(fig)
    container.write("ข้อมูลจาก กรมควบคุมโรค (https://covid19.ddc.moph.go.th)")

with col3_row2:
    container = st.container(border=True)
    container.subheader("จำนวนผู้ที่ได้รับวัคซีนในประเทศไทย")
    container.metric("จำนวนผู้ที่ฉีดวัคซีน", f"{total_vac:,} ราย")  

    fig = px.line(owid_df_weekly, x='date', y='new_vaccinations', title='จำนวนผู้ติดเชื้อในแต่ละปี')

    container.plotly_chart(fig)

    container.write("ข้อมูลจาก owid (https://ourworldindata.org)")