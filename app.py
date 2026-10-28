app.py
import streamlit as st

# عنوان التطبيق
st.title("نظام تشخيص وتصنيف الفطريات الكبيرة 🍄")

# نص تعريفي
st.write("أهلاً بكِ في منصة التحليل الميداني لدراسة تنوع الفطريات الكبيرة في ليبيا.")

# إضافة زر رفع الصور للتجربة
uploaded_file = st.file_uploader("اختر صورة الفطر أو العينة...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="تم رفع الصورة بنجاح", use_column_width=True)
    st.success("جاهز للتحليل والتصنيف الآلي!")
