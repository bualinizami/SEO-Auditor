import streamlit as st
import requests
import tempfile
import json
import io
from docx import Document

# Set up PageSpeed API key and endpoint
API_KEY = "YOUR_PAGESPEED_API_KEY"
API_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

def fetch_pagespeed_data(url):
    params = {"url": url, "key": API_KEY, "strategy": "mobile"}
    response = requests.get(API_ENDPOINT, params=params)
    return response.json()

def extract_summary(data):
    try:
        title = data["lighthouseResult"]["finalUrl"]
        seo_score = data["lighthouseResult"]["categories"]["seo"]["score"] * 100
        perf_score = data["lighthouseResult"]["categories"]["performance"]["score"] * 100
        return {
            "title": title,
            "seo_score": int(seo_score),
            "perf_score": int(perf_score),
        }
    except KeyError:
        return None

def generate_docx(summary_data):
    doc = Document()
    doc.add_heading("SEO Audit Report", 0)
    doc.add_paragraph(f"URL: {summary_data['title']}")
    doc.add_paragraph(f"SEO Score: {summary_data['seo_score']}%")
    doc.add_paragraph(f"Performance Score: {summary_data['perf_score']}%")

    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    return output

# Streamlit UI
st.title("🔍 Mini SEO Auditor")

site_url = st.text_input("Enter website URL to audit", "")

if site_url:
    if st.button("Run Audit"):
        with st.spinner("Auditing..."):
            full_json = fetch_pagespeed_data(site_url)
            summary_data = extract_summary(full_json)

            if summary_data:
                st.success("Audit completed!")
                st.subheader("Summary Report")
                st.write(summary_data)

                # Word download
                docx_file = generate_docx(summary_data)
                st.download_button("📄 Download Word Report", docx_file, file_name="seo_report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

                # Optional JSON download
                json_file = io.BytesIO(json.dumps(full_json).encode("utf-8"))
                st.download_button("📄 Download Full JSON Report", json_file, file_name="seo_report.json", mime="application/json")
            else:
                st.error("Could not extract summary data from the PageSpeed response.")
