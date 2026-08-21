import streamlit as st
import json
import os
import urllib.parse
from datetime import datetime

# १. पेज सेटिंग्ज
st.set_page_config(page_title="Satish Custom Song Studio Pro", page_icon="🎙️", layout="centered")

CORRECT_APP_URL = "https://satish-ai-song-studio-iekebqdhhxmq6f2lycinyq.streamlit.app/"
OWNER_EMAIL = "satishpradhan3392@gmail.com"
OWNER_PHONE = "8668235395"
ADMIN_SECRET_PIN = "550"
DB_FILE = "custom_song_studio_db.json"

# २. डेटाबेस फंक्शन्स
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_to_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_user_order(record):
    db = load_db()
    db.append(record)
    save_to_db(db)

# ३. कॉम्पॅक्ट व व्यावसायिक CSS
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Mukta:wght@400;600;700;800;900&display=swap');
* { font-family: 'Mukta', sans-serif !important; }

#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    visibility: hidden; display: none !important;
}
div[class^="viewerBadge"] { visibility: hidden; display: none !important; }
button[title="View source"] { display: none; }

h1 { color: #1E3A8A; font-weight: 900; text-align: center; font-size: 22px; margin-bottom: 2px; }
h2, h3 { font-size: 15px !important; font-weight: 800 !important; }
p, label, span { font-size: 13px !important; }

/* मुख्य हायलाइट बॅनर */
.hero-banner {
    background: linear-gradient(135deg, #1E1B4B, #312E81);
    color: white;
    padding: 14px;
    border-radius: 12px;
    text-align: center;
    border: 2px solid #818CF8;
    margin-bottom: 12px;
}
.hero-banner h2 { color: #FACC15; font-size: 18px !important; margin: 0 0 4px 0; }
.hero-banner p { color: #E0E7FF; font-size: 12px !important; margin: 0; }

.track-box {
    background: #F8FAFC;
    border: 1.5px solid #CBD5E1;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ४. सेशन स्टेट
if 'view_mode' not in st.session_state: st.session_state.view_mode = "user_portal"
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'user_phone' not in st.session_state: st.session_state.user_phone = ""
if 'selected_cat' not in st.session_state: st.session_state.selected_cat = "महापुरुषांवरील गाणी (डॉ. बाबासाहेब आंबेडकर / शिवराय)"
if 'generated_lyrics_1' not in st.session_state: st.session_state.generated_lyrics_1 = ""
if 'generated_lyrics_2' not in st.session_state: st.session_state.generated_lyrics_2 = ""
if 'order_id' not in st.session_state: st.session_state.order_id = ""

# ५. शीर्ष बॅनर
st.markdown("""
<div class="hero-banner">
    <h2>🎙️ तुमच्या नावाचं कस्टम गाणं</h2>
    <p>तुमच्या भावना... आमच्या शब्दात... तयार होईल एकदम खास!</p>
</div>
""", unsafe_allow_html=True)

# होम पेज सोशल मीडिया शेअरिंग
share_default_text = f"हे बघा! 'Satish AI Song Studio' वरून स्वतःच्या नावाचे कस्टम गाणे बनवा:\n{CORRECT_APP_URL}"
encoded_share_default = urllib.parse.quote(share_default_text)

st.markdown(f"""
<div style="background: #F0FDF4; border: 1.5px solid #86EFAC; padding: 6px 10px; border-radius: 8px; margin-bottom: 10px; text-align: center;">
    <span style="font-weight: bold; color: #166534; font-size: 12px;">📲 ॲप मित्रांना पाठवा: </span>
    <a href="https://api.whatsapp.com/send?text={encoded_share_default}" target="_blank" style="text-decoration:none;">
        <span style="background:#25D366; color:white; padding:4px 10px; border-radius:6px; font-weight:bold; font-size:11px; margin: 0 3px;">WhatsApp</span>
    </a>
    <a href="https://www.facebook.com/sharer/sharer.php?u={CORRECT_APP_URL}" target="_blank" style="text-decoration:none;">
        <span style="background:#1877F2; color:white; padding:4px 10px; border-radius:6px; font-weight:bold; font-size:11px; margin: 0 3px;">Facebook</span>
    </a>
    <a href="sms:?body={encoded_share_default}" target="_blank" style="text-decoration:none;">
        <span style="background:#4B5563; color:white; padding:4px 10px; border-radius:6px; font-weight:bold; font-size:11px; margin: 0 3px;">SMS</span>
    </a>
</div>
""", unsafe_allow_html=True)

# नेव्हिगेशन
col_n1, col_n2 = st.columns(2)
with col_n1:
    if st.button("🎤 गाणे बनवा (Create Song)"):
        st.session_state.view_mode = "user_portal"
        st.rerun()
with col_n2:
    if st.button("🔐 मालक डॅशबोर्ड (Control 550)"):
        st.session_state.view_mode = "admin_dashboard"
        st.rerun()

st.markdown("---")

# ==============================================================================
#                      विभाग १: मालक डॅशबोर्ड (Control 550)
# ==============================================================================
if st.session_state.view_mode == "admin_dashboard":
    st.markdown("### 🔐 मालक ॲडमिन डॅशबोर्ड (Control 550)")
    c_au1, c_au2 = st.columns(2)
    with c_au1: admin_email = st.text_input("नोंदणीकृत ईमेल:", placeholder="satishpradhan3392@gmail.com")
    with c_au2: admin_mob = st.text_input("नोंदणीकृत फोन:", placeholder="8668235395")
    admin_pin = st.text_input("मास्टर पिन प्रविष्ट करा:", type="password", placeholder="पिन: 550")

    if admin_pin == ADMIN_SECRET_PIN and admin_mob.strip() in [OWNER_PHONE, ""] and (admin_email.strip() == OWNER_EMAIL or admin_email.strip() == ""):
        records = load_db()
        st.success(f"✅ मालक लॉगिन यशस्वी! एकूण तयार झालेली गाणी: {len(records)}")
        if not records:
            st.info("अद्याप कोणत्याही युझरने गाणे तयार केलेले नाही.")
        else:
            for idx, item in enumerate(reversed(records)):
                with st.expander(f"👤 {item.get('name')} ({item.get('phone')}) - {item.get('category')} [{item.get('time')}]"):
                    st.write(f"**ऑर्डर आयडी:** `{item.get('id')}`")
                    st.write(f"**प्रकार:** {item.get('category')}")
                    st.write(f"**माहिती:** {item.get('prompt')}")
                    st.text_area(f"गाण्याचे बोल (Track 1) #{idx+1}:", value=item.get('lyrics_1', ''), height=100, key=f"ad_l1_{idx}")
                    wa_msg = urllib.parse.quote(f"नमस्कार {item.get('name')}, Satish AI Song Studio कडून तुमचे गाणे तयार झाले आहे!")
                    st.markdown(f"""
                    <a href="https://api.whatsapp.com/send?phone=91{item.get('phone')}&text={wa_msg}" target="_blank" style="text-decoration:none;">
                        <div style="background:#25D366; color:white; padding:8px; border-radius:6px; text-align:center; font-weight:bold; font-size:12px;">📲 WhatsApp वर संपर्क साधा</div>
                    </a>
                    """, unsafe_allow_html=True)
    else:
        if admin_pin: st.error("चुकीची माहिती! योग्य ५५० पिन टाका.")

# ==============================================================================
#                      विभाग २: ग्राहक गाणे पोर्टल (पोस्टरनुसार सर्व प्रकार)
# ==============================================================================
else:
    # पोस्टरमधील सर्व लोकप्रिय कॅटेगरीज
    song_categories = [
        "🎂 वाढदिवस विशेष गाणी (Birthday Special)",
        "💙 महापुरुषांवरील गाणी (डॉ. बाबासाहेब आंबेडकर / शिवराय)",
        "👥 मंडळ / ग्रुप / मित्र गाणी",
        "👑 भाईगिरी / स्वॅग / ॲटिट्युड गाणी",
        "💼 व्यावसायिक (Business / Shop) गाणी",
        "🏛️ राजकीय / प्रचार / नेता गाणी",
        "🐂 बैलगाडा शर्यत / नाद गाणी",
        "💍 लग्न समारंभ / हळद / बारात गाणी",
        "🏆 स्पर्धा / स्पोर्ट्स / इव्हेंट गाणी",
        "❤️ प्रेमगीत (Love & Romantic Songs)",
        "🌟 तुमच्या आयुष्यावर आधारित खास गाणी"
    ]

    st.session_state.selected_cat = st.selectbox("१. गाण्याचा प्रकार निवडा:", song_categories)

    c_f1, c_f2 = st.columns(2)
    with c_f1:
        st.session_state.user_name = st.text_input("गाण्यात कोणाचे नाव जोडायचे?:", value=st.session_state.user_name, placeholder="उदा. सतीश, राहुल दादा...")
    with c_f2:
        st.session_state.user_phone = st.text_input("तुमचा व्हॉट्सॲप नंबर:", value=st.session_state.user_phone, placeholder="उदा. 8668235395")

    user_info = st.text_area(
        "गाण्यासाठी खास माहिती / प्रसंग (ऐच्छिक):",
        placeholder="उदा. भावाचा वाढदिवस आहे, कडक डीजे वाजला पाहिजे, गावामध्ये हवा आहे..."
    )

    if st.button("🚀 २ वेगवेगळ्या चालींचे ओरिजिनल गाणे तयार करा"):
        if not st.session_state.user_name:
            st.warning("कृपया गाण्यासाठी नाव प्रविष्ट करा.")
        else:
            with st.spinner("AI द्वारे २ वेगवेगळ्या चालींचे स्टुडिओ गाणे कम्पोझ होत आहे..."):
                u_name = st.session_state.user_name
                cat = st.session_state.selected_cat

                # ट्रॅक १: हाय-एनर्जी डीजे चाल
                st.session_state.generated_lyrics_1 = f"""🎵 [पर्याय १ - कडक डीजे व फास्ट बीट चाल]
(ढोल-ताशांचा गजर आणि डीजेचा हाय बेस!)
आला रे आला बघा कोण आला...
{u_name} च्या नावाने अवघा महाराष्ट्र डोलायला लागला!

[Chorus]
शून्यातून विश्व निर्माण केलं स्वतःच्या हिंमतीवर,
{u_name} चं नाव कोरलंय प्रत्येकाच्या काळजावर!
नाद करायचा पण आमचा कुठं... वाजवा डीजे जोरात आता!"""

                # ट्रॅक २: भावपूर्ण व स्वॅग चाल
                st.session_state.generated_lyrics_2 = f"""🎵 [पर्याय २ - स्वॅग व रॉयल एन्ट्री चाल]
(रॉयल ब्रास बँड व संबळ मिक्स!)
हवा नाही तर थेट वादळ येतं...
{u_name} ची एन्ट्री झाली की मैदान शांत होतं!

[Chorus]
शब्दाला जागणारा, जिवाभावाचा माणूस...
{u_name} च्या प्रेमाचा सर्वांवर अखंड पाऊस!
एकच वादा... {u_name} दादा!"""

                gen_id = f"SONG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.order_id = gen_id

                add_user_order({
                    "id": gen_id,
                    "name": u_name,
                    "phone": st.session_state.user_phone,
                    "category": cat,
                    "prompt": user_info,
                    "lyrics_1": st.session_state.generated_lyrics_1,
                    "lyrics_2": st.session_state.generated_lyrics_2,
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                })

    # निकाल: २ स्वतंत्र ऑडिओ ट्रॅक्स
    if st.session_state.generated_lyrics_1:
        st.success(f"✅ २ वेगवेगळ्या चालींची गाणी तयार झाली! ऑर्डर आयडी: `{st.session_state.order_id}`")

        # ट्रॅक १ प्रिव्ह्यू
        st.markdown("""
        <div class="track-box">
            <h4 style="margin:0 0 6px 0; color:#1E40AF;">🎧 पर्याय १: हाय-एनर्जी डीजे व ढोल-ताशा ट्रॅक</h4>
        </div>
        """, unsafe_allow_html=True)
        st.code(st.session_state.generated_lyrics_1, language="text")
        st.audio("https://ia800905.us.archive.org/19/items/free-marathi-dj-remix-dhol-bass/marathi_dj_bass_drop.mp3")

        # ट्रॅक २ प्रिव्ह्यू
        st.markdown("""
        <div class="track-box">
            <h4 style="margin:0 0 6px 0; color:#DC2626;">🎧 पर्याय २: रॉयल एन्ट्री व संबळ मिक्स ट्रॅक</h4>
        </div>
        """, unsafe_allow_html=True)
        st.code(st.session_state.generated_lyrics_2, language="text")
        st.audio("https://ia801503.us.archive.org/15/items/bhim-geet-dhol-tasha-mix/bhim_dhol_tasha_track.mp3")

        # मोफत डाऊनलोड
        st.markdown("---")
        st.markdown("### 📥 मोफत गाणे डाऊनलोड करा")
        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                label="📥 ट्रॅक १ डाऊनलोड करा (MP3/Text)",
                data=st.session_state.generated_lyrics_1.encode('utf-8'),
                file_name=f"{st.session_state.user_name}_track_1.txt",
                mime="text/plain"
            )
        with d2:
            st.download_button(
                label="📥 ट्रॅक २ डाऊनलोड करा (MP3/Text)",
                data=st.session_state.generated_lyrics_2.encode('utf-8'),
                file_name=f"{st.session_state.user_name}_track_2.txt",
                mime="text/plain"
            )

        # सोशल शेअरिंग
        user_song_share = f"🎵 मी Satish AI Song Studio वरून स्वतःच्या नावाचे कडक गाणे बनवले आहे!\nनाव: {st.session_state.user_name}\nतुम्हीही ट्राय करा: {CORRECT_APP_URL}"
        enc_share = urllib.parse.quote(user_song_share)
        st.markdown(f"""
        <div style="text-align:center; margin-top:12px;">
            <a href="https://api.whatsapp.com/send?text={enc_share}" target="_blank" style="text-decoration:none;">
                <div style="background:#25D366; color:white; padding:10px; border-radius:8px; font-weight:bold; font-size:14px;">
                    📲 तयार झालेले गाणे WhatsApp वर मित्रांना पाठवा
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
