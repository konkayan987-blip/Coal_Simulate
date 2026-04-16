import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Coal Cost Calculator", layout="centered")

st.title("⚖️ เครื่องคำนวณเปรียบเทียบต้นทุนถ่านหิน")
st.markdown("โปรแกรมจำลองสำหรับเปรียบเทียบความคุ้มค่าระหว่างเชื้อเพลิงถ่านหิน 2 ชนิด")

# ---------------- ส่วนที่ 1: ตั้งค่าระบบ (Sidebar) ----------------
st.sidebar.header("⚙️ พารามิเตอร์หลัก (Global Settings)")
steam_output = st.sidebar.number_input("กำลังผลิต Steam (ตัน/ชม.)", min_value=0.0, value=4.0, step=0.5)
efficiency = st.sidebar.number_input("ประสิทธิภาพ Boiler (%)", min_value=1.0, max_value=100.0, value=66.55, step=1.0)

# ค่าคงที่เอนทัลปีที่สตรีมดูดซับ (kcal/kg)
enthalpy_diff = 564.0  

# ---------------- ส่วนที่ 2: รับค่าข้อมูลถ่านหิน (Input) ----------------
st.subheader("📝 ข้อมูลจำเพาะของถ่านหิน")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ถ่านหินชนิดที่ 1")
    name_1 = st.text_input("ชื่อชนิดที่ 1", value="AR3800")
    hv_1 = st.number_input(f"ค่าความร้อน {name_1} (kcal/kg)", min_value=1000.0, value=3819.0, step=100.0)
    price_1 = st.number_input(f"ราคา {name_1} (บาท/kg)", min_value=0.0, value=2.65, step=0.05)

with col2:
    st.markdown("#### ถ่านหินชนิดที่ 2")
    name_2 = st.text_input("ชื่อชนิดที่ 2", value="AR5000")
    hv_2 = st.number_input(f"ค่าความร้อน {name_2} (kcal/kg)", min_value=1000.0, value=5000.0, step=100.0)
    price_2 = st.number_input(f"ราคา {name_2} (บาท/kg)", min_value=0.0, value=3.50, step=0.05)

# ---------------- ส่วนที่ 3: ฟังก์ชันคำนวณ (Calculation) ----------------
def calculate_coal(steam, eff, hv, price):
    # ป้องกันการหารด้วยศูนย์
    if hv == 0 or eff == 0:
        return 0, 0, 0
    
    # สูตร: (Steam * 1000 * 564) / (HV * (Efficiency / 100))
    consumption = (steam * 1000 * enthalpy_diff) / (hv * (eff / 100))
    cost_hr = consumption * price
    cost_day = cost_hr * 24
    
    return consumption, cost_hr, cost_day

# ดึงผลลัพธ์จากฟังก์ชัน
cons_1, cost_hr_1, cost_day_1 = calculate_coal(steam_output, efficiency, hv_1, price_1)
cons_2, cost_hr_2, cost_day_2 = calculate_coal(steam_output, efficiency, hv_2, price_2)

# ---------------- ส่วนที่ 4: แสดงผลลัพธ์ (Output) ----------------
st.divider()
st.subheader("📊 ผลการประเมินต้นทุน")

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.markdown(f"**{name_1}**")
    st.metric(label="ปริมาณการใช้ (kg/ชม.)", value=f"{cons_1:,.1f}")
    st.metric(label="ต้นทุน (บาท/ชม.)", value=f"{cost_hr_1:,.2f}")
    st.metric(label="ต้นทุนรวม (บาท/วัน)", value=f"{cost_day_1:,.2f}")

with res_col2:
    st.markdown(f"**{name_2}**")
    st.metric(label="ปริมาณการใช้ (kg/ชม.)", value=f"{cons_2:,.1f}")
    st.metric(label="ต้นทุน (บาท/ชม.)", value=f"{cost_hr_2:,.2f}")
    st.metric(label="ต้นทุนรวม (บาท/วัน)", value=f"{cost_day_2:,.2f}")

# ---------------- ส่วนที่ 5: สรุปจุดคุ้มทุน (Conclusion) ----------------
st.divider()
if cost_day_1 < cost_day_2:
    diff = cost_day_2 - cost_day_1
    st.success(f"💡 **ข้อเสนอแนะ:** เลือกใช้ **{name_1}** จะช่วยประหยัดต้นทุนได้มากกว่า **{diff:,.2f} บาท/วัน**")
elif cost_day_2 < cost_day_1:
    diff = cost_day_1 - cost_day_2
    st.success(f"💡 **ข้อเสนอแนะ:** เลือกใช้ **{name_2}** จะช่วยประหยัดต้นทุนได้มากกว่า **{diff:,.2f} บาท/วัน**")
else:
    st.info("💡 **ข้อเสนอแนะ:** ถ่านหินทั้ง 2 ชนิดมีต้นทุนรวมเท่ากันพอดี")
