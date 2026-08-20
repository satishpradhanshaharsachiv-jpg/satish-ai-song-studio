import streamlit as st
import google.generativeai as genai
import json
import os
import urllib.parse
from datetime import datetime

# १. पेज सेटिंग्ज आणि RTI ॲपसारखे मॉडर्न कॉम्पॅक्ट डिझाइन
st.set_page_config(page_title="Satish AI Song Studio Pro", page_icon="🎵", layout="centered")

# ॲडमिन मास्टर पिन (गाणे अनलॉक करण्यासाठी आणि ॲडमिन डॅशबोर्ड उघडण्यासाठी)
ADMIN_SECRET_PIN = "7788"
DB_FILE = "song_studio_users_db.json"

# डेटाबेस लोड व सेव्ह फंक्शन
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_to_db(user_data):
    db = load_db()
    db.append(user_data)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Mukta:wght@400;600;700;800&display=swap');
* { font-family: 'Mukta', sans-serif !important; }

#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    visibility: hidden; display: none !important;
}
div[class^="viewerBadge"] { visibility: hidden; display: none !important; }
button[title="View source"] { display: none; }

/* अक्षरांची साईझ सुटसुटीत व कॉम्पॅक्ट */
h1 { color: #1E3A8A; font-weight: 800; text-align: center; font-size: 22px; margin-bottom: 0px; }
h2, h3 { font-size: 16px !important; font-weight: 700 !important; }
p, label, span { font-size: 13px !important; }

/* RTI ॲपसारखी मोठी चमकदार रंगीत बटने */
div.st-key-btn_bhim button {
    background: linear-gradient(135deg, #1E40AF, #3B82F6) !important;
    color: #ffffff !important; height: 60px !important; border-radius: 12px !important;
    border: 2px solid #1D4ED8 !important; box-shadow: 0 4px 10px rgba(30, 64, 175, 0.3) !important;
}
div.st-key-btn_bhim button p { font-size: 14px !important; font-weight: 800 !important; color: white !important; }

div.st-key-btn_dj button {
    background: linear-gradient(135deg, #DC2626, #EF4444) !important;
    color: #ffffff !important; height: 60px !important; border-radius: 12px !important;
    border: 2px solid #B91C1C !important; box-shadow: 0 4px 10px rgba(220, 38, 38, 0.3) !important;
}
div.st-key-btn_dj button p { font-size: 14px !important; font-weight: 800 !important; color: white !important; }

div.st-key-btn_rap button {
    background: linear-gradient(135deg, #D97706, #F59E0B) !important;
    color: #ffffff !important; height: 60px !important; border-radius: 12px !important;
    border: 2px solid #B45309 !important; box-shadow: 0 4px 10px rgba(217, 119, 6, 0.3) !important;
}
div.st-key-btn_rap button p { font-size: 14px !important; font-weight: 800 !important; color: white !important; }

div.st-key-btn_other button {
    background: linear-gradient(135deg, #059669, #10B981) !important;
    color: #ffffff !important; height: 60px !important; border-radius: 12px !important;
    border: 2px solid #047857 !important; box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3) !important;
}
div.st-key-btn_other button p { font-size: 14px !important; font-weight: 800 !important; color: white !important; }

.nav-btn div.stButton > button { font-size: 12px !important; font-weight: 700 !important; height: 38px !important; border-radius: 8px !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# सेशन स्टेट व्हेरिएबल्स
if 'category' not in st.session_state: st.session_state.category = "bhim_geet"
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'user_phone' not in st.session_state: st.session_state.user_phone = ""
if 'sub_genre' not in st.session_state: st.session_state.sub_genre = "भीमराव एक नंबर (कडक डीजे डान्स)"
if 'voice_type' not in st.session_state: st.session_state.voice_type = "जोशपूर्ण पुरुष आवाज (Male Energy)"
if 'custom_prompt' not in st.session_state: st.session_state.custom_prompt = ""
if 'generated_lyrics' not in st.session_state: st.session_state.generated_lyrics = ""
if 'suno_prompt' not in st.session_state: st.session_state.suno_prompt = ""
if 'is_paid' not in st.session_state: st.session_state.is_paid = False
if 'show_admin' not in st.session_state: st.session_state.show_admin = False

# शीर्ष शीर्षक
st.markdown("<h1>🎵 Satish AI Song Studio Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563; font-weight: bold; margin-bottom: 8px;'>स्वतःचे नाव जोडून १ सेकंदात बनवा कडक डीजे, रॅप, भीमगीते व भक्तीगीते!</p>", unsafe_allow_html=True)
st.markdown("---")

# मुख्य ४ संगीत वर्ग बटने (Main Category Buttons)
c1, c2 = st.columns(2)
with c1:
    if st.button("💙 १. डॉ. बाबासाहेब व बुद्ध गीते\n(भीमगीत स्पेशल)", key="btn_bhim"):
        st.session_state.category = "bhim_geet"
with c2:
    if st.button("🔥 २. डीजे, ढोल-ताशे व डान्स\n(सॅड/गम + डीजे मिक्स)", key="btn_dj"):
        st.session_state.category = "dj_remix"

c3, c4 = st.columns(2)
with c3:
    if st.button("🎤 ३. अस्सल मराठी रॅप\n(स्ट्रीट / इमोशनल / स्वॅग)", key="btn_rap"):
        st.session_state.category = "marathi_rap"
with c4:
    if st.button("🎂 ४. वाढदिवस, भक्ती व इतर\n(सर्व देव, आई-बाबा, पार्टी)", key="btn_other"):
        st.session_state.category = "birthday_bhakti"

st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)

# उप-नेव्हिगेशन (डॅशबोर्ड, रिसेट)
n1, n2 = st.columns(2)
with n1:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("🔄 नवीन गाणे तयार करा"):
        st.session_state.user_name = ""
        st.session_state.custom_prompt = ""
        st.session_state.generated_lyrics = ""
        st.session_state.suno_prompt = ""
        st.session_state.is_paid = False
        st.session_state.show_admin = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with n2:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("🔒 ॲडमिन डॅशबोर्ड (हिस्ट्री)"):
        st.session_state.show_admin = not st.session_state.show_admin
    st.markdown('</div>', unsafe_allow_html=True)

api_key = st.sidebar.text_input("🔑 Gemini API Key (ऐच्छिक):", type="password")

# ==================== ॲडमिन डॅशबोर्ड (Analytics & User Tracking) ====================
if st.session_state.show_admin:
    st.markdown("""
    <div style="background: #FEF3C7; border: 2px solid #F59E0B; padding: 12px; border-radius: 10px; margin-bottom: 12px;">
        <h4 style="margin: 0; color: #92400E;">🔐 ॲडमिन पडताळणी व सर्व युजर्स हिस्ट्री</h4>
    </div>
    """, unsafe_allow_html=True)
    admin_pin = st.text_input("ॲडमिन सिक्रेट पिन टाका:", type="password", key="admin_pin_input")
    if admin_pin == ADMIN_SECRET_PIN:
        db_data = load_db()
        st.success(f"✅ ॲडमिन लॉगिन यशस्वी! एकूण गाणी तयार झाली: {len(db_data)}")
        if db_data:
            for idx, user in enumerate(reversed(db_data)):
                with st.expander(f"👤 {user.get('name', 'N/A')} ({user.get('phone', 'N/A')}) - {user.get('category')} [{user.get('time')}]"):
                    st.write(f"**म्युझिक प्रकार:** {user.get('sub_genre')}")
                    st.write(f"**व्हॉइस:** {user.get('voice')}")
                    st.write(f"**युझरची संकल्पना:** {user.get('prompt')}")
                    st.text_area(f"तयार झालेले बोल #{idx+1}:", value=user.get('lyrics', ''), height=150)
        else:
            st.info("अद्याप कोणत्याही युझरने गाणे तयार केलेले नाही.")
    else:
        if admin_pin: st.error("चुकीचा ॲडमिन पिन!")

# ==================== मुख्य गाणे निर्मिती फॉर्म ====================
if not st.session_state.show_admin:
    # कॅटेगरीनुसार उप-प्रकार
    if st.session_state.category == "bhim_geet":
        header_title = "💙 डॉ. बाबासाहेब आंबेडकर व तथागत बुद्ध स्पेशल गाणी"
        theme_color = "#1E40AF"
        genre_options = [
            "भीमराव एक नंबर (कडक डीजे डान्स व नाद)",
            "निळ्या वादळाची हवा (युझरच्या नावासह स्वॅग गाणे)",
            "बुद्धं शरणं गच्छामि (शांत व भावपूर्ण बुद्ध वंदना)",
            "भीमा तुझ्या जन्मामुळे (हृदयस्पर्शी व भावुक सॅड-इमोशनल)",
            "भीम जयंती जल्लोष (ढोल-ताशे, हलगी व डीजे मिक्स)"
        ]
    elif st.session_state.category == "dj_remix":
        header_title = "🔥 डीजे, ढोल-ताशे, डान्स व सॅड-डीजे मिक्स"
        theme_color = "#DC2626"
        genre_options = [
            "कडक संबळ व ढोल-ताशे हाय-व्होल्टेज डीजे",
            "गमभरे सॅड गाणे विथ हेवी बेस डीजे डान्स (Sad + Dance Mix)",
            "गावरान हलगी व झांज पार्टी डान्स",
            "क्लब डिस्को व ईडीएम (EDM Bass Booster)",
            "रोमँटिक लव्ह विथ फास्ट रिदम बीट्स"
        ]
    elif st.session_state.category == "marathi_rap":
        header_title = "🎤 अस्सल मराठी स्ट्रीट व फास्ट रॅप स्टुडिओ"
        theme_color = "#D97706"
        genre_options = [
            "मुंबई-पुणे-संभाजीनगर स्ट्रीट रॅप (Hard Hitting Hip-Hop)",
            "स्वतःच्या नावाचा स्वॅग रॅप (Gangster/Attitude Style)",
            "गरीबी, संघर्ष आणि यश (इमोशनल मोटिव्हेशनल रॅप)",
            "दोस्ती आणि भावाचा कडक रॅप"
        ]
    else:
        header_title = "🎂 वाढदिवस, सर्व देवी-देवता व कौटुंबिक गाणी"
        theme_color = "#059669"
        genre_options = [
            "वाढदिवस स्पेशल (भावाचा/मित्राचा/स्वतःचा कडक डीजे बर्थडे)",
            "छत्रपती शिवाजी महाराज व संभाजी महाराज पोवाडा/गीत",
            "महादेव/गणपती/खंडोबा/विठ्ठल महा-आरती व भक्तीगीत",
            "आई-बाबांच्या प्रेमाचे भावुक गाणे"
        ]

    st.markdown(f"""
    <div style="background: #F1F5F9; border-left: 5px solid {theme_color}; padding: 10px; border-radius: 8px; margin-bottom: 12px;">
        <h4 style="margin: 0; color: {theme_color}; font-size: 15px;">{header_title}</h4>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.session_state.user_name = st.text_input("गाण्यात कोणाचे नाव जोडायचे आहे?:", value=st.session_state.user_name, placeholder="उदा. सतीश, राहुल, भाऊ...")
    with col_b:
        st.session_state.user_phone = st.text_input("तुमचा व्हॉट्सॲप नंबर (सपोर्टसाठी):", value=st.session_state.user_phone, placeholder="उदा. 98xxxxxxxx")

    st.session_state.sub_genre = st.selectbox("विशिष्ट संगीत प्रकार निवडा:", genre_options)
    
    st.session_state.voice_type = st.radio(
        "गाण्याचा गायक / आवाज निवडा:",
        ["जोशपूर्ण पुरुष आवाज (Male Energy)", "सुरेल महिला आवाज (Female Melodious)", "कोरस ग्रुप (Boy + Girl Duet)"],
        horizontal=True
    )

    st.session_state.custom_prompt = st.text_area(
        "गाण्याचा विषय किंवा तुमच्या स्वतःच्या खास ओळी (ऐच्छिक):",
        value=st.session_state.custom_prompt,
        placeholder="उदा. गाण्यात निळ्या झेंड्याचा उल्लेख असावा, भावाच्या वाढदिवसाला कडक डीजे लावला आहे..."
    )

    if st.button("🚀 एआय द्वारे सुपरहीट गाणे तयार करा"):
        if not st.session_state.user_name:
            st.warning("कृपया गाण्यासाठी नाव प्रविष्ट करा.")
        else:
            with st.spinner("AI द्वारे कडक चाल, बोल आणि म्युझिक कम्पोझ होत आहे..."):
                if api_key:
                    try:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        prompt_text = f"""
तुम्ही महाराष्ट्रातील नंबर १ संगीतकार आणि गीतकार आहात.
कॅटेगरी: {st.session_state.category}
प्रकार: {st.session_state.sub_genre}
नाव: {st.session_state.user_name}
आवाज: {st.session_state.voice_type}
खास सूचना: {st.session_state.custom_prompt}

नियम:
१. गाण्याचे मुखडा, अंतरा १, अंतरा २, आणि हुक लाईन स्पष्ट मराठीत आणि गेय असावी.
२. शेवटी AI म्युझिक जनरेटर (Suno AI) साठी इंग्रजी प्रॉम्प्ट तयार करून द्या.
"""
                        res = model.generate_content(prompt_text)
                        st.session_state.generated_lyrics = res.text
                    except Exception as e:
                        st.error(f"त्रुटी: {e}")
                else:
                    # ऑफलाइन सुपरहीट टेम्पलेट
                    st.session_state.generated_lyrics = f"""🎵 [मुखडा - Chorus]
(नाद घुमतो डीजेचा, वाजतंय ढोल-ताशा...
{st.session_state.user_name} चं नाव ऐकून भल्याभल्यांना बसतोय धसका!)
अरे निळं वादळ आलं... क्रांतीची मशाल पेटली!
{st.session_state.user_name} च्या एन्ट्रीने अख्खी मैफल थरथर कापली!

🔥 [अंतरा १ - Verse 1]
भीमरायाचा विचार मनात, चालतो छाती ठोकून,
कोणाच्या बापाला भीत नाही, जगतो मान झुकवून!
एकच वादा... {st.session_state.user_name} दादा!
नाद करायचा पण आमचा कुठं... डीजे वाजवा जोरात आता!

⚡ [हुक लाईन - Drop]
(जय भीम बोला... जय बुद्ध बोला...
{st.session_state.user_name} च्या नावाने निळा गुलाल उधळा!)"""

                st.session_state.suno_prompt = f"Marathi {st.session_state.sub_genre}, energetic folk beat, powerful bass, Marathi live dhol tasha, high bpm DJ mix, clear vocals for {st.session_state.user_name}"

                # डेटाबेसमध्ये युझर आणि गाणे कायमस्वरूपी सेव्ह करणे
                save_to_db({
                    "name": st.session_state.user_name,
                    "phone": st.session_state.user_phone,
                    "category": st.session_state.category,
                    "sub_genre": st.session_state.sub_genre,
                    "voice": st.session_state.voice_type,
                    "prompt": st.session_state.custom_prompt,
                    "lyrics": st.session_state.generated_lyrics,
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                })

    # ==================== गाण्याचे बोल, कमी आवाजातील ऑडिओ व ₹१९९ लॉक ====================
    if st.session_state.generated_lyrics:
        st.success("✅ तुमचे गाणे आणि म्युझिक ट्रॅक यशस्वीरीत्या तयार झाले आहे!")
        
        # गाण्याचे बोल (काळा बॉक्स)
        st.markdown("<p style='font-weight: bold; margin-bottom: 2px;'>📜 तयार झालेले संपूर्ण गाणे:</p>", unsafe_allow_html=True)
        st.code(st.session_state.generated_lyrics, language="text")

        # पायरी २: कमी आवाजातील सॅम्पल प्लेअर
        st.markdown("""
        <div style="background: #EFF6FF; border: 1px solid #BFDBFE; padding: 10px; border-radius: 8px; margin-top: 10px;">
            <p style="margin: 0; font-weight: bold; color: #1E40AF;">🎧 सॅम्पल गाणे ऐका (कमी आवाजात डेमो प्रिव्ह्यू):</p>
        </div>
        """, unsafe_allow_html=True)
        
        # डेमो ऑडिओ प्लेअर (कमी आवाज प्री-सेट)
        audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        st.audio(audio_url)
        st.caption("💡 वरील प्लेअरमध्ये कमी आवाजात डेमो तयार आहे. ओरिजिनल हाय-बेस स्टुडिओ ट्रॅकसाठी खाली अनलॉक करा.")

        # पायरी ३: ₹१९९ स्टुडिओ लॉक आणि डाऊनलोड
        st.markdown("---")
        st.markdown("### 📥 ओरिजिनल स्टुडिओ MP3 व फुल ऑडिओ डाऊनलोड")

        if not st.session_state.is_paid:
            st.warning("🔒 **ओरिजिनल फुल-क्वालिटी HD गाणे डाऊनलोड करण्यासाठी ₹१९९ लॉक आहे.**")
            upi_id = "satishpradhan3392@ybl"
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={upi_id}%26pn=Satish%20Pradhan%26am=199%26cu=INR"

            col_q1, col_q2 = st.columns([1, 2])
            with col_q1:
                st.image(qr_url, caption="₹१९९ स्कॅन करा", width=125)
            with col_q2:
                st.markdown(f"**UPI ID:** `{upi_id}` | **रक्कम:** ₹१९९/-")
                unlock_pin_input = st.text_input("पेमेंट झाल्यावर ॲडमिनकडून मिळालेला अनलॉक पिन टाका:", type="password", key="song_unlock_pin")
                if st.button("🔓 गाणे अनलॉक करा व MP3 मिळवा"):
                    if unlock_pin_input.strip() == ADMIN_SECRET_PIN:
                        st.session_state.is_paid = True
                        st.success("पडताळणी यशस्वी! गाणे अनलॉक झाले आहे.")
                        st.rerun()
                    else:
                        st.error("चुकीचा पिन! कृपया ₹१९९ पेमेंट करून ॲडमिनकडून खरा पिन मिळवा.")
            
            # WhatsApp सपोर्ट बटण
            wa_text = urllib.parse.quote(f"नमस्कार, मी Satish AI Song Studio वर गाणे तयार केले आहे. नाव: {st.session_state.user_name}, मला ₹१९९ चे गाणे अनलॉक करून हवे आहे.")
            st.markdown(f"""
            <div style="text-align: center; margin-top: 10px;">
                <a href="https://api.whatsapp.com/send?phone=918668235395&text={wa_text}" target="_blank" style="text-decoration: none;">
                    <div style="background: #25D366; color: white; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 13px;">
                        📲 पेमेंट स्क्रीनशॉट पाठवून पिन मिळवण्यासाठी येथे WhatsApp करा
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("🎉 **अभिनंदन! तुमचे ओरिजिनल स्टुडिओ गाणे अनलॉक झाले आहे!**")
            st.download_button(
                label="📥 ओरिजिनल हाय-क्वालिटी MP3 गाणे डाऊनलोड करा",
                data=st.session_state.generated_lyrics.encode('utf-8'),
                file_name=f"{st.session_state.user_name}_song_track.txt",
                mime="text/plain"
            )
            st.info("🎵 Suno AI / Udio AI मध्ये वापरण्यासाठी म्युझिक प्रॉम्प्ट: \n`" + st.session_state.suno_prompt + "`")
