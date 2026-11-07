import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="قاعدة بيانات فطريات الجبل الأخضر", page_icon="🍄", layout="wide"
)

st.title("نظام توثيق الفطريات في الجبل الأخضر - ليبيا 🍄")
st.markdown("---")

# رابط المستودع المباشر لجلب الصور بدون مشاكل المسارات المحلية
GITHUB_USER = "asmaalmabruk5-cmyk"
REPO_NAME = "macro-fungi-diversity-libya"
RAW_IMAGE_BASE_URL = (
    f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/images/"
)


# إلغاء الكاش مؤقتاً لضمان قراءة أحدث بيانات الإكسل
@st.cache_data(ttl=1)
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


  # دالة ذكية تجرب التحميل عبر الإنترنت مباشرة ثم محلياً
  def display_image(img_name, label):
    st.markdown(f"### {label}")
    if pd.isna(img_name) or str(img_name).strip() == "":
      st.info(f"{label} غير متوفرة")
      return

    clean_name = str(img_name).strip()

    # 1. التجربة الأولى: الرابط المباشر من GitHub (الأضمن والأسرع)
    remote_url = f"{RAW_IMAGE_BASE_URL}{clean_name}"

    # 2. التجربة الثانية: المسار المحلي
    local_path = os.path.join("images", clean_name)

    if os.path.exists(local_path):
      st.image(local_path, use_container_width=True)
    else:
      # عرض الصورة عبر الرابط المباشر
      st.image(remote_url, use_container_width=True)


  c1, c2, c3 = st.columns(3)
  with c1:
    display_image(specimen.get("Field_Image"), "صورة الحقل")
  with c2:
    display_image(specimen.get("Cap_Image"), "صورة القلنسوة")
  with c3:
    display_image(specimen.get("Spore_Image"), "الصورة المجهرية (الجراثيم)")

except Exception as e:
  st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
