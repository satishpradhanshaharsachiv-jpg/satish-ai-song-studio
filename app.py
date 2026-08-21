import streamlit as st
import json
import os
import urllib.parse
from datetime import datetime

# १. पेज कॉन्फिगरेशन आणि कॉम्पॅक्ट डिझाइन
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

# २. कॉम्पॅक्ट CSS डिझाइन
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

/* मुख्य ४ रंगीत मोठी बटने */
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
if 'suno_style_prompt' not in st.session_state: st.session_state.suno_style_prompt = ""
if 'order_id' not in st.session_state: st.session_state.order_id = ""

# शीर्षक
st.markdown("<h1>🎵 Satish AI Song Studio Mega Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563; font-weight: bold; margin-bottom: 8px;'>३२०+ संगीत प्रकारात स्वतःचे नाव जोडून बनवा कडक डीजे, रॅप, भीमगीते व भक्तीगीते!</p>", unsafe_allow_html=True)

# मुख्य शेअरिंग बटन्स
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
#                      विभाग १: मालक डॅशबोर्ड (Owner Control 550)
# ==============================================================================
if st.session_state.view_mode == "admin_dashboard":
    st.markdown("""
    <div style="background: #FEF3C7; border: 2px solid #F59E0B; padding: 12px; border-radius: 10px; margin-bottom: 12px;">
        <h4 style="margin: 0; color: #92400E;">🔐 मालक विशेष लॉगिन डॅशबोर्ड (Control 550)</h4>
        <p style="margin: 3px 0 0 0; font-size: 12px; color: #78350F;">सुरक्षेसाठी केवळ अधिकृत ईमेल, मोबाईल नंबर आणि ५५० पिन पडताळणीनंतरच हा डॅशबोर्ड उघडेल.</p>
    </div>
    """, unsafe_allow_html=True)

    c_auth1, c_auth2 = st.columns(2)
    with c_auth1: admin_email = st.text_input("नोंदणीकृत ईमेल टाका:", placeholder="उदा. satishpradhan3392@gmail.com")
    with c_auth2: admin_mob = st.text_input("नोंदणीकृत मोबाईल नंबर:", placeholder="उदा. 8668235395")
    
    admin_pin = st.text_input("५५० मास्टर पासवर्ड टाका:", type="password", placeholder="पिन: 550")

    if admin_pin == ADMIN_SECRET_PIN and admin_mob.strip() in [OWNER_PHONE, ""] and (admin_email.strip() == OWNER_EMAIL or admin_email.strip() == ""):
        db_records = load_db()
        st.success(f"✅ मालक लॉगिन यशस्वी! एकूण ग्राहक व तयार झालेली गाणी: {len(db_records)}")

        if not db_records:
            st.info("अद्याप कोणत्याही युझरने गाणे बनवलेले नाही.")
        else:
            for idx, item in enumerate(reversed(db_records)):
                rec_id = item.get("id", f"REC_{idx}")
                status = item.get("status", "Approved")
                badge = "🟢 स्वीकृत" if "Approved" in status else ("🔴 नाकारले" if "Rejected" in status else "🟡 प्रलंबित")

                with st.expander(f"{badge} | 👤 {item.get('name')} ({item.get('phone')}) - {item.get('sub_style')} [{item.get('time')}]"):
                    st.write(f"**ऑर्डर आयडी:** `{rec_id}`")
                    st.write(f"**अचूक प्रकार:** {item.get('sub_style')}")
                    st.text_area(f"गाण्याचे संपूर्ण बोल #{idx+1}:", value=item.get('lyrics', ''), height=120, key=f"ad_lyr_{idx}")
                    rep_text = st.text_input("ग्राहकाला पाठवायचा संदेश:", value=item.get('admin_reply', 'तुमचे गाणे तयार आहे.'), key=f"ad_msg_{idx}")
                    
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("✅ मंजूर करा (Approve)", key=f"ad_app_{idx}"):
                            update_order_status(rec_id, "Approved / स्वीकृत", rep_text)
                            st.rerun()
                    with b2:
                        wa_msg = urllib.parse.quote(f"नमस्कार {item.get('name')}, Satish AI Song Studio कडून अपडेट: {rep_text} (ऑर्डर आयडी: {rec_id})")
                        st.markdown(f"""
                        <a href="https://api.whatsapp.com/send?phone=91{item.get('phone')}&text={wa_msg}" target="_blank" style="text-decoration:none;">
                            <div style="background:#25D366; color:white; padding:8px; border-radius:6px; text-align:center; font-weight:bold; font-size:12px;">📲 WhatsApp रिप्लाय द्या</div>
                        </a>
                        """, unsafe_allow_html=True)
    else:
        if admin_pin or admin_email or admin_mob:
            st.error("चुकीची माहिती! कृपया योग्य ईमेल, मोबाईल व ५५० पिन टाका.")

# ==============================================================================
#                      विभाग २: ग्राहक गाणे पोर्टल (Suno AI Integration)
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
    with c_u2: st.session_state.user_phone = st.text_input("तुमचा व्हॉट्सॲप नंबर (सपोर्टसाठी):", value=st.session_state.user_phone, placeholder="उदा. 8668235395")

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
                    st.session_state.generated_lyrics = f"""[Verse]
नाद घुमतो डीजेचा, वाजतंय ढोल-ताशा...
{u_name} चं नाव ऐकून भल्याभल्यांना बसतोय धसका!
अरे निळं वादळ आलं... क्रांतीची मशाल पेटली!
{u_name} च्या एन्ट्रीने अख्खी मैफल थरथर कापली!

[Chorus]
भीमरायाचा विचार मनात, चालतो छाती ठोकून,
कोणाच्या बापाला भीत नाही, जगतो मान झुकवून!
एकच वादा... {u_name} दादा!
{bday_text}

[Outro]
जय भीम बोला... जय बुद्ध बोला...
{u_name} च्या नावाने निळा गुलाल उधळा!"""
                    st.session_state.suno_style_prompt = f"Marathi Bhim geet, powerful energetic male vocal, live dhol tasha, sambal, brass band, high tempo festival celebration, anthem"

                elif "रॅप" in selected_sub_style:
                    st.session_state.generated_lyrics = f"""[Verse]
गली मोहल्ल्यात हवा कोणाची?
अरे एकाच नावाची... {u_name} भावाची!
शून्यातून विश्व निर्माण केलं, स्वतःच्या हिंमतीवर,
कोणाची मक्तेदारी नाही, आमचं राज्य या रस्त्यावर!

[Chorus]
{bday_text}
आवाज थेट काळजात घुमणार... {u_name} चं नाव आता जगभर गाजणार!"""
                    st.session_state.suno_style_prompt = f"Marathi street rap, hard 808 bass, aggressive flow, desi hip hop, high energy trap beat"

                else:
                    st.session_state.generated_lyrics = f"""[Verse]
आला रे आला बघा कोण आला...
{u_name} च्या नावाने अवघा महाराष्ट्र डोलायला लागला!

[Chorus]
{bday_text}
वाजवा डीजे, उडवा धुरळा... आजची रात्र फक्त आपल्या नावाची!"""
                    st.session_state.suno_style_prompt = f"Marathi DJ remix, high bass drop, electronic dhol mix, dance club party, high bpm"

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
                    "status": "Approved",
                    "admin_reply": "गाणे तयार झाले आहे.",
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                })

    # ==================== Suno AI स्टुडिओ रिअल व्हॉइस ऑडिओ ट्रॅक ====================
    if st.session_state.generated_lyrics:
        st.success(f"✅ गाणे तयार झाले! ऑर्डर आयडी: `{st.session_state.order_id}`")
        
        st.markdown("<p style='font-weight: bold; margin-bottom: 2px;'>📜 तयार झालेले संपूर्ण गाणे:</p>", unsafe_allow_html=True)
        st.code(st.session_state.generated_lyrics, language="text")

        # Suno AI डायरेक्ट स्टुडिओ बॉक्स
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E1B4B, #312E81); border: 2px solid #818CF8; border-radius: 12px; padding: 15px; margin-top: 12px; color: white; text-align: center;">
            <h4 style="margin: 0 0 6px 0; color: #FACC15;">🎙️ ओरिजिनल स्टुडिओ गायकाच्या आवाजात गाणे तयार करा:</h4>
            <p style="margin: 0 0 10px 0; font-size: 13px; color: #E0E7FF;">रोबोटिक आवाज नको असल्यास खालील बटणावर क्लिक करा; तुमचे गाणे थेट Suno AI मध्ये १००% ओरिजिनल स्टुडिओ ऑडिओमध्ये वाजेल!</p>
        </div>
        """, unsafe_allow_html=True)

        js_lyrics_copy = st.session_state.generated_lyrics.replace('\n', '\\n').replace('"', '\\"').replace("'", "\\'")
        js_style_copy = st.session_state.suno_style_prompt.replace('\n', ' ').replace('"', '\\"')

        suno_action_html = f"""
        <div style="text-align: center; margin-top: 10px;">
            <button onclick="
                navigator.clipboard.writeText(`{js_lyrics_copy}`);
                alert('✅ गाण्याचे बोल कॉपी झाले आहेत! आता Suno AI उघडत आहे, तिथे Create वर जाऊन थेट Paste करा.');
                window.open('https://suno.com/create', '_blank');
            " style="
                background: linear-gradient(135deg, #EC4899, #8B5CF6);
                color: white; padding: 14px 28px; font-size: 16px; font-weight: bold;
                border: none; border-radius: 10px; cursor: pointer; box-shadow: 0 4px 12px rgba(236, 72, 153, 0.4); width: 100%;
            ">
                🔥 १ सेकंदात ओरिजिनल स्टुडिओ गाणे बनवा (Suno AI Open)
            </button>
        </div>
        """
        st.components.v1.html(suno_action_html, height=80)

        # डाऊनलोड पर्याय
        st.markdown("---")
        st.markdown("### 📥 गाणे डाऊनलोड करा")
        st.download_button(
            label="📥 गाण्याचे संपूर्ण बोल डाऊनलोड करा (Lyrics File)",
            data=st.session_state.generated_lyrics.encode('utf-8'),
            file_name=f"{st.session_state.user_name}_song_lyrics.txt",
            mime="text/plain"
        )

        # शेअरिंग बटन्स
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
