# # Converted YouTube Influencer Dashboard using Altair
# import streamlit as st
# import pandas as pd
# import altair as alt

# st.set_page_config(page_title="YouTube Influencer Dashboard", layout="wide")
# st.markdown("""
#     <style>
#         .title {
#             font-size: 36px;
#             font-weight: bold;
#             color: #FF0000;
#         }
#         h1{
#              color: #FF0000;
#             }
#         .subheader {
#             font-size: 24px;
#             font-weight: bold;
#             color: #333;
#         }
#         .metric {
#             font-size: 22px;
#             font-weight: bold;
#             color: #4CAF50;
#         }
#         .card {
#             background-color: #FFFFFF;
#             padding: 20px;
#             margin-bottom: 30px;
#             border-radius: 15px;
#             box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
#             transition: transform 0.3s ease, box-shadow 0.3s ease;
#             height: 100%;
#             display: flex;
#             flex-direction: column;
#             justify-content: flex-start;
#             align-items: center;  /* Center the content */
#         }
#         .card:hover {
#             transform: scale(1.05);
#             box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
#         }
#         .card img {
#             width: 150px;  /* Adjusted width */
#             height: 150px;  /* Adjusted height */
#             border-radius: 15px;
#             object-fit: cover;
#             margin-bottom: 20px;
#         }
#         .card a {
#             text-decoration: none;
#             color: #333;
#             font-weight: bold;
#         }
#         .card h4 {
#             margin-top: 10px;
#             font-size: 20px;
#             color: #4CAF50;
#             text-align: center;
#         }
#         .card p {
#             font-size: 14px;
#             color: #777;
#             margin: 5px 0;
#         }
#         .card .social-icons {
#             display: flex;
#             justify-content: center;
#             gap: 15px;
#             margin-top: 15px;
#         }
#         .card .social-icons a {
#             font-size: 20px;
#             color: #4CAF50;
#             text-decoration: none;
#         }
#         .card .social-icons a:hover {
#             color: #333;
#         }
#         .container {
#             display: flex;
#             gap: 20px;
#             flex-wrap: wrap;
#             justify-content: center; /* Center the cards */
#         }
#     </style>
# """, unsafe_allow_html=True)
# # Load and preprocess data
# @st.cache_data
# def load_data():
#     df = pd.read_csv("cleaned_influencer_data.csv")
#     df = df[df['Platform Used'].str.contains('YouTube', case=False, na=False)]

#     def parse_follower_count(val):
#         val = str(val).replace('~', '').replace('+', '').strip()
#         try:
#             if 'M' in val:
#                 return float(val.replace('M', '')) * 1e6
#             elif 'K' in val:
#                 return float(val.replace('K', '')) * 1e3
#             elif 'B' in val:
#                 return float(val.replace('B', '')) * 1e9
#             else:
#                 return float(val)
#         except:
#             return None

#     def parse_engagement_rate(val):
#         val = str(val).replace('%', '').replace('~', '').strip()
#         try:
#             return float(val)
#         except:
#             return None

#     df["Follower Count"] = df["Follower Count"].apply(parse_follower_count)
#     df["Engagement Rate"] = df["Engagement Rate"].apply(parse_engagement_rate)
#     df = df.dropna(subset=["Follower Count", "Engagement Rate"])
#     df["Platform List"] = df["Platform Used"].str.split(',').apply(lambda x: [i.strip() for i in x] if isinstance(x, list) else [])
#     df = df.explode("Platform List")
#     return df

# df = load_data()

# # Sidebar filters
# st.sidebar.header("🔍 Filter Influencers")
# selected_country = st.sidebar.multiselect("Country", options=sorted(df["Country"].dropna().unique()))
# selected_category = st.sidebar.selectbox("Category", options=["All"] + sorted(df["Category"].dropna().unique()))

# filtered_df = df.copy()
# if selected_country:
#     filtered_df = filtered_df[filtered_df["Country"].isin(selected_country)]
# if selected_category != "All":
#     filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# if filtered_df.empty:
#     st.warning("⚠️ No data available after applying filters.")
#     st.stop()
# j = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtSsD_I85MznoyUIZXUHaRBzfiRPL4DNZhjw&s"
# st.markdown(
#     f"""
#     <h1 style='color: #FF0000; display:flex; align-items:center; gap:15px;'>
#         <img src="{j}" alt="YouTube" style="width:50px; height:50px; border-radius:10px;"/>
#         YouTube Influencer Dashboard
#     </h1>
#     """,
#     unsafe_allow_html=True
# )

# col1, col2, col3 = st.columns(3)
# col1.metric("Total Influencers", len(filtered_df))
# col2.metric("Avg Engagement Rate", f"{filtered_df['Engagement Rate'].mean():.2f}%")
# col3.metric("Avg Follower Count", f"{filtered_df['Follower Count'].mean():,.0f}")

# # Category Distribution - Bar
# st.subheader("🎯 Category Distribution")
# cat_counts = filtered_df["Category"].value_counts().nlargest(10).reset_index()
# cat_counts.columns = ["Category", "Count"]
# bar_chart = alt.Chart(cat_counts).mark_bar().encode(
#     x=alt.X("Category", sort="-y"),
#     y="Count",
#     color="Category"
# ).properties(title="Top Categories by Influencer Count")
# st.altair_chart(bar_chart, use_container_width=True)

# # Category Distribution - Pie as arc chart
# pie_chart = alt.Chart(cat_counts).mark_arc(innerRadius=50).encode(
#     theta=alt.Theta(field="Count", type="quantitative"),
#     color=alt.Color(field="Category", type="nominal"),
#     tooltip=["Category", "Count"]
# ).properties(title="Category Distribution")
# st.altair_chart(pie_chart, use_container_width=True)

# # Subcategory Distribution
# if selected_category != "All":
#     st.subheader(f"📂 Subcategories under \"{selected_category}\"")
#     subcat_counts = filtered_df["Subcategory"].value_counts().nlargest(10).reset_index()
#     subcat_counts.columns = ["Subcategory", "Count"]

#     sub_bar = alt.Chart(subcat_counts).mark_bar().encode(
#         x=alt.X("Subcategory", sort="-y"),
#         y="Count",
#         color="Subcategory"
#     ).properties(title="Top Subcategories")
#     st.altair_chart(sub_bar, use_container_width=True)

#     sub_pie = alt.Chart(subcat_counts).mark_arc(innerRadius=50).encode(
#         theta=alt.Theta(field="Count", type="quantitative"),
#         color=alt.Color(field="Subcategory", type="nominal"),
#         tooltip=["Subcategory", "Count"]
#     ).properties(title="Subcategory Distribution")
#     st.altair_chart(sub_pie, use_container_width=True)

# # Platform Distribution
# st.subheader("🧩 Platform Usage Distribution")
# platform_counts = filtered_df["Platform List"].value_counts().reset_index()
# platform_counts.columns = ["Platform", "Count"]
# platform_pie = alt.Chart(platform_counts).mark_arc(innerRadius=50).encode(
#     theta=alt.Theta(field="Count", type="quantitative"),
#     color=alt.Color(field="Platform", type="nominal"),
#     tooltip=["Platform", "Count"]
# ).properties(title="Platform Distribution")
# st.altair_chart(platform_pie, use_container_width=True)

# # Engagement vs Follower Count
# st.subheader("📌 Engagement Rate vs Follower Count")
# scatter = alt.Chart(filtered_df).mark_circle(size=60).encode(
#     x=alt.X("Follower Count", scale=alt.Scale(type="log")),
#     y="Engagement Rate",
#     color="Category",
#     tooltip=["Influencer Name", "Country", "Subcategory"]
# ).interactive().properties(title="Engagement vs Follower Count")
# st.altair_chart(scatter, use_container_width=True)
# st.markdown('<p class="subheader">🔥 Top YouTubers</p>', unsafe_allow_html=True)

# # Load a second dataset for top YouTubers
# @st.cache_data
# def load_top_youtubers_data():
#     df = pd.read_excel("youtube2.xlsx")  # Replace with your actual Excel file name

#     # Parse followers/views/likes/likes/comments from formats like '289M', '100K'
#     def parse_count(val):
#         try:
#             val = str(val).strip().replace("+", "")
#             if 'B' in val:
#                 return float(val.replace('B', '')) * 1e9
#             elif 'M' in val:
#                 return float(val.replace('M', '')) * 1e6
#             elif 'K' in val:
#                 return float(val.replace('K', '')) * 1e3
#             else:
#                 return float(val)
#         except:
#             return None

#     df["Followers"] = df["Followers"].apply(parse_count)
#     df["Views (Avg.)"] = df["Views (Avg.)"].apply(parse_count)
#     df["Likes (Avg.)"] = df["Likes (Avg.)"].apply(parse_count)
#     df["Comments (Avg.)"] = df["Comments (Avg.)"].apply(parse_count)

#     return df

# top_df = load_top_youtubers_data()

# # Display top YouTubers based on follower count
# top_df = top_df.sort_values(by="Followers", ascending=False).head(5)

# # Display influencer cards
# st.markdown('<p class="subheader">✨ Influencers Showcase</p>', unsafe_allow_html=True)
# with st.container():
#     influencer_cols = st.columns(len(top_df))
#     for idx, row in top_df.iterrows():
#         with influencer_cols[list(top_df.index).index(idx)]:
#             st.markdown(f"""
#             <div class="card">
#                 <img src="{row['youtuber image link']}" alt="{row['youtuber name']}" />
#                 <a href="{row['channel image link']}" target="_blank">
#                     <h4>{row['youtuber name']}</h4>
#                 </a>
#                 <p><strong>Category</strong>: {row['Category']} ({row['subcategory']})</p>
#                 <p><strong>Country</strong>: {row['Country']} 🌍</p>
#                 <p><strong>Followers</strong>: {int(row['Followers']):,}</p>
#                 <p><strong>Avg. Views</strong>: {int(row['Views (Avg.)']):,}</p>
#                 <p><strong>Avg. Likes</strong>: {int(row['Likes (Avg.)']):,}</p>
#                 <p><strong>Avg. Comments</strong>: {int(row['Comments (Avg.)']):,}</p>
#             </div>
#             """, unsafe_allow_html=True)