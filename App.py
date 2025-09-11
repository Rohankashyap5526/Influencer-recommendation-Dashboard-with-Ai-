import streamlit as st
import pandas as pd
import numpy as np
import joblib
import groq
import os
from streamlit_extras.metric_cards import style_metric_cards

# Initialize session state
if "predicted" not in st.session_state:
    st.session_state.predicted = False
if "top3_df" not in st.session_state:
    st.session_state.top3_df = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Set your Groq API Key
groq.api_key = "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"

# Streamlit Page Setup
# st.set_page_config(page_title="🎯 Influencer Recommender", layout="wide")

# Load ML model
model = joblib.load("influencer_model.pkl")

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_influencer_data.csv")

    def parse_followers(value):
        if isinstance(value, str):
            value = value.strip("~+").upper().replace(",", "").strip()
            try:
                if 'M' in value:
                    return float(value.replace('M', '')) * 1_000_000
                elif 'K' in value:
                    return float(value.replace('K', '')) * 1_000
                elif 'B' in value:
                    return float(value.replace('B', '')) * 1_000_000_000
                else:
                    return float(value)
            except:
                return np.nan
        return value

    def parse_engagement_rate(rate):
        if isinstance(rate, str):
            rate = rate.strip("~%")
            try:
                return float(rate)
            except:
                return np.nan
        return rate

    df["Follower Count"] = df["Follower Count"].apply(parse_followers)
    df["Engagement Rate"] = df["Engagement Rate"].apply(parse_engagement_rate)
    df = df.dropna(subset=["Follower Count", "Engagement Rate", "Category", "Country", "Platform Used"])
    return df

df = load_data()

# def generate_influencer_summary(influencer):
#     name = influencer['Influencer Name']
#     platform = influencer['Platform Used']
#     followers = int(influencer['Follower Count'])
#     engagement_rate = influencer['Engagement Rate']
#     category = influencer['Category']
#     country = influencer['Country']
#     return (
#         f"{name} is a prominent influencer in the {category} category, based in {country}. "
#         f"With {followers:,} followers on {platform}, they maintain an engagement rate of {engagement_rate}%. "
#         f"Ideal for promoting {category} products in {country}."
#     )
def generate_influencer_summary(influencer):
    name = influencer['Influencer Name']
    category = influencer['Category']
    country = influencer['Country']
    return (
        f"{name} is a well-known influencer in the {category} category from {country}. "
        f"Please look up their latest platform, follower count, engagement rate, and video promotion cost."
    )


# def get_groq_insight(influencer):
#     try:
#         client = groq.Groq(api_key=groq.api_key)
#         summary = generate_influencer_summary(influencer)
#         prompt_text = f"Return the influencer name, platform,followers, aprox cost per video, and detail summary of 100 words from this list:\n{summary}"

#         response = client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[
#                 {"role": "system", "content": "You are an assistant trained to summarize influencers."},
#                 {"role": "user", "content": prompt_text}
#             ]
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"❌ Groq API Error: {e}"
def get_groq_insight(influencer):
    try:
        client = groq.Groq(api_key=groq.api_key)
        summary = generate_influencer_summary(influencer)
        prompt_text = (
            f"Using the following influencer info:\n{summary}\n\n"
            f"Please return:\n- Influencer Name\n- Main Platform Used\n"
            f"- Approximate Follower Count\n- Engagement Rate (%)\n"
            f"- Estimated Cost per Sponsored Video\n"
            f"- A short (100-word) summary of the influencer’s content and reach."
        )

        response = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[
                {"role": "system", "content": "You are an assistant trained to find influencer data and summarize their impact."},
                {"role": "user", "content": prompt_text}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error fetching influencer insight: {e}"
def get_recommendation_from_groq(prompt):
    try:
        client = groq.Groq(api_key=groq.api_key)
        response = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[
                {"role": "system", "content": "You are an assistant providing influencer recommendations."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error in generating recommendation: {e}"

def extract_platforms(df):
    major_platforms = ["Instagram", "YouTube", "TikTok", "Twitter"]
    found_platforms = set()
    for value in df["Platform Used"]:
        for platform in major_platforms:
            if platform.lower() in value.lower():
                found_platforms.add(platform)
    return ["All"] + sorted(found_platforms)

# Tabs
tab1, tab2 = st.tabs(["Influencer Recommendations", "Chatbot"])

# ---------------------------------- Tab 1: Recommendations ----------------------------------
with tab1:
    st.markdown(
    """
   <style>
/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #0e1117;
}
::-webkit-scrollbar-thumb {
    background-color: #30363d;
    border-radius: 10px;
}

/* Input text boxes and labels */
input, textarea, .stTextInput > div > div > input, .stTextArea > div > textarea {
    background-color: #161b22;
    color: #f0f6fc;
    border: 1px solid #30363d;
    border-radius: 8px;
}

label {
    color: #c9d1d9 !important;
    font-weight: 500;
}

/* Chat message history styling */
.chat-entry {
    background-color: #161b22;
    color: #f0f6fc;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
}

/* Markdown tweaks */
.markdown-text-container p {
    color: #c9d1d9;
}

/* Tabs customization */
[data-baseweb="tab"] {
    background-color: #0e1117;
    color: #58a6ff;
}
</style>

    """,
    unsafe_allow_html=True
)

    st.title("🎯 Influencer Recommendation Dashboard")
    st.header("📌 Select Filters and Get Recommendations")

    col1, col2, col3 = st.columns(3)
    platform_options = extract_platforms(df)

    with col1:
        platform = st.selectbox("Platform", platform_options)
    with col2:
        category = st.selectbox("Product Category", sorted(df["Category"].unique()))
    with col3:
        country = st.selectbox("Target Country", sorted(df["Country"].unique()))

    budget = st.slider("Promotion Budget ($)", 100, 100000, 5000, step=500)
    submitted = st.button("🔍 Recommend Influencers")

    if submitted:
        df_filtered = df.copy()

        if platform != "All":
            df_filtered = df_filtered[df_filtered["Platform Used"].str.contains(platform, case=False, na=False)]

        df_filtered = df_filtered[
            (df_filtered["Category"] == category) & (df_filtered["Country"] == country)
        ]

        if df_filtered.empty:
            st.warning("No influencers match the selected filters.")
        else:
            X = df_filtered[["Follower Count", "Engagement Rate", "Category", "Country", "Platform Used"]]
            df_filtered["Score"] = model.predict(X)
            df_filtered["Estimated Cost"] = (df_filtered["Follower Count"] / 1000) * 10

            df_budgeted = df_filtered[df_filtered["Estimated Cost"] <= budget]

            if df_budgeted.empty:
                st.warning("No influencers within budget. Showing top 3 regardless.")
                top3 = df_filtered.sort_values("Score", ascending=False).head(3)
            else:
                top3 = df_budgeted.sort_values("Score", ascending=False).head(3)

            st.session_state.top3_df = top3.copy()
            st.session_state.predicted = True

            col1, col2, col3 = st.columns(3)
            st.markdown(
    """
 <style>
/* Custom metric card styling for dark mode */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1f6feb, #a371f7);
    color: #ffffff;
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
    border: 1px solid #30363d;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-align: center;
}

/* Add hover effect */
div[data-testid="stMetric"]:hover {
    transform: scale(1.03);
    box-shadow: 0 8px 20px rgba(163, 113, 247, 0.4);
}

/* Metric label (title) */
div[data-testid="stMetric"] > div:first-child {
    color: #c9d1d9;
    font-weight: 600;
    font-size: 16px;
    margin-bottom: 4px;
}

/* Metric value */
div[data-testid="stMetric"] > div:nth-child(2) {
    color: #ffffff;
    font-size: 24px;
    font-weight: bold;
}

/* Metric delta (change indicator) */
div[data-testid="stMetric"] > div:nth-child(3) {
    color: #2ea043; /* green tone */
    font-size: 14px;
}
</style>

    """,
    unsafe_allow_html=True
)

            col1.metric("🎯 Top Influencer", top3.iloc[0]['Influencer Name'])
            col2.metric("💵 Est. Cost", f"${top3.iloc[0]['Estimated Cost']:.2f}")
            col3.metric("📊 Engagement", f"{top3.iloc[0]['Engagement Rate']}%")
            style_metric_cards()

            st.markdown("---")
            st.subheader("📋 Top 3 Recommended Influencers")
            st.dataframe(top3[[
                "Influencer Name", "Platform Used", "Follower Count", "Engagement Rate",
                "Category", "Country", "Score", "Estimated Cost"
            ]], use_container_width=True)

            st.success("✅ ML recommendation complete")
            st.markdown("---")
            st.subheader("🧠 AI-Powered Insight")

            for _, influencer in top3.iterrows():
                with st.expander(f"{influencer['Influencer Name']} - {influencer['Platform Used']}"):
                    insight = get_groq_insight(influencer)
                    st.info(insight)

            # Best Match Summary
            best = top3.iloc[0]
            st.subheader("🤖 Best Match Summary")

            category = best["Category"]
            country = best["Country"]
            budget_val = best["Estimated Cost"]
            prompt = f"Provide a recommendation for the top 5 influencers in the {category} category from {country}, within a budget of ${budget_val:.2f}"
            recommendation = get_recommendation_from_groq(prompt)

            st.write(f"**AI Recommendation**: {recommendation}")

# ---------------------------------- Tab 2: Chatbot ----------------------------------

with tab2:
    if "enter_pressed" not in st.session_state:
        st.session_state.enter_pressed = False
    if "clear_input" not in st.session_state:
        st.session_state.clear_input = False

    def enter_callback():
        st.session_state.enter_pressed = True

    st.subheader("💬 Chat About Recommendations")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Clear input before rendering text_input
    if st.session_state.clear_input:
        st.session_state.chat_input = ""
        st.session_state.clear_input = False

    # Custom CSS (unchanged)
    st.markdown("""
        <style>
            .chat-container {
                max-height: 500px;
                overflow-y: auto;
                padding: 10px;
                border: 1px solid #444;
                border-radius: 10px;
                background-color: #1e1e1e;
                color: white;
            }
            .user-msg, .assistant-msg {
                display: inline-block;
                max-width: 80%;
                padding: 10px 15px;
                border-radius: 15px;
                margin-bottom: 8px;
                word-wrap: break-word;
            }
            .user-msg {
                background-color: #0b93f6;
                color: white;
                text-align: left;
                align-self: flex-end;
            }
            .assistant-msg {
                background-color: #3a3a3a;
                color: white;
                text-align: left;
                align-self: flex-start;
            }
        </style>
    """, unsafe_allow_html=True)

    # Chat container
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            if isinstance(chat, dict) and "role" in chat and "content" in chat:
                css_class = "user-msg" if chat["role"] == "You" else "assistant-msg"
                st.markdown(f'<div class="{css_class}"><strong>{chat["role"]}:</strong><br>{chat["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Input + Buttons
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        user_input = st.text_input(
            "Ask something about your recommendations", 
            label_visibility="collapsed", 
            key="chat_input", 
            on_change=enter_callback
        )
    with col2:
        send_clicked = st.button("Send", use_container_width=True)
    with col3:
        clear_clicked = st.button("🧹", use_container_width=True, help="Clear chat")

    input_submitted = send_clicked or st.session_state.enter_pressed

    if clear_clicked:
        st.session_state.chat_history.clear()
        st.session_state.enter_pressed = False
        st.experimental_rerun()

    if input_submitted and user_input:
        allowed = ["influencer", "promotion", "paid", "platform", "engagement", "budget", "reach", "followers", "hi", "hello", "hey", "tell", "who"]

        if not any(word in user_input.lower() for word in allowed):
            reply = "❌ Sorry, I can only assist with influencer recommendations."
        else:
            influencer_details = ""
            for _, row in st.session_state.top3_df.iterrows():
                influencer_details += (
                    f"Name: {row['Influencer Name']}, Platform: {row['Platform Used']}, "
                    f"Followers: {row['Follower Count']}, Engagement: {row['Engagement Rate']}%, "
                    f"Estimated Cost: ${row['Estimated Cost']:.2f}\n"
                )

            try:
                client = groq.Groq(api_key=groq.api_key)
                response = client.chat.completions.create(
                    model="meta-llama/llama-4-maverick-17b-128e-instruct",
                    messages=[
                        {"role": "system", "content": "Answer influencer promotion queries."},
                        {"role": "user", "content": user_input}
                    ]
                )
                reply = response.choices[0].message.content.strip()
            except Exception as e:
                reply = f"❌ API Error: {e}"

        st.session_state.chat_history.append({"role": "You", "content": user_input})
        st.session_state.chat_history.append({"role": "Assistant", "content": reply})

        # Reset states
        st.session_state.enter_pressed = False
        st.session_state.clear_input = True  # Trigger clearing input

        st.experimental_rerun()
