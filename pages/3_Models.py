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
    initial_sidebar_state="expanded"
)

st.title("แดชบอร์ดการคาดการณ์ข้อมูล")

# Function to load and preprocess data
@st.cache_data
def load_data():
    # Load the dataset (update the path if necessary)
    df = pd.read_csv("Datasets/Main_Dashboard/Modified/DDC/report/report.csv")
    
    # Convert year and weeknum to datetime
    df['date'] = df.apply(lambda row: pd.to_datetime(f"{row['year']}-{row['weeknum']}-1", format="%Y-%W-%w"), axis=1)
    df = df[['date', 'year', 'weeknum', 'new_case', 'total_case', 'new_case_excludeabroad',
             'total_case_excludeabroad', 'new_recovered', 'total_recovered', 
             'new_death', 'total_death', 'case_foreign', 'case_prison', 'case_walkin']]
    return df

# Load the data
df = load_data()

# Sidebar - Model selection
st.sidebar.header("การเลือกโมเดล")
target = st.sidebar.selectbox("เลือกเป้าหมายที่จะทำนาย", ("new_death", "new_recovered"))
model_choice = st.sidebar.selectbox("เลือกโมเดลสำหรับการคาดการณ์", ("การถดถอยเชิงเส้น (Linear Regression)", "การคาดการณ์ด้วย Random Forest"))

# Sidebar - Train/test split
test_size = st.sidebar.slider("เลือกขนาดชุดข้อมูลทดสอบ (%)", 10, 50, 20)

# Prepare data for modeling
X = df.drop(columns=[target, 'date'])  # Exclude the 'date' column for modeling
y = df[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size / 100, random_state=42)

# Model training and prediction
if model_choice == "การถดถอยเชิงเส้น (Linear Regression)":
    model = LinearRegression()
elif model_choice == "การคาดการณ์ด้วย Random Forest":
    model = RandomForestRegressor(n_estimators=100, random_state=42)

model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, predictions)

# Display results with additional performance interpretations
st.subheader(f"ผลลัพธ์ของโมเดล {model_choice}")
st.write(f"**ตัวแปรเป้าหมาย**: {target}")
st.write(f"**ค่าเฉลี่ยของข้อผิดพลาดแบบสัมบูรณ์ (MAE)**: {mae:.2f}")
if mae < 10:
    st.write("ข้อผิดพลาดเฉลี่ยต่ำ แสดงว่าโมเดลมีความแม่นยำในการทำนาย")
elif mae < 20:
    st.write("ข้อผิดพลาดเฉลี่ยปานกลาง โมเดลอาจต้องการการปรับปรุงเพิ่มเติม")
else:
    st.write("ข้อผิดพลาดเฉลี่ยสูง โมเดลอาจไม่เหมาะสมกับข้อมูล")

st.write(f"**ค่าเฉลี่ยของข้อผิดพลาดแบบยกกำลังสอง (MSE)**: {mse:.2f}")
if mse < 100:
    st.write("ค่า MSE ต่ำ แสดงว่าโมเดลมีข้อผิดพลาดรวมน้อย")
elif mse < 500:
    st.write("ค่า MSE ปานกลาง ข้อผิดพลาดยังค่อนข้างน้อย")
else:
    st.write("ค่า MSE สูง โมเดลอาจไม่แม่นยำ")

st.write(f"**ค่ารากที่สองของค่าเฉลี่ยข้อผิดพลาด (RMSE)**: {rmse:.2f}")
if rmse < 10:
    st.write("ค่า RMSE ต่ำ แสดงว่าโมเดลมีความแม่นยำสูง")
elif rmse < 20:
    st.write("ค่า RMSE ปานกลาง อาจต้องปรับปรุงโมเดล")
else:
    st.write("ค่า RMSE สูง โมเดลอาจมีข้อผิดพลาดที่สำคัญ")

st.write(f"**ค่าอธิบายสัดส่วนการกระจายของข้อมูล (R²)**: {r2:.2f}")
if r2 > 0.8:
    st.write("มีความแม่นยำสูง โมเดลอธิบายข้อมูลได้ดี")
elif r2 > 0.5:
    st.write("มีความแม่นยำปานกลาง โมเดลอธิบายข้อมูลได้พอสมควร")
else:
    st.write("มีความแม่นยำน้อย โมเดลอาจต้องการการปรับปรุง")

# Show prediction results as a DataFrame
results_df = pd.DataFrame({"ค่าจริง": y_test, "ค่าที่คาดการณ์": predictions})
st.write("## ผลลัพธ์การคาดการณ์")
st.write(results_df.head(20))

# Simulate future data based on report.csv
st.subheader("การจำลองข้อมูลในอนาคต")
days_to_simulate = st.slider("เลือกจำนวนวันในการจำลอง", 1, 60, 30)
if st.button("จำลองข้อมูลในอนาคต"):
    # Generate future dates
    future_dates = pd.date_range(df['date'].max(), periods=days_to_simulate + 1)[1:]
    
    # Simulate future data
    last_row = df.iloc[-1]
    future_data = []
    for date in future_dates:
        simulated_row = last_row.copy()
        simulated_row['date'] = date
        # Add some random noise to numeric columns to simulate future values
        for col in ['new_case', 'total_case', 'new_case_excludeabroad', 'total_case_excludeabroad',
                    'new_recovered', 'total_recovered', 'new_death', 'total_death',
                    'case_foreign', 'case_prison', 'case_walkin']:
            simulated_row[col] += np.random.randint(-10, 10)  # Adjust the range as needed for realism
            simulated_row[col] = max(0, simulated_row[col])  # Ensure no negative values
        future_data.append(simulated_row)
    
    future_df = pd.DataFrame(future_data)
    st.write("## ข้อมูลที่จำลองในอนาคต")
    st.write(future_df)
    st.line_chart(future_df.set_index("date")[[target]])
