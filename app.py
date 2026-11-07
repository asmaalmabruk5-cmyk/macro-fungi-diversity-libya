import os
from PIL import Image
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="قاعدة بيانات فطريات الجبل الأخضر", page_icon="🍄", layout="wide"
)

st.title("نظام توثيق الفطريات في الجبل الأخضر - ليبيا 🍄")
st.markdown("---")

# --- ميزة تشخيصية فورية لمكان الملفات والصور ---
with st.expander("🔍 لوحة التشخيص لمعرفة مكان الملفات والصور", expanded=True):
  st.write("**محتويات المجلد الحالي على السيرفر:**", os.listdir("."))
  if os.path.exists("images"):
    st.write(
        "**محتويات مجلد `images`:**",
        os.listdir("images")
        if os.path.isdir("images")
        else "مجلد images غير صالح",
    )
  else:
    st.warning("⚠️ تنبيه: مجلد `images` غير موجود في المسار الحالي!")
st.markdown("---")


@st.cache_data
def load_data():
  return pd.read_excel("macrofungi_database_template.xlsx")


try:
  df = load_data()

  selected_species = st.selectbox(
      "اختر الفطر للاستعراض:", df["Scientific_Name"].unique()
  )
  specimen = df[df["Scientific_Name"] == selected_species].iloc[0]

  st.subheader(
      f"🌱 معلومات العينة والوصف: {specimen.get('Scientific_Name', '')}"
  )

  col_info1, col_info2 = st.columns(2)
  with col_info1:
    st.write(f"**رقم العينة:** {specimen.get('Specimen_ID', 'N/A')}")
    if "Arabic_Name" in specimen and pd.notna(specimen["Arabic_Name"]):
      st.write(f"**الاسم بالعربية:** {specimen['Arabic_Name']}")
    st.write(f"**الحالة الغذائية:** {specimen.get('Edibility', 'N/A')}")
    st.write(f"**موقع الجمع:** {specimen.get('Location', 'N/A')}")
    st.write(f"**تاريخ الجمع:** {specimen.get('Collection_Date', 'N/A')}")

  with col_info2:
    st.write(f"**الصفات الحقلية:** {specimen.get('Field_Traits', 'N/A')}")
    st.write(
        f"**الصفات المجهرية:** {specimen.get('Microscopic_Traits', 'N/A')}"
    )

  st.markdown("---")
  st.subheader("📷 الصور التوثيقية")


  def display_image(img_name, label):
    st.markdown(f"### {label}")
    if pd.isna(img_name) or str(img_name).strip() == "":
      st.info(f"{label} غير متوفرة")
      return

    clean_name = str(img_name).strip()
    base_name = os.path.splitext(clean_name)[0]

    # قائمة مسارات شاملة تبحث في كل الاحتمالات الممكنة
    possible_paths = [
        os.path.join("images", clean_name),
        os.path.join("images", f"{clean_name}.jpg"),
        os.path.join("images", f"{base_name}.jpg"),
        clean_name,
        f"{clean_name}.jpg",
        f"{base_name}.jpg",
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


  c1, c2, c3 = st.columns(3)
  with c1:
    display_image(specimen.get("Field_Image"), "صورة الحقل")
  with c2:
    display_image(specimen.get("Cap_Image"), "صورة القلنسوة")
  with c3:
    display_image(specimen.get("Spore_Image"), "الصورة المجهرية (الجراثيم)")

except Exception as e:
  st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
