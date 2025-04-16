
import streamlit as st
from scraper import scrape_site
from alert import scan_for_alerts
from db import init_db, save_alerts, fetch_alerts

st.set_page_config(page_title="Dark Web Threat Monitor", layout="wide")
st.title("🕵️ Dark Web Threat Monitor")
st.markdown("Monitor dark web pages for leaks, keywords, and threat intel.")

init_db()

user_url = st.text_input("Enter Onion URL (e.g., http://example.onion)", key="url_input")

if st.button("Start Analysis"):
    if not user_url.endswith(".onion"):
        st.error("Invalid .onion link.")
    else:
        with st.spinner("Scraping and analyzing..."):
            html = scrape_site(user_url)
            if html:
                alerts = scan_for_alerts(html)
                if alerts:
                    save_alerts(user_url, alerts)
                    st.success(f"✅ {len(alerts)} alert(s) found and saved to database.")
                else:
                    st.info("No keyword alerts found.")
            else:
                st.error("Failed to scrape the site.")

st.divider()
st.subheader("📋 Recent Alerts (from Database)")

results = fetch_alerts()
if results:
    for id, url, keyword, context, timestamp in results:
        st.markdown(f"""
        **[{timestamp}]**  
        🔗 `{url}`  
        🔍 **Keyword**: `{keyword}`  
        📄 *{context}*
        """)
else:
    st.info("No alerts found yet.")
