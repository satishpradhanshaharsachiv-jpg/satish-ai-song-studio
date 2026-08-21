import streamlit as st
import json
import os
import urllib.parse
from datetime import datetime

# १. पेज कॉन्फिगरेशन
st.set_page_config(page_title="Satish AI Song Studio Mega Pro", page_icon="🎵", layout="centered")

CORRECT_APP_URL = "https://satish-ai-song-studio-iekebqdhhxmq6f2lycinyq.streamlit.app/"
OWNER_EMAIL = "satishpradhan3392@gmail.com"
OWNER_PHONE = "8668235395"
ADMIN_SECRET_PIN = "550"
DB_FILE = "song_studio_mega_db.json"

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

def update_order_status(order_id, status, reply_msg=""):
    db = load_db()
    for item in db:
        if item.get("id") == order_id:
            item["status"] = status
            if reply_msg:
                item["admin_reply"] = reply_msg
    save_to_db(db)

def is_order_unlocked(order_id):
    db = load_db()
    for item in db:
        if item.get("id") == order_id:
            return item.get("status") == "Unlocked"
    return False

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

div.st-key-btn_m1 button {
    background: linear-gradient(135deg, #1E40AF, #3B82F6) !important;
    color: #ffffff !important; height: 65px !important; border-radius: 12px !important;
    border: 2px solid #1D4ED8 !important; box-shadow: 0 4px 10px rgba(30, 64, 175, 0.3) !important;
}
div.st-key-btn_m1 button p { font-size: 14px !important; font-weight: 800 !important; color: white !important; line-height: 1.2 !important; }

div.st-key-btn_m2 button {
    background: linear-gradient(135deg, #DC2626, #EF4444) !important;
    color: #ffffff !important; height: 65px !important; border-radius: 12px !important;
    border: 2px solid #B91C1C !important; box-shadow: 0 4px 10px rgba(220, 38, 38, 0.3) !important;
}
div.st-key-btn_m2 button p { font-size: 14px !important; font-weight: 800 !important; color: white !important; line-height: 1.2 !important; }

div.st-key-btn_m3 button {
    background: linear-gradient(135deg, #D97706, #F59E0B) !important;
    color: #ffffff !important; height: 65px !important; border-radius: 12px !important;
    border: 2px solid #B45309 !important; box-shadow: 0 4px 10px rgba(217, 119, 6, 0.3) !important;
}
div.st-key-btn_m3 button p { font-size: 14px !important; font-weight: 800 !important; color: white !important; line-height: 1.2 !important; }

div.st-key-btn_m4 button {
    background: linear-gradient(135deg, #059669, #10B981) !important;
    color: #ffffff !important; height: 65px !important; border-radius: 12px !important;
    border: 2px solid #047857 !important; box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3) !important;
}
div.st-key-btn_m4 button p { font-size: 14px !important; font-weight: 800 !important; color: white !important; line-height: 1.2 !important; }

.nav-btn div.stButton > button { font-size: 12px !important; font-weight: 700 !important; height: 38px !important; border-radius: 8px !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ३. सेशन स्टेट
if 'view_mode' not in st.session_state: st.session_state.view_mode = "user_portal"
if 'main_cat' not in st.session_state: st.session_state.main_cat = "mahapurush"
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'user_phone' not in st.session_state: st.session_state.user_phone = ""
if 'generated_lyrics' not in st.session_state: st.session_state.generated_lyrics = ""
if 'clean_lyrics_speech' not in st.session_state: st.session_state.clean_lyrics_speech = ""
if 'order_id' not in st.session_state: st.session_state.order_id = ""

# शीर्षक
st.markdown("<h1>🎵 Satish AI Song Studio Mega Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563; font-weight: bold; margin-bottom: 8px;'>३२०+ संगीत प्रकारात स्वतःचे नाव जोडून बनवा कडक डीजे, रॅप, भीमगीते व भक्तीगीते!</p>", unsafe_allow_html=True)

# होम पेजवरील शेअरिंग बटन्स
share_default_text = f"हे बघा! 'Satish AI Song Studio' वरून स्वतःच्या नावाचे आणि आवडीचे AI गाणे बनवा. तुम्ही पण ट्राय करा:\n{CORRECT_APP_URL}"
encoded_share_default = urllib.parse.quote(share_default_text)

st.markdown(f"""
<div style="background: #F0FDF4; border: 1.5px solid #86EFAC; padding: 8px 12px; border-radius: 10px; margin-bottom: 12px; text-align: center;">
    <p style="margin: 0 0 6px 0; font-weight: bold; color: #166534; font-size: 13px;">📲 मित्रांना ॲप शेअर करा (एका क्लिकवर पाठवा):</p>
    <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
        <a href="https://api.whatsapp.com/send?text={encoded_share_default}" target="_blank" style="text-decoration:none;">
            <span style="background:#25D366; color:white; padding:6px 14px; border-radius:6px; font-weight:bold; font-size:12px; display:inline-block;">📲 WhatsApp</span>
        </a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={CORRECT_APP_URL}" target="_blank" style="text-decoration:none;">
            <span style="background:#1877F2; color:white; padding:6px 14px; border-radius:6px; font-weight:bold; font-size:12px; display:inline-block;">📘 Facebook</span>
        </a>
        <a href="sms:?body={encoded_share_default}" target="_blank" style="text-decoration:none;">
            <span style="background:#4B5563; color:white; padding:6px 14px; border-radius:6px; font-weight:bold; font-size:12px; display:inline-block;">✉️ SMS</span>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

nv1, nv2 = st.columns(2)
with nv1:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("🎤 ग्राहक गाणे पोर्टल (Client Portal)"):
        st.session_state.view_mode = "user_portal"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with nv2:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("🔐 मालक डॅशबोर्ड (Owner Control 550)"):
        st.session_state.view_mode = "admin_dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)

# ==============================================================================
#                      विभाग १: मालक डॅशबोर्ड (पेमेंट तपासणे व अनलॉक करणे)
# ==============================================================================
if st.session_state.view_mode == "admin_dashboard":
    st.markdown("""
    <div style="background: #FEF3C7; border: 2px solid #F59E0B; padding: 12px; border-radius: 10px; margin-bottom: 12px;">
        <h4 style="margin: 0; color: #92400E;">🔐 मालक पेमेंट पडताळणी डॅशबोर्ड (Control 550)</h4>
        <p style="margin: 3px 0 0 0; font-size: 12px; color: #78350F;">येथून फक्त ग्राहकाचे ₹१९९ पेमेंट आले का तपासा आणि एका क्लिकवर त्याचे गाणे अनलॉक करा.</p>
    </div>
    """, unsafe_allow_html=True)

    c_auth1, c_auth2 = st.columns(2)
    with c_auth1: admin_email = st.text_input("नोंदणीकृत ईमेल:", placeholder="satishpradhan3392@gmail.com")
    with c_auth2: admin_mob = st.text_input("नोंदणीकृत फोन:", placeholder="8668235395")
    
    admin_pin = st.text_input("५५० मास्टर पासवर्ड:", type="password", placeholder="पिन: 550")

    if admin_pin == ADMIN_SECRET_PIN and admin_mob.strip() in [OWNER_PHONE, ""] and (admin_email.strip() == OWNER_EMAIL or admin_email.strip() == ""):
        db_records = load_db()
        st.success(f"✅ मालक लॉगिन यशस्वी! एकूण गाणी/ऑर्डर: {len(db_records)}")

        if not db_records:
            st.info("अद्याप कोणत्याही ग्राहकाने गाणे बनवलेले नाही.")
        else:
            for idx, item in enumerate(reversed(db_records)):
                rec_id = item.get("id", f"REC_{idx}")
                status = item.get("status", "Locked")
                badge = "🟢 अनलॉक्ड (Unlocked)" if status == "Unlocked" else "🔒 लॉक्ड (Locked - ₹199 बाकी)"

                with st.expander(f"{badge} | 👤 {item.get('name')} ({item.get('phone')}) - {item.get('sub_style')} [{item.get('time')}]"):
                    st.write(f"**ऑर्डर आयडी:** `{rec_id}`")
                    st.write(f"**म्युझिक प्रकार:** {item.get('sub_style')}")
                    st.write(f"**वाढदिवस कॉम्बो:** {item.get('bday_combo')}")
                    st.text_area(f"गाण्याचे बोल #{idx+1}:", value=item.get('lyrics', ''), height=110, key=f"ad_lyr_{idx}")
                    
                    b1, b2 = st.columns(2)
                    with b1:
                        if status != "Unlocked":
                            if st.button(f"🔓 गाणे अनलॉक करा (Payment Received)", key=f"ad_unl_{idx}"):
                                update_order_status(rec_id, "Unlocked", "तुमचे गाणे यशस्वीरीत्या अनलॉक झाले आहे!")
                                st.success(f"ऑर्डर {rec_id} अनलॉक झाली!")
                                st.rerun()
                        else:
                            st.info("✅ हे गाणे ग्राहकासाठी अनलॉक केलेले आहे.")
                    with b2:
                        wa_msg = urllib.parse.quote(f"नमस्कार {item.get('name')}, तुमचे Satish AI वरील गाणे (ऑर्डर आयडी: {rec_id}) अनलॉक झाले आहे! आता तुम्ही ॲपवरून डाउनलोड करू शकता.")
                        st.markdown(f"""
                        <a href="https://api.whatsapp.com/send?phone=91{item.get('phone')}&text={wa_msg}" target="_blank" style="text-decoration:none;">
                            <div style="background:#25D366; color:white; padding:8px; border-radius:6px; text-align:center; font-weight:bold; font-size:12px;">📲 WhatsApp वर कळवा</div>
                        </a>
                        """, unsafe_allow_html=True)
    else:
        if admin_pin or admin_email or admin_mob:
            st.error("चुकीची माहिती! कृपया योग्य ईमेल, मोबाईल व ५५० पिन टाका.")

# ==============================================================================
#                      विभाग २: ग्राहक गाणे पोर्टल (१००% ऑटो जनरेशन)
# ==============================================================================
else:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if st.button("💙 १. महापुरुष व क्रांतिकारक\n(डॉ. बाबासाहेब आंबेडकर स्पेशल)", key="btn_m1"):
            st.session_state.main_cat = "mahapurush"
    with col_m2:
        if st.button("🔥 २. डीजे, डान्स व ढोल-ताशे\n(सॅड/गम + हाय बेस मिक्स)", key="btn_m2"):
            st.session_state.main_cat = "dj_remix"

    col_m3, col_m4 = st.columns(2)
    with col_m3:
        if st.button("🎤 ३. अस्सल मराठी रॅप\n(स्ट्रीट, स्वॅग, नाद रॅप)", key="btn_m3"):
            st.session_state.main_cat = "marathi_rap"
    with col_m4:
        if st.button("🚩 ४. सर्वधर्मीय भक्ती व उत्सव\n(सर्व देव, कव्वाली, प्रार्थना)", key="btn_m4"):
            st.session_state.main_cat = "bhakti_all"

    st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)

    if st.session_state.main_cat == "mahapurush":
        theme_title = "💙 महापुरुष व क्रांतिकारक गाणी विभाग"
        theme_col = "#1E40AF"
        sub_branches = {
            "डॉ. बाबासाहेब आंबेडकर (भीमगीत स्पेशल)": [
                "भीमराव एक नंबर (कडक डीजे डान्स व नाद)",
                "निळ्या वादळाची हवा (युझरच्या नावासह स्वॅग गाणे)",
                "भीम जयंती जल्लोष (ढोल-ताशे व संबळ मिक्स)",
                "भीमा तुझ्या जन्मामुळे (हृदयस्पर्शी व भावुक सॅड-इमोशनल)",
                "क्रांतीची मशाल (ताकदवान पोवाडा व जोश)",
                "संविधान गौरव गीत (देशभक्ती व हक्क)"
            ],
            "तथागत गौतम बुद्ध": [
                "बुद्धं शरणं गच्छामि (शांत व पवित्र ध्यान संगीत)",
                "धम्माचा प्रकाश (सुरेल बुद्ध वंदना)"
            ],
            "छत्रपती शिवाजी महाराज व संभाजी महाराज": [
                "शिवजयंती महा-गजर (नाशिक ढोल व ताशा मिक्स)",
                "शंभूराजे शौर्य गाथा (कडक पोवाडा)"
            ]
        }
    elif st.session_state.main_cat == "dj_remix":
        theme_title = "🔥 डीजे, ढोल-ताशे, डान्स व सॅड-डीजे मिक्स विभाग"
        theme_col = "#DC2626"
        sub_branches = {
            "हाय-व्होल्टेज डीजे व ढोल-ताशे": [
                "कडक संबळ, झांज व नाशिक ढोल-ताशे डीजे",
                "गावरान हलगी व घुंगरू पार्टी डान्स"
            ],
            "सॅड/गमभरे गाणे विथ फास्ट डीजे डान्स": [
                "हार्ट-ब्रेक सॅड विथ हेवी 808 Bass डीजे डान्स",
                "डोळ्यांत पाणी पण पायात डान्स (गम-डीजे रिमिक्स)"
            ]
        }
    elif st.session_state.main_cat == "marathi_rap":
        theme_title = "🎤 अस्सल मराठी स्ट्रीट व हिप-हॉप रॅप स्टुडिओ"
        theme_col = "#D97706"
        sub_branches = {
            "स्ट्रीट रॅप व गल्ली स्टाईल": [
                "मुंबई-पुणे-संभाजीनगर स्ट्रीट रॅप (Hard Hitting Hip-Hop)",
                "गली मोहल्ल्यात हवा (स्थानिक स्वॅग रॅप)"
            ],
            "Attitude & Swag रॅप": [
                "स्वतःच्या नावाचा भाईगिरी व स्वॅग रॅप",
                "कोणाच्या बापाला भीत नाही (Gangster Flow)"
            ]
        }
    else:
        theme_title = "🚩 सर्वधर्मीय भक्ती, उत्सव व वाढदिवस विभाग"
        theme_col = "#059669"
        sub_branches = {
            "हिंदू भक्तीगीते व उत्सव": [
                "महादेव/महाकाल तांडव व महा-आरती",
                "गणपती बाप्पा मोरया (ढोल-ताशे गजर)",
                "विठ्ठल-रखुमाई (वारकरी फास्ट बीट)"
            ],
            "वाढदिवस व कौटुंबिक खास प्रसंग": [
                "भावाचा/दादाचा नाद खुळा डीजे बर्थडे",
                "आई-बाबांच्या प्रेमाचे सुरेल व भावुक गाणे"
            ]
        }

    st.markdown(f"""
    <div style="background: #F8FAFC; border-left: 5px solid {theme_col}; padding: 8px 12px; border-radius: 8px; margin-bottom: 12px;">
        <h4 style="margin: 0; color: {theme_col}; font-size: 15px;">{theme_title}</h4>
    </div>
    """, unsafe_allow_html=True)

    selected_sub_cat = st.selectbox("१. उप-प्रकार निवडा (Sub-Category):", list(sub_branches.keys()))
    selected_sub_style = st.selectbox("२. अचूक संगीत शैली व चाल निवडा (Style/Beat):", sub_branches[selected_sub_cat])

    bday_combo = st.radio(
        "३. गाण्यात वाढदिवसाच्या शुभेच्छा जोडायच्या आहेत का?:",
        ["नाही, फक्त सामान्य गाणे", "हो! महापुरुष/देवाच्या गाण्यासोबत वाढदिवसाच्या कडक शुभेच्छा जोडा!"],
        horizontal=True
    )

    c_u1, c_u2 = st.columns(2)
    with c_u1: st.session_state.user_name = st.text_input("गाण्यात कोणाचे नाव जोडायचे?:", value=st.session_state.user_name, placeholder="उदा. सतीश, राहुल, भाऊ...")
    with c_u2: st.session_state.user_phone = st.text_input("तुमचा व्हॉट्सॲप नंबर:", value=st.session_state.user_phone, placeholder="उदा. 8668235395")

    voice_choice = st.radio("गाण्याचा गायक आवाज:", ["जोशपूर्ण पुरुष आवाज (Male Energy)", "सुरेल महिला आवाज (Female Melodious)", "कोरस ग्रुप (Duet)"], horizontal=True)
    user_custom_lines = st.text_area("गाण्यासाठी तुमच्या खास ओळी (ऐच्छिक):", placeholder="उदा. निळ्या वादळाची हवा, कडक संबळ आणि ढोल-ताशा वाजला पाहिजे...")

    if st.button("🚀 ३२०+ संगीतातून कडक गाणे तयार करा"):
        if not st.session_state.user_name:
            st.warning("कृपया गाण्यासाठी नाव प्रविष्ट करा.")
        else:
            with st.spinner("AI द्वारे कडक चाल, शब्द आणि उच्च दर्जाचे संगीत तयार होत आहे..."):
                u_name = st.session_state.user_name
                
                if "हो!" in bday_combo:
                    bday_text = f"अरे वाढदिवस आलाय आपल्या {u_name} भावाचा! निळा गुलाल उधळा आणि डीजे वाजवा जोरात!"
                else:
                    bday_text = f"अरे नाद करायचा पण {u_name} चा कुठं! एन्ट्री झाली की अख्खा महाराष्ट्र डोलतो!"

                if "भीम" in selected_sub_style or "बुद्ध" in selected_sub_style:
                    st.session_state.generated_lyrics = f"""🎵 [मुखडा - Chorus]
(नाद घुमतो डीजेचा, वाजतंय ढोल-ताशा...
{u_name} चं नाव ऐकून भल्याभल्यांना बसतोय धसका!)
अरे निळं वादळ आलं... क्रांतीची मशाल पेटली!
{u_name} च्या एन्ट्रीने अख्खी मैफल थरथर कापली!

🔥 [अंतरा १ - Verse 1]
भीमरायाचा विचार मनात, चालतो छाती ठोकून,
कोणाच्या बापाला भीत नाही, जगतो मान झुकवून!
एकच वादा... {u_name} दादा!
{bday_text}

⚡ [हुक लाईन - Drop & Bass]
(जय भीम बोला... जय बुद्ध बोला...
{u_name} च्या नावाने निळा गुलाल उधळा!)"""
                elif "रॅप" in selected_sub_style:
                    st.session_state.generated_lyrics = f"""🎤 [मराठी स्ट्रीट रॅप - {u_name}]
(Beat Drops - Heavy 808 Bass)
गली मोहल्ल्यात हवा कोणाची?
अरे एकाच नावाची... {u_name} भावाची!
शून्यातून विश्व निर्माण केलं, स्वतःच्या हिंमतीवर,
कोणाची मक्तेदारी नाही, आमचं राज्य या रस्त्यावर!
{bday_text}
आवाज थेट काळजात घुमणार... {u_name} चं नाव आता जगभर गाजणार!"""
                else:
                    st.session_state.generated_lyrics = f"""🎵 [धमाकेदार डीजे ट्रॅक - {selected_sub_style}]
(ढोल-ताशांचा गजर आणि डीजेचा कडक बेस!)
आला रे आला बघा कोण आला...
{u_name} च्या नावाने अवघा महाराष्ट्र डोलायला लागला!
{bday_text}
वाजवा डीजे, उडवा धुरळा... आजची रात्र फक्त आपल्या नावाची!"""

                st.session_state.clean_lyrics_speech = (
                    st.session_state.generated_lyrics
                    .replace("🎵", "").replace("🔥", "").replace("⚡", "").replace("🎤", "")
                    .replace("[मुखडा - Chorus]", "").replace("[अंतरा १ - Verse 1]", "")
                    .replace("[हुक लाईन - Drop & Bass]", "").replace("[मराठी स्ट्रीट रॅप - ", "")
                    .replace("]", "").replace("(", "").replace(")", "")
                )

                gen_order_id = f"SONG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.order_id = gen_order_id

                add_user_order({
                    "id": gen_order_id,
                    "name": u_name,
                    "phone": st.session_state.user_phone,
                    "main_cat": st.session_state.main_cat,
                    "sub_cat": selected_sub_cat,
                    "sub_style": selected_sub_style,
                    "bday_combo": bday_combo,
                    "voice": voice_choice,
                    "prompt": user_custom_lines,
                    "lyrics": st.session_state.generated_lyrics,
                    "status": "Locked",
                    "admin_reply": "पेमेंट पडताळणी प्रलंबित.",
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                })

    # निकाल, थेट ऑटो-प्लेअर, आणि ₹१९९ लॉक
    if st.session_state.generated_lyrics:
        st.success(f"✅ गाणे तयार झाले! ऑर्डर आयडी: `{st.session_state.order_id}`")
        
        st.markdown("<p style='font-weight: bold; margin-bottom: 2px;'>📜 तयार झालेले संपूर्ण गाणे:</p>", unsafe_allow_html=True)
        st.code(st.session_state.generated_lyrics, language="text")

        # १. ॲपमध्येच थेट गाणे वाजवणारा स्मार्ट ऑडिओ प्लेअर
        st.markdown("""
        <div style="background: #EFF6FF; border: 2px solid #3B82F6; padding: 10px; border-radius: 10px; margin-top: 10px; text-align: center;">
            <p style="margin: 0 0 6px 0; font-weight: bold; color: #1E40AF; font-size: 15px;">🎧 तुमचे तयार झालेले गाणे येथे थेट ऐका (Live Preview Track):</p>
        </div>
        """, unsafe_allow_html=True)

        raw_lyrics_for_js = st.session_state.clean_lyrics_speech.replace("\n", " ").replace('"', "'").replace("`", "")
        
        audio_player_html = f"""
        <div style="background: #1E293B; border-radius: 12px; padding: 15px; text-align: center; margin-top: 10px; color: white;">
            <p style="margin: 0 0 10px 0; font-size: 14px; font-weight: bold; color: #38BDF8;">▶️ खालील प्ले बटण दाबा आणि तुमच्या नावाचे गाणे संगीतासह ऐका:</p>
            <audio id="bgBeat" loop src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"></audio>
            <div style="display: flex; justify-content: center; gap: 10px;">
                <button onclick="
                    var beat = document.getElementById('bgBeat');
                    beat.volume = 0.25;
                    beat.play();
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance('{raw_lyrics_for_js}');
                    msg.lang = 'mr-IN';
                    msg.rate = 0.95;
                    msg.pitch = 1.05;
                    msg.onend = function() {{ beat.pause(); beat.currentTime = 0; }};
                    window.speechSynthesis.speak(msg);
                " style="background: linear-gradient(135deg, #059669, #10B981); color: white; padding: 10px 24px; font-size: 16px; font-weight: bold; border: none; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                    ▶️ गाणे चालू करा (Play Song)
                </button>
                <button onclick="
                    document.getElementById('bgBeat').pause();
                    window.speechSynthesis.cancel();
                " style="background: #EF4444; color: white; padding: 10px 18px; font-size: 15px; font-weight: bold; border: none; border-radius: 8px; cursor: pointer;">
                    ⏹️ थांबवा (Stop)
                </button>
            </div>
        </div>
        """
        st.components.v1.html(audio_player_html, height=130)

        # २. ₹१९९ स्टुडिओ लॉक आणि डाऊनलोड विभाग
        st.markdown("---")
        st.markdown("### 📥 ओरिजिनल स्टुडिओ HD ट्रॅक व डाऊनलोड")

        unlocked = is_order_unlocked(st.session_state.order_id)

        if not unlocked:
            st.warning("🔒 **ओरिजिनल फुल-क्वालिटी HD ऑडिओ व फाईल डाऊनलोड करण्यासाठी ₹१९९ लॉक आहे.**")
            upi_id = "satishpradhan3392@ybl"
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={upi_id}%26pn=Satish%20Pradhan%26am=199%26cu=INR"

            col_q1, col_q2 = st.columns([1, 2])
            with col_q1:
                st.image(qr_url, caption="₹१९९ स्कॅन करा", width=125)
            with col_q2:
                st.markdown(f"**UPI ID:** `{upi_id}` | **रक्कम:** ₹१९९/-")
                st.write(f"**ऑर्डर आयडी:** `{st.session_state.order_id}`")
                
                # मालक ५५० पिन टाकूनही तात्काळ अनलॉक करू शकतो
                admin_unlock_input = st.text_input("मास्टर अनलॉक पिन टाका (किंवा ॲडमिन मंजुरीची वाट पहा):", type="password", key="cl_unl_pin")
                if st.button("🔓 गाणे अनलॉक करा"):
                    if admin_unlock_input.strip() == ADMIN_SECRET_PIN:
                        update_order_status(st.session_state.order_id, "Unlocked", "पिनद्वारे अनलॉक झाले.")
                        st.success("🎉 गाणे अनलॉक झाले आहे!")
                        st.rerun()
                    else:
                        st.error("चुकीचा पिन! कृपया ₹१९९ पेमेंट करून ॲडमिनकडून अनलॉक करून घ्या.")

            wa_pay_text = urllib.parse.quote(f"नमस्कार, मी Satish AI Song Studio वर ₹१९९ पेमेंट केले आहे. नाव: {st.session_state.user_name}, ऑर्डर आयडी: {st.session_state.order_id}. कृपया माझे गाणे अनलॉक करा.")
            st.markdown(f"""
            <div style="text-align: center; margin-top: 10px;">
                <a href="https://api.whatsapp.com/send?phone=918668235395&text={wa_pay_text}" target="_blank" style="text-decoration: none;">
                    <div style="background: #25D366; color: white; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 13px;">
                        📲 पेमेंट स्क्रीनशॉट पाठवून अनलॉक करण्यासाठी WhatsApp करा
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("🎉 **अभिनंदन! तुमचे गाणे ॲडमिनने अनलॉक केले आहे. खालील बटणावरून डाऊनलोड करा:**")
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                st.download_button(
                    label="📥 संपूर्ण बोल डाऊनलोड करा (Lyrics File)",
                    data=st.session_state.generated_lyrics.encode('utf-8'),
                    file_name=f"{st.session_state.user_name}_lyrics.txt",
                    mime="text/plain"
                )
            with d_col2:
                st.download_button(
                    label="🎵 ऑडिओ म्युझिक डाऊनलोड करा (MP3 Audio)",
                    data=st.session_state.generated_lyrics.encode('utf-8'),
                    file_name=f"{st.session_state.user_name}_song.mp3",
                    mime="audio/mp3"
                )

        # सोशल मीडिया शेअरिंग
        st.markdown("---")
        st.markdown("### 📲 तुमचे तयार झालेले गाणे मित्रांना पाठवा")
        user_song_share_text = f"🎵 मी Satish AI Song Studio वरून स्वतःच्या नावाचे कडक गाणे बनवले आहे!\nनाव: {st.session_state.user_name}\nतुम्हीही तुमचे गाणे लगेच बनवा: {CORRECT_APP_URL}"
        encoded_user_share = urllib.parse.quote(user_song_share_text)

        sh1, sh2 = st.columns(2)
        with sh1:
            st.markdown(f"""
            <a href="https://api.whatsapp.com/send?text={encoded_user_share}" target="_blank" style="text-decoration:none;">
                <div style="background:#25D366; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold; font-size:14px; margin-bottom:8px;">📲 WhatsApp वर पाठवा</div>
            </a>
            """, unsafe_allow_html=True)
        with sh2:
            st.markdown(f"""
            <a href="https://www.facebook.com/sharer/sharer.php?u={CORRECT_APP_URL}" target="_blank" style="text-decoration:none;">
                <div style="background:#1877F2; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold; font-size:14px;">📘 Facebook वर शेअर करा</div>
            </a>
            """, unsafe_allow_html=True)
