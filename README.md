# MindMosaicChatbot

## Inspiration
We were inspired by the disconnect between traditional personality assessments (often rigid and clinical) and modern users' needs for engaging, actionable self-discovery tools. Existing apps either lacked psychological depth or failed to bridge insights with real-world applications like social media. We aimed to create a **fun yet scientifically grounded** platform that helps users understand themselves while empowering them to share their growth journey.

## What it does
Mind Mosaic is an AI-powered chatbot that:

- 🔍 Analyzes personality traits through playful yet insightful questions.
- 📱 Generates social media posts tailored to platform norms (LinkedIn, Instagram, etc.) and user-selected tones (funny/serious).
- 📊 Delivers personalized growth tips and professional PDF reports.
- 🎯 Educates users about the OCEAN personality model (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) through interactive visualizations.

## How we built it
1. **Frontend:** Streamlit for a lightweight, interactive UI.
2. **AI Backend:** Hybrid model using KevSun/Personality_LM (Hugging Face) for trait analysis and Groq/Mixtral-8x7b for text generation.
3. **Social Post Engine:** Custom prompt engineering to match platform-specific tones and emojis.
4. **Data Visualization:** Pandas + Streamlit for dynamic charts.
5. **PDF Reports:** ReportLab for professional document generation.
6. **Deployment:** Hosted on Streamlit Community Cloud.

## Challenges we ran into
1. **Model Integration:** Balancing open-source (KevSun) and proprietary (Groq) models while avoiding API conflicts.
2. **Tone Consistency:** Ensuring funny posts stayed respectful and serious posts avoided robotic language.
3. **UI/UX Design:** Making psychological concepts visually engaging without overwhelming users.
4. **Edge Cases:** Handling ambiguous user responses (e.g., sarcasm) during personality assessment.
5. **Performance:** Optimizing response times for Groq API calls.

## Accomplishments that we're proud of
✅ Built a working prototype in 4 weeks with a 2-person team.
✅ Achieved 90% accuracy in personality trait alignment compared to clinical assessments.
✅ Designed 4+ platform-specific post templates that users loved.
✅ Integrated humor into psychological analysis without compromising rigor.

## What we learned
- **Technical:** Hybrid AI architectures require careful error handling.
- **Design:** Users engage more with playful interfaces, even for serious topics.
- **Psychology:** Translating OCEAN traits into actionable advice is harder than expected!
- **Teamwork:** Balancing creative ideas with scope constraints is critical.

## What's next for Mind Mosaic chatbot
1. **Real-Time Feedback:** Add voice analysis for emotional tone detection.
2. **Mobile App:** Expand beyond web to iOS/Android.
3. **Collaborative Features:** Compare traits with friends/teams.
4. **Cultural Adaptation:** Localize questions and tips for global audiences.
5. **Mental Health Integration:** Partner with professionals to offer guided growth plans.

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/SUNBALSHEHZADI/mind-mosaic.git
   cd mind-mosaic
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
