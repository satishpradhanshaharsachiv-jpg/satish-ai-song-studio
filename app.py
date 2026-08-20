import streamlit as st
import urllib.parse

st.set_page_config(page_title="Satish AI Song Studio", page_icon="🎵", layout="centered")

# डिझाईन आणि स्टाईल
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
.main-title { text-align: center; color: #1E3A8A; font-weight: bold; }
.price-tag { background-color: #FEF08A; padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; color: #854D0E; }
</style>
""", unsafe_allow_html=True)

# ॲप शीर्षक
st.markdown("<h1 class='main-title'>🎵 Satish AI Song Studio</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center;'>तुमच्या मनाप्रमाणे गाण्याचे बोल आणि संगीत तयार करा!</p>", unsafe_allow_html=True)

st.markdown("---")

# ----------------- १. गाण्याची माहिती व बदल -----------------
st.subheader("✍️ पायरी १: गाण्याची माहिती व बोल (Edit Lyrics)")
st.info("💡 तुम्हाला हवे तितक्या वेळा तुम्ही खालील माहिती आणि गाण्याचे बोल बदलू शकता.")

name = st.text_input("१. तुमचे / ज्याच्यावर गाणे आहे त्याचे नाव:", value="")
mobile = st.text_input("२. तुमचा व्हॉट्सॲप नंबर:", value="")
genre = st.selectbox("३. संगीताचा प्रकार निवडा:", [
    "🎂 वाढदिवस स्पेशल (Birthday Special)",
    "❤️ रोमँटिक / प्रेमगीत (Romantic)",
    "🕺 पार्टी / डान्स (Dance / Party)",
    "🎤 रॅप / हिप-हॉप (Rap / Hip-Hop)",
    "🚩 भक्ती / ढोल-ताशा (Devotional)",
    "😢 भावनिक (Sad / Emotional)"
])
voice = st.radio("४. गाण्याचा आवाज:", ["पुरुष (Male Voice)", "स्त्री (Female Voice)", "लहान बाळ (Child Voice)"])
custom_lyrics = st.text_area("५. गाण्याचा विषय किंवा स्वतःचे बोल (Lyrics):", placeholder="उदा. विशालचा वाढदिवस आहे, तो खूप हसमुख आणि सर्वांचा लाडका आहे...")

st.markdown("---")

# ----------------- २. सॅम्पल गाणे (Preview) -----------------
st.subheader("🎧 पायरी २: सॅम्पल गाणे ऐका (Demo Track)")
st.write("🔊 खालील सॅम्पल गाणे कमी आवाजात ऐकून तपासा:")

# सॅम्पल ऑडिओ (डेमो ऑडिओ प्लेअर)
demo_audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
st.audio(demo_audio_url, format="audio/mp3")

st.markdown("---")

# ----------------- ३. लॉक व पेमेंट अनलॉक सिस्टीम -----------------
st.subheader("🔒 पायरी ३: फुल HD गाणे अनलॉक व डाउनलोड (₹199)")

st.markdown("<div class='price-tag'>💰 Full HD गाणे + WhatsApp डिलिव्हरी चार्ज: फक्त ₹199</div>", unsafe_allow_html=True)
st.write("")

st.markdown("👉 **UPI ID वर ₹199 भरा:** `satishpradhan3392@ybl`")

# व्हॉट्सॲप ऑर्डर बटण
msg = f"नमस्कार सतीशजी!\nमी गाण्याची ऑर्डर दिली आहे.\n\n*नाव:* {name}\n*मोबाईल:* {mobile}\n*प्रकार:* {genre}\n*विषय/बोल:* {custom_lyrics}\n\nमी ₹199 पेमेंट केले आहे, स्क्रीनशॉट सोबत जोडत आहे. मला अनलॉक कोड पाठवा."
encoded_msg = urllib.parse.quote(msg)
wa_order_url = f"https://wa.me/918668235395?text={encoded_msg}"

st.markdown(f"""
    <a href="{wa_order_url}" target="_blank">
        <button style="background-color:#25D366; color:white; padding:12px; border:none; border-radius:8px; font-weight:bold; width:100%; font-size:16px; cursor:pointer; margin-bottom:15px;">
            📲 सतीशजींना ₹199 चा स्क्रीनशॉट पाठवा
        </button>
    </a>
""", unsafe_allow_html=True)

# अनलॉक कोड इनपुट (केवळ मालकाने कोड दिल्यावर अनलॉक होईल)
st.write("🔑 **सतीशजींकडून मिळालेला 'अनलॉक पासवर्ड' इथे टाका:**")
unlock_code = st.text_input("पासवर्ड / Unlock Code:", type="password")

# मालकाचा सिक्रेट पासवर्ड (उदा. SATISH199)
if unlock_code == "SATISH199":
    st.success("🎉 बधाई हो! तुमचे गाणे यशस्वीरित्या अनलॉक झाले आहे.")
    st.audio(demo_audio_url, format="audio/mp3")
    st.download_button(label="📥 फुल HD गाणे डाउनलोड करा (MP3)", data=b"Audio Content", file_name="Satish_AI_Song.mp3", mime="audio/mp3")
elif unlock_code != "":
    st.error("❌ चुकीचा पासवर्ड! कृपया सतीशजींना ₹199 च्या पेमेंटचा स्क्रीनशॉट पाठवून खरा पासवर्ड मिळवा.")
else:
    st.warning("🔒 सध्या गाणे लॉक आहे. पेमेंट करून सतीशजींकडून कोड मिळवा.")

st.markdown("---")

# ----------------- ४. मित्रांना ॲप शेअर करा -----------------
st.subheader("📲 मित्रांना हे ॲप शेअर करा")
share_text = "हे बघा! 'Satish AI Song Studio' वरून स्वतःच्या नावाचे आणि आवडीचे AI गाणे बनवा. तुम्ही पण ट्राय करा:"
app_url = "https://satish-ai-song-studio.streamlit.app"
encoded_share = urllib.parse.quote(f"{share_text}\n{app_url}")
wa_share_url = f"https://api.whatsapp.com/send?text={encoded_share}"

st.markdown(f"""
    <a href="{wa_share_url}" target="_blank">
        <button style="background-color:#075E54; color:white; padding:10px; border:none; border-radius:8px; font-weight:bold; width:100%; font-size:14px; cursor:pointer;">
            📤 WhatsApp वर मित्रांना शेअर करा
        </button>
    </a>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; font-size:12px; color:gray;'>मुख्य मालक व विकासक: सतीश अशोक प्रधान</p>", unsafe_allow_html=True)
