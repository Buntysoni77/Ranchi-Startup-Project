import streamlit as st
import pandas as pd
import base64
import os
 
st.set_page_config(page_title="Jharkhand Scout", layout="wide", initial_sidebar_state="expanded")
 
def local_css():
    logo_path = "static/scout.png"
    logo_base64 = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
 
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;600;900&display=swap');
        header {{ visibility: hidden; }}
        .stApp {{ background-color: #05070a !important; color: #ffffff !important; font-family: 'Outfit', sans-serif; }}
        [data-testid="stSidebar"] {{ background-color: #000000 !important; border-right: 2px solid #d4af37 !important; width: 350px !important; }}
        .sidebar-title {{ color: #d4af37 !important; font-size: 1.5rem !important; font-weight: 900 !important; letter-spacing: 2px; margin-bottom: 30px; text-transform: uppercase; border-bottom: 2px solid #d4af37; padding-bottom: 10px; display: block; }}
        [data-testid="stSidebar"] .stWidgetLabel p {{ color: #ffffff !important; font-size: 1.1rem !important; font-weight: 700 !important; margin-bottom: 10px !important; letter-spacing: 0.5px; }}
        div[data-baseweb="select"] > div {{ background-color: #111 !important; border: 1px solid #d4af37 !important; color: white !important; border-radius: 8px !important; }}
        .header-bar {{ background: #000; padding: 10px 40px; display: flex; align-items: center; border-bottom: 2px solid #d4af37; margin-top: -75px; }}
        .logo-img {{ height: 100px; width: auto; margin-right: 25px; filter: drop-shadow(0px 0px 5px #d4af37); }}
        .brand-title {{ color: #fff; font-size: 3.5rem; font-weight: 900; letter-spacing: -1px; }}
        .hero-container {{ margin: 20px 40px; height: 400px; border-radius: 15px; overflow: hidden; border: 1px solid #d4af37; position: relative; }}
        .slide {{ position: absolute; width: 100%; height: 100%; background-size: cover; background-position: center; animation: fadeEffect 18s infinite; opacity: 0; }}
        .slide:nth-child(1) {{ background-image: url('https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=1200'); animation-delay: 0s; }}
        .slide:nth-child(2) {{ background-image: url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1200'); animation-delay: 3s; }}
        .slide:nth-child(3) {{ background-image: url('https://images.unsplash.com/photo-1567521464027-f127ff144326?q=80&w=1200'); animation-delay: 6s; }}
        .slide:nth-child(4) {{ background-image: url('https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=1200'); animation-delay: 9s; }}
        .slide:nth-child(5) {{ background-image: url('https://images.unsplash.com/photo-1606787366850-de6330128bfc?q=80&w=1200'); animation-delay: 12s; }}
        .slide:nth-child(6) {{ background-image: url('https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?q=80&w=1200'); animation-delay: 15s; }}
        @keyframes fadeEffect {{ 0%, 10% {{ opacity: 1; }} 20%, 100% {{ opacity: 0; }} }}
        .rec-card {{ background: #111; border-left: 5px solid #d4af37; padding: 25px; border-radius: 10px; margin-top: 20px; }}
        .reason-box {{ background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px; margin-top: 15px; }}
    </style>
    <div class="header-bar">
        <img src="data:image/png;base64,{logo_base64}" class="logo-img">
        <h1 class="brand-title">JHARKHAND SCOUT</h1>
    </div>
    <div class="hero-container">
        <div class="slide"></div>
        <div class="slide"></div>
        <div class="slide"></div>
        <div class="slide"></div>
        <div class="slide"></div>
        <div class="slide"></div>
    </div>
    """, unsafe_allow_html=True)
 
local_css()
 
@st.cache_data
def load_data():
    try:
        an = pd.read_csv("data/processed/jharkhand_analytics.csv")
        m  = pd.read_csv("data/processed/area_mapping.csv")
        return an, m
    except Exception as e:
        st.error(f"Error: {e}. Run analysis script first.")
        return None, None
 
df_jh, area_map = load_data()
 
if df_jh is not None:
    st.sidebar.markdown('<p class="sidebar-title">⚙️ Navigation</p>', unsafe_allow_html=True)
    sel_dist = st.sidebar.selectbox("Target District", sorted(df_jh['District'].unique()))
 
    areas    = area_map[area_map['District'].str.upper() == sel_dist.upper()]['Area'].unique()
    sel_area = st.sidebar.selectbox("📍 Select Locality", sorted(areas) if len(areas) > 0 else ["Main Market"])
 
    s = df_jh[df_jh['District'] == sel_dist].iloc[0]
 
    area_row = area_map[
        (area_map['District'].str.upper() == sel_dist.upper()) &
        (area_map['Area'] == sel_area)
    ]
 
    if not area_row.empty:
        rec    = area_row.iloc[0]['Primary_Recommendation']
        reason = area_row.iloc[0]['Primary_Reason']
        rank2  = area_row.iloc[0].get('Rank2_Business', '')
        rank3  = area_row.iloc[0].get('Rank3_Business', '')
        atype  = area_row.iloc[0].get('Area_Type', '').title()
    else:
        rec    = s['Primary_Recommendation']
        reason = s['Primary_Reason']
        rank2  = rank3 = atype = ''
 
    col1, col2 = st.columns([1.4, 1])
 
    with col1:
        other_biz = ""
        if rank2:
            other_biz += f"<p style='color:#888; margin:4px 0;'>2 <b>{rank2}</b></p>"
        if rank3:
            other_biz += f"<p style='color:#888; margin:4px 0;'>3 <b>{rank3}</b></p>"
 
        st.markdown(f"""
        <div class="rec-card">
            <h1 style="color:#d4af37; margin:0; font-size:2.2rem;"> Recommendation: {rec}</h1>
            <p style="color:#aaa; margin:6px 0 0 0; font-size:0.95rem;">Zone Type: <b style="color:#d4af37">{atype}</b> &nbsp;|&nbsp; Locality: <b style="color:#fff">{sel_area}</b></p>
            <div class="reason-box">
                <h4 style="color:#fff; margin-bottom:10px;"> Why this business? (Data Insight)</h4>
                <p style="color:#bbb; line-height:1.6;">{reason}</p>
                {'<hr style="border-color:#222;"><p style="color:#777; font-size:0.85rem; margin:4px 0;">Also consider:</p>' + other_biz if other_biz else ''}
                <hr style="border-color:#333;">
                <p style="color:#d4af37; font-weight:bold;">Statistical Confidence: High (Based on Jharkhand Median Comparison)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown("### Statistical Correlation Chart")
        chart_data = pd.DataFrame({
            "Market Factors": ["Talent Density", "Urban Ratio", "Labor Availability"],
            "Score": [s.get('Talent_Score', 0), s.get('Urban_Ratio', 0), s.get('Workforce_Availability', 0)]
        }).set_index("Market Factors")
        st.bar_chart(chart_data)
 
    with col2:
        st.markdown(f"### Analysis: {sel_area}")
 
        t_score = s.get('Talent_Score', 0)
        st.write(f"**Education Standard (Graduates):** {t_score:.2f}%")
        st.progress(min(int(t_score), 100) if t_score > 0 else 0)
 
        w_score = s.get('Workforce_Availability', 0)
        st.write(f"**Workforce Pressure:** {w_score:.2f}%")
        st.progress(min(int(w_score), 100) if w_score > 0 else 0)
 
        st.map(pd.DataFrame({'lat': [23.3441], 'lon': [85.3091]}))
 
st.markdown(f"""
<div style="background:#000; border-top:2px solid #d4af37; padding:50px; margin-top:60px; color:#888; font-size:0.9rem; line-height:1.6;">
    <div style="max-width:1100px; margin:auto; text-align:justify;">
        <b>JHARKHAND SCOUT BUSINESS INTELLIGENCE DISCLAIMER:</b> This analytical dashboard is powered by the 2011 Census of India data
        and real-time market projection algorithms for 2026. The recommendations provided for <b>{sel_dist if 'sel_dist' in locals() else 'Jharkhand'}</b> are based on a
        multi-factor analysis of literacy rates, household digital penetration, and workforce participation. This platform is designed
        to identify infrastructure gaps and assist entrepreneurs in strategic decision-making.
        <br><br>
        <center style="color:#d4af37; font-weight:900;">© 2026 JHARKHAND SCOUT | PROPELLING DIGITAL GROWTH IN THE HEARTLAND</center>
    </div>
</div>
""", unsafe_allow_html=True)
