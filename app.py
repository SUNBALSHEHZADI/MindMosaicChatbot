import streamlit as st
import torch
import random
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from groq import Groq

# Initialize components
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    model = AutoModelForSequenceClassification.from_pretrained("KevSun/Personality_LM", ignore_mismatched_sizes=True)
    tokenizer = AutoTokenizer.from_pretrained("KevSun/Personality_LM")
except Exception as e:
    st.error(f"Initialization error: {str(e)}")
    st.stop()

# Configure Streamlit
st.set_page_config(page_title="🧠 Mind Mosaic chatbot", layout="wide", page_icon="🚀")

# Custom CSS
st.markdown("""
<style>
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.quote-box {
    animation: fadeIn 1s ease-in;
    border-left: 5px solid #4CAF50;
    padding: 20px;
    margin: 20px 0;
    background: #f8fff9;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.tip-card {
    padding: 15px;
    margin: 10px 0;
    background: #fff3e0;
    border-radius: 10px;
    border: 1px solid #ffab40;
}
.social-post {
    background: #e3f2fd;
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
}
.nav-btn {
    margin: 8px 0;
    width: 100%;
    transition: all 0.3s ease;
}
.nav-btn:hover {
    transform: scale(1.02);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Personality configuration
OCEAN_TRAITS = ["agreeableness", "openness", "conscientiousness", "extraversion", "neuroticism"]
QUESTION_BANK = [
    {"text": "If your personality was a pizza topping, what would you be? 🍕", "trait": "openness"},
    {"text": "Describe your ideal morning vs reality ☀️", "trait": "conscientiousness"},
    {"text": "How would you survive a zombie apocalypse? 🧟", "trait": "neuroticism"},
    {"text": "What's your spirit animal in meetings? 🦄", "trait": "agreeableness"},
    {"text": "Plan a perfect day for your arch-rival 😈", "trait": "extraversion"},
    {"text": "If stress was weather, what's your forecast? ⛈️", "trait": "neuroticism"},
    {"text": "What would your Netflix history say about you? 🎬", "trait": "openness"},
    {"text": "Describe your phone as a Shakespearean sonnet 📱", "trait": "conscientiousness"},
    {"text": "React to 'We need to talk' 💬", "trait": "agreeableness"},
    {"text": "Your superhero name in awkward situations? 🦸", "trait": "extraversion"}
]

# Session state management
if 'started' not in st.session_state:
    st.session_state.started = False
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

# Functions
def generate_quote():
    prompt = "Create an inspirational quote about self-improvement with 2 emojis"
    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def analyze_personality(text):
    encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=64)
    with torch.no_grad():
        outputs = model(**encoded_input)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return {trait: score.item() for trait, score in zip(OCEAN_TRAITS, predictions[0])}

def create_pdf_report(traits, quote):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "🌟 Mind Mosaic chatbot Report 🌟")
    p.setFont("Helvetica", 12)
    
    y_position = 700
    for trait, score in traits.items():
        p.drawString(100, y_position, f"{trait.upper()}: {score:.2f}")
        y_position -= 20
    
    p.drawString(100, y_position-40, "Personalized Quote:")
    p.drawString(100, y_position-60, quote)
    p.save()
    buffer.seek(0)
    return buffer

def generate_social_post(platform, tone, traits):
    tone_instructions = {
        "funny": "Include humor and 3+ emojis. Make it lighthearted but not offensive",
        "serious": "Professional tone with inspirational message. Use 1-2 relevant emojis"
    }
    platform_formats = {
        "LinkedIn": "professional networking style",
        "Instagram": "visual storytelling with emojis",
        "Facebook": "community-oriented friendly tone",
        "WhatsApp": "casual conversational style",
        "Twitter": "concise with trending hashtags"
    }
    prompt = f"""Create a {tone} {platform} post about personal growth using these traits:
{traits}
Format: {platform_formats[platform]}
Tone: {tone_instructions[tone]}
Max length: 280 characters"""
    
    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9 if tone == "funny" else 0.5
    )
    return response.choices[0].message.content

# Main UI
if not st.session_state.started:
    st.markdown(f"""
    <div class="quote-box">
        <h2>🌟 Welcome to Mind Mosaic chatbot 🌟</h2>
        <h3>{generate_quote()}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Start Personality Analysis!", use_container_width=True):
        st.session_state.started = True
        st.session_state.selected_questions = random.sample(QUESTION_BANK, 5)
        st.rerun()
else:
    # Sidebar navigation
    with st.sidebar:
        st.title("🧭 Navigation")
        st.markdown("---")
        nav_options = {
            "📋 Personality Report": "View detailed personality analysis",
            "📱 Social Media Post": "Generate platform-specific posts",
            "💡 Success Tips": "Get personalized improvement tips",
            "📥 Download Report": "Download complete PDF report"
        }
        
        for option, help_text in nav_options.items():
            if st.button(option, key=option, use_container_width=True, help=help_text):
                st.session_state.page = option

    # Question flow
    if st.session_state.current_q < 5:
        q = st.session_state.selected_questions[st.session_state.current_q]
        st.progress(st.session_state.current_q/5, text="Assessment Progress")
        
        with st.chat_message("assistant"):
            st.markdown(f"### {q['text']}")
            user_input = st.text_input("Your response:", key=f"q{st.session_state.current_q}")
            
            if st.button("Next ➡️"):
                st.session_state.responses.append(user_input)
                st.session_state.current_q += 1
                st.rerun()
    else:
        # Process responses
        traits = analyze_personality("\n".join(st.session_state.responses))
        quote = generate_quote()
        
        # Current page display
        if st.session_state.page == "📋 Personality Report":
            st.header("📊 Personality Breakdown")
            cols = st.columns(5)
            for i, (trait, score) in enumerate(traits.items()):
                cols[i].metric(label=trait.upper(), value=f"{score:.2f}")
            
            st.divider()
            st.header("🎭 Emotional Landscape")
            df = pd.DataFrame({
                "Trait": traits.keys(),
                "Score": traits.values()
            })
            st.bar_chart(df.set_index("Trait"))

        elif st.session_state.page == "📱 Social Media Post":
            st.header("🎨 Create Social Post")
            col1, col2 = st.columns(2)
            with col1:
                platform = st.selectbox("Select Platform:", ["LinkedIn", "Instagram", "Facebook", "WhatsApp", "Twitter"])
            with col2:
                tone = st.radio("Post Tone:", ["😄 Funny", "🎯 Serious"], horizontal=True)
            
            if st.button("✨ Generate Post", type="primary"):
                post = generate_social_post(platform, tone.split()[1].lower(), traits)
                st.session_state.post = post
            
            if 'post' in st.session_state:
                st.markdown(f"""
                <div class="social-post">
                    <p>{st.session_state.post}</p>
                </div>
                """, unsafe_allow_html=True)
                st.button("📋 Copy Post", on_click=lambda: st.write(st.session_state.post))

        elif st.session_state.page == "💡 Success Tips":
            st.header("💎 Personality Success Tips")
            tips = [
                "🌅 Morning reflection: Start each day with 5 minutes of self-reflection",
                "🤝 Weekly connection: Have one meaningful conversation with someone new",
                "🎯 SMART goals: Set weekly Specific-Measurable-Achievable-Relevant-Timebound goals",
                "🧠 Neuroplasticity practice: Learn one new skill each month",
                "📚 Cross-training: Read outside your field 30 minutes daily",
                "💬 Active listening: Practice repeating back what others say before responding",
                "🔄 Feedback loop: Request constructive feedback weekly",
                "⚖️ Balance audit: Weekly review of work-life harmony",
                "😊 Emotional agility: Label emotions precisely throughout the day",
                "🚀 Growth challenges: Monthly comfort-zone expansion activity"
            ]
            for tip in tips:
                st.markdown(f"<div class='tip-card'>{tip}</div>", unsafe_allow_html=True)

        elif st.session_state.page == "📥 Download Report":
            st.header("📄 Complete Report")
            pdf_buffer = create_pdf_report(traits, quote)
            st.download_button(
                "⬇️ Download PDF Report",
                data=pdf_buffer,
                file_name="personacraft_pro_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
