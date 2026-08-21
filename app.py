import streamlit as st
import json
import os
import urllib.parse
from datetime import datetime

# १. पेज कॉन्फिगरेशन
st.set_page_config(page_title="Satish AI Song Genie (जिन स्टुडिओ)", page_icon="🧞‍♂️", layout="centered")

CORRECT_APP_URL = "https://satish-ai-song-studio-iekebqdhhxmq6f2lycinyq.streamlit.app/"
OWNER_EMAIL = "satishpradhan3392@gmail.com"
OWNER_PHONE = "8668235395"
ADMIN_SECRET_PIN = "550"
DB_FILE = "song_genie_memory_db.json"

# २. जिनची कायमस्वरूपी मेमरी (Database System)
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

def add_genie_memory(record):
    db = load_db()
    db.append(record)
    save_to_db(db)

# ३. कॉम्पॅक्ट CSS
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

.genie-banner {
    background: linear-gradient(135deg, #311042, #581C87);
    color: white;
    padding: 14px;
    border-radius: 12px;
    text-align: center;
    border: 2px solid #C084FC;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(88, 28, 135, 0.4);
}
.genie-banner h2 { color: #FACC15; font-size: 19px !important; margin: 0 0 4px 0; }
.genie-banner p { color: #F3E8FF; font-size: 13px !important; margin: 0; }

.track-box {
    background: #FAF5FF;
    border: 1.5px solid #E9D5FF;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 12px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ४. सेशन स्टेट
if 'view_mode' not in st.session_state: st.session_state.view_mode = "user_portal"
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'user_phone' not in st.session_state: st.session_state.user_phone = ""
if 'lyrics_1' not in st.session_state: st.session_state.lyrics_1 = ""
if 'lyrics_2' not in st.session_state: st.session_state.lyrics_2 = ""
if 'clean_lyrics_1' not in st.session_state: st.session_state.clean_lyrics_1 = ""
if 'clean_lyrics_2' not in st.session_state: st.session_state.clean_lyrics_2 = ""
if 'order_id' not in st.session_state: st.session_state.order_id = ""

# जिन बॅनर
st.markdown("""
<div class="genie-banner">
    <h2>🧞‍♂️ सतीश एआय सॉन्ग जिन (Song Genie AI)</h2>
    <p>हुकूम करा मालक! तुम्ही जशी फर्माईश कराल, तसे कडक गाणे १ सेकंदात तयार होईल!</p>
</div>
""", unsafe_allow_html=True)

# शेअरिंग बार
share_default_text = f"🧞‍♂️ 'Satish AI Song Genie' वरून स्वतःच्या फर्माईशप्रमाणे गाणे बनवा:\n{CORRECT_APP_URL}"
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
    if st.button("🎤 गाण्याची फर्माईश करा (Create)"):
        st.session_state.view_mode = "user_portal"
        st.rerun()
with col_n2:
    if st.button("🔐 जिन मेमरी डॅशबोर्ड (Control 550)"):
        st.session_state.view_mode = "admin_dashboard"
        st.rerun()

st.markdown("---")

# ==============================================================================
#                      विभाग १: मालक डॅशबोर्ड व पक्की मेमरी (Control 550)
# ==============================================================================
if st.session_state.view_mode == "admin_dashboard":
    st.markdown("### 🔐 जिन पक्की मेमरी व मालक कंट्रोल (550)")
    c_au1, c_au2 = st.columns(2)
    with c_au1: admin_email = st.text_input("नोंदणीकृत ईमेल:", placeholder="satishpradhan3392@gmail.com")
    with c_au2: admin_mob = st.text_input("नोंदणीकृत फोन:", placeholder="8668235395")
    admin_pin = st.text_input("मास्टर ५५० पासवर्ड:", type="password", placeholder="पिन: 550")

    if admin_pin == ADMIN_SECRET_PIN and admin_mob.strip() in [OWNER_PHONE, ""] and (admin_email.strip() == OWNER_EMAIL or admin_email.strip() == ""):
        records = load_db()
        st.success(f"✅ जिन मेमरी उघडली! एकूण पूर्ण झालेल्या फर्माईशी: {len(records)}")
        if not records:
            st.info("अद्याप कोणत्याही ग्राहकाने फर्माईश केलेली नाही.")
        else:
            for idx, item in enumerate(reversed(records)):
                with st.expander(f"🧞‍♂️ {item.get('name')} ({item.get('phone')}) [{item.get('time')}]"):
                    st.write(f"**ऑर्डर आयडी:** `{item.get('id')}`")
                    st.write(f"**ग्राहकाची संपूर्ण फर्माईश:**")
                    st.info(item.get('prompt', 'माहिती उपलब्ध नाही'))
                    st.text_area(f"तयार झालेले गाणे #{idx+1}:", value=item.get('lyrics_1', ''), height=130, key=f"gen_l1_{idx}")
                    wa_msg = urllib.parse.quote(f"नमस्कार {item.get('name')}, Satish AI Song Genie कडून तुमची फर्माईश पूर्ण झाली आहे!")
                    st.markdown(f"""
                    <a href="https://api.whatsapp.com/send?phone=91{item.get('phone')}&text={wa_msg}" target="_blank" style="text-decoration:none;">
                        <div style="background:#25D366; color:white; padding:8px; border-radius:6px; text-align:center; font-weight:bold; font-size:12px;">📲 WhatsApp वर संपर्क साधा</div>
                    </a>
                    """, unsafe_allow_html=True)
    else:
        if admin_pin: st.error("चुकीचा पिन! योग्य ५५० पिन टाका.")

# ==============================================================================
#                      विभाग २: ग्राहक जिन फर्माईश पोर्टल (नो लिमिट)
# ==============================================================================
else:
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        st.session_state.user_name = st.text_input("१. गाण्यात कोणाचे नाव जोडायचे?:", value=st.session_state.user_name, placeholder="उदा. सतीश, राहुल दादा, भाऊ...")
    with c_f2:
        st.session_state.user_phone = st.text_input("२. तुमचा व्हॉट्सॲप नंबर:", value=st.session_state.user_phone, placeholder="उदा. 8668235395")

    user_wish = st.text_area(
        "३. जिनला तुमची फर्माईश सांगा (कशीही आणि कितीही सांगा):",
        placeholder="उदा. भाऊचा नाद लय खुळा, भाऊला दादा म्हणतात, भावकीत आणि जगात भाऊची खूप प्रगती झाली आहे, भाऊने कष्टाने विश्व निर्माण केले, कडक डीजे आणि ढोल-ताशे वाजले पाहिजेत..."
    )

    if st.button("🧞‍♂️ जिन महाराज, गाण्याची फर्माईश पूर्ण करा!"):
        if not st.session_state.user_name:
            st.warning("कृपया गाण्यासाठी नाव प्रविष्ट करा.")
        else:
            with st.spinner("🧞‍♂️ जिन तुमच्या संपूर्ण फर्माईशवर आधारित २ कडक गाणी कम्पोझ करत आहे..."):
                u_name = st.session_state.user_name
                wish = user_wish.strip() if user_wish.strip() else f"शून्यातून विश्व निर्माण केलं, {u_name} दादांची आज जगभर कीर्ती गाजतीये!"

                # फर्माईशचे गाण्यात रूपांतर (पर्याय १: कडक डीजे व ढोल-ताशा चाल)
                st.session_state.lyrics_1 = f"""🎵 [पर्याय १ - कडक डीजे व ढोल-ताशा चाल]
(ढोल-ताशांचा गजर... डीजेचा हाय बेस... {u_name} च्या नावाने अवघा महाराष्ट्र डोलतोय!)

🔥 [मुखडा - Chorus]
आला रे आला बघा कोण आला...
{u_name} च्या नावाने विजयाचा महा-गुलाल उधळायला लागला!
शून्यातून विश्व निर्माण केलं, स्वतःच्या हिंमतीवर,
{u_name} चं नाव कोरलंय प्रत्येकाच्या काळजावर!

⚡ [अंतरा १ - फर्माईश व कर्तृत्व]
{wish}
कष्टाच्या घामाने रचला हा इतिहास,
{u_name} दादांचा शब्द म्हणजे जगाला पक्का विश्वास!
भावकी असो वा मित्र परिवार, पाठीशी उभा अखंड डोंगर,
नाद करायचा पण आमचा कुठं... वाजवा डीजे जोरात आता!

👑 [हुक लाईन - Grand Drop]
एकच वादा... {u_name} दादा!
वाजवा डीजे, उडवा धुरळा... आजची रात्र फक्त आपल्या नावाची!"""

                # पर्याय २: रॉयल एन्ट्री व संबळ मिक्स चाल
                st.session_state.lyrics_2 = f"""🎵 [पर्याय २ - रॉयल एन्ट्री व संबळ मिक्स चाल]
(रॉयल ब्रास बँड, हलगी आणि संबळचा कडक गजर!)

🔥 [मुखडा - Chorus]
हवा नाही तर थेट वादळ येतं...
{u_name} ची एन्ट्री झाली की मैदान शांत होतं!
शब्दाला जागणारा, जिवाभावाचा माणूस...
{u_name} च्या कर्तृत्वाचा अखंड वाहतोय झरा!

⚡ [अंतरा १ - यशाची गाथा]
{wish}
ज्याने कधी हार मानली नाही, संकटांना सामोरे गेले,
{u_name} च्या हिमतीने आज नशिबाचेही तारे चमकले!
गावात, जिल्ह्यात आणि सातासमुद्रापार गाजतोय डंका,
नाव ऐकताच मनात उरत नाही कसलीही शंका!

👑 [हुक लाईन]
नाद खुळा... रुबाब मोठा... {u_name} दादा एक नंबर!
संबळ वाजू द्या, गुलाल उधळू द्या... विजयाचा महा-उत्सव साजरा होऊ द्या!"""

                st.session_state.clean_lyrics_1 = st.session_state.lyrics_1.replace("🎵", "").replace("🔥", "").replace("⚡", "").replace("👑", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "")
                st.session_state.clean_lyrics_2 = st.session_state.lyrics_2.replace("🎵", "").replace("🔥", "").replace("⚡", "").replace("👑", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "")

                gen_id = f"GENIE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.order_id = gen_id

                # जिन मेमरीमध्ये कायमस्वरूपी नोंद
                add_genie_memory({
                    "id": gen_id,
                    "name": u_name,
                    "phone": st.session_state.user_phone,
                    "prompt": wish,
                    "lyrics_1": st.session_state.lyrics_1,
                    "lyrics_2": st.session_state.lyrics_2,
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                })

    # ==================== निकाल व थेट ऑडिओ प्लेअर्स ====================
    if st.session_state.lyrics_1:
        st.success(f"✅ जिनने तुमची फर्माईश पूर्ण केली! ऑर्डर आयडी: `{st.session_state.order_id}`")

        # ट्रॅक १
        st.markdown("""
        <div class="track-box">
            <h4 style="margin:0 0 6px 0; color:#581C87;">🎧 पर्याय १: हाय-एनर्जी डीजे व ढोल-ताशा ट्रॅक (Live Play)</h4>
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

        # ट्रॅक २
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
        user_song_share = f"🧞‍♂️ मी Satish AI Song Genie वरून स्वतःच्या फर्माईशचे कडक गाणे बनवले आहे!\nनाव: {st.session_state.user_name}\nतुम्हीही फर्माईश करा: {CORRECT_APP_URL}"
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
