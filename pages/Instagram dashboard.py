import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Instagram Influencer Dashboard", layout="wide")
st.markdown("""
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
        }
        .subheader {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        .metric {
            font-size: 22px;
            font-weight: bold;
            color: #4CAF50;
        }
        .card {
            background-color: #FFFFFF;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;  /* Center the content */
        }
        .card:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .card img {
            width: 150px;  /* Adjusted width */
            height: 180px;  /* Adjusted height */
            border-radius: 15px;
            object-fit: cover;
            margin-bottom: 20px;
        }
        .card a {
            text-decoration: none;
            color: #333;
            font-weight: bold;
        }
        .card h4 {
            margin-top: 10px;
            font-size: 20px;
            color: #4CAF50;
            text-align: center;
        }
        .card p {
            font-size: 14px;
            color: #777;
            margin: 5px 0;
        }
        .card .social-icons {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 15px;
        }
        .card .social-icons a {
            font-size: 20px;
            color: #4CAF50;
            text-decoration: none;
        }
        .card .social-icons a:hover {
            color: #333;
        }
        .container {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center; /* Center the cards */
        }
    </style>
""", unsafe_allow_html=True)
# ------------------ Load & Preprocess Data ------------------ #
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_influencer_data.csv")
    df = df[df['Platform Used'].str.contains('Instagram', case=False, na=False)]

    def parse_follower_count(val):
        val = str(val).replace('~', '').replace('+', '').strip()
        try:
            if 'M' in val:
                return float(val.replace('M', '')) * 1e6
            elif 'K' in val:
                return float(val.replace('K', '')) * 1e3
            elif 'B' in val:
                return float(val.replace('B', '')) * 1e9
            else:
                return float(val)
        except:
            return None

    def parse_engagement_rate(val):
        val = str(val).replace('%', '').replace('~', '').strip()
        try:
            return float(val)
        except:
            return None

    df["Follower Count"] = df["Follower Count"].apply(parse_follower_count)
    df["Engagement Rate"] = df["Engagement Rate"].apply(parse_engagement_rate)
    df = df.dropna(subset=["Follower Count", "Engagement Rate"])
    df["Platform List"] = df["Platform Used"].str.split(',').apply(lambda x: [i.strip() for i in x] if isinstance(x, list) else [])
    df = df.explode("Platform List")
    return df

df = load_data()

# ------------------ Sidebar Filters ------------------ #
st.sidebar.header("🔍 Filter Influencers")

selected_country = st.sidebar.multiselect("Country", options=sorted(df["Country"].dropna().unique()))
selected_category = st.sidebar.selectbox("Category", options=["All"] + sorted(df["Category"].dropna().unique()))

filtered_df = df.copy()
if selected_country:
    filtered_df = filtered_df[filtered_df["Country"].isin(selected_country)]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if filtered_df.empty:
    st.warning("⚠️ No data available after applying filters.")
    st.stop()

# ------------------ Title and Key Metrics ------------------ #
insta_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/240px-Instagram_logo_2016.svg.png"
st.markdown(
    f"""
    <h1 style=''>
        <img src="{insta_img}" alt="Instagram" style="width:50px; height:50px; border-radius:10px;" />
        Instagram Influencer Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)
col1.metric("Total Influencers", len(filtered_df))
col2.metric("Avg Engagement Rate", f"{filtered_df['Engagement Rate'].mean():.2f}%")
col3.metric("Avg Follower Count", f"{filtered_df['Follower Count'].mean():,.0f}")

# ------------------ Category Distribution ------------------ #
st.subheader("🎯 Category Distribution")

cat_counts = filtered_df["Category"].value_counts().nlargest(10).reset_index()
cat_counts.columns = ['Category', 'Count']

col1, col2 = st.columns(2)

with col1:
    bar_chart = alt.Chart(cat_counts).mark_bar(color="#6c63ff").encode(
        x=alt.X('Category:N', sort='-y'),
        y='Count:Q',
        tooltip=['Category', 'Count']
    ).properties(title="Top Categories by Influencer Count", width=350, height=300)
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    pie_chart = alt.Chart(cat_counts).mark_arc(innerRadius=50).encode(
        theta="Count:Q",
        color=alt.Color("Category:N", legend=None),
        tooltip=["Category:N", "Count:Q"]
    ).properties(title="Category Distribution")
    st.altair_chart(pie_chart, use_container_width=True)

# ------------------ Subcategory Distribution ------------------ #
if selected_category != "All":
    st.subheader(f"📂 Subcategories under '{selected_category}'")
    subcat_counts = filtered_df["Subcategory"].value_counts().nlargest(10).reset_index()
    subcat_counts.columns = ['Subcategory', 'Count']

    col3, col4 = st.columns(2)

    with col3:
        sub_bar = alt.Chart(subcat_counts).mark_bar(color="#f39c12").encode(
            x=alt.X('Subcategory:N', sort='-y'),
            y='Count:Q',
            tooltip=['Subcategory', 'Count']
        ).properties(title="Top Subcategories", width=350, height=300)
        st.altair_chart(sub_bar, use_container_width=True)

    with col4:
        sub_pie = alt.Chart(subcat_counts).mark_arc(innerRadius=50).encode(
            theta="Count:Q",
            color=alt.Color("Subcategory:N", legend=None),
            tooltip=["Subcategory:N", "Count:Q"]
        ).properties(title="Subcategory Distribution")
        st.altair_chart(sub_pie, use_container_width=True)

# ------------------ Platform Usage Pie ------------------ #
st.subheader("🧩 Platform Usage Distribution")
platform_counts = filtered_df["Platform List"].value_counts().reset_index()
platform_counts.columns = ['Platform', 'Count']

platform_pie = alt.Chart(platform_counts).mark_arc(innerRadius=50).encode(
    theta="Count:Q",
    color=alt.Color("Platform:N", legend=None),
    tooltip=["Platform:N", "Count:Q"]
).properties(title="Platform Distribution")
st.altair_chart(platform_pie, use_container_width=True)

# ------------------ Engagement vs Follower Scatter ------------------ #
st.subheader("📌 Engagement Rate vs Follower Count")
scatter = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x=alt.X("Follower Count:Q", scale=alt.Scale(type="log")),
    y="Engagement Rate:Q",
    color=alt.Color("Category:N"),
    tooltip=["Influencer Name", "Country", "Subcategory", "Follower Count", "Engagement Rate"]
).interactive().properties(title="Engagement vs Follower Count", height=400)
st.altair_chart(scatter, use_container_width=True)
# Load a second dataset for top YouTubers
@st.cache_data
def load_top_youtubers_data():
    df = pd.read_excel("Top_Instagram_Influencers_India.xlsx")  # Replace with your actual Excel file name

    # Parse followers/views/likes/likes/comments from formats like '289M', '100K'
    def parse_count(val):
        try:
            val = str(val).strip().replace("+", "")
            if 'B' in val:
                return float(val.replace('B', '')) * 1e9
            elif 'M' in val:
                return float(val.replace('M', '')) * 1e6
            elif 'K' in val:
                return float(val.replace('K', '')) * 1e3
            else:
                return float(val)
        except:
            return None

    df["Followers"] = df["Followers"].apply(parse_count)
    # df["Views (Avg.)"] = df["Views (Avg.)"].apply(parse_count)
    # df["Likes (Avg.)"] = df["Likes (Avg.)"].apply(parse_count)
    # df["Comments (Avg.)"] = df["Comments (Avg.)"].apply(parse_count)

    return df

top_df = load_top_youtubers_data()

# Display top YouTubers based on follower count
top_df = top_df.sort_values(by="Followers", ascending=False).head(5)

# Display influencer cards
st.markdown('<p class="subheader">✨ Influencers Showcase</p>', unsafe_allow_html=True)
with st.container():
    influencer_cols = st.columns(len(top_df))
    for idx, row in top_df.iterrows():
        with influencer_cols[list(top_df.index).index(idx)]:
            st.markdown(f"""
            <div class="card">
                <img src="{row['Influencer Image Link']}" alt="{row['Influencer Name']}" />
                <a href="{row['Instagram Link']}" target="_blank">
                    <h4>{row['Influencer Name']}</h4>
                </a>
                <p><strong>Category</strong>: {row['Category']} ({row['Subcategory']})</p>
                <p><strong>Country</strong>: {row['Country']} 🌍</p>
                <p><strong>Followers</strong>: {int(row['Followers']):,}</p>
            </div>
            """, unsafe_allow_html=True)