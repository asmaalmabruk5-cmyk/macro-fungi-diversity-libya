import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="فطريات الجبل الأخضر - ليبيا", page_icon="🍄", layout="wide"
)

st.title("🍄 توثيق وعرض الفطريات الكبيرة في الجبل الأخضر")
st.write("استعراض بيانات العينات الحقلية والصور التوثيقية")

# تحميل ملف الإكسل
@st.cache_data
def load_data():
  # تأكدي من تطابق اسم ملف الإكسل هنا مع الملف المرفوع في الجيت هاب
  df = pd.read_excel("macrofungi_database_template.xlsx")
  return df


try:
  df = load_data()

  # اختيار العينة من القائمة
  specimen_list = df["Scientific_Name"].tolist()
  selected_specimen = st.selectbox("اختر الفطر للاستعراض:", specimen_list)

  # عرض بيانات الفطر المحدد
  specimen_data = df[df["Scientific_Name"] == selected_specimen].iloc[0]

  st.header(f"🌿 {specimen_data['Scientific_Name']}")

  col1, col2 = st.columns(2)

  with col1:
    st.subheader("معلومات الحقل والوصف")
    st.write(f"**رقم العينة:** {specimen_data['Specimen_ID']}")
    st.write(f"**الحالة الغذائية:** {specimen_data['Edibility']}")
    st.write(f"**موقع الجمع:** {specimen_data['Location']}")
    st.write(f"**تاريخ الجمع:** {specimen_data['Collection_Date']}")
    st.write(f"**الصفات الحقلية:** {specimen_data['Field_Traits']}")
    st.write(f"**الصفات المجهرية:** {specimen_data['Microscopic_Traits']}")

  with col2:
    st.subheader("الصور التوثيقية")
    # عرض صور الفطر من مجلد images
    try:
      field_img_path = f"images/{specimen_data['Field_Image']}"
      st.image(
          Image.open(field_img_path),
          caption="صورة الحقل",
          use_container_width=True,
      )
    except Exception:
      st.info("صورة الحقل غير متوفرة حالياً")

    try:
      cap_img_path = f"images/{specimen_data['Cap_Image']}"
      st.image(
          Image.open(cap_img_path),
          caption="صورة القلنسوة/الغطاء",
          use_container_width=True,
      )
    except Exception:
      pass

except Exception as e:
  st.error(f"حدث خطأ في قراءة البيانات أو ملف الإكسل: {e}")
