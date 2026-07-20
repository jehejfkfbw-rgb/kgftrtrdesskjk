import streamlit as st
import requests

# إعدادات الصفحة لتناسب متصفح جوجل كروم على الكمبيوتر والموبايل بشكل تلقائي
st.set_page_config(
    page_title="مكتبة القرآن الكريم الشاملة", 
    page_icon="📖", 
    layout="centered"  # تجعل المحتوى في منتصف الشاشة ومناسباً للهواتف
)

# تنبيهات علوية مرنة تظهر بشكل ممتاز على شاشات الموبايل
st.warning("⚠️ تنبيه: التطبيق حالياً قيد التطوير والتحسين المستمر.")
st.info("📱 تصميم مرن: هذا التطبيق يدعم التشغيل على متصفح جوجل كروم لجميع الهواتف الذكية في العالم.")

# إضافة صورة مميزة تتكيف تلقائياً مع حجم الشاشة
image_url = "https://images.unsplash.com/photo-1609599006353-e629aaabfeae?q=80&w=600&auto=format&fit=crop"
st.image(image_url, use_container_width=True, caption="📖 المَصحَف الشَّرِيف")

# عنوان التطبيق واسمك الكريم في المنتصف
st.markdown("<h1 style='text-align: center; font-size: 1.8rem;'>📖 مكتبة استماع القرآن الكريم الكبرى (114 سورة)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4CAF50; font-weight: bold;'>تطوير المبرمج: محمد عادل أحمد</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>اختر الشيخ لتظهر لك السور مباشرة في سطور عريضة سهلة اللمس</p>", unsafe_allow_html=True)

st.write("---")

# دالة جلب البيانات من السيرفر
@st.cache_data
def get_all_reciters():
    url = "https://www.mp3quran.net/api/v3/reciters?language=ar"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("reciters", [])
    except:
        return []

# أسماء الـ 114 سورة كاملة مرتبة
all_surahs = [
    "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"
]

reciters_data = get_all_reciters()

if reciters_data:
    st.write("### 📜 اختر الشيخ والسورة فوراً:")
    
    # قائمة اختيار الشيخ - تتسع تلقائياً لعرض كامل على جوجل كروم للموبايل
    reciter_names = [r["name"] for r in reciters_data]
    selected_reciter = st.selectbox("🔍 اضغط هنا واكتب اسم الشيخ أو القارئ:", reciter_names)
    
    current_reciter_data = next((r for r in reciters_data if r["name"] == selected_reciter), None)
    
    if current_reciter_data:
        moshafs = current_reciter_data.get("moshaf", [])
        if moshafs:
            server_url = moshafs[0].get("server", "")
            surah_list = moshafs[0].get("surah_list", "").split(",")
            
            if server_url and surah_list:
                st.write(f"--- تلاوات الشيخ **{selected_reciter}** المتاحة ---")
                
                # توليد السطور كأزرار عريضة (use_container_width) تناسب لمس الشاشة في كروم
                for surah_id_str in surah_list:
                    if surah_id_str.strip():
                        surah_index = int(surah_id_str) - 1
                        if 0 <= surah_index < len(all_surahs):
                            surah_name = all_surahs[surah_index]
                            formatted_id = surah_id_str.zfill(3)
                            
                            line_text = f"🎙️ {selected_reciter} —— 📖 سورة {surah_name}"
                            audio_link = f"{server_url}/{formatted_id}.mp3"
                            
                            # الزرار هنا بياخد عرض شاشة التليفون بالكامل أوتوماتيك
                            if st.button(line_text, key=f"chrome_{formatted_id}", use_container_width=True):
                                st.session_state["play_full_url"] = audio_link
                                st.session_state["play_full_title"] = f"{selected_reciter} - سورة {surah_name}"

st.write("---")

# مشغل الصوت التلقائي يظهر بشكل متناسق في أسفل شاشة الهاتف
if "play_full_url" in st.session_state:
    st.subheader("🎧 مشغل الصوت:")
    st.success(f"▶️ أنت تستمع الآن إلى: {st.session_state['play_full_title']}")
    # استخدام عنصر تشغيل الصوت القياسي المتوافق 100% مع متصفح كروم للموبايل
    st.audio(st.session_state["play_full_url"], format="audio/mp3", autoplay=True)
