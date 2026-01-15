import streamlit as st
import pandas as pd
import plotly.express as px
import data_manager

# 페이지 설정
st.set_page_config(page_title="COVID-19 Hybrid Dashboard", layout="wide", page_icon="💉")

st.title("🦠 COVID-19 하이브리드 대시보드")
st.markdown("""
이 대시보드는 **이중 데이터 소스**를 사용합니다:
1. **실시간 현황**: [Disease.sh API](https://disease.sh/) (즉시 로딩)
2. **과거 추세**: [OWID GitHub Data](https://github.com/owid/covid-19-data) (CSV 분석)
""")

# --- 1. 실시간 데이터 섹션 (API) ---
st.subheader("🔴 실시간 현황 (Live API)")
realtime_data = data_manager.fetch_realtime_api("South Korea")

if realtime_data:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("오늘 확진자", f"+{realtime_data['todayCases']:,}")
    with col2:
        st.metric("총 확진자", f"{realtime_data['cases']:,}")
    with col3:
        st.metric("총 사망자", f"{realtime_data['deaths']:,}")
    with col4:
        st.metric("위중증", f"{realtime_data['critical']:,}")
    
    st.caption(f"데이터 업데이트: {pd.to_datetime(realtime_data['updated'], unit='ms')}")
else:
    st.error("실시간 API 연결에 실패했습니다.")

st.divider()

# --- 2. 과거 데이터 섹션 (CSV) ---
st.subheader("📈 과거 추세 분석 (OWID Data)")

# 데이터 로딩 (캐싱 적용)
@st.cache_data
def get_cached_history():
    return data_manager.load_history_data("KOR")

with st.spinner("대용량 과거 데이터를 불러오는 중입니다... (최초 실행 시 다운로드로 인해 1-2분 소요될 수 있습니다)"):
    df_history = get_cached_history()

if not df_history.empty:
    # 탭으로 보기 방식 변경
    tab1, tab2 = st.tabs(["확진자 추이", "백신 접종 현황"])
    
    with tab1:
        fig_cases = px.line(df_history, x='date', y=['new_cases_smoothed', 'new_deaths_smoothed'], 
                            title="일일 신규 확진/사망 (7일 이동평균)",
                            labels={'value': '명', 'date': '날짜', 'variable': '구분'})
        st.plotly_chart(fig_cases, use_container_width=True)
        
    with tab2:
        fig_vac = px.area(df_history, x='date', y=['people_vaccinated', 'people_fully_vaccinated'],
                          title="백신 접종 누적 추이",
                          labels={'value': '명', 'date': '날짜', 'variable': '접종 상태'})
        st.plotly_chart(fig_vac, use_container_width=True)
else:
    st.warning("과거 데이터를 로드할 수 없습니다. 'data/owid-covid-data.csv' 파일이 있는지 확인해주세요.")
    if st.button("데이터 수동 다운로드 시도"):
        if data_manager.download_owid_data():
            st.rerun()
