# Influencer-recommendation-Dashboard-with-Ai-

 Influencer Recommendation Dashboard
Welcome to the Influencer Recommendation Dashboard – a smart, interactive dashboard built using Python, Streamlit, Machine Learning, and Data Analytics. This project helps businesses, marketers, and brands discover the most suitable influencers based on their preferences such as platform, product category, budget, target country, and engagement metrics.

🚀 Features
🔍 Filter-Based Influencer Search: Choose platform (Instagram, YouTube, Twitter), country, category, and budget to view tailored influencer data.

🤖 ML-Based Recommendation Score: Predicts how well an influencer matches your campaign criteria.

📈 Interactive Visualizations: Dynamic charts, graphs, and KPIs using Plotly and Matplotlib.

🧠 Multi-Dashboard Tabs: Separate dashboards for Instagram, YouTube, and combined overview.

🧮 Key Metrics: Real-time stats like average engagement rate, total influencers, and follower counts.

📁 Cleaned Datasets: Supports preprocessed CSV data from Instagram, YouTube, and Twitter.

🧰 Streamlit App: Fully interactive and responsive web UI.

🗂️ Project Structure
bash
Copy
Edit
influencer_dashboard/
│
├── data/
│   ├── top_1000_instagrammers.csv
│   ├── YouTube_Influencer_Channels.csv
│   ├── Twitterdatainsheets.csv
│
├── app.py                  # Main Streamlit dashboard script
├── utils.py                # Utility functions for data cleaning & formatting
├── model/
│   └── influencer_model.pkl # Trained ML model for recommendation
│
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
💡 Technologies Used
Python 3.10+

Streamlit

Pandas, NumPy

Scikit-learn (ML Model)

Plotly, Seaborn, Matplotlib

Joblib (for model serialization)

⚙️ How It Works
User Input: Select filters like country, category, budget, and platform.

Data Filtering: Dashboard dynamically updates the list of influencers based on input.

Model Prediction: Trained ML model calculates a recommendation score for each influencer.

Display: The dashboard shows influencer cards, charts, and tables with detailed metrics.

🛠️ Installation
Clone the repository

bash
Copy
Edit
git clone [https://github.com/yourusername/influencer-dashboard.git](https://github.com/Rohankashyap5526/Influencer-recommendation-Dashboard-with-Ai-.git)
cd influencer-dashboard
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the Streamlit app

bash
Copy
Edit
streamlit run app.py
📌 Use Cases
For brands wanting to hire the right influencer.

For marketers doing competitor and niche analysis.

For analysts wanting to visualize social influencer trends.

📷 Screenshots
Add screenshots of your dashboard tabs here – Main, Instagram, YouTube dashboards.

📈 Sample KPIs
Total Influencers: 1000+

Avg Engagement Rate: 3.5%

Avg Followers: 500K+

📓 Future Enhancements
Add email integration to contact influencers directly.

Include real-time social media API to keep data fresh.

Add TikTok and other emerging platforms.

Integrate Power BI/Tableau export options.

🙋‍♂️ Author
Er. Rohan Kashyap
Computer Science Engineer
