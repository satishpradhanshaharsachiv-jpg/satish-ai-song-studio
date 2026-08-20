import streamlit as st
import urllib.parse

st.set_page_config(page_title="Satish AI Song Studio", page_icon="🎵", layout="centered")

# मेनू लपवण्यासाठी डिझाईन
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("🎵 Satish AI Song Studio")
st.write("खास तुमच्या नावाचे आणि प्रसंगाचे AI गाणे बनवून घ्या!")

st.markdown("---")

# १. गाण्याचे बोल माहिती
st.subheader("पायरी १: गाण्याचे बोल (Lyrics) माहिती")
name = st.text_input("१. तुमचे पूर्ण नाव:")
mobile = st.text_input("२. तुमचा व्हॉट्सॲप नंबर:")
topic = st.text_area("३. गाण्याचा विषय (उदा. मित्राचा वाढदिवस, प्रेमाचे गाणे):")

# २. म्युझिक स्टाईल
st.subheader("पायरी २: म्युझिक स्टाईल (Music Style)")
genre = st.selectbox("गाण्याचा प्रकार निवडा:", [
    "🎂 वाढदिवस स्पेशल (Birthday Special)",
    "❤️ प्रेमाचे / रोमँटिक (Romantic)",
    "🕺 डान्स / पार्टी (Dance / Party)",
    "🎤 रॅप / हिप-हॉप (Rap / Hip-Hop)",
    "🚩 भक्ती / ढोल-ताशा (Devotional / Folk)",
    "😢 भावनिक / सॅड (Emotional / Sad)"
])

# ३. आवाजाची निवड
st.subheader("पायरी ३: आवाजाची निवड (Voice Selection)")
voice = st.radio("गाण्याचा आवाज कसा हवा?", ["पुरुष (Male Voice)", "स्त्री (Female Voice)", "लहान बाळ (Child Voice)"])

# ४. ऑर्डर आणि पेमेंट
st.subheader("पायरी ४: ऑर्डर आणि पेमेंट (Order & Payment)")

if st.button("🚀 गाण्याची ऑर्डर तयार करा"):
    if not name or not mobile or not topic:
        st.error("⚠️ कृपया नाव, मोबाईल नंबर आणि गाण्याचा विषय पूर्ण भरा!")
    else:
        st.success("तुमची गाण्याची ऑर्डर तयार झाली आहे!")
        st.info("हे गाणे सन [Suno AI] द्वारे संगीतबद्ध करून ऑडिओ फाईल मिळवण्यासाठी **₹49** पेमेंट करा.")
        st.markdown("👉 **UPI ID:** `satishpradhan3392@ybl`")
        
        # WhatsApp मेसेज
        msg = f"नमस्कार सतीशजी!\nमी गाण्याची ऑर्डर दिली आहे.\n\n*नाव:* {name}\n*मोबाईल:* {mobile}\n*प्रकार:* {genre}\n*आवाज:* {voice}\n*विषय:* {topic}\n\nमी पेमेंट केले आहे, स्क्रीनशॉट जोडत आहे."
        encoded_msg = urllib.parse.quote(msg)
        wa_url = f"https://wa.me/918668235395?text={encoded_msg}"
        
        st.markdown(f"""
            <a href="{wa_url}" target="_blank">
                <button style="background-color:#25D366; color:white; padding:15px; border:none; border-radius:10px; font-weight:bold; width:100%; font-size:16px; cursor:pointer;">
                    📲 WhatsApp वर ऑर्डर व स्क्रीनशॉट पाठवा
                </button>
            </a>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; font-size:12px; color:gray;'>विकासक: सतीश अशोक प्रधान</p>", unsafe_allow_html=True)

