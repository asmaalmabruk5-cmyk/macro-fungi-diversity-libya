ِ# macro-fungi-diversity-libya
National Checklist &amp; Data Analysis Pipeline for Fungi in Libya
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="دليل تشخيص وفطريات الجبل الأخضر", layout="wide")

st.title("🍄 تطبيق توثيق وتصنيف فطريات الجبل الأخضر")
st.write("دليل تفاعلي للتمييز بين الأنواع الصالحة والسامة (مثل الأجاركس) وتوثيق العينات الميدانية والمجهرية.")

# شريط جانبي للتنقل بين الأقسام
menu = st.sidebar.radio("اختر القسم:", ["الاختبار الميداني السريع (الأجاركس)", "معرض العينات الموثقة", "بيانات التوثيق"])

if menu == "الاختبار الميداني السريع (الأجاركس)":
    st.header("🔍 فحص العلامات الفارقة للسمية في جنس Agaricus")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. اختبار التفاعل اللوني لقاعدة الساق")
        yellow_staining = st.selectbox("عند خدش قاعدة الساق أو جرحها، هل يظهر لون أصفر فاقع (كبريتي)؟", ["اختر...", "نعم - أصفر فاقع سريع", "لا - لا يتغير أو يتغير للوردي/البني"])
        
    with col2:
        st.subheader("2. اختبار الرائحة")
        smell = st.selectbox("ما هي رائحة العينة؟", ["اختر...", "رائحة حبر / فينول / كيمياء نفاذة", "رائحة الفطر الطازج العطرة"])
        
    if st.button("إجراء التحليل وإعطاء النتيجة"):
        if yellow_staining == "نعم - أصفر فاقع سريع" or smell == "رائحة حبر / فينول / كيمياء نفاذة":
            st.error("⚠️ تنبيه هام: العينة تطابق صفات الأغاريكوس أصفر القشرة السام (Agaricus xanthodermus). تسبب اضطرابات معوية حادة، يُمنع استهلاكها تماماً!")
        elif yellow_staining == "لا - لا يتغير أو يتغير للوردي/البني" and smell == "رائحة الفطر الطازج العطرة":
            st.success("✅ العينة تتطابق مبدئياً مع صفات الأغاريكوس الحقلي الصالح للاستهلاك (مع التأكيد على استكمال الفحص المجهري وبصمة الأبواغ).")
        else:
            st.info("الرجاء اختيار الإجابات بدقة للحصول على النتيجة.")

elif menu == "معرض العينات الموثقة":
    st.header("📸 معرض الصور الحقلية والمجهرية")
    
    # عرض صور العينات التي قمتِ برفعها
    st.subheader("🍄 عينات الفطر الريشي والعينات الأخرى")
    
    try:
        col_a, col_b = st.columns(2)
        with col_a:
            img_rishi = Image.open("فطر الريشي.jpeg")
            st.image(img_rishi, caption="فطر الريشي - التوثيق الميداني", use_container_width=True)
        with col_b:
            img_rishi_micro = Image.open("مجهرية للريشي.jpeg")
            st.image(img_rishi_micro, caption="الفحص المجهري لأبواغ الفطر الريشي", use_container_width=True)
    except Exception as e:
        st.info("الصورة غير متوفرة حالياً في مجلد المستودع، تأكد من رفعها بالاسم الصحيح.")

elif menu == "بيانات التوثيق":
    st.header("📊 جداول وتجارب التوثيق المعشبي")
    try:
        df_naama = pd.read_excel("Agaricus_Naama_Specimen_Report_2026.xlsx")
        st.subheader("سجل عينة فطر المبلع (نعمة)")
        st.dataframe(df_naama)
    except:
        st.warning("ملف تقرير إكسل المبلع غير موجود في المستودع.")

    try:
        df_xanth = pd.read_excel("Agaricus_xanthodermus_Specimen_Report_2026.xlsx")
        st.subheader("سجل عينة الأجاركس الأصفر السام")
        st.dataframe(df_xanth)
    except:
        st.warning("ملف تقرير إكسل الأجاركس الأصفر غير موجود في المستودع.")
