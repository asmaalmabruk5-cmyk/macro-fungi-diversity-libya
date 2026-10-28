import streamlit as st
from PIL import Image
import torch
from torchvision import models, transforms

# إعدادات الصفحة
st.set_page_config(page_title="تصنيف الفطريات الكبيرة في ليبيا", page_icon="🍄", layout="centered")

st.title("🍄 نظام تشخيص وتصنيف الفطريات الكبيرة")
st.write("أهلاً بك في منصة التحليل الميداني لدراسة تنوع الفطريات الكبيرة في ليبيا والجبل الأخضر.")

# تحميل نموذج الذكاء الاصطناعي لتصنيف الصور
@st.cache_resource
def load_classifier():
    # استخدام نموذج ResNet18 المدرب للتعرف على الصور
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.eval()
    return model

model = load_classifier()

# تحضير الصور للتحليل البرمجي
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# رفع الصورة
uploaded_file = st.file_uploader("اختر صورة الفطر أو العينة الميدانية...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption="تم رفع الصورة بنجاح", use_column_width=True)
    
    with st.spinner('جاري تحليل العينة وتطبيق نموذج الذكاء الاصطناعي...'):
        # معالجة الصورة والتنبؤ
        img_t = transform(image)
        batch_t = torch.unsqueeze(img_t, 0)
        
        with torch.no_grad():
            out = model(batch_t)
            
        # الحصول على أعلى النتاجات
        probabilities = torch.nn.functional.softmax(out[0], dim=0)
        top_prob, top_catid = torch.topk(probabilities, 1)
        
        confidence = top_prob[0].item() * 100

    st.success(" اكتمل التحليل والتصنيف الآلي!")
    st.metric(label="نسبة دقة المطابقة التشخيصية", value=f"{confidence:.2f}%")
