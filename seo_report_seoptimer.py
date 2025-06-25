import streamlit as st
import requests
import tempfile
import json

st.set_page_config(page_title="Mini SEO Auditor", layout="centered")
st.title("🚀 Mini SEO Auditor - Google PageSpeed API")

# Input field for the URL
site_url = st.text_input("Enter the website URL to audit:", placeholder="https://example.com")

# Input field for the API key
api_key = st.text_input("Enter your Google PageSpeed API Key:", type="password")

# Function to fetch data from Google PageSpeed API
def fetch_lighthouse_data(site_url, api_key):
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={site_url}&category=performance&category=seo&strategy=mobile&key={api_key}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        seo_score = data['lighthouseResult']['categories']['seo']['score'] * 100
        perf_score = data['lighthouseResult']['categories']['performance']['score'] * 100
        title = data['lighthouseResult']['finalUrl']

        return {
            'title': title,
            'seo_score': seo_score,
            'perf_score': perf_score
        }, data
    except Exception as e:
        st.error(f"Failed to fetch audit data: {e}")
        return None, None

# Main logic
if site_url and api_key:
    if st.button("Run Audit"):
        with st.spinner("Fetching audit data..."):
            summary_data, full_json = fetch_lighthouse_data(site_url, api_key)
            if summary_data:
                st.success("Audit completed!")
                st.write("### Summary:")
                st.write(f"**URL**: {summary_data['title']}")
                st.write(f"**SEO Score**: {summary_data['seo_score']}%")
                st.write(f"**Performance Score**: {summary_data['perf_score']}%")

                # Optional: Offer JSON download
                with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as jf:
                    json.dump(full_json, jf)
                    jf.seek(0)
                    st.download_button("📄 Download Full JSON Report", jf, file_name="raw_lighthouse_report.json", mime="application/json")
