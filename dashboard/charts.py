import streamlit as st
import plotly.express as px


def rating_chart(df):

    fig = px.histogram(
        df,
        x="rating",
        color="rating",
        title="Rating Distribution"
    )

    st.plotly_chart(fig, use_container_width=True,key="rating_chart")
def region_chart(df):

    fig = px.pie(
        df,
        names="region",
        title="Region Distribution"
    )

    st.plotly_chart(fig, use_container_width=True,key="region_chart")


def product_chart(df):

    temp = (
        df.groupby("product")
        .size()
        .reset_index(name="Reviews")
    )

    fig = px.bar(
        temp,
        x="product",
        y="Reviews",
        title="Reviews by Product"
    )

    st.plotly_chart(fig, use_container_width=True,key="product_chart")