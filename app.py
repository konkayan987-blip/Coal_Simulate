import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Advanced Coal Calculator", layout="wide", page_icon="🏭")

st.title("🏭 เครื่องคำนวณประสิทธิภาพและต้นทุนถ่านหิน (Advanced)")
st.markdown("ระบบคำนวณเชิงลึกอ้างอิงตามค่าพลังงาน kJ/kg และอุณหภูมิน้ำป้อน (Feedwater)")

# ==========================================
# ⚙️ ส่วนที่ 1: พารามิเตอร์ของระบบ (Thermodynamic Params)
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
    h_fw = st.number_input("เอนทาลปีน้ำป้อน (h_fw) [kJ/kg]", min_value=10.0, value=105.0, step=5.0, help="เช่น น้ำ 25°C = 105 kJ/kg")

# คำนวณพลังงานที่ต้องการต่อ kg steam (ตามในรูปภาพ)
energy_req_kj = h_fg + h_fw

st.info(f"💡 **พลังงานที่ต้องการต่อ kg steam:** {h_fg:,.0f} + {h_fw:,.0f} = **{energy_req_kj:,.0f} kJ/kg**")
st.markdown("---")

# ==========================================
# 📝 ส่วนที่ 2: ข้อมูลถ่านหินเปรียบเทียบ
# ==========================================
st.markdown("### 📝 ข้อมูลถ่านหินเปรียบเทียบ")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🪨 ถ่านหิน A")
    name_1 = st.text_input("ชื่อถ่านหิน A", value="AR3800 (ค่าเฉลี่ย เม.ย.)")
    hv_kcal_1 = st.number_input(f"ค่าความร้อน A (kcal/kg)", min_value=1000.0, value=3819.0, step=100.0)
    price_1 = st.number_input(f"ราคา A (บาท/kg)", min_value=0.0, value=2.65, step=0.05)
    
    # แปลงหน่วย kcal/kg เป็น kJ/kg (1 kcal = 4.184 kJ)
    hv_kj_1 = hv_kcal_1 * 4.184
    st.caption(f"แปลงเป็นหน่วย kJ/kg = {hv_kj_1:,.0f} kJ/kg")

with col2:
    st.markdown("#### 🪨 ถ่านหิน B")
    name_2 = st.text_input("ชื่อถ่านหิน B", value="AR5000")
    hv_kcal_2 = st.number_input(f"ค่าความร้อน B (kcal/kg)", min_value=1000.0, value=5000.0, step=100.0)
    price_2 = st.number_input(f"ราคา B (บาท/kg)", min_value=0.0, value=3.50, step=0.05)
    
    # แปลงหน่วย kcal/kg เป็น kJ/kg
    hv_kj_2 = hv_kcal_2 * 4.184
    st.caption(f"แปลงเป็นหน่วย kJ/kg = {hv_kj_2:,.0f} kJ/kg")

# ---------------- ฟังก์ชันคำนวณตามสูตรในรูป ----------------
def calculate_advanced(steam_tons, eff, hv_kj, price, energy_req):
    if hv_kj == 0 or eff == 0:
        return 0, 0, 0
    # สูตร: ปริมาณถ่าน (kg/hr) = (Steam(kg/hr) * Energy_Req(kJ/kg)) / (Heating_Value(kJ/kg) * Efficiency)
    steam_kg_hr = steam_tons * 1000
    consumption = (steam_kg_hr * energy_req) / (hv_kj * (eff / 100))
    
    cost_hr = consumption * price
    cost_day = consumption * price * 24
    return consumption, cost_hr, cost_day

cons_1, cost_hr_1, cost_day_1 = calculate_advanced(steam_output, efficiency, hv_kj_1, price_1, energy_req_kj)
cons_2, cost_hr_2, cost_day_2 = calculate_advanced(steam_output, efficiency, hv_kj_2, price_2, energy_req_kj)

# ==========================================
# 📊 ส่วนที่ 3: สรุปผลและกราฟเปรียบเทียบ
# ==========================================
st.markdown("---")
st.markdown("### 📊 สรุปผลการคำนวณ (Calculation Results)")

# สร้างกล่อง Dashboard แบบในรูปภาพ
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.success(f"**{name_1}**")
    m1, m2, m3 = st.columns(3)
    m1.metric("ถ่านที่ต้องใช้/ชั่วโมง", f"{cons_1:,.0f} kg")
    m2.metric("ถ่านที่ต้องใช้/วัน", f"{cons_1*24:,.0f} kg")
    m3.metric("ต้นทุนถ่าน/ชั่วโมง", f"{cost_hr_1:,.0f} บาท")

with res_col2:
    st.info(f"**{name_2}**")
    n1, n2, n3 = st.columns(3)
    n1.metric("ถ่านที่ต้องใช้/ชั่วโมง", f"{cons_2:,.0f} kg")
    n2.metric("ถ่านที่ต้องใช้/วัน", f"{cons_2*24:,.0f} kg")
    n3.metric("ต้นทุนถ่าน/ชั่วโมง", f"{cost_hr_2:,.0f} บาท")

st.markdown("<br>", unsafe_allow_html=True)

# กราฟเปรียบเทียบ
df_chart = pd.DataFrame({
    "ประเภทถ่านหิน": [name_1, name_2],
    "ต้นทุนต่อวัน (บาท)": [cost_day_1, cost_day_2],
    "ปริมาณการใช้ (kg/ชม.)": [cons_1, cons_2]
})

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_cost = px.bar(df_chart, x="ประเภทถ่านหิน", y="ต้นทุนต่อวัน (บาท)",
                      color="ประเภทถ่านหิน", text_auto='.2f',
                      title="💰 เปรียบเทียบต้นทุนรวมต่อวัน (บาท)",
                      color_discrete_sequence=["#1f77b4", "#ff7f0e"])
    fig_cost.update_traces(textposition="outside")
    fig_cost.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_cost, use_container_width=True)

with chart_col2:
    fig_cons = px.bar(df_chart, x="ประเภทถ่านหิน", y="ปริมาณการใช้ (kg/ชม.)",
                      color="ประเภทถ่านหิน", text_auto='.1f',
                      title="🔥 เปรียบเทียบปริมาณการใช้ถ่าน (kg/ชม.)",
                      color_discrete_sequence=["#1f77b4", "#ff7f0e"])
    fig_cons.update_traces(textposition="outside")
    fig_cons.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_cons, use_container_width=True)

# สรุปส่วนต่าง
st.markdown("---")
if cost_day_1 < cost_day_2:
    diff = cost_day_2 - cost_day_1
    st.warning(f"🏆 **สรุปความคุ้มค่า:** ณ ราคาและสภาวะปัจจุบัน การเลือกใช้ **{name_1}** จะประหยัดต้นทุนกว่า **{diff:,.2f} บาท/วัน**")
elif cost_day_2 < cost_day_1:
    diff = cost_day_1 - cost_day_2
    st.warning(f"🏆 **สรุปความคุ้มค่า:** ณ ราคาและสภาวะปัจจุบัน การเลือกใช้ **{name_2}** จะประหยัดต้นทุนกว่า **{diff:,.2f} บาท/วัน**")
