import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บเป็นแนวกว้างเพื่อให้ดูกราฟได้สวยงาม
st.set_page_config(page_title="Coal Cost Calculator", layout="wide", page_icon="⚖️")

st.title("⚖️ เครื่องคำนวณเปรียบเทียบต้นทุนถ่านหิน")
st.markdown("จำลองการใช้เชื้อเพลิง พร้อมกราฟเปรียบเทียบความคุ้มค่าแบบ Real-time")

# ==========================================
# ⚙️ ส่วนที่ 1: ตัวแปรหลัก (Global Parameters)
# ==========================================
st.markdown("### ⚙️ ตัวแปรหลักของระบบ")
c1, c2, c3, c4 = st.columns(4)

with c1:
    steam_output = st.number_input("ปริมาณไอน้ำ (ตัน/ชม.)", min_value=0.0, value=4.0, step=0.5)
with c2:
    efficiency = st.number_input("ประสิทธิภาพ Boiler (%)", min_value=1.0, max_value=100.0, value=80.0, step=1.0)
with c3:
    enthalpy_diff = st.number_input("ผลต่างเอนทาลปี (kcal/kg)", min_value=1.0, value=564.0, step=1.0)
with c4:
    work_hours = st.number_input("ชั่วโมงการทำงาน (ชม./วัน)", min_value=1, max_value=24, value=24)

st.markdown("---")

# ==========================================
# 📝 ส่วนที่ 2: ข้อมูลถ่านหิน (Coal Inputs)
# ==========================================
st.markdown("### 📝 ข้อมูลถ่านหินเปรียบเทียบ")
col1, col2 = st.columns(2)

with col1:
    st.info("**ถ่านหิน A**")
    name_1 = st.text_input("ชื่อถ่านหิน A", value="AR3800")
    hv_1 = st.number_input(f"ค่าความร้อน A (kcal/kg)", min_value=1000.0, value=3819.0, step=100.0)
    price_1 = st.number_input(f"ราคา A (บาท/kg)", min_value=0.0, value=2.65, step=0.05)

with col2:
    st.success("**ถ่านหิน B**")
    name_2 = st.text_input("ชื่อถ่านหิน B", value="AR5000")
    hv_2 = st.number_input(f"ค่าความร้อน B (kcal/kg)", min_value=1000.0, value=5000.0, step=100.0)
    price_2 = st.number_input(f"ราคา B (บาท/kg)", min_value=0.0, value=3.50, step=0.05)

# ฟังก์ชันคำนวณ
def calculate_coal(steam, eff, hv, price, enthalpy, hours):
    if hv == 0 or eff == 0:
        return 0, 0, 0
    # สูตร: (Steam * 1000 * Enthalpy) / (HV * (Efficiency / 100))
    consumption = (steam * 1000 * enthalpy) / (hv * (eff / 100))
    cost_hr = consumption * price
    cost_day = cost_hr * hours
    return consumption, cost_hr, cost_day

# ดึงผลลัพธ์
cons_1, cost_hr_1, cost_day_1 = calculate_coal(steam_output, efficiency, hv_1, price_1, enthalpy_diff, work_hours)
cons_2, cost_hr_2, cost_day_2 = calculate_coal(steam_output, efficiency, hv_2, price_2, enthalpy_diff, work_hours)

# ==========================================
# 📊 ส่วนที่ 3: กราฟแสดงผล (Visualizations)
# ==========================================
st.markdown("---")
st.markdown("### 📊 กราฟเปรียบเทียบ (Visual Comparison)")

# สร้าง Dataframe สำหรับทำกราฟ
df_chart = pd.DataFrame({
    "ประเภทถ่านหิน": [name_1, name_2],
    "ต้นทุนต่อวัน (บาท)": [cost_day_1, cost_day_2],
    "ปริมาณการใช้ (kg/ชม.)": [cons_1, cons_2]
})

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # กราฟแท่ง: เปรียบเทียบต้นทุน (เน้นเรื่องเงิน)
    fig_cost = px.bar(df_chart, x="ประเภทถ่านหิน", y="ต้นทุนต่อวัน (บาท)",
                      color="ประเภทถ่านหิน", text_auto='.2f',
                      title="💰 ต้นทุนรวมต่อวัน (บาท)",
                      color_discrete_sequence=["#1f77b4", "#2ca02c"]) # สีฟ้า และ เขียว
    fig_cost.update_traces(textfont_size=14, textposition="outside", cliponaxis=False)
    fig_cost.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_cost, use_container_width=True)

with chart_col2:
    # กราฟแท่ง: เปรียบเทียบปริมาณการใช้
    fig_cons = px.bar(df_chart, x="ประเภทถ่านหิน", y="ปริมาณการใช้ (kg/ชม.)",
                      color="ประเภทถ่านหิน", text_auto='.1f',
                      title="🔥 ปริมาณการใช้ถ่าน (kg/ชม.)",
                      color_discrete_sequence=["#ff7f0e", "#d62728"]) # สีส้ม และ แดง
    fig_cons.update_traces(textfont_size=14, textposition="outside", cliponaxis=False)
    fig_cons.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_cons, use_container_width=True)

# ==========================================
# 💡 ส่วนที่ 4: สรุปผลลัพธ์ (Summary Box)
# ==========================================
st.markdown("---")
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric(label=f"ต้นทุน {name_1} (บาท/ชั่วโมง)", value=f"{cost_hr_1:,.2f} ฿")
with res_col2:
    st.metric(label=f"ต้นทุน {name_2} (บาท/ชั่วโมง)", value=f"{cost_hr_2:,.2f} ฿")

# คำนวณส่วนต่างและแนะนำ
if cost_day_1 < cost_day_2:
    diff = cost_day_2 - cost_day_1
    st.success(f"🏆 **สรุป:** เลือกใช้ **{name_1}** ประหยัดกว่า **{diff:,.2f} บาท/วัน**")
elif cost_day_2 < cost_day_1:
    diff = cost_day_1 - cost_day_2
    st.success(f"🏆 **สรุป:** เลือกใช้ **{name_2}** ประหยัดกว่า **{diff:,.2f} บาท/วัน**")
else:
    st.info("⚖️ **สรุป:** ถ่านหินทั้ง 2 ชนิดมีต้นทุนรวมเท่ากันพอดี")
