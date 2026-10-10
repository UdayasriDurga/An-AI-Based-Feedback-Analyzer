import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import time,base64

st.set_page_config(page_title="AI Feedback Analyzer",layout="wide")

def get_base64_video(path):
    with open(path,"rb") as f:
        return base64.b64encode(f.read()).decode()

video_base64=get_base64_video("bg_video.mp4")

st.markdown(f"""
<style>
.stApp{{background:transparent}}
.bg-video{{position:fixed;top:0;left:0;width:100%;height:100%;object-fit:cover;z-index:-1;opacity:0.75}}
div.stButton>button{{background:rgba(31,119,180,0.35);color:white;border:2px solid #1f77b4;border-radius:8px;padding:8px 18px;font-weight:600;transition:0.3s}}
div.stButton>button:hover{{background:#1f77b4;color:white;border:2px solid #1f77b4;transform:scale(1.05)}}
div.stDownloadButton>button{{background:rgba(31,119,180,0.35);color:white;border:2px solid #1f77b4;border-radius:8px;padding:8px 18px;font-weight:600;transition:0.3s}}
div.stDownloadButton>button:hover{{background:#1f77b4;color:white;border:2px solid #1f77b4;transform:scale(1.05)}}
[data-testid="metric-container"]{{background:rgba(31,119,180,0.45);padding:15px;border-radius:10px;color:white;text-align:center;box-shadow:0 0 12px rgba(31,119,180,0.6);backdrop-filter:blur(6px)}}
[data-testid="metric-container"] label,[data-testid="metric-container"] div{{color:white}}
div[data-testid="stAlert"]{{background:rgba(31,119,180,0.45);border-radius:10px;border:1px solid #1f77b4;color:white;box-shadow:0 0 12px rgba(31,119,180,0.6);backdrop-filter:blur(6px)}}
div[data-testid="stAlert"] p{{color:white!important;font-weight:500}}
textarea{{background:rgba(31,119,180,0.45)!important;color:white!important;border-radius:10px!important;border:1px solid #1f77b4!important;backdrop-filter:blur(6px)!important;padding:10px!important}}
div[data-testid="stFileUploader"]>div{{background:rgba(31,119,180,0.45)!important;border-radius:10px!important;border:1px solid #1f77b4!important;backdrop-filter:blur(6px)!important;color:white!important;padding:15px!important}}
div[data-testid="stFileUploader"] label{{color:white!important;font-weight:500!important}}
</style>
<video autoplay muted loop class="bg-video">
<source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
</video>
""",unsafe_allow_html=True)

page=st.radio("",["Home","Feedback Analyzer","About"],horizontal=True)

def get_sentiment(text):
    p=TextBlob(text).sentiment.polarity
    if p>0:return "Positive"
    if p<0:return "Negative"
    return "Neutral"

def get_topic(text):
    text=text.lower()
    if "lab" in text:return "Lab Facilities"
    if "fast" in text or "syllabus" in text:return "Teaching Pace"
    if "maintenance" in text or "classroom" in text:return "Infrastructure"
    if "faculty" in text or "teaching" in text:return "Teaching Quality"
    return "General"

def get_suggestion(topic,sentiment):
    if sentiment=="Negative":
        suggestions={"Lab Facilities":"Upgrade lab equipment and improve facilities.","Teaching Pace":"Reduce teaching pace and add revision sessions.","Infrastructure":"Improve classroom maintenance and infrastructure.","Teaching Quality":"Provide additional teaching support or training."}
        return suggestions.get(topic,"Review student concerns and take corrective action.")
    return "Overall performance is good. Maintain the quality."

if page=="Home":
    st.markdown("""
    <style>
    .title{font-size:60px;font-weight:bold;text-align:center;background:linear-gradient(90deg,#00f2ff,#ffffff,#00f2ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:glow 3s infinite alternate}
    @keyframes glow{from{letter-spacing:2px}to{letter-spacing:6px}}
    .subtitle{text-align:center;font-size:22px;color:white;margin-bottom:30px}
    .box{background:rgba(0,0,0,0.55);padding:25px;border-radius:12px;margin-top:20px;color:white;font-size:18px;line-height:1.7;animation:fade 1.5s ease-in}
    @keyframes fade{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    .step{background:rgba(31,119,180,0.45);padding:15px;backdrop-filter:blur(6px);border-radius:10px;margin:10px;text-align:center;font-size:17px;color:white}
    </style>
    """,unsafe_allow_html=True)

    st.markdown("<div class='title'>AI-Based Feedback Analyzer</div>",unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Understanding Student Opinions Automatically</div>",unsafe_allow_html=True)

    st.markdown("""<div class='box'>
    Educational institutions collect large amounts of feedback from students every semester. Reading each response manually takes a lot of time and important opinions may be missed. This project helps automatically analyze student feedback and summarize what students actually feel about their learning experience. Instead of reading hundreds of comments one by one, the system quickly studies the feedback and provides a clear summary of the overall opinion of students.
    </div>""",unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center;color:white;margin-top:30px;'>How This System Works</h3>",unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)
    with c1:st.markdown("<div class='step'>Students give their feedback about classes, labs, or facilities.</div>",unsafe_allow_html=True)
    with c2:st.markdown("<div class='step'>The system reads the feedback and understands the opinion expressed in it.</div>",unsafe_allow_html=True)
    with c3:st.markdown("<div class='step'>It groups similar comments together to identify common topics.</div>",unsafe_allow_html=True)
    with c4:st.markdown("<div class='step'>Finally, it shows a simple visual report that summarizes the feedback.</div>",unsafe_allow_html=True)

    st.markdown("""<div class='box'>
    The goal of this project is to make feedback analysis simple, fast, and easy to understand. Teachers and administrators can quickly see whether students are satisfied or if any improvements are required.
    </div>""",unsafe_allow_html=True)

elif page=="Feedback Analyzer":
    mode=st.radio("Select Mode",["Manual Feedback","File Upload"],horizontal=True)

    if mode=="Manual Feedback":
        feedback=st.text_area("Enter Student Feedback",height=150)
        analyze=st.button("Analyze Feedback")
        if analyze:
            if not feedback.strip():st.warning("Please enter feedback")
            else:
                progress=st.progress(0)
                for i in range(100):time.sleep(0.01);progress.progress(i+1)
                progress.empty()
                sentiment=get_sentiment(feedback)
                topic=get_topic(feedback)
                suggestion=get_suggestion(topic,sentiment)
                c1,c2,c3=st.columns(3)
                c1.metric("Sentiment",sentiment)
                c2.metric("Detected Topic",topic)
                c3.metric("Status","Completed")
                st.markdown("### Suggestion")
                st.success(suggestion)

    elif mode=="File Upload":
        file=st.file_uploader("Upload CSV or TXT",type=["csv","txt"])
        analyze_file=st.button("Analyze Feedback")

        if file and analyze_file:
            df=pd.read_csv(file) if file.name.endswith(".csv") else pd.DataFrame({"feedback":file.read().decode("utf-8").splitlines()})
            if "feedback" not in df.columns:st.error("File must contain 'feedback' column")
            else:
                progress=st.progress(0)
                for i in range(100):time.sleep(0.01);progress.progress(i+1)
                progress.empty()

                df["Sentiment"]=df["feedback"].astype(str).apply(get_sentiment)
                df["Topic"]=df["feedback"].astype(str).apply(get_topic)

                st.markdown("### Feedback Statistics")
                c1,c2,c3=st.columns(3)
                c1.metric("Total Feedback",len(df))
                c2.metric("Positive",(df["Sentiment"]=="Positive").sum())
                c3.metric("Negative",(df["Sentiment"]=="Negative").sum())

                st.markdown("### Feedback Analysis")
                
                col1, col2 = st.columns(2)
                with col1:
                    sentiment_counts = df["Sentiment"].value_counts()
                    fig1, ax1 = plt.subplots(figsize=(6,5))   
                    ax1.pie(sentiment_counts.values,
                            labels=sentiment_counts.index,
                            autopct='%1.1f%%',
                            startangle=90)
                    ax1.set_title("Sentiment Overview")
                    ax1.axis("equal")
                    st.pyplot(fig1)

                with col2:
                    topic_counts = df["Topic"].value_counts()
                    fig2, ax2 = plt.subplots(figsize=(6,5))   
                    ax2.bar(topic_counts.index, topic_counts.values)
                    ax2.set_title("Topic Analysis")
                    ax2.set_ylabel("Count")
                    plt.xticks(rotation=90, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig2)
                    
                positive=(df["Sentiment"]=="Positive").sum()
                negative=(df["Sentiment"]=="Negative").sum()
                total=len(df)
                pos_pct=round((positive/total)*100,2)
                neg_pct=round((negative/total)*100,2)

                if positive>negative:
                    insight=f"Most students appear satisfied with the learning experience.\n\nPositive feedback accounts for {pos_pct}% of total responses.\n\nContinue maintaining high-quality teaching and facilities."
                elif negative>positive:
                    insight=f"Many students are dissatisfied. Improvements may be required.\n\nNegative feedback accounts for {neg_pct}% of total responses.\n\nConsider addressing lab facilities, teaching pace, and infrastructure."
                else:
                    insight=f"Student feedback shows mixed opinions.\n\nPositive: {pos_pct}%, Negative: {neg_pct}%\n\nReview comments carefully to understand students’ concerns."

                st.subheader("AI Suggestion")
                st.info(insight)

                buffer=BytesIO()
                styles=getSampleStyleSheet()
                elements=[]
                elements.append(Paragraph("AI FEEDBACK ANALYSIS REPORT",styles['Title']))
                elements.append(Paragraph(f"<b>Total Feedback:</b> {total}",styles['Normal']))
                elements.append(Paragraph("<b>Sentiment Distribution</b>",styles['Heading3']))
                for s,c in sentiment_counts.items():elements.append(Paragraph(f"{s}: {c}",styles['Normal']))
                elements.append(Paragraph("<b>Topic Analysis</b>",styles['Heading3']))
                for t,c in topic_counts.items():elements.append(Paragraph(f"{t}: {c}",styles['Normal']))
                elements.append(Paragraph("<b>AI Insight</b>",styles['Heading3']))
                for line in insight.split("\n"):
                    if line.strip():elements.append(Paragraph(line.strip(),styles['Normal']))
                elements.append(Paragraph("<b>Recommendation</b>",styles['Heading3']))
                elements.append(Paragraph(get_suggestion(topic_counts.idxmax(),"Negative"),styles['Normal']))
                doc=SimpleDocTemplate(buffer);doc.build(elements)
                pdf=buffer.getvalue();buffer.close()
                st.download_button("Download Analysis Report",pdf,"feedback_report.pdf","application/pdf")

elif page=="About":
    st.markdown("<h3 style='text-align:center;'>Implementation Technologies</h3>",unsafe_allow_html=True)

    st.markdown("""
    <h4><b>Natural Language Processing (NLP)</b></h4><p>Used to analyze student feedback and determine sentiment polarity. It helps in understanding the underlying opinions expressed in textual data.</p>

    <h4><b>TextBlob Library</b></h4><p>Provides sentiment analysis by calculating polarity scores. It simplifies NLP tasks and allows quick evaluation of positive, negative, or neutral feedback.</p>

    <h4><b>Keyword-Based Topic Detection</b></h4><p>Identifies feedback themes such as teaching quality, infrastructure, and lab facilities. Helps to categorize student opinions automatically for better insights.</p>

    <h4><b>Bulk Data Processing</b></h4><p>Allows CSV and Text file upload for analyzing large volumes of student feedback. Ensures efficient processing of multiple entries without manual effort.</p>

    <h4><b>Streamlit Framework</b></h4><p>Used to develop the interactive web application interface. Provides easy-to-use components like text areas, buttons, and file uploaders for a smooth user experience.</p>

    <h4><b>Python Programming</b></h4><p>Core language used to implement the feedback analysis logic. Handles data manipulation, looping, condition checking, and integration with libraries.</p>

    <h4><b>Matplotlib Library</b></h4><p>Used to visualize sentiment distribution and topic analysis. Provides pie and bar charts to present the results graphically for better understanding.</p>

    <h4><b>ReportLab Library</b></h4><p>Generates PDF reports of the analysis. Allows formatting text, adding headings, spacers, and structured insights in a downloadable report.</p>

    <h4><b>Base64 & io.BytesIO</b></h4><p>Base64 is used to embed the video background seamlessly in Streamlit. BytesIO is used to manage in-memory PDF streams for download functionality.</p>
    """,unsafe_allow_html=True)

    st.markdown("## Developed By")
    c1,c2,c3,c4=st.columns(4)
    with c1:st.markdown("<div style='background-color:#1f77b4;padding:10px;border-radius:8px;text-align:center;color:white;'>T. Udayasri Durga - 25ME5A5409</div>",unsafe_allow_html=True)
    with c2:st.markdown("<div style='background-color:#1f77b4;padding:10px;border-radius:8px;text-align:center;color:white;'>Sk. Ushna - 24ME1A54A6</div>",unsafe_allow_html=True)
    with c3:st.markdown("<div style='background-color:#1f77b4;padding:10px;border-radius:8px;text-align:center;color:white;'>V. Harsha Priya - 24ME1A54C1</div>",unsafe_allow_html=True)
    with c4:st.markdown("<div style='background-color:#1f77b4;padding:10px;border-radius:8px;text-align:center;color:white;'>S. Navyasri - 24ME1A54A9</div>",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    st.caption("AI Feedback Analyzer © 2026")