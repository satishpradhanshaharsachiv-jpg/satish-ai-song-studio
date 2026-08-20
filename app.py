import streamlit as st
import json
import os
import urllib.parse
from datetime import datetime

# १. पेज सेटिंग्ज
st.set_page_config(page_title="Satish AI Song Studio Pro", page_icon="🎵", layout="centered")

# मास्टर ॲडमिन सिक्रेट पिन (५५० किंवा ७७८८)
ADMIN_SECRET_PIN = "550"
DB_FILE = "song_studio_portal_db.json"

# डेटाबेस फंक्शन्स
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_to_db(all_data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

def add_user_record(user_dict):
    db = load_db()
    db.append(user_dict)
    save_to_db(db)

def update_user_status(record_id, new_status, admin_msg=""):
    db = load_db()
    for item in db:
        if item.get("id") == record_id:
            item["status"] = new_status
            if admin_msg:
                item["admin_reply"] = admin_msg
    save_to_db(db)

# २. कॉम्पॅक्ट व मॉडर्न CSS
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Mukta:wght@400;600;700;800&display=swap');
* { font-family: 'Mukta', sans-serif !important; }

#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    visibility: hidden; display: none !important;
}
div[class^="viewerBadge"] { visibility: hidden; display: none !important; }
button[title="View source"] { display: none; }

h1 { color: #1E3A8A; font-weight: 800; text-align: center; font-size: 22px; margin-bottom: 2px; }
h2, h3 { font-size: 16px !important; font-weight: 700 !important; }
p, label, span { font-size: 13px !important; }

/* मुख्य ४ चमकदार बटने */
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

# ३. सेशन स्टेट
if 'view_mode' not in st.session_state: st.session_state.view_mode = "user_portal"
if 'category' not in st.session_state: st.session_state.category = "bhim_geet"
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'user_phone' not in st.session_state: st.session_state.user_phone = ""
if 'sub_genre' not in st.session_state: st.session_state.sub_genre = "भीमराव एक नंबर (कडक डीजे डान्स)"
if 'voice_type' not in st.session_state: st.session_state.voice_type = "जोशपूर्ण पुरुष आवाज (Male Energy)"
if 'custom_prompt' not in st.session_state: st.session_state.custom_prompt = ""
if 'generated_lyrics' not in st.session_state: st.session_state.generated_lyrics = ""
if 'current_order_id' not in st.session_state: st.session_state.current_order_id = ""

# शीर्षक
st.markdown("<h1>🎵 Satish AI Song Studio & Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563; font-weight: bold; margin-bottom: 8px;'>स्वतःचे नाव जोडून १ सेकंदात बनवा कडक डीजे, रॅप, भीमगीते व भक्तीगीते!</p>", unsafe_allow_html=True)
st.markdown("---")

# वरचे नेव्हिगेशन
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("🎤 ग्राहक गाणे पोर्टल (Client Portal)"):
        st.session_state.view_mode = "user_portal"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_nav2:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("🔐 मास्टर ॲडमिन डॅशबोर्ड (Control 550)"):
        st.session_state.view_mode = "admin_dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)

# ==============================================================================
#                      विभाग १: मास्टर ॲडमिन डॅशबोर्ड
# ==============================================================================
if st.session_state.view_mode == "admin_dashboard":
    st.markdown("""
    <div style="background: #FEF3C7; border: 2px solid #F59E0B; padding: 12px; border-radius: 10px; margin-bottom: 12px;">
        <h4 style="margin: 0; color: #92400E;">🔐 मास्टर ॲडमिन कंट्रोल डॅशबोर्ड (Admin Master 550)</h4>
        <p style="margin: 3px 0 0 0; font-size: 12px; color: #78350F;">येथून तुम्ही सर्व ग्राहकांचे अर्ज तपासू शकता, मंजूर/नामंजूर करू शकता व थेट रिप्लाय देऊ शकता.</p>
    </div>
    """, unsafe_allow_html=True)

    admin_pass = st.text_input("मास्टर पिन प्रविष्ट करा:", type="password", key="admin_pin_box", placeholder="पिन: 550")

    if admin_pass == ADMIN_SECRET_PIN:
        db_records = load_db()
        st.success(f"✅ ॲडमिन अधिकृत लॉगिन झाले! एकूण नोंदणीकृत ग्राहक/गाणी: {len(db_records)}")

        if not db_records:
            st.info("अद्याप कोणत्याही युझरने ऑर्डर किंवा गाणे सबमिट केलेले नाही.")
        else:
            for idx, item in enumerate(reversed(db_records)):
                rec_id = item.get("id", f"REC_{idx}")
                status = item.get("status", "Pending / पडताळणी बाकी")
                
                # स्टेटस रंग
                if "Approved" in status or "स्वीकृत" in status:
                    badge = "🟢 स्वीकृत (Approved)"
                elif "Rejected" in status or "नाकारले" in status:
                    badge = "🔴 नाकारले (Rejected)"
                else:
                    badge = "🟡 प्रलंबित (Pending)"

                with st.expander(f"{badge} | 👤 {item.get('name')} ({item.get('phone')}) - {item.get('category')} [{item.get('time')}]"):
                    st.write(f"**ऑर्डर आयडी:** `{rec_id}`")
                    st.write(f"**संगीत प्रकार:** {item.get('sub_genre')}")
                    st.write(f"**गायक आवाज:** {item.get('voice')}")
                    st.write(f"**ग्राहकाची संकल्पना:** {item.get('prompt')}")
                    st.text_area(f"गाण्याचे बोल (Lyrics #{idx+1}):", value=item.get('lyrics', ''), height=130, key=f"lyr_{idx}")

                    # ॲडमिन ॲक्शन: मंजूर / नामंजूर आणि रिप्लाय
                    st.markdown("---")
                    st.markdown("##### ⚡ ॲडमिन निर्णय व थेट रिप्लाय:")
                    
                    rep_msg = st.text_input(f"ग्राहकाला द्यायचा रिप्लाय / मेसेज:", value=item.get('admin_reply', 'तुमचे गाणे तपासून तयार झाले आहे.'), key=f"msg_{idx}")
                    
                    act1, act2, act3 = st.columns(3)
                    with act1:
                        if st.button(f"✅ स्वीकृत करा (Approve)", key=f"app_{idx}"):
                            update_user_status(rec_id, "Approved / स्वीकृत", rep_msg)
                            st.success("गाणे मंजूर झाले!")
                            st.rerun()
                    with act2:
                        if st.button(f"❌ नामंजूर करा (Reject)", key=f"rej_{idx}"):
                            update_user_status(rec_id, "Rejected / नाकारले", rep_msg)
                            st.error("गाणे नाकारले!")
                            st.rerun()
                    with act3:
                        # थेट ग्राहकाला WhatsApp पाठवा
                        wa_reply_text = urllib.parse.quote(f"नमस्कार {item.get('name')}, Satish AI Song Studio कडून अपडेट: {rep_msg} (ऑर्डर आयडी: {rec_id})")
                        wa_link = f"https://api.whatsapp.com/send?phone=91{item.get('phone')}&text={wa_reply_text}"
                        st.markdown(f"""
                        <a href="{wa_link}" target="_blank" style="text-decoration:none;">
                            <div style="background:#25D366; color:white; padding:8px; border-radius:6px; text-align:center; font-weight:bold; font-size:12px;">
                                📲 WhatsApp रिप्लाय द्या
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
    else:
        if admin_pass:
            st.error("चुकीचा मास्टर पिन! योग्य ५५० पिन टाका.")

# ==============================================================================
#                      विभाग २: ग्राहक गाणे निर्मिती पोर्टल
# ==============================================================================
else:
    # मुख्य ४ चमकदार संगीत वर्ग बटने
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

    # ऑडिओ किंवा रेफरन्स डॉक्युमेंट अपलोड पर्याय (फायनान्स ॲपसारखा)
    uploaded_file = st.file_uploader("तुमचा स्वतःचा व्हॉइस सॅम्पल किंवा संदर्भ फाईल अपलोड करा (ऐच्छिक):", type=["mp3", "wav", "m4a", "txt", "png", "jpg"])

    if st.button("🚀 एआय द्वारे सुपरहीट गाणे तयार करा"):
        if not st.session_state.user_name:
            st.warning("कृपया गाण्यासाठी नाव प्रविष्ट करा.")
        else:
            with st.spinner("AI द्वारे कडक चाल, बोल आणि म्युझिक तयार होत आहे..."):
                # स्मार्ट इनबिल्ट गीतकार इंजिन
                u_name = st.session_state.user_name
                s_genre = st.session_state.sub_genre

                if "भीम" in s_genre or "बुद्ध" in s_genre:
                    st.session_state.generated_lyrics = f"""🎵 [मुखडा - Chorus]
(नाद घुमतो डीजेचा, वाजतंय ढोल-ताशा...
{u_name} चं नाव ऐकून भल्याभल्यांना बसतोय धसका!)
अरे निळं वादळ आलं... क्रांतीची मशाल पेटली!
{u_name} च्या एन्ट्रीने अख्खी मैफल थरथर कापली!

🔥 [अंतरा १ - Verse 1]
भीमरायाचा विचार मनात, चालतो छाती ठोकून,
कोणाच्या बापाला भीत नाही, जगतो मान झुकवून!
एकच वादा... {u_name} दादा!
नाद करायचा पण आमचा कुठं... डीजे वाजवा जोरात आता!

⚡ [हुक लाईन - Drop]
(जय भीम बोला... जय बुद्ध बोला...
{u_name} च्या नावाने निळा गुलाल उधळा!)"""
                elif "रॅप" in s_genre:
                    st.session_state.generated_lyrics = f"""🎤 [मराठी स्ट्रीट रॅप - {u_name}]
(Beat Drops - Heavy 808 Bass)
गली मोहल्ल्यात हवा कोणाची?
अरे एकाच नावाची... {u_name} भावाची!
शून्यातून विश्व निर्माण केलं, स्वतःच्या हिंमतीवर,
कोणाची मक्तेदारी नाही, आमचं राज्य या रस्त्यावर!
आवाज थेट काळजात घुमणार... {u_name} चं नाव आता जगभर गाजणार!"""
                else:
                    st.session_state.generated_lyrics = f"""🎵 [धमाकेदार डीजे ट्रॅक - {u_name}]
(ढोल-ताशांचा गजर आणि डीजेचा कडक बेस!)
आला रे आला बघा कोण आला...
{u_name} च्या नावाने अवघा महाराष्ट्र डोलायला लागला!
वाजवा डीजे, उडवा धुरळा... आजची रात्र फक्त आपल्या नावाची!"""

                # युनिक ऑर्डर आयडी
                order_id = f"SONG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.current_order_id = order_id

                # डेटाबेसमध्ये कायमस्वरूपी नोंद
                add_user_record({
                    "id": order_id,
                    "name": u_name,
                    "phone": st.session_state.user_phone,
                    "category": st.session_state.category,
                    "sub_genre": s_genre,
                    "voice": st.session_state.voice_type,
                    "prompt": st.session_state.custom_prompt,
                    "lyrics": st.session_state.generated_lyrics,
                    "has_file": True if uploaded_file else False,
                    "status": "Pending / पडताळणी चालू",
                    "admin_reply": "अर्ज प्राप्त झाला आहे. ॲडमिन पडताळणी करत आहेत.",
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                })

    # ==================== निकाल, ऑडिओ व स्टेटस ====================
    if st.session_state.generated_lyrics:
        st.success(f"✅ गाणे तयार झाले! तुमची ऑर्डर आयडी: `{st.session_state.current_order_id}`")
        
        st.markdown("<p style='font-weight: bold; margin-bottom: 2px;'>📜 तयार झालेले संपूर्ण गाणे:</p>", unsafe_allow_html=True)
        st.code(st.session_state.generated_lyrics, language="text")

        # कमी आवाजातील सॅम्पल प्लेअर
        st.markdown("""
        <div style="background: #EFF6FF; border: 1px solid #BFDBFE; padding: 10px; border-radius: 8px; margin-top: 10px;">
            <p style="margin: 0; font-weight: bold; color: #1E40AF;">🎧 सॅम्पल गाणे ऐका (कमी आवाजात प्रिव्ह्यू):</p>
        </div>
        """, unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

        # ₹१९९ स्टुडिओ लॉक
        st.markdown("---")
        st.markdown("### 📥 ओरिजिनल स्टुडिओ HD ट्रॅक डाऊनलोड")
        st.info("🔒 **ओरिजिनल फुल-क्वालिटी HD ऑडिओ मिळवण्यासाठी ₹१९९ शुल्क आहे. पेमेंट झाल्यावर ॲडमिनकडून मिळालेला ५५० मास्टर पिन टाका.**")
        
        upi_id = "satishpradhan3392@ybl"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=upi://pay?pa={upi_id}%26pn=Satish%20Pradhan%26am=199%26cu=INR"

        col_q1, col_q2 = st.columns([1, 2])
        with col_q1:
            st.image(qr_url, caption="₹१९९ स्कॅन करा", width=125)
        with col_q2:
            st.markdown(f"**UPI ID:** `{upi_id}` | **रक्कम:** ₹१९९/-")
            unlock_pin_input = st.text_input("ॲडमिन अनलॉक पिन टाका:", type="password", key="client_unlock_pin")
            if st.button("🔓 गाणे अनलॉक करा"):
                if unlock_pin_input.strip() == ADMIN_SECRET_PIN:
                    st.success("🎉 गाणे अनलॉक झाले आहे!")
                    st.download_button(
                        label="📥 ओरिजिनल गाणे डाऊनलोड करा (Text/MP3)",
                        data=st.session_state.generated_lyrics.encode('utf-8'),
                        file_name=f"{st.session_state.user_name}_song.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("चुकीचा पिन! कृपया ॲडमिनशी संपर्क करा.")

        # WhatsApp सपोर्ट
        wa_text = urllib.parse.quote(f"नमस्कार, मी Satish AI Song Studio वर गाणे तयार केले आहे. नाव: {st.session_state.user_name}, ऑर्डर आयडी: {st.session_state.current_order_id}, कृपया माझे गाणे अप्रूव्ह करा.")
        st.markdown(f"""
        <div style="text-align: center; margin-top: 12px;">
            <a href="https://api.whatsapp.com/send?phone=918668235395&text={wa_text}" target="_blank" style="text-decoration: none;">
                <div style="background: #25D366; color: white; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 13px;">
                    📲 पेमेंट स्क्रीनशॉट पाठवण्यासाठी येथे WhatsApp करा
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
