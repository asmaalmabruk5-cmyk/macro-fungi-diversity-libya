import os
from PIL import Image
import pandas as pd
import streamlit as st

# ضبط عنوان الصفحة والتنسيق
st.set_page_config(
    page_title="قاعدة بيانات فطريات الجبل الأخضر", page_icon="🍄", layout="wide"
)

st.title("نظام توثيق الفطريات في الجبل الأخضر - ليبيا 🍄")
st.markdown("---")


# 1. تحميل البيانات من ملف الإكسل
@st.cache_data
def load_data():
  return pd.read_excel("macrofungi_database_template.xlsx")


try:
  df = load_data()

  # 2. قائمة اختيار الفطر
  selected_species = st.selectbox(
      "اختر الفطر للاستعراض:", df["Scientific_Name"].unique()
  )
  specimen = df[df["Scientific_Name"] == selected_species].iloc[0]

  # 3. عرض التفاصيل العلمية والحقلية
  st.subheader(f"🌱 معلومات العينة والوصف: {specimen['Scientific_Name']}")

  col_info1, col_info2 = st.columns(2)
  with col_info1:
    st.write(f"**رقم العينة:** {specimen['Specimen_ID']}")
    st.write(f"**الاسم بالعربية:** {specimen['Arabic_Name']}")
    st.write(f"**الحالة الغذائية:** {specimen['Edibility']}")
    st.write(f"**موقع الجمع:** {specimen['Location']}")
    st.write(f"**تاريخ الجمع:** {specimen['Collection_Date']}")

  with col_info2:
    st.write(f"**الصفات الحقلية:** {specimen['Field_Traits']}")
    st.write(f"**الصفات المجهرية:** {specimen['Microscopic_Traits']}")

  st.markdown("---")
  st.subheader("📷 الصور التوثيقية")


  # 4. دالة عرض الصور المرنة مع الامتدادات المتعددة
  def display_image(img_name, label):
    st.markdown(f"### {label}")
    if pd.isna(img_name) or str(img_name).strip() == "":
      st.info(f"{label} غير متوفرة")
      return

    clean_name = str(img_name).strip()
    base_name = os.path.splitext(clean_name)[0]

    # احتمالات المسارات المختلفة للأيقونات والصور
    possible_paths = [
        os.path.join("images", clean_name),
        os.path.join("images", f"{clean_name}.jpg"),
        os.path.join("images", f"{clean_name}.jpeg"),
        os.path.join("images", f"{base_name}.jpg"),
        os.path.join("images", f"{base_name}.jpeg"),
        os.path.join("images", f"{base_name}.jpg.jpeg"),
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
      st.warning(f"عذراً، لم يتم العثور على الملف: {clean_name}")


  # عرض الصور الثلاث في 3 أعمدة
  c1, c2, c3 = st.columns(3)
  with c1:
    display_image(specimen.get("Field_Image"), "صورة الحقل")
  with c2:
    display_image(specimen.get("Cap_Image"), "صورة القلنسوة")
  with c3:
    display_image(specimen.get("Spore_Image"), "الصورة المجهرية (الجراثيم)")

except Exception as e:
  st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
