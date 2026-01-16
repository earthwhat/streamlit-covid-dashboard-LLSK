import streamlit as st
import pandas as pd
import plotly.express as px
import data_manager
import style  # Hynex 스타일 모듈

# 1. 페이지 설정
st.set_page_config(
    page_title="COVID-19 Analytics", 
    layout="wide", 
    page_icon="🦠",
    initial_sidebar_state="collapsed"
)

# 2. Custom Sidebar (CSS & HTML) - Dashboard Active
st.markdown(f"""
<style>
    /* 기본 헤더 배경 투명화 (우측 상단 메뉴는 보이게 유지) */
    header[data-testid="stHeader"] {{
        background-color: transparent;
    }}
    /* 기본 사이드바 숨김 */
    [data-testid="stSidebar"] {{
        display: none;
    }}
    /* 메인 콘텐츠 패딩 조정 (데스크톱 기준) */
    .main .block-container {{
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 6rem !important; 
        padding-right: 3rem !important;
        max-width: none !important;
        padding-top: 1rem !important; 
    }}
    /* 커스텀 사이드바 컨테이너 */
    .custom-sidebar {{
        position: fixed;
        left: 0; top: 0;
        width: 50px; height: 100vh;
        background-color: {style.COLORS['bg_main']};
        border-right: 1px solid {style.COLORS['border']};
        display: flex; flex-direction: column; align-items: center;
        padding-top: 20px; z-index: 999999;
    }}

    /* 모바일 대응 (768px 이하) */
    @media (max-width: 768px) {{
        .custom-sidebar {{
            width: 100%;
            height: 50px;
            bottom: 0;
            top: auto;
            flex-direction: row;
            justify-content: center;
            padding-top: 0;
            border-right: none;
            border-top: 1px solid {style.COLORS['border']};
        }}
        .main .block-container {{
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            padding-bottom: 5rem !important; /* 사이드바에 가리지 않게 하단 여백 추가 */
        }}
        .sidebar-btn {{
            margin-bottom: 0 !important;
            margin-right: 15px;
        }}
    }}

    /* 아이콘 버튼 스타일 */
    .sidebar-btn {{
        width: 34px; height: 34px;
        border-radius: 8px;
        display: flex; justify-content: center; align-items: center;
        margin-bottom: 6px; cursor: pointer;
        transition: all 0.2s ease;
        color: {style.COLORS['text_sub']};
    }}
    .sidebar-btn:hover {{
        background-color: rgba(255, 255, 255, 0.05);
        color: {style.COLORS['primary']};
    }}
    .sidebar-btn.active {{
        background-color: rgba(123, 97, 255, 0.15);
        color: {style.COLORS['primary']};
        box-shadow: 0 0 0 1px {style.COLORS['primary']};
    }}
</style>

<div class="custom-sidebar">
    <!-- Dashboard Link (Active) -->
    <a href="/" target="_self" style="text-decoration: none;" aria-label="Dashboard">
        <div class="sidebar-btn active" title="Dashboard">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
        </div>
    </a>
    <!-- Design Guide Link -->
    <a href="/design_guide" target="_self" style="text-decoration: none;" aria-label="Design Guide">
        <div class="sidebar-btn" title="Design Guide">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

# 3. 스타일 적용
style.apply_hynex_style()

# 3. 헤더 섹션
st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 20px;'>
        <h1 style='color: {style.COLORS['text_main']}; font-size: 36px; margin: 0;'>
            🦠 COVID-19 <span style='color: {style.COLORS['primary']};'>Analytics</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

# 4. 데이터 소스 설명 (Hynex Info Box Style)
st.markdown(f"""
    <div class="info-box">
        <p class="info-text">
            <b>Data Sources</b>: 
            <span style='color: {style.COLORS['text_main']};'>Real-time</span> via <a href="https://disease.sh/" target="_blank" style="color: {style.COLORS['success']}; text-decoration: none;">Disease.sh API</a> & 
            <span style='color: {style.COLORS['text_main']};'>Historical Trends</span> via <a href="https://github.com/owid/covid-19-data" target="_blank" style="color: {style.COLORS['success']}; text-decoration: none;">OWID Data</a>
        </p>
    </div>
""", unsafe_allow_html=True)

# --- 5. 실시간 데이터 섹션 (API) ---
# style.py에 정의된 .dot-red 클래스 사용 (맥박 애니메이션)
st.markdown("""
    <h3 style='color: #A0A3BD; margin-bottom: 20px; display: flex; align-items: center; gap: 15px;'>
        <div class="dot-red"></div> Live Status
    </h3>
""", unsafe_allow_html=True)

realtime_data = data_manager.fetch_realtime_api("South Korea")

if realtime_data:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("New Cases", f"+{realtime_data['todayCases']:,}", delta_color="inverse")
    with col2:
        st.metric("Total Cases", f"{realtime_data['cases']:,}")
    with col3:
        st.metric("Total Deaths", f"{realtime_data['deaths']:,}")
    with col4:
        st.metric("Critical", f"{realtime_data['critical']:,}")
else:
    st.error("API 연결 실패")

st.markdown("---")

# --- 6. 과거 데이터 섹션 (CSV) ---
st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 20px; margin-top: 20px;'>
        <div class="icon-box" style="background-color: rgba(67, 24, 255, 0.1);">
            <!-- Activity Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{style.COLORS['info']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
        </div>
        <h3 style='margin: 0; color: {style.COLORS['text_main']};'>Historical Trends</h3>
    </div>
""", unsafe_allow_html=True)

@st.cache_data
def get_cached_history():
    return data_manager.load_history_data("KOR")

with st.spinner("Loading Historical Data..."):
    df_history = get_cached_history()

if not df_history.empty:
    tab1, tab2 = st.tabs(["Trends (Daily)", "Vaccination"])
    
    chart_layout = style.get_chart_layout()

    with tab1:
        # 확진자(Primary) vs 사망자(Danger)
        fig_cases = px.line(df_history, x='date', y=['new_cases_smoothed', 'new_deaths_smoothed'],
                            color_discrete_sequence=[style.COLORS['primary'], style.COLORS['danger']])
        fig_cases.update_layout(**chart_layout)
        st.plotly_chart(fig_cases, use_container_width=True)
        
    with tab2:
        # 백신(Success)
        fig_vac = px.area(df_history, x='date', y=['people_vaccinated', 'people_fully_vaccinated'],
                          color_discrete_sequence=[style.COLORS['success'], style.COLORS['info']])
        fig_vac.update_layout(**chart_layout)
        st.plotly_chart(fig_vac, use_container_width=True)
else:
    st.warning("No Data Available")