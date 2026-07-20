import streamlit as st
import requests

# إعدادات الصفحة لتناسب جميع الهواتف والكمبيوتر
st.set_page_config(page_title="مكتبة القرآن الكريم الشاملة", page_icon="📖", layout="centered")

# التنبيهات العلوية
st.warning("⚠️ تنبيه: التطبيق حالياً قيد التطوير والتحسين المستمر.")
st.info("📱 تصميم مرن: هذا التطبيق يدعم التشغيل على جميع الهواتف الذكية والأجهزة اللوحية في العالم.")

st.markdown("<h1 style='text-align: center;'>📖 مكتبة استماع القرآن الكريم الكبرى (114 سورة)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>اضغط على الزر بالأسفل لفتح قائمة التلاوات لجميع سور القرآن الكريم</p>", unsafe_allow_html=True)

st.write("---")

# دالة لجلب قائمة كل القراء من السيرفر
@st.cache_data
def get_all_reciters():
    url = "https://www.mp3quran.net/api/v3/reciters?language=ar"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("reciters", [])
    except:
        return []

# قائمة بأسماء كل سور القرآن الكريم بالترتيب (114 سورة)
all_surahs = [
    "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد", "الإخلاص", "الفلق", "الناس"
]

reciters_data = get_all_reciters()

# زر رئيسي لفتح قائمة الاستماع الكبرى
if st.button("🎧 اضغط هنا لفتح قائمة استماع القرآن الكريم كاملاً (114 سورة)", use_container_width=True, type="primary"):
    st.session_state["show_full_quran"] = True

# عرض السطور عند الضغط على الزر
if st.session_state.get("show_full_quran", False) and reciters_data:
    st.write("### 📜 اختر السطر المفضل لديك للاستماع فوراً:")
    
    # قائمة اختيار لتصفية القراء عشان الصفحة ما تبقاش تقيلة وتفتح بسرعة على أي موبايل
    reciter_names = [r["name"] for r in reciters_data]
    selected_reciter = st.selectbox("🔍 اختر الشيخ أو القارئ لعرض كل سوره وتحميلها في سطور:", reciter_names)
    
    # البحث عن بيانات القارئ المختار
    current_reciter_data = next((r for r in reciters_data if r["name"] == selected_reciter), None)
    
    if current_reciter_data:
        moshafs = current_reciter_data.get("moshaf", [])
        if moshafs:
            server_url = moshafs[0].get("server", "")
            surah_list = moshafs[0].get("surah_list", "").split(",") # السور المتاحة بصوت الشيخ ده
            
            if server_url and surah_list:
                st.write(f"--- تلاوات الشيخ **{selected_reciter}** المتاحة ---")
                
                # توليد السطور أوتوماتيكياً بناءً على السور اللي مسجلها الشيخ
                for surah_id_str in surah_list:
                    if surah_id_str.strip():
                        surah_index = int(surah_id_str) - 1
                        if 0 <= surah_index < len(all_surahs):
                            surah_name = all_surahs[surah_index]
                            formatted_id = surah_id_str.zfill(3)
                            
                            line_text = f"🎙️ {selected_reciter} —— 📖 سورة {surah_name}"
                            audio_link = f"{server_url}/{formatted_id}.mp3"
                            
                            # عمل كل سطر على هيئة زرار كامل متوافق مع شاشات الهواتف
                            if st.button(line_text, key=f"full_{formatted_id}", use_container_width=True):
                                st.session_state["play_full_url"] = audio_link
                                st.session_state["play_full_title"] = f"{selected_reciter} - سورة {surah_name}"

st.write("---")

# مشغل الصوت التلقائي يظهر في الأسفل عند الضغط على أي سطر
if "play_full_url" in st.session_state:
    st.subheader("🎧 مشغل الصوت الحالي:")
    st.success(f"▶️ أنت تستمع الآن إلى: {st.session_state['play_full_title']}")
    
    st.audio(st.session_state["play_full_url"], format="audio/mp3", autoplay=True)
    st.caption("⚙️ مشغل الصوت هذا قيد التطوير لإضافة مزايا جديدة قريباً.")
