import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import pandas as pd
import numpy as np
import sys
import os

# 상위 폴더 모듈 임포트
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import style

# 1. Page Config (반드시 가장 먼저 호출)
st.set_page_config(page_title="Design Master Guide", page_icon="🎨", layout="wide", initial_sidebar_state="collapsed")

# 2. Custom Sidebar (CSS & HTML)
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
            padding-bottom: 5rem !important;
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
    <!-- Dashboard Link -->
    <a href="/" target="_self" style="text-decoration: none;" aria-label="Dashboard">
        <div class="sidebar-btn" title="Dashboard">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
        </div>
    </a>
    <!-- Design Guide Link -->
    <a href="/design_guide" target="_self" style="text-decoration: none;" aria-label="Design Guide">
        <div class="sidebar-btn active" title="Design Guide">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

# 스타일 적용 (Page Config 이후에 호출)
style.apply_hynex_style()

st.title("🎨 Design System Guide")
st.markdown(f"""
<div style='color: {style.COLORS['text_sub']}; margin-bottom: 40px; font-size: 16px;'>
    <b>팀 협업을 위한 마스터 디자인 가이드</b><br>
    모든 예시는 실제 작동하는 전체 코드를 포함하고 있습니다. 그대로 복사하여 사용하세요.
</div>
""", unsafe_allow_html=True)

# =========================================================
# 1. Color Palette
# =========================================================
st.header("1. Color Palette")
st.markdown("데이터의 성격에 맞춰 정의된 색상을 사용하세요.")

cols = st.columns(5)
colors = [
    ("Primary", "primary", "확진자, 메인 포인트"),
    ("Success", "success", "완치, 백신, 긍정 지표"),
    ("Danger", "danger", "사망, 경고, 위기"),
    ("Warning", "warning", "위중증, 주의 단계"),
    ("Info", "info", "검사 수, 일반 정보")
]

for col, (name, key, desc) in zip(cols, colors):
    code = style.COLORS[key]
    with col:
        st.markdown(f"""
        <div style='background-color: {style.COLORS['bg_card']}; border: 1px solid {style.COLORS['border']}; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 10px;'>
            <div style='background-color: {code}; height: 50px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 4px 12px {code}40;'></div>
            <h4 style='margin: 0; color: #fff; font-size: 16px;'>{name}</h4>
            <p style='margin: 5px 0; color: {style.COLORS['primary']}; font-family: monospace; font-size: 14px;'>{code}</p>
            <p style='margin: 0; color: {style.COLORS['text_sub']}; font-size: 12px; opacity: 0.7;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        st.code(f"style.COLORS['{key}']", language="python")

st.divider()

# =========================================================
# 2. Typography & Headers
# =========================================================
st.header("2. Typography & Headers")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Simple Icon Header")
    header_html = f"""
<div style='display: flex; align-items: center; margin-bottom: 10px;'>
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{style.COLORS['primary']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 15px;"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
    <h3 style='margin: 0; color: {style.COLORS['text_main']};'>Health Analytics</h3>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)
    with st.expander("Copy Code", expanded=True):
        st.code($1import streamlit as st

st.markdown("""
<div style='display: flex; align-items: center; margin-bottom: 10px;'>
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" 
         stroke="{style.COLORS['primary']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 15px;">
        <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
    </svg>
    <h3 style='margin: 0; color: #FFFFFF;'>제목 입력</h3>
</div>
""", unsafe_allow_html=True)
''', language="python")

with c2:
    st.subheader("Boxed Header")
    boxed_html = f"""
<div style='display: flex; align-items: center; margin-bottom: 10px;'>
    <div class="icon-box" style="margin-right:15px">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{style.COLORS['info']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
    </div>
    <h3 style='margin: 0; color: {style.COLORS['text_main']};'>Global Statistics</h3>
</div>
"""
    st.markdown(boxed_html, unsafe_allow_html=True)
    with st.expander("Copy Code", expanded=True):
        st.code($1import streamlit as st

st.markdown("""
<div style='background: {style.COLORS['bg_card']}; padding: 15px; border-radius: 12px; border: 1px solid {style.COLORS['border']}; display: flex; align-items: center;'>
    <div class="icon-box" style="margin-right:15px">
        <svg ...>...</svg>
    </div>
    <span style="font-weight:600; font-size: 18px; color:white;">제목 입력</span>
</div>
""", unsafe_allow_html=True)
''', language="python")

st.divider()

# =========================================================
# 3. UI Components
# =========================================================
st.header("3. UI Components")

col_ui1, col_ui2 = st.columns(2)

with col_ui1:
    st.markdown("**Live & Sync Indicators**")
    st.markdown(f"""
    <div style='background: {style.COLORS['bg_card']}; padding: 20px; border-radius: 12px; border: 1px solid {style.COLORS['border']}; display: flex; gap: 30px; align-items: center;'>
        <div style='display: flex; align-items: center; gap: 10px;'>
            <div class="dot-red"></div> <span style="color:white; font-weight:bold;">Live Recording</span>
        </div>
        <div style='display: flex; align-items: center; gap: 10px;'>
            <div class="spinner-ring"></div> <span style="color:white; font-weight:bold;">Syncing...</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("Copy Code", expanded=True):
        st.code('''
# Live Red Dot
st.markdown('<div class="dot-red"></div> Live', unsafe_allow_html=True)

# Loading Spinner
st.markdown('<div class="spinner-ring"></div> Syncing', unsafe_allow_html=True)
''', language="python")

with col_ui2:
    st.markdown("**Trend Badges**")
    st.markdown(f"""
    <div style='background: {style.COLORS['bg_card']}; padding: 20px; border-radius: 12px; border: 1px solid {style.COLORS['border']}; display: flex; gap: 15px; align-items: center;'>
        <div class="badge badge-danger">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg> +15.4%
        </div>
        <div class="badge badge-success">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg> -2.1%
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("Copy Code", expanded=True):
        st.code($1import streamlit as st

st.markdown("""
<div class="badge badge-danger">
    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg> +15.4%
</div>
""", unsafe_allow_html=True)
''', language="python")

st.divider()

# =========================================================
# 4. Icon Library (10 Types)
# =========================================================
st.header("4. Icon Library (SVG)")
st.markdown("Hynex 스타일의 10종 핵심 아이콘 세트입니다.")

def icon_card_with_code(name, svg_content, color_key="primary"):
    color = style.COLORS[color_key]
    full_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{svg_content}</svg>'
    
    st.markdown(f"""
    <div style='background: {style.COLORS['bg_card']}; border: 1px solid {style.COLORS['border']}; border-radius: 10px; padding: 15px; text-align: center; height: 100px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;'>
        <div style='margin-bottom: 8px;'>{full_svg}</div>
        <div style='color: {style.COLORS['text_main']}; font-size: 13px; font-weight: 600;'>{name}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 코드는 접을 수 있게(Expander) 하되, 기본적으로 열어둠
    with st.expander("Copy Code", expanded=True):
        code_text = f"""st.markdown('''
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    {svg_content}
</svg>
''', unsafe_allow_html=True)"""
        st.code(code_text, language="python")

# 2 Rows of 5 icons
r1 = st.columns(5)
with r1[0]: icon_card_with_code("Activity", '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>')
with r1[1]: icon_card_with_code("Virus", '<path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/><circle cx="12" cy="12" r="3"/>', "danger")
with r1[2]: icon_card_with_code("Vaccine", '<path d="M19 3l-6 6"/><path d="M13 13l-4 4"/><path d="M10 10l-6 6 2 2 6-6"/><path d="M21 7l-4-4"/><path d="M3 21l4-4"/>', "success")
with r1[3]: icon_card_with_code("Hospital", '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>', "warning")
with r1[4]: icon_card_with_code("Users", '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>', "info")

r2 = st.columns(5)
with r2[0]: icon_card_with_code("Globe", '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>', "info")
with r2[1]: icon_card_with_code("Search", '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>')
with r2[2]: icon_card_with_code("Shield", '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>', "success")
with r2[3]: icon_card_with_code("Calendar", '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>', "text_sub")
with r2[4]: icon_card_with_code("Alert", '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>', "danger")

st.divider()

# =========================================================
# 5. Chart Guidelines
# =========================================================
st.header("5. Chart Guidelines")

st.markdown("#### Chart Header Icons")
ci1, ci2, ci3, ci4 = st.columns(4)
with ci1: icon_card_with_code("Bar Chart", '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>')
with ci2: icon_card_with_code("Trending", '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>', "success")
with ci3: icon_card_with_code("Pie Chart", '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>', "info")
with ci4: icon_card_with_code("Map", '<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/>', "warning")

st.divider()

# 데이터 준비
dates = pd.date_range(start="2023-01-01", periods=10)
df_sample = pd.DataFrame({
    "Date": dates,
    "Confirmed": [100, 120, 150, 140, 180, 200, 250, 300, 280, 320],
    "Recovered": [80, 100, 110, 130, 150, 180, 220, 250, 270, 300],
    "Category_A": [30, 40, 35, 50, 60, 55, 70, 80, 75, 90],
    "Category_B": [20, 30, 25, 40, 50, 45, 60, 70, 65, 80],
    "Category_C": [50, 60, 55, 70, 80, 75, 90, 100, 95, 110]
})
df_long = df_sample.melt(id_vars='Date', value_vars=['Category_A', 'Category_B', 'Category_C'], var_name='Type', value_name='Count')

chart_layout = style.get_chart_layout()

tab1, tab2, tab3, tab4 = st.tabs(["Basic", "Composition", "Radar", "3D Map"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Stacked Bar Chart")
        fig_stack = px.bar(df_long, x='Date', y='Count', color='Type', color_discrete_sequence=[style.COLORS['primary'], style.COLORS['success'], style.COLORS['info']])
        fig_stack.update_layout(**chart_layout)
        st.plotly_chart(fig_stack, use_container_width=True)
        with st.expander("Copy Code", expanded=True):
            st.code('''
import plotly.express as px
import style

fig = px.bar(df, x='Date', y='Count', color='Type',
             color_discrete_sequence=[style.COLORS['primary'], style.COLORS['success'], style.COLORS['info']])

fig.update_layout(**style.get_chart_layout())
st.plotly_chart(fig, use_container_width=True)
''', language="python")

    with col2:
        st.markdown("#### Multi-Line Chart")
        fig_line = px.line(df_sample, x='Date', y=['Confirmed', 'Recovered'], markers=True, color_discrete_sequence=[style.COLORS['danger'], style.COLORS['success']])
        fig_line.update_layout(**chart_layout)
        st.plotly_chart(fig_line, use_container_width=True)
        with st.expander("Copy Code", expanded=True):
            st.code('''
import plotly.express as px
import style

fig = px.line(df, x='Date', y=['Confirmed', 'Recovered'], markers=True,
              color_discrete_sequence=[style.COLORS['danger'], style.COLORS['success']])

fig.update_layout(**style.get_chart_layout())
st.plotly_chart(fig, use_container_width=True)
''', language="python")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Donut Chart")
        fig_pie = px.pie(values=[60, 30, 10], names=['A', 'B', 'C'], hole=0.6, color_discrete_sequence=[style.COLORS['primary'], style.COLORS['info'], style.COLORS['bg_card']])
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=True, font_color='white')
        st.plotly_chart(fig_pie, use_container_width=True)
        with st.expander("Copy Code", expanded=True):
            st.code('''
import plotly.express as px
import style

fig = px.pie(values=[60, 30, 10], names=['A', 'B', 'C'], hole=0.6,
             color_discrete_sequence=[style.COLORS['primary'], style.COLORS['info'], style.COLORS['bg_card']])

fig.update_layout(
    **style.get_chart_layout(),
    showlegend=True,
    annotations=[dict(text='60%', x=0.5, y=0.5, font_size=24, showarrow=False, font=dict(color='white'))]
)
st.plotly_chart(fig, use_container_width=True)
''', language="python")

    with col2:
        st.markdown("#### Treemap")
        fig_tree = px.treemap(df_long, path=['Type'], values='Count', color='Type', color_discrete_sequence=[style.COLORS['primary'], style.COLORS['success'], style.COLORS['info']])
        fig_tree.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, l=0, r=0, b=0))
        st.plotly_chart(fig_tree, use_container_width=True)
        with st.expander("Copy Code", expanded=True):
            st.code('''
import plotly.express as px
import style

fig = px.treemap(df, path=['Type'], values='Count', color='Type',
                 color_discrete_sequence=[style.COLORS['primary'], style.COLORS['success'], style.COLORS['info']])

fig.update_layout(
    **style.get_chart_layout(),
    margin=dict(t=0, l=0, r=0, b=0)
)
st.plotly_chart(fig, use_container_width=True)
''', language="python")

with tab3:
    st.markdown("#### Radar Chart")
    categories = ['Confirmed', 'Deaths', 'Recovered', 'Tests', 'Vaccinated']
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=[20, 5, 95, 85, 90], theta=categories, fill='toself', name='Korea', line_color=style.COLORS['success'], fillcolor='rgba(5, 205, 153, 0.2)'))
    fig_radar.add_trace(go.Scatterpolar(r=[85, 40, 60, 30, 45], theta=categories, fill='toself', name='High Risk', line_color=style.COLORS['danger'], fillcolor='rgba(255, 91, 91, 0.2)'))
    fig_radar.update_layout(polar=dict(bgcolor=style.COLORS['bg_card'], radialaxis=dict(visible=True, range=[0, 100], color=style.COLORS['text_sub'], gridcolor=style.COLORS['border'])), paper_bgcolor='rgba(0,0,0,0)', font_color=style.COLORS['text_main'], showlegend=True)
    st.plotly_chart(fig_radar, use_container_width=True)
    with st.expander("Copy Code", expanded=True):
        st.code('''
import plotly.graph_objects as go
import style

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=[20, 5, 95, 85, 90], theta=['확진', '사망', '회복', '검사', '백신'], 
    fill='toself', name='Korea', 
    line_color=style.COLORS['success'], fillcolor='rgba(5, 205, 153, 0.2)'
))

fig.update_layout(
    polar=dict(
        bgcolor=style.COLORS['bg_card'],
        radialaxis=dict(visible=True, range=[0, 100], color='#A3AED0')
    ),
    paper_bgcolor='rgba(0,0,0,0)', font_color='white'
)
st.plotly_chart(fig, use_container_width=True)
''', language="python")

with tab4:
    st.markdown("#### 3D Column Map")
    map_data = pd.DataFrame({'lat': [37.5, 35.1, 35.6], 'lon': [126.9, 129.0, 139.6], 'cases': [5000, 3000, 8000]})
    layer = pdk.Layer("ColumnLayer", map_data, get_position=["lon", "lat"], get_elevation="cases", elevation_scale=200, radius=40000, get_fill_color=[123, 97, 255, 255], pickable=True, auto_highlight=True)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=pdk.ViewState(latitude=36, longitude=130, zoom=3, pitch=50), map_style=None))
    with st.expander("Copy Code", expanded=True):
        st.code('''
import pydeck as pdk

layer = pdk.Layer(
    "ColumnLayer", data=df, get_position=["lon", "lat"], get_elevation="cases",
    elevation_scale=100, radius=30000, 
    get_fill_color=[123, 97, 255, 255], pickable=True, auto_highlight=True
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=pdk.ViewState(latitude=36.0, longitude=128.0, zoom=5, pitch=50),
    map_style=None
))
''', language="python")
