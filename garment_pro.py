import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import datetime
import os

# --- كود الـ SEO (هنا التعديل اللي هيغير اسم الموقع فوق وفي جوجل) ---
st.set_page_config(
    page_title="Production Expert BA | خبير إنتاج الملابس", 
    layout="wide",
    page_icon="📊"
)

# إضافة ميتا تاق لجوجل
st.markdown('<meta name="description" content="Production Expert BA - أقوى نظام رقمي لحساب كفاءة الإنتاج والتكاليف لمصانع الملابس">', unsafe_allow_html=True)

# --- باقي الكود الشغال بتاعك ---
USER_FILE = "users_db.csv"

def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    return pd.DataFrame(columns=["username", "password", "factory_name"])

def save_user(username, password, factory):
    df = load_users()
    if username in df['username'].values:
        return False
    new_user = pd.DataFrame([[username, password, factory]], columns=["username", "password", "factory_name"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Garment Ultimate ERP", layout="wide")

# --- 2. إدارة قاعدة بيانات المستخدمين ---
USER_FILE = "users_db.csv"

def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    return pd.DataFrame(columns=["username", "password", "factory_name"])

def save_user(username, password, factory):
    df = load_users()
    if username in df['username'].values:
        return False
    new_user = pd.DataFrame([[username, password, factory]], columns=["username", "password", "factory_name"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

# --- 3. دالة الـ PDF الاحترافية ---
def create_comprehensive_pdf(factory_name, date, results_dict, logo_file=None):
    pdf = FPDF()
    pdf.add_page()
    if logo_file:
        try:
            with open("temp_logo.png", "wb") as f: f.write(logo_file.getbuffer())
            pdf.image("temp_logo.png", x=10, y=8, w=30)
            pdf.ln(20)
        except: pdf.ln(10)
    else: pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Comprehensive Plant Performance Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 7, txt=f"Factory: {factory_name} | Date: {date}", ln=True, align='C')
    pdf.ln(5)

    pdf.set_fill_color(44, 62, 80); pdf.set_text_color(255, 255, 255)
    pdf.cell(110, 10, "Metric Description", 1, 0, 'L', 1)
    pdf.cell(80, 10, "Final Result", 1, 1, 'C', 1)

    pdf.set_text_color(0, 0, 0); pdf.set_font("Arial", size=9)
    for label, value in results_dict.items():
        clean_v = str(value).encode('latin-1', 'ignore').decode('latin-1')
        pdf.cell(110, 8, label, 1)
        pdf.cell(80, 8, clean_v, 1, 1, 'C')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 4. إدارة الحالة ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_factory" not in st.session_state:
    st.session_state["user_factory"] = ""

# --- 5. واجهة الدخول والتسجيل ---
if not st.session_state["authenticated"]:
    st.title("🛡️ نظام إدارة مصانع الملابس الذكي")
    tab_login, tab_signup = st.tabs(["🔑 تسجيل الدخول", "📝 تسجيل مصنع جديد"])
    
    with tab_login:
        l_user = st.text_input("اسم المستخدم", key="login_user")
        l_pwd = st.text_input("كلمة المرور", type="password", key="login_pwd")
        if st.button("دخول النظام"):
            users_df = load_users()
            user_data = users_df[(users_df['username'] == l_user) & (users_df['password'] == l_pwd)]
            if not user_data.empty:
                st.session_state["authenticated"] = True
                st.session_state["user_factory"] = user_data.iloc[0]['factory_name']
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")

    with tab_signup:
        s_factory = st.text_input("اسم المصنع بالكامل")
        s_user = st.text_input("اختر اسم مستخدم")
        s_pwd = st.text_input("اختر كلمة مرور", type="password")
        if st.button("إنشاء حساب والدخول فوراً"):
            if s_factory and s_user and s_pwd:
                if save_user(s_user, s_pwd, s_factory):
                    st.session_state["authenticated"] = True
                    st.session_state["user_factory"] = s_factory
                    st.rerun()
                else:
                    st.error("اسم المستخدم موجود بالفعل")
            else:
                st.warning("الرجاء ملء كافة الحقول")

# --- 6. النظام الرئيسي ---
else:
    st.sidebar.success(f"🏢 مصنع: {st.session_state['user_factory']}")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title(f"📊 لوحة تحكم: {st.session_state['user_factory']}")

    # صندوق المعطيات
    with st.expander("🛠️ إدخال المعطيات اليومية", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            s_date = st.date_input("تاريخ اليوم", datetime.date.today())
            workers = st.number_input("إجمالي العمال", value=30, min_value=1)
            machines = st.number_input("عدد الماكينات", value=25)
        with c2:
            hours = st.number_input("ساعات العمل", value=8.0)
            sam_val = st.number_input("الزمن القياسي (SAM)", value=2.0)
        with c3:
            actual_pcs = st.number_input("الإنتاج الفعلي", value=500)
            absent_count = st.number_input("عدد الغائبين", value=2)
            target_eff_pct = st.slider("الكفاءة المستهدفة (%)", 10, 100, 75)
        with c4:
            daily_wages = st.number_input("الأجور اليومية", value=1500)
            rework_pcs = st.number_input("قطع الـ Rework", value=10)
            f_gsm = st.number_input("وزن القماش (GSM)", value=200)

    # --- الحسابات المنفصلة ---
    available_mins = workers * hours * 60
    produced_mins = actual_pcs * sam_val
    line_eff = (produced_mins / available_mins) * 100 if available_mins > 0 else 0
    worker_prod = actual_pcs / workers if workers > 0 else 0
    max_cap = available_mins / sam_val
    actual_cap = ((workers - absent_count) * hours * 60) / sam_val
    lost_mins = available_mins - produced_mins
    cost_pc = daily_wages / actual_pcs if actual_pcs > 0 else 0
    
    # حسابات القماش (Marker Equations)
    marker_length = 120 # سم
    marker_width = 160 # سم
    cons_pc = (marker_length * marker_width * f_gsm) / 1000000 # كجم/قطعة
    total_fabric_needed = cons_pc * actual_pcs
    fabric_waste = total_fabric_needed * 0.03 # 3% هالك
    total_with_waste = total_fabric_needed + fabric_waste

    # --- عرض التبويبات (مليئة بالبيانات) ---
    st.write("---")
    t1, t2, t3, t4, t5 = st.tabs(["📦 الإنتاج", "📈 الكفاءة", "💰 التكاليف", "⏱️ الطاقة والوقت", "🧵 القماش"])

    with t1:
        st.subheader("📊 أداء الإنتاج")
        c_p1, c_p2 = st.columns(2)
        c_p1.metric("الإنتاج الفعلي", f"{actual_pcs} Pcs")
        c_p2.metric("إنتاجية العامل", f"{worker_prod:.2f}")

    with t2:
        st.subheader("📈 تحليل الكفاءة")
        c_e1, c_e2 = st.columns(2)
        c_e1.metric("كفاءة الخط", f"{line_eff:.2f}%")
        c_e2.metric("كفاءة العمالة", f"{line_eff:.1f}%")

    with t3:
        st.subheader("💰 تحليل التكاليف")
        c_c1, c_c2 = st.columns(2)
        c_c1.metric("تكلفة العمالة/قطعة", f"{cost_pc:.2f} EGP")
        c_c2.metric("قطع الـ Rework", f"{rework_pcs} Pcs")

    with t4:
        st.subheader("⏱️ دراسة الطاقة والوقت (مليء)")
        c_t1, c_t2, c_t3, c_t4 = st.columns(4)
        # هنا المعادلات اللي كانت ناقصة
        c_t1.metric("الطاقة القصوى (100%)", f"{int(max_cap)} Pcs")
        c_t2.metric("الطاقة الفعلية المتاحة", f"{int(actual_cap)} Pcs")
        c_t3.metric("الدقائق المتاحة", f"{available_mins} Min")
        c_t4.metric("الدقائق المفقودة", f"{lost_mins} Min")
        
        st.info(f"إجمالي زمن الإنتاج الفعلي: {produced_mins} دقيقة")

    with t5:
        st.subheader("🧵 حسابات القماش (مليء)")
        c_f1, c_f2, c_f3 = st.columns(3)
        # هنا معادلات القماش كاملة
        c_f1.metric("استهلاك القطعة", f"{cons_pc:.3f} كجم")
        c_f2.metric("القماش المطلوب", f"{total_fabric_needed:.2f} كجم")
        c_f3.metric("الهالك (3%)", f"{fabric_waste:.2f} كجم")
        
        st.success(f"إجمالي وزن القماش شامل الهالك: {total_with_waste:.2f} كجم")

    # زر الـ PDF
    if st.button("📥 تحميل التقرير الشامل"):
        res = {
            "Efficiency": f"{line_eff:.2f}%",
            "Max Capacity": f"{int(max_cap)} Pcs",
            "Lost Minutes": f"{lost_mins} Min",
            "Fabric Needed": f"{total_fabric_needed:.2f} Kg",
            "Consumption/Pc": f"{cons_pc:.3f} Kg"
        }
        pdf_bytes = create_comprehensive_pdf(st.session_state['user_factory'], s_date, res)
        st.download_button("تحميل الملف الآن", data=pdf_bytes, file_name="Full_Report.pdf")