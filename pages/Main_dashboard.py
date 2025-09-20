import streamlit as st
import pandas as pd
import altair as alt

# --- Page Config ---
st.set_page_config(page_title="📱 Influencer Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_influencer_data.csv")
    return df

df = load_data()

# --- Data Preprocessing ---
df["Female %"] = pd.to_numeric(df["Female %"], errors="coerce")
df["Country"] = df["Country"].astype(str)
df = df[df["Country"].str.strip().str.lower() != 'nan']
df["Platform List"] = df["Platform Used"].fillna("").str.split(", ").apply(lambda x: [p.strip() for p in x])

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filter Influencers")

# Platform Filter
all_platforms = sorted(set(p for sublist in df["Platform List"] for p in sublist if p))
selected_platforms = st.sidebar.multiselect("🌐 Platform", all_platforms)

# Category Filter
categories = df["Category"].dropna().unique().tolist()
selected_category = st.sidebar.multiselect("📁 Category", categories)

# Filter DataFrame
filtered_df = df.copy()
if selected_platforms:
    filtered_df = filtered_df[filtered_df["Platform List"].apply(lambda lst: any(p in lst for p in selected_platforms))]
if selected_category:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_category)]

# --- Main Title ---
st.markdown("## 📊 Influencer Analytics Dashboard")

# --- KPI Cards ---
st.markdown("### 📌 Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("👤 Total Influencers", len(filtered_df))
kpi2.metric("👥 Total Followers", f"{filtered_df['Follower Count'].sum():,}")
kpi3.metric("📈 Avg. Engagement Rate", f"{filtered_df['Engagement Rate'].mean():.2%}")

st.markdown("---")

# --- Tabs for Sections ---
tab1, tab2, tab3 = st.tabs(["🔥 Top Influencers", "📊 Visual Insights", "📄 Data Table"])

# --- Tab 1: Top Influencers ---
with tab1:
    st.subheader("🔥 Top Influencers by Follower Count")
    top_influencers = filtered_df.sort_values(by="Follower Count", ascending=False).head(10)
    bar_chart = alt.Chart(top_influencers, title="Top 10 Influencers").mark_bar().encode(
        x=alt.X("Follower Count:Q", title="Followers"),
        y=alt.Y("Influencer Name:N", sort='-x'),
        color=alt.Color("Category:N", legend=None),
        tooltip=["Influencer Name", "Follower Count", "Engagement Rate"]
    ).properties(height=400)
    st.altair_chart(bar_chart, use_container_width=True)

# --- Tab 2: Visual Insights ---
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Avg. Engagement Rate by Category")
        category_eng = filtered_df.groupby("Category")["Engagement Rate"].mean().reset_index()
        eng_chart = alt.Chart(category_eng).mark_bar().encode(
            x=alt.X("Engagement Rate:Q", title="Avg. Engagement Rate"),
            y=alt.Y("Category:N", sort='-x'),
            color=alt.Color("Category:N", legend=None),
            tooltip=["Category", "Engagement Rate"]
        ).properties(height=400)
        st.altair_chart(eng_chart, use_container_width=True)

    with col2:
        st.subheader("🔍 Platform Usage Distribution")
        platform_counts = filtered_df["Platform Used"].str.split(", ").explode().value_counts().reset_index()
        platform_counts.columns = ["Platform", "Count"]
        platform_chart = alt.Chart(platform_counts).mark_arc(innerRadius=50).encode(
            theta="Count:Q",
            color="Platform:N",
            tooltip=["Platform", "Count"]
        )
        st.altair_chart(platform_chart, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("👥 Audience Gender Distribution")
        female_avg = filtered_df["Female %"].mean(skipna=True)
        gender_data = pd.DataFrame({
            "Gender": ["Female", "Male"],
            "Average %": [female_avg, 100 - female_avg]
        })
        gender_chart = alt.Chart(gender_data).mark_bar().encode(
            x=alt.X("Gender:N"),
            y=alt.Y("Average %:Q"),
            color="Gender:N",
            tooltip=["Gender", "Average %"]
        ).properties(height=300)
        st.altair_chart(gender_chart, use_container_width=True)

    with col4:
        st.subheader("🌍 Influencers by Country")
        country_counts = filtered_df["Country"].value_counts().reset_index()
        country_counts.columns = ["Country", "Count"]
        country_chart = alt.Chart(country_counts).mark_bar().encode(
            x=alt.X("Count:Q"),
            y=alt.Y("Country:N", sort='-x'),
            tooltip=["Country", "Count"]
        ).properties(height=300)
        st.altair_chart(country_chart, use_container_width=True)

# --- Tab 3: Data Table ---
with tab3:
    st.subheader("📄 Filtered Influencer Data")
    st.dataframe(filtered_df, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("📊 Designed with ❤️ by Rohan using Streamlit & Altair")
