import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Advanced Coal Calculator", layout="wide", page_icon="🏭")

st.title("🏭 เครื่องคำนวณประสิทธิภาพและต้นทุนถ่านหิน (Advanced)")

# ข้อมูลถ่านหินมาตรฐาน (kcal/kg)
COAL_DATA = {
    "AR3500": 3500.0,
    "AR3800": 3819.0, # อ้างอิงค่าเดิมของคุณ
    "AR4200": 4200.0,
    "AR5000": 5000.0,
    "กำหนดเอง (Custom)": 0.0
}

# ==========================================
# ⚙️ ส่วนที่ 1: พารามิเตอร์ของระบบ
# ==========================================
st.markdown("### ⚙️ พารามิเตอร์ของ Boiler และ Steam")
c1, c2, c3, c4 = st.columns(4)

with c1:
    steam_output = st.number_input("กำลังผลิตไอน้ำ (ตัน/ชม.)", min_value=0.0, value=4.0, step=0.5)
with c2:
    efficiency = st.number_input("ประสิทธิภาพ Boiler (%)", min_value=1.0, max_value=100.0, value=80.0, step=1.0)
with c3:
    h_fg = st.number_input("ค่าความร้อนแฝง (h_fg) [kJ/kg]", min_value=1000.0, value=2257.0, step=10.0)
with c4:
    h_fw = st.number_input("เอนทาลปีน้ำป้อน (h_fw) [kJ/kg]", min_value=10.0, value=105.0, step=5.0)

energy_req_kj = h_fg + h_fw
st.info(f"💡 พลังงานที่ต้องการต่อ kg steam: **{energy_req_kj:,.0f} kJ/kg**")

# ==========================================
# 📝 ส่วนที่ 2: ข้อมูลถ่านหินเปรียบเทียบ (ปรับปรุงใหม่)
# ==========================================
st.markdown("### 📝 ข้อมูลถ่านหินเปรียบเทียบ")
col1, col2 = st.columns(2)

def get_coal_input(label, default_type, default_price):
    st.markdown(f"#### 🪨 ถ่านหิน {label}")
    selected_type = st.selectbox(f"เลือกชนิดถ่านหิน {label}", options=list(COAL_DATA.keys()), index=list(COAL_DATA.keys()).index(default_type))
    
    if selected_type == "กำหนดเอง (Custom)":
        hv_kcal = st.number_input(f"ระบุค่าความร้อน {label} (kcal/kg)", min_value=1000.0, value=3500.0, step=100.0)
    else:
        hv_kcal = COAL_DATA[selected_type]
        st.write(f"ค่าความร้อน: **{hv_kcal:,.0f}** kcal/kg")
    
    price = st.number_input(f"ราคา {label} (บาท/kg)", min_value=0.0, value=default_price, step=0.05, key=f"price_{label}")
    hv_kj = hv_kcal * 4.184
    return selected_type, hv_kj, price

with col1:
    name_1, hv_kj_1, price_1 = get_coal_input("A", "AR3800", 2.65)

with col2:
    name_2, hv_kj_2, price_2 = get_coal_input("B", "AR5000", 3.50)

# ---------------- ฟังก์ชันคำนวณ ----------------
def calculate_advanced(steam_tons, eff, hv_kj, price, energy_req):
    if hv_kj == 0 or eff == 0: return 0, 0, 0
    steam_kg_hr = steam_tons * 1000
    consumption = (steam_kg_hr * energy_req) / (hv_kj * (eff / 100))
    cost_hr = consumption * price
    cost_day = cost_hr * 24
    return consumption, cost_hr, cost_day

cons_1, cost_hr_1, cost_day_1 = calculate_advanced(steam_output, efficiency, hv_kj_1, price_1, energy_req_kj)
cons_2, cost_hr_2, cost_day_2 = calculate_advanced(steam_output, efficiency, hv_kj_2, price_2, energy_req_kj)

# ==========================================
# 📊 ส่วนที่ 3: สรุปผล
# ==========================================
st.markdown("---")
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.success(f"**{name_1}**")
    st.metric("ใช้ถ่าน/ชม.", f"{cons_1:,.0f} kg")
    st.metric("ต้นทุน/วัน", f"{cost_day_1:,.0f} บาท")

with res_col2:
    st.info(f"**{name_2}**")
    st.metric("ใช้ถ่าน/ชม.", f"{cons_2:,.0f} kg")
    st.metric("ต้นทุน/วัน", f"{cost_day_2:,.0f} บาท")

# (ส่วนของกราฟ Plotly และการสรุปส่วนต่างคงเดิม)
