import streamlit as st
import pandas as pd
import os
from pdf2image import convert_from_path

from compare_engine import clear_screenshots
from workflow import run_comparison
from excel_report import generate_excel_report
from excel_report_v2 import generate_excel_report_v2
from report_generator import generate_pdf_report
from statistics_generator import calculate_statistics

POPPLER_PATH = None 


def pdf_to_images(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    pages = convert_from_path(
        pdf_path,
        dpi=300,
        
    )

    for i, page in enumerate(pages):
        page.save(
            os.path.join(output_folder, f"page_{i+1}.png"),
            "PNG"
        )


st.set_page_config(
    page_title="AI Document Comparison Agent",
    page_icon="📄",
    layout="wide"
)

st.markdown("# 📄 AI Document Comparison Agent")
st.markdown(
    "Compare PDF documents using AI-powered text analysis, visual comparison, OCR extraction and automated reporting."
)

st.markdown("""
### 🚀 Features
✅ Visual PDF Comparison
✅ OCR-Based Text Detection
✅ AI Change Analysis
✅ Executive Summary Generation
✅ PDF Report Export
✅ Excel Report Export
✅ Dashboard Analytics
""")

col1, col2 = st.columns(2)

with col1:
    source_pdf = st.file_uploader("📄 Source PDF", type=["pdf"])

with col2:
    target_pdf = st.file_uploader("📄 Target PDF", type=["pdf"])

compare = st.button(
    "🚀 Compare Documents",
    use_container_width=True
)

if compare:

    if source_pdf is None or target_pdf is None:
        st.error("Please upload both PDFs")
        st.stop()

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("source_pages", exist_ok=True)
    os.makedirs("target_pages", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)

    clear_screenshots()

    source_path = "uploads/source.pdf"
    target_path = "uploads/target.pdf"

    with open(source_path, "wb") as f:
        f.write(source_pdf.getbuffer())

    with open(target_path, "wb") as f:
        f.write(target_pdf.getbuffer())

    pdf_to_images(source_path, "source_pages")
    pdf_to_images(target_path, "target_pages")

    st.success("PDF pages generated successfully!")

    results,avg_score,page_summaries,document_summary,change_stats = run_comparison()

    stats = calculate_statistics(page_summaries)

    st.header("📊 Comparison Dashboard")

    st.success(f"Similarity Score: {avg_score:.4f}")
    st.progress(float(avg_score))

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric("Critical", stats["critical"])
    m2.metric("High", stats["high"])
    m3.metric("Medium", stats["medium"])
    m4.metric("Low", stats["low"])
    m5.metric("Total", stats["total"])

    st.info(f"Pages Compared: {len(results)}")

    chart_data = pd.DataFrame({
        "Severity": ["Critical", "High", "Medium", "Low"],
        "Count": [
            stats["critical"],
            stats["high"],
            stats["medium"],
            stats["low"]
        ]
    })

    st.subheader("📈 Change Distribution")
    st.bar_chart(chart_data.set_index("Severity"))

    st.subheader("📝 Executive Summary")
    st.info(document_summary)

    pdf_file = generate_pdf_report(
        avg_score,
        document_summary,
        page_summaries,
        source_pdf.name,
        target_pdf.name,
        stats
    )

    excel_file = generate_excel_report(
        results,
        page_summaries
    )

    excel_v2_file = generate_excel_report_v2(
        page_summaries
    )
    st.subheader("📊 Change Categories")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📝 Text",
            change_stats["text"]
        )
    
    with col2:
        st.metric(
            "🖼️ Visual",
            change_stats["visual"]
        )
    
    with col3:
        st.metric(
            "📐 Layout",
            change_stats["layout"]
        )
    
    with col4:
        st.metric(
            "🎨 Formatting",
            change_stats["formatting"]
        )

    st.subheader("📥 Reports")

    c1, c2, c3 = st.columns(3)

    with c1:
        with open(pdf_file, "rb") as f:
            st.download_button(
                "📥 PDF Report",
                f,
                file_name=pdf_file,
                mime="application/pdf"
            )

    with c2:
        with open(excel_file, "rb") as f:
            st.download_button(
                "📊 Excel Report",
                f,
                file_name=excel_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with c3:
        with open(excel_v2_file, "rb") as f:
            st.download_button(
                "📊 Excel Report V2",
                f,
                file_name=excel_v2_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    tab1, tab2 = st.tabs(
        ["📄 Page Summaries", "🔍 Visual Comparisons"]
    )

    with tab1:

        for page_num in sorted(page_summaries.keys()):

            st.subheader(f"Page {page_num}")
            st.info(page_summaries[page_num])

    with tab2:

        for result in results:

            st.markdown("---")

            st.subheader(
                f"Page {result['page']} Comparison"
            )

            st.caption(
                f"Visual regions detected: {result['regions']}"
            )

            left, right = st.columns(2)

            with left:
                st.write("Source")
                st.image(
                    result["source"],
                    width="stretch"
                )

            with right:
                st.write("Target")
                st.image(
                    result["target"],
                    width="stretch"
                )

            st.success(result["summary"])

    st.markdown("---")

    st.caption(
        "AI Document Comparison Agent v1.0 | Powered by Streamlit, OpenCV, OCR and Gemini AI"
    )
