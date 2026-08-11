


import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
api_key = st.secrets.get("GENAI_API_KEY") 
client = genai.Client(api_key=api_key)
load_dotenv()

st.title("Oil Price Tracker & AI Insights")

try:
    df = pd.read_csv("oil_prices.csv")

    if "date" in df.columns and "price" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")


    if not df.empty and "price" in df.columns:
        latest_price = df["price"].iloc[-1]
        currency = df["currency"].iloc[-1] if "currency" in df.columns else ""
        st.metric(label="Latest Oil Price", value=f"{latest_price} {currency}")


    st.subheader("Price History")
    st.line_chart(df, x="date", y="price")


    st.subheader("AI Market Analysis")
    
    if st.button("Generate AI Market Summary"):
        
        recent_data = df.tail(10).to_string(index=False)
        prompt = f"Analyze these recent oil prices and provide a concise 2-sentence market summary:\n\n{recent_data}"

        client = genai.Client(api_key=os.getenv('genai'))
        
        with st.spinner("Analyzing market data..."):
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            st.info(response.text)

    st.subheader("Raw Data")
    st.dataframe(df)

except FileNotFoundError:
    st.error("oil_prices.csv not found. Please run your data fetching script first.")
