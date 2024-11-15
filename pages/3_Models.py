import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

st.set_page_config(
    page_title="แดชบอร์ดการคาดการณ์",
    layout="wide",
    initial_sidebar_state="expanded")

st.title("แดชบอร์ดการคาดการณ์ข้อมูล")

# Function to load and preprocess data
@st.cache_data
def load_data():
    # Load the dataset (update the path if necessary)
    df = pd.read_csv("Datasets/Main_Dashboard/Modified/DDC/report/report.csv")
    
    # Convert year and weeknum to datetime if needed
    df['date'] = df.apply(lambda row: pd.to_datetime(f"{row['year']}-{row['weeknum']}-1", format="%Y-%W-%w"), axis=1)
    df = df[['year', 'weeknum', 'new_case', 'total_case', 'new_case_excludeabroad',
             'total_case_excludeabroad', 'new_recovered', 'total_recovered', 
             'new_death', 'total_death', 'case_foreign', 'case_prison', 'case_walkin']]
    return df

# Load the data
df = load_data()

# Sidebar - Model selection
st.sidebar.header("การเลือกโมเดล")
target = st.sidebar.selectbox("เลือกเป้าหมายที่จะทำนาย", ("new_death", "total_death"))
model_choice = st.sidebar.selectbox("เลือกโมเดลสำหรับการคาดการณ์", ("การถดถอยเชิงเส้น (Linear Regression)", "การคาดการณ์ด้วยป่าไม้สุ่ม (Random Forest)"))

# Sidebar - Train/test split
test_size = st.sidebar.slider("เลือกขนาดชุดข้อมูลทดสอบ (%)", 10, 50, 20)

# Prepare data for modeling
X = df.drop(columns=[target])
y = df[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size / 100, random_state=42)

# Model training and prediction
if model_choice == "การถดถอยเชิงเส้น (Linear Regression)":
    model = LinearRegression()
elif model_choice == "การคาดการณ์ด้วยป่าไม้สุ่ม (Random Forest)":
    model = RandomForestRegressor(n_estimators=100, random_state=42)

model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, predictions)

# Display results
st.subheader(f"ผลลัพธ์ของโมเดล {model_choice}")
st.write(f"**ตัวแปรเป้าหมาย**: {target}")
st.write(f"**ค่าเฉลี่ยของข้อผิดพลาดแบบสัมบูรณ์ (MAE)**: {mae:.2f}")
st.write(f"**ค่าเฉลี่ยของข้อผิดพลาดแบบยกกำลังสอง (MSE)**: {mse:.2f}")
st.write(f"**ค่ารากที่สองของค่าเฉลี่ยข้อผิดพลาด (RMSE)**: {rmse:.2f}")
st.write(f"**ค่าอธิบายสัดส่วนการกระจายของข้อมูล (R2)**: {r2:.2f}")

# Show prediction results as a DataFrame
results_df = pd.DataFrame({"ค่าจริง": y_test, "ค่าที่คาดการณ์": predictions})
st.write("## ผลลัพธ์การคาดการณ์")
st.write(results_df.head(20))

# Optional: Plot actual vs. predicted values
st.subheader("ค่าจริงเทียบกับค่าที่คาดการณ์")
st.line_chart(results_df.reset_index(drop=True))