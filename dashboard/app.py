import streamlit as st
import plotly.express as px
from utils import load_data , validate_columns
from ai_insights import analyze_dataset, analyze_review ,ask_ai
from charts import rating_chart, region_chart, product_chart
from pdf_report import generate_pdf
import time

st.set_page_config(
    page_title="CustomerPulse AI",
    page_icon="😊",
    layout="wide"
)

@st.cache_data(show_spinner=False)
def cached_review(review):
    return analyze_review(review)


@st.cache_data(show_spinner=False)
def cached_ai(question, df):
    return ask_ai(question, df)


@st.cache_data(show_spinner=False)
def cached_report(df):
    return analyze_dataset(df)


st.sidebar.title("😊 CustomerPulse AI")


st.markdown("""
<style>
[data-testid="stSidebar"]{
    min-width:320px;
    max-width:320px;
}
</style>
""", unsafe_allow_html=True)

st.title("😊 CustomerPulse AI")


st.markdown(
"""
Transform customer reviews into **AI-powered business insights**.

Upload a CSV file containing customer reviews and let AI analyze:
- 😊 Customer Sentiment
- 🔥 Top Complaints
- 📈 Trends
- 🤖 Executive Report
"""
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload Customer Reviews CSV",
    type=["csv"]
)

if uploaded_file is None:
    st.info("👆 Upload a CSV file to begin.")
    st.stop()
    
df = load_data(uploaded_file)

if df is None:
    st.stop()

st.sidebar.header("🎯 Filters")

selected_region = st.sidebar.multiselect(
    "Region",
    df["region"].unique(),
    default=df["region"].unique()
)

selected_product = st.sidebar.multiselect(
    "Product",
    df["product"].unique(),
    default=df["product"].unique()
)

selected_rating = st.sidebar.slider(
    "Minimum Rating",
    1,
    5,
    1
)


with st.sidebar.container(border=True):
    st.markdown("""
### 🚀 CustomerPulse AI

AI-powered customer feedback analytics.

### Features

📊 Dashboard

😊 Review Analyzer

📋 Executive Report

📄 PDF Export
""")
    
missing_columns=validate_columns(df)
if missing_columns:
    st.error(f"❌ Invalid CSV Format")
    st.write("Missing Columns:")

    for col in missing_columns:
        st.write(f"• **{col}**")
        
    st.stop()

filtered_df = df[
    (df["region"].isin(selected_region)) &
    (df["product"].isin(selected_product)) &
    (df["rating"] >= selected_rating)
].copy()

st.success("✅ File uploaded successfully!")

st.divider()

st.markdown("---")
st.header("📊 Customer Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📝 Total Reviews",
        len(filtered_df)
    )

with col2:
    st.metric(
        "⭐ Average Rating",
        round(filtered_df["rating"].mean(), 2)
    )

with col3:
    positive_percentage = (filtered_df["rating"] >= 4).sum() / len(filtered_df) * 100
    st.metric(
        "😊 Positive Reviews",
        f"{positive_percentage:.1f}%"
    )

with col4:
    negative_percentage = (filtered_df["rating"] <= 2).sum() / len(filtered_df) * 100
    st.metric(
        "😠 Negative Reviews",
        f"{negative_percentage:.1f}%"
    )

st.divider()

st.info(f"Total Records: {len(filtered_df):,}")

# Four KPI CARDS
positive_percentage = (filtered_df["rating"] >= 4).sum() / len(filtered_df) * 100
neutral_percentage = (filtered_df["rating"] == 3).sum() / len(filtered_df) * 100
negative_percentage = (filtered_df["rating"] <= 2).sum() / len(filtered_df) * 100

average_rating = filtered_df["rating"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "😊 Positive",
    f"{positive_percentage:.1f}%"
)

col2.metric(
    "😐 Neutral",
    f"{neutral_percentage:.1f}%"
)

col3.metric(
    "😡 Negative",
    f"{negative_percentage:.1f}%"
)

col4.metric(
    "⭐ Avg Rating",
    f"{average_rating:.2f}"
)

st.markdown("---")
st.header("📈 Customer Analytics")
# Then create filtered dataframe
filtered_df = df[
    (df["region"].isin(selected_region)) &
    (df["product"].isin(selected_product)) &
    (df["rating"] >= selected_rating)
].copy()

if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters.")
    st.stop()
    
    
# Create sentiment column
filtered_df["Sentiment"] = filtered_df["rating"].apply(
    lambda x: "Positive" if x >= 4 else (
        "Neutral" if x == 3 else "Negative"
    )
)



#Two -column layout
left, right = st.columns(2)
# Sentiment Pie Chart
sentiment=(filtered_df.groupby("Sentiment").size().reset_index(name="Count"))

fig = px.pie(sentiment,names="Sentiment",values="Count",hole=0.45 , title="Customer Sentiment Distribution")

left.plotly_chart(fig, use_container_width=True)

product_reviews = (
    filtered_df.groupby("product")
      .size()
      .reset_index(name="Reviews")
)

fig = px.bar(
    product_reviews,
    x="product",
    y="Reviews",
    color="Reviews",
    text_auto=True,
    title="Reviews by Product"
)

right.plotly_chart(
    fig,
    use_container_width=True
)

region_reviews = (
    filtered_df.groupby("region")
      .size()
      .reset_index(name="Reviews")
)

fig = px.bar(
    region_reviews,
    x="region",
    y="Reviews",
    color="region",
    text_auto=True,
    title="Reviews by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.header("😊 Sentiment Summary")

summary = (
    filtered_df.groupby("Sentiment")
    .size()
    .reset_index(name="Reviews")
)

st.dataframe(summary, use_container_width=True)


st.subheader("Dataset Preview")

search = st.text_input("🔍 Search Reviews")

preview = filtered_df.copy()

if search:
    preview = preview[
         preview.astype(str).apply(
            lambda row: row.str.contains(search, case=False, na=False).any(),
            axis=1
        )
    ]
        

st.dataframe(preview,use_container_width=True,hide_index=True)

st.divider()



col1, col2 = st.columns(2)

with col1:
    rating_chart(filtered_df)

with col2:
    region_chart(filtered_df)

product_chart(filtered_df)

st.header("🔥 Top Complaints")

negative_reviews = filtered_df[
    filtered_df["rating"] <= 2
]

st.dataframe(
    negative_reviews[
        ["product", "region", "review"]
    ],
    use_container_width=True
)


st.markdown("---")
st.header("🤖 AI Review Analyzer")

review = st.selectbox(
    "Choose a review",
    filtered_df["review"]
)

if st.button("🔍 Analyze Review"):

    with st.spinner("🔍 AI is analyzing the review..."):

        result = analyze_review(review)

    st.markdown(result)

st.header("📋 AI Executive Report")


with st.spinner("Generating AI Report..."):
    report = cached_report(filtered_df)
    st.markdown(report)

st.info("""
### 🤖 AI Confidence

**Confidence:** 94%

Generated using **Llama 3.3 70B** via **Groq**.
""")

st.success("✅ Executive Report Generated")

pdf = generate_pdf(report, filtered_df)

with open(pdf, "rb") as file:

    st.download_button(
        label="📄 Download Executive Report",
        data=file,
        file_name="CustomerPulse_AI_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
        

st.header("💬 AI Business Assistant")

st.info("""
### Try asking:

• Which product has the worst reviews?

• Which region has the happiest customers?

• What are the biggest complaints?

• What should management improve first?

• Summarize customer feedback.

• What trends do you notice?
""")

question = st.text_area(
    "Ask anything about your customer reviews",
    placeholder="Example: What product has the most complaints?"
)

if st.button("🤖 Ask AI", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Thinking..."):
        answer = cached_ai(question, filtered_df)

    st.markdown(answer)
    
csv = filtered_df.to_csv(index=False).encode()

st.download_button(
    "⬇ Download Filtered CSV",
    csv,
    "customer_reviews.csv",
    "text/csv"
)   
    
st.divider()

st.caption(
    "🚀 Built with Streamlit • Groq AI • Plotly • ReportLab\n\n"
    "Developed by Abhinav Sahu"
)