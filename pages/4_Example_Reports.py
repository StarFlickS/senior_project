import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="รายงานการวิเคราะห์ COVID-19",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("ตัวอย่างรายงานการวิเคราะห์ COVID-19")

# โหลดชุดข้อมูล
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

# 1. แนวโน้มและจำนวนผู้ติดเชื้อ COVID-19 รายวัน
st.header("1. แนวโน้มและจำนวนผู้ติดเชื้อ COVID-19 รายวัน")
fig1 = px.line(report_df, x='date', y='new_case', title="จำนวนผู้ติดเชื้อ COVID-19 รายวัน")
st.plotly_chart(fig1)

# 2. จำนวนผู้ติดเชื้อ COVID-19 สะสม
st.header("2. จำนวนผู้ติดเชื้อ COVID-19 สะสม")
fig2 = px.line(report_df, x='date', y='total_case', title="จำนวนผู้ติดเชื้อ COVID-19 สะสม")
st.plotly_chart(fig2)

# 3. แนวโน้มผู้เสียชีวิตรายใหม่และอัตราการเสียชีวิต (ข้อมูลที่ใช้แทน)
st.header("3. แนวโน้มผู้เสียชีวิตรายใหม่และอัตราการเสียชีวิต (ข้อมูลที่ใช้แทน)")
fig3 = px.line(report_df, x='date', y='new_death', title="จำนวนผู้เสียชีวิต COVID-19 รายวัน") if 'new_death' in report_df.columns else st.write("ไม่พบคอลัมน์ 'new_death'")
st.plotly_chart(fig3)

# 4. อัตราการเสียชีวิตตามช่วงเวลา (ข้อมูลที่ใช้แทน)
st.header("4. อัตราการเสียชีวิตตามช่วงเวลา")
if 'total_case' in report_df.columns and 'total_death' in report_df.columns:
    report_df['death_rate'] = (report_df['total_death'] / report_df['total_case']) * 100
    fig4 = px.line(report_df, x='date', y='death_rate', title="อัตราการเสียชีวิตของ COVID-19 ตามช่วงเวลา")
    st.plotly_chart(fig4)
else:
    st.write("ไม่พบคอลัมน์ 'total_case' หรือ 'total_death'")

# 5. การกระจายช่วงอายุของผู้ติดเชื้อตามจังหวัด
st.header("5. การกระจายช่วงอายุของผู้ติดเชื้อตามจังหวัด")
selected_provinces = st.multiselect("เลือกจังหวัดเพื่อเปรียบเทียบ", sorted(death_df['province'].unique()), default="กรุงเทพมหานคร")
age_data = death_df[death_df['province'].isin(selected_provinces)]
fig5 = px.bar(age_data, x='province', color='age_range', title="การกระจายช่วงอายุของผู้ติดเชื้อตามจังหวัด", barmode='stack')
st.plotly_chart(fig5)

# 6. ผู้ติดเชื้อ COVID-19 ที่ไม่นำเข้าจากต่างประเทศ
st.header("6. ผู้ติดเชื้อ COVID-19 เฉพาะภายในประเทศ")
fig6 = px.line(report_df, x='date', y='new_case_excludeabroad', title="จำนวนผู้ติดเชื้อ COVID-19 ในประเทศเท่านั้น")
st.plotly_chart(fig6)

# 7. ผลกระทบต่อกลุ่มอาชีพต่าง ๆ จาก COVID-19
st.header("7. ผลกระทบต่อกลุ่มอาชีพต่าง ๆ จาก COVID-19")
if 'occupation' in death_df.columns:
    occupation_cases = death_df['occupation'].value_counts().reset_index()
    occupation_cases.columns = ['occupation', 'count']
    fig7 = px.bar(occupation_cases, x='occupation', y='count', title="จำนวนผู้ติดเชื้อ COVID-19 ตามอาชีพ")
    st.plotly_chart(fig7)
else:
    st.write("ไม่พบคอลัมน์ 'occupation' ในชุดข้อมูล")

# 8. ผู้หายป่วยรายสัปดาห์
st.header("8. ผู้หายป่วยรายสัปดาห์")
fig8 = px.line(report_df, x='date', y='new_recovered', title="ผู้หายป่วยรายสัปดาห์")
st.plotly_chart(fig8)

# 9. ผู้ติดเชื้อ COVID-19 ในเรือนจำและผู้ที่เข้ารับการรักษาเอง
st.header("9. ผู้ติดเชื้อ COVID-19 ในเรือนจำและผู้ที่เข้ารับการรักษาเอง")
if 'case_prison' in report_df.columns and 'case_walkin' in report_df.columns:
    fig9 = px.line(report_df, x='date', y=['case_prison', 'case_walkin'], title="ผู้ติดเชื้อ COVID-19 ในเรือนจำและผู้ที่เข้ารับการรักษาเอง")
    st.plotly_chart(fig9)
else:
    st.write("ไม่พบคอลัมน์ 'case_prison' หรือ 'case_walkin'")

# 10. จำนวนผู้ติดเชื้อรวมตามจังหวัด
st.header("10. จำนวนผู้ติดเชื้อรวมตามจังหวัด")
if 'province' in death_df.columns:
    province_cases = death_df['province'].value_counts().reset_index()
    province_cases.columns = ['province', 'count']
    fig10 = px.bar(province_cases, x='province', y='count', title="จำนวนผู้ติดเชื้อ COVID-19 รวมตามจังหวัด")
    st.plotly_chart(fig10)
else:
    st.write("ไม่พบคอลัมน์ 'province' ในชุดข้อมูล")
