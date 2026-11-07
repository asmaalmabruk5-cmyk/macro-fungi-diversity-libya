from PIL import Image
import pandas as pd
import streamlit as st

st.title("نظام توثيق الفطريات في الجبل الأخضر - ليبيا 🍄")

# 1. قراءة ملف الإكسل
@st.cache_data
def load_data():
  return pd.read_excel("macrofungi_database_template.xlsx")


df = load_data()

# 2. اختيار الفطر من القائمة
selected_species = st.selectbox(
    "اختر الفطر للاستعراض:", df["Scientific_Name"].unique()
)
specimen = df[df["Scientific_Name"] == selected_species].iloc[0]

# 3. عرض تفاصيل العينة
st.subheader(f"معلومات الحقل والوصف: {specimen['Scientific_Name']}")
st.write(f"**رقم العينة:** {specimen['Specimen_ID']}")
st.write(f"**الحالة الغذائية:** {specimen['Edibility']}")
st.write(f"**موقع الجمع:** {specimen['Location']}")
st.write(f"**تاريخ الجمع:** {specimen['Collection_Date']}")

# 4. عرض الصور الثلاث المرتبطة (الحقل، القلنسوة، الجراثيم)
st.subheader("الصور التوثيقية")

col1, col2, col3 = st.columns(3)

# عرض صورة الحقل
with col1:
  st.markdown("**صورة الحقل**")
  field_img_name = str(specimen["Field_Image"]).strip()
  try:
    img_field = Image.open(f"images/{field_img_name}")
    st.image(img_field, use_container_width=True)
  except Exception:
    st.info("صورة الحقل غير متوفرة حالياً")

# عرض صورة القلنسوة
with col2:
  st.markdown("**صورة القلنسوة**")
  cap_img_name = str(specimen["Cap_Image"]).strip()
  try:
    img_cap = Image.open(f"images/{cap_img_name}")
    st.image(img_cap, use_container_width=True)
  except Exception:
    st.info("صورة القلنسوة غير متوفرة حالياً")

# عرض صورة الجراثيم
with col3:
  st.markdown("**الصورة المجهرية (الجراثيم)**")
  spore_img_name = str(specimen["Spore_Image"]).strip()
  try:
    img_spore = Image.open(f"images/{spore_img_name}")
    st.image(img_spore, use_container_width=True)
  except Exception:
    st.info("الصورة المجهرية غير متوفرة حالياً")
