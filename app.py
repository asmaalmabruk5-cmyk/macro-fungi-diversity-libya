import os
from PIL import Image
import pandas as pd
import streamlit as st

st.title("نظام توثيق الفطريات في الجبل الأخضر - ليبيا 🍄")


@st.cache_data
def load_data():
  return pd.read_excel("macrofungi_database_template.xlsx")


df = load_data()

selected_species = st.selectbox(
    "اختر الفطر للاستعراض:", df["Scientific_Name"].unique()
)
specimen = df[df["Scientific_Name"] == selected_species].iloc[0]

st.subheader(f"معلومات الحقل والوصف: {specimen['Scientific_Name']}")
st.write(f"**رقم العينة:** {specimen['Specimen_ID']}")
st.write(f"**الحالة الغذائية:** {specimen['Edibility']}")
st.write(f"**موقع الجمع:** {specimen['Location']}")
st.write(f"**تاريخ الجمع:** {specimen['Collection_Date']}")
st.write(f"**الصفات الحقلية:** {specimen['Field_Traits']}")
st.write(f"**الصفات المجهرية:** {specimen['Microscopic_Traits']}")


# دالة ذكية للبحث عن الصورة وعرضها حتى لو كان الامتداد مختلفاً
def display_image(img_name, label):
  st.markdown(f"**{label}**")
  if pd.isna(img_name) or str(img_name).strip() == "":
    st.info(f"{label} غير متوفرة")
    return

  img_name = str(img_name).strip()
  possible_paths = [
      os.path.join("images", img_name),
      os.path.join("images", img_name + ".jpeg"),
      os.path.join("images", img_name + ".jpg"),
      os.path.join("images", img_name + ".jpg.jpeg"),
  ]

  loaded_img = None
  for path in possible_paths:
    if os.path.exists(path):
      try:
        loaded_img = Image.open(path)
        break
      except Exception:
        continue

  if loaded_img:
    st.image(loaded_img, use_container_width=True)
  else:
    st.info(f"عذراً، لم يتم العثور على الملف: {img_name}")


st.subheader("الصور التوثيقية")
col1, col2, col3 = st.columns(3)

with col1:
  display_image(specimen.get("Field_Image"), "صورة الحقل")

with col2:
  display_image(specimen.get("Cap_Image"), "صورة القلنسوة")

with col3:
  display_image(specimen.get("Spore_Image"), "الصورة المجهرية (الجراثيم)")
