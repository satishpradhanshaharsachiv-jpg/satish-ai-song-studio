import streamlit as st
import json
import os
import urllib.parse
from datetime import datetime

# १. पेज कॉन्फिगरेशन
st.set_page_config(page_title="Satish Custom Song Studio Pro", page_icon="🎙️", layout="centered")

CORRECT_APP_URL = "https://satish-ai-song-studio-iekebqdhhxmq6f2lycinyq.streamlit.app/"
OWNER_EMAIL = "satishpradhan3392@gmail.com"
OWNER_PHONE = "8668235395"
ADMIN_SECRET_PIN = "550"
DB_FILE = "custom_song_studio_db.json"

# डेटाबेस व्यवस्थापन
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

# २. कॉम्पॅक्ट CSS
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
    margin-bottom: 12px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ३. सेशन स्टेट
if 'view_mode' not in st.session_state: st.session_state.view_mode = "user_portal"
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'user_phone' not in st.session_state: st.session_state.user_phone = ""
if 'selected_cat' not in st.session_state: st.session_state.selected_cat = "👑 भाईगिरी / स्वॅग / ॲटिट्युड गाणी"
if 'lyrics_1' not in st.session_state: st.session_state.lyrics_1 = ""
if 'lyrics_2' not in st.session_state: st.session_state.lyrics_2 = ""
if 'clean_lyrics_1' not in st.session_state: st.session_state.clean_lyrics_1 = ""
if 'clean_lyrics_2' not in st.session_state: st.session_state.clean_lyrics_2 = ""
if 'order_id' not in st.session_state: st.session_state.order_id = ""

# शीर्षक बॅनर
st.markdown("""
<div class="hero-banner">
    <h2>🎙️ तुमच्या नावाचं कस्टम गाणं</h2>
    <p>तुमच्या भावना... आमच्या शब्दात... तयार होईल एकदम खास!</p>
</div>
""", unsafe_allow_html=True)

# शेअरिंग बार
share_default_text = f"हे बघा! 'Satish AI Song Studio' वरून स्वतःच्या नावाचे सविस्तर कस्टम गाणे बनवा:\n{CORRECT_APP_URL}"
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
#                      विभाग १: मालक डॅशबोर्ड
# ==============================================================================
if st.session_state.view_mode == "admin_dashboard":
    st.markdown("### 🔐 मालक ॲडमिन डॅशबोर्ड (Control 550)")
    c_au1, c_au2 = st.columns(2)
    with c_au1: admin_email = st.text_input("नोंदणीकृत ईमेल:", placeholder="satishpradhan3392@gmail.com")
    with c_au2: admin_mob = st.text_input("नोंदणीकृत फोन:", placeholder="8668235395")
    admin_pin = st.text_input("मास्टर पिन टाका:", type="password", placeholder="पिन: 550")

    if admin_pin == ADMIN_SECRET_PIN and admin_mob.strip() in [OWNER_PHONE, ""] and (admin_email.strip() == OWNER_EMAIL or admin_email.strip() == ""):
        records = load_db()
        st.success(f"✅ मालक लॉगिन यशस्वी! एकूण तयार झालेली गाणी: {len(records)}")
        if not records:
            st.info("अद्याप कोणत्याही युझरने गाणे तयार केलेले नाही.")
        else:
            for idx, item in enumerate(reversed(records)):
                with st.expander(f"👤 {item.get('name')} ({item.get('phone')}) - {item.get('category')} [{item.get('time')}]"):
                    st.write(f"**ऑर्डर आयडी:** `{item.get('id')}`")
                    st.write(f"**ग्राहकाची फर्माईश:** {item.get('prompt')}")
                    st.text_area(f"तयार झालेले गाणे #{idx+1}:", value=item.get('lyrics_1', ''), height=130, key=f"ad_l1_{idx}")
                    wa_msg = urllib.parse.quote(f"नमस्कार {item.get('name')}, Satish AI Song Studio कडून तुमचे गाणे तयार झाले आहे!")
                    st.markdown(f"""
                    <a href="https://api.whatsapp.com/send?phone=91{item.get('phone')}&text={wa_msg}" target="_blank" style="text-decoration:none;">
                        <div style="background:#25D366; color:white; padding:8px; border-radius:6px; text-align:center; font-weight:bold; font-size:12px;">📲 WhatsApp वर संपर्क साधा</div>
                    </a>
                    """, unsafe_allow_html=True)
    else:
        if admin_pin: st.error("चुकीचा पिन! ५५० पिन प्रविष्ट करा.")

# ==============================================================================
#                      विभाग २: ग्राहक गाणे पोर्टल (सविस्तर फर्माईश गाणे)
# ==============================================================================
else:
    song_categories = [
        "👑 भाईगिरी / स्वॅग / ॲटिट्युड गाणी",
        "🎂 वाढदिवस विशेष गाणी (Birthday Special)",
        "💙 महापुरुषांवरील गाणी (डॉ. बाबासाहेब आंबेडकर / शिवराय)",
        "👥 मंडळ / ग्रुप / मित्र गाणी",
        "💼 व्यावसायिक (Business / Shop) गाणी",
        "🏛️ राजकीय / प्रचार / नेता गाणी",
        "🐂 बैलगाडा शर्यत / नाद गाणी",
        "💍 लग्न समारंभ / हळद / बारात गाणी",
        "🏆 स्पर्धा / स्पोर्ट्स / इव्हेंट गाणी",
        "❤️ प्रेमगीत (Love Songs)",
        "🌟 तुमच्या आयुष्यावर आधारित खास गाणी"
    ]

    st.session_state.selected_cat = st.selectbox("१. गाण्याचा प्रकार निवडा:", song_categories)

    c_f1, c_f2 = st.columns(2)
    with c_f1:
        st.session_state.user_name = st.text_input("गाण्यात कोणाचे नाव जोडायचे?:", value=st.session_state.user_name, placeholder="उदा. सतीश, राहुल दादा...")
    with c_f2:
        st.session_state.user_phone = st.text_input("तुमचा व्हॉट्सॲप नंबर:", value=st.session_state.user_phone, placeholder="उदा. 8668235395")

    user_info = st.text_area(
        "गाण्यासाठी तुमची सविस्तर फर्माईश / प्रसंग / प्रगती (५० ते १००० शब्द):",
        placeholder="उदा. भाऊचा नाद लय खुळा, भाऊला दादा म्हणतात, जगमध्ये भाऊची खूप प्रगती झाली आहे, भाऊने शून्यातून विश्व निर्माण केलं..."
    )

    word_length = st.select_slider(
        "गाण्याची लांबी निवडा (शब्दांची संख्या):",
        options=["१०० शब्द (शॉर्ट व फास्ट)", "३०० शब्द (स्टँडर्ड)", "५०० शब्द (सविस्तर)", "१००० शब्द (महा-गाथा)"],
        value="५०० शब्द (सविस्तर)"
    )

    if st.button("🚀 फर्माईशनुसार २ वेगवेगळ्या चालींचे गाणे तयार करा"):
        if not st.session_state.user_name:
            st.warning("कृपया गाण्यासाठी नाव प्रविष्ट करा.")
        else:
            with st.spinner("AI द्वारे तुमच्या संपूर्ण फर्माईशवर आधारित सविस्तर स्टुडिओ गाणे तयार होत आहे..."):
                u_name = st.session_state.user_name
                cat = st.session_state.selected_cat
                extra_story = user_info if user_info.strip() else f"शून्यातून विश्व निर्माण केलं, {u_name} दादांची आज जगभर कीर्ती गाजतीये!"

                # ट्रॅक १: हाय-एनर्जी डीजे व ढोल-ताशा चाल (सविस्तर मोठे गाणे)
                st.session_state.lyrics_1 = f"""🎵 [पर्याय १ - कडक डीजे व फास्ट बीट चाल]
(नाद घुमतो डीजेचा, वाजतंय ढोल-ताशा... {u_name} चं नाव ऐकून विरोधकांना बसतोय धसका!)

🔥 [मुखडा - Chorus]
आला रे आला बघा कोण आला... 
{u_name} च्या नावाने अवघा महाराष्ट्र डोलायला लागला!
शून्यातून विश्व निर्माण केलं, स्वतःच्या हिंमतीवर,
{u_name} चं नाव कोरलंय प्रत्येकाच्या काळजावर!

⚡ [अंतरा १ - प्रगती व कर्तृत्व]
{extra_story}
कष्टाच्या घामाने रचला हा इतिहास,
{u_name} दादांचा शब्द म्हणजे जगात पक्का विश्वास!
भावकी असो वा मित्र परिवार, पाठीशी उभा अखंड डोंगर,
नाद करायचा पण आमचा कुठं... वाजवा डीजे जोरात आता!

👑 [अंतरा २ - स्वॅग व दरारा]
दुनियेत हवा नाही तर थेट वादळ येतं,
{u_name} ची गाडी थांबली की अवघं गाव शांत होतं!
जिवाभावाच्या माणसांसाठी जीव देणारा राजा माणूस,
कौतुकाचा पडतोय आज यांच्यावर अखंड पाऊस!

💥 [हुक लाईन - Grand Drop]
एकच वादा... {u_name} दादा!
वाजवा डीजे, उडवा धुरळा... आजची रात्र फक्त आपल्या नावाची!"""

                # ट्रॅक २: रॉयल एन्ट्री व संबळ मिक्स चाल
                st.session_state.lyrics_2 = f"""🎵 [पर्याय २ - रॉयल एन्ट्री व संबळ मिक्स चाल]
(रॉयल ब्रास बँड, हलगी आणि संबळचा कडक गजर!)

🔥 [मुखडा - Chorus]
हवा नाही तर थेट वादळ येतं...
{u_name} ची एन्ट्री झाली की मैदान शांत होतं!
शब्दाला जागणारा, जिवाभावाचा माणूस...
{u_name} च्या कर्तृत्वाचा अखंड वाहतोय झरा!

⚡ [अंतरा १ - संघर्षातून यशाकडे]
{extra_story}
ज्याने कधी हार मानली नाही, संकटांना सामोरे गेले,
{u_name} च्या हिमतीने आज नशिबाचेही तारे चमकले!
गावात, जिल्ह्यात आणि सातासमुद्रापार गाजतोय डंका,
नाव ऐकताच मनात उरत नाही कसलीही शंका!

👑 [हुक लाईन]
नाद खुळा... रुबाब मोठा... {u_name} दादा एक नंबर!
संबळ वाजू द्या, गुलाल उधळू द्या... विजयाचा महा-उत्सव साजरा होऊ द्या!"""

                # स्पीच सिंथेसिससाठी स्वच्छ शब्द
                st.session_state.clean_lyrics_1 = st.session_state.lyrics_1.replace("🎵", "").replace("🔥", "").replace("⚡", "").replace("👑", "").replace("💥", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "")
                st.session_state.clean_lyrics_2 = st.session_state.lyrics_2.replace("🎵", "").replace("🔥", "").replace("⚡", "").replace("👑", "").replace("💥", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "")

                gen_id = f"SONG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.order_id = gen_id

                add_user_order({
                    "id": gen_id,
                    "name": u_name,
                    "phone": st.session_state.user_phone,
                    "category": cat,
                    "prompt": user_info,
                    "lyrics_1": st.session_state.lyrics_1,
                    "lyrics_2": st.session_state.lyrics_2,
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                })

    # ==================== निकाल व थेट जागेवर वाजणारे ऑडिओ प्लेअर्स ====================
    if st.session_state.lyrics_1:
        st.success(f"✅ २ वेगवेगळ्या चालींची सविस्तर गाणी तयार झाली! ऑर्डर आयडी: `{st.session_state.order_id}`")

        # ट्रॅक १ प्लेअर (थेट इनबिल्ट चालू होणारा)
        st.markdown("""
        <div class="track-box">
            <h4 style="margin:0 0 6px 0; color:#1E40AF;">🎧 पर्याय १: हाय-एनर्जी डीजे व ढोल-ताशा ट्रॅक (Live Play)</h4>
        </div>
        """, unsafe_allow_html=True)
        st.code(st.session_state.lyrics_1, language="text")

        js_t1 = st.session_state.clean_lyrics_1.replace("\n", " ").replace('"', "'").replace("`", "")
        player_1_html = f"""
        <div style="background:#1E293B; border-radius:10px; padding:12px; text-align:center; color:white; margin-bottom:15px;">
            <p style="margin:0 0 8px 0; font-size:13px; color:#38BDF8; font-weight:bold;">▶️ पर्याय १ गाणे थेट येथे वाजवून ऐका:</p>
            <div style="display:flex; justify-content:center; gap:10px;">
                <button onclick="
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance('{js_t1}');
                    msg.lang = 'mr-IN';
                    msg.rate = 0.95;
                    msg.pitch = 1.0;
                    window.speechSynthesis.speak(msg);
                " style="background:linear-gradient(135deg, #059669, #10B981); color:white; padding:8px 20px; font-size:14px; font-weight:bold; border:none; border-radius:6px; cursor:pointer;">
                    ▶️ गाणे चालू करा (Play Track 1)
                </button>
                <button onclick="window.speechSynthesis.cancel();" style="background:#EF4444; color:white; padding:8px 14px; font-size:14px; font-weight:bold; border:none; border-radius:6px; cursor:pointer;">
                    ⏹️ थांबवा (Stop)
                </button>
            </div>
        </div>
        """
        st.components.v1.html(player_1_html, height=100)

        # ट्रॅक २ प्लेअर
        st.markdown("""
        <div class="track-box">
            <h4 style="margin:0 0 6px 0; color:#DC2626;">🎧 पर्याय २: रॉयल एन्ट्री व संबळ मिक्स ट्रॅक (Live Play)</h4>
        </div>
        """, unsafe_allow_html=True)
        st.code(st.session_state.lyrics_2, language="text")

        js_t2 = st.session_state.clean_lyrics_2.replace("\n", " ").replace('"', "'").replace("`", "")
        player_2_html = f"""
        <div style="background:#1E293B; border-radius:10px; padding:12px; text-align:center; color:white; margin-bottom:15px;">
            <p style="margin:0 0 8px 0; font-size:13px; color:#FACC15; font-weight:bold;">▶️ पर्याय २ गाणे थेट येथे वाजवून ऐका:</p>
            <div style="display:flex; justify-content:center; gap:10px;">
                <button onclick="
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance('{js_t2}');
                    msg.lang = 'mr-IN';
                    msg.rate = 0.90;
                    msg.pitch = 0.95;
                    window.speechSynthesis.speak(msg);
                " style="background:linear-gradient(135deg, #D97706, #F59E0B); color:white; padding:8px 20px; font-size:14px; font-weight:bold; border:none; border-radius:6px; cursor:pointer;">
                    ▶️ गाणे चालू करा (Play Track 2)
                </button>
                <button onclick="window.speechSynthesis.cancel();" style="background:#EF4444; color:white; padding:8px 14px; font-size:14px; font-weight:bold; border:none; border-radius:6px; cursor:pointer;">
                    ⏹️ थांबवा (Stop)
                </button>
            </div>
        </div>
        """
        st.components.v1.html(player_2_html, height=100)

        # मोफत डाऊनलोड
        st.markdown("---")
        st.markdown("### 📥 मोफत गाणे डाऊनलोड करा")
        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                label="📥 ट्रॅक १ डाऊनलोड करा (Lyrics/Text)",
                data=st.session_state.lyrics_1.encode('utf-8'),
                file_name=f"{st.session_state.user_name}_track_1.txt",
                mime="text/plain"
            )
        with d2:
            st.download_button(
                label="📥 ट्रॅक २ डाऊनलोड करा (Lyrics/Text)",
                data=st.session_state.lyrics_2.encode('utf-8'),
                file_name=f"{st.session_state.user_name}_track_2.txt",
                mime="text/plain"
            )

        # सोशल शेअरिंग
        user_song_share = f"🎵 मी Satish AI Song Studio वरून स्वतःच्या नावाची व प्रगतीची सविस्तर २ गाणी बनवली आहेत!\nनाव: {st.session_state.user_name}\nतुम्हीही तुमचे गाणे तयार करा: {CORRECT_APP_URL}"
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
