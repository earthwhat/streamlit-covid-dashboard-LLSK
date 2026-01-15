import streamlit as st

# Hynex Color Palette
COLORS = {
    "bg_main": "#0D0E12",
    "bg_card": "#1A1C24",
    "border": "#2E303A",
    "text_main": "#FFFFFF",
    "text_sub": "#A3AED0",
    "primary": "#7B61FF",      # Purple (확진자)
    "success": "#05CD99",      # Mint (회복/백신)
    "danger": "#FF5B5B",       # Red (사망)
    "warning": "#FFB547",      # Orange (위중증)
    "info": "#4318FF"          # Blue (검사)
}

# 차트용 컬러 시퀀스 (Plotly용)
CHART_SEQ = [COLORS['primary'], COLORS['success'], COLORS['danger'], COLORS['warning'], COLORS['info']]

def apply_hynex_style():
    st.markdown(f"""
        <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        html, body, [class*="css"] {{
            font-family: 'Pretendard', sans-serif;
            color: {COLORS['text_main']};
        }}
        
        /* 메트릭 카드 (Hynex Card Style) */
        div[data-testid="stMetric"] {{
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 20px;
            padding: 20px 24px;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
        }}
        
        div[data-testid="stMetricLabel"] {{
            color: {COLORS['text_sub']} !important;
            font-size: 14px !important;
            font-weight: 500 !important;
        }}
        
        div[data-testid="stMetricValue"] {{
            color: {COLORS['text_main']} !important;
            font-size: 26px !important;
            font-weight: 700 !important;
        }}

        /* 데이터 소스 박스 스타일 */
        .info-box {{
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-left: 4px solid {COLORS['primary']};
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 30px;
        }}
        
        .info-text {{
            color: {COLORS['text_sub']};
            font-size: 14px;
            margin: 0;
        }}

        /* 아이콘 컨테이너 */
        .icon-box {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border-radius: 10px;
            background-color: rgba(123, 97, 255, 0.1); /* Primary 10% opacity */
            margin-right: 12px;
        }}

        /* 탭 스타일 */
        button[data-baseweb="tab"] {{
            background-color: transparent !important;
            color: {COLORS['text_sub']} !important;
            font-weight: 600 !important;
        }}
        
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {COLORS['primary']} !important;
            border-bottom: 2px solid {COLORS['primary']} !important;
        }}

        /* --- Animations & Dots --- */
        @keyframes pulse-red {{
            0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 91, 91, 0.7); }}
            70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(255, 91, 91, 0); }}
            100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 91, 91, 0); }}
        }}
        
        @keyframes pulse-purple {{
            0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(123, 97, 255, 0.7); }}
            70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(123, 97, 255, 0); }}
            100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(123, 97, 255, 0); }}
        }}

        .dot-red {{
            width: 8px; height: 8px; background-color: {COLORS['danger']}; border-radius: 50%;
            display: inline-block; animation: pulse-red 2s infinite;
            margin-right: 5px;
        }}

        .dot-purple {{
            width: 8px; height: 8px; background-color: {COLORS['primary']}; border-radius: 50%;
            display: inline-block; animation: pulse-purple 2s infinite;
            margin-right: 5px;
        }}

        /* --- New Components (Badges & Loaders) --- */
        .badge {{
            padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;
            display: inline-flex; align-items: center; gap: 5px;
        }}
        .badge-danger {{ background-color: rgba(255, 91, 91, 0.15); color: {COLORS['danger']}; border: 1px solid rgba(255, 91, 91, 0.3); }}
        .badge-success {{ background-color: rgba(5, 205, 153, 0.15); color: {COLORS['success']}; border: 1px solid rgba(5, 205, 153, 0.3); }}
        
        .spinner-ring {{
            width: 20px; height: 20px; border: 3px solid rgba(123, 97, 255, 0.3);
            border-top: 3px solid {COLORS['primary']}; border-radius: 50%;
            animation: spin 1s linear infinite; display: inline-block;
        }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}

        </style>
    """, unsafe_allow_html=True)

def card_metric(label, value, delta=None, color="primary"):
    """
    커스텀 메트릭 카드 (필요시 사용, 현재는 st.metric 스타일링으로 대체 가능)
    """
    pass