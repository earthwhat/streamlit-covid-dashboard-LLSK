# 🦠 COVID-19 Hybrid Dashboard

OWID(Our World in Data)와 Disease.sh API를 활용한 하이브리드 코로나 대시보드 프로젝트입니다.
Windows(작성자)와 macOS(팀원) 간의 원활한 협업을 위해 **Docker** 기반으로 구축되었습니다.

## 📊 데이터 소스 (Data Strategy)

이 프로젝트는 두 가지 데이터 소스를 결합하여 사용합니다.

1.  **실시간 데이터 (Live)**
    *   **Source**: [Disease.sh API](https://disease.sh/docs/)
    *   **용도**: 상단 메트릭 카드 (오늘 확진자, 총 사망자 등 실시간 현황)
    *   **방법**: `data_manager.py`의 `fetch_realtime_api()` 함수가 호출 시점에 API를 타격합니다.

2.  **과거 데이터 (Historical)**
    *   **Source**: [OWID COVID-19 Data (GitHub)](https://github.com/owid/covid-19-data)
    *   **용도**: 시계열 그래프 분석 (추세, 백신 접종률 등)
    *   **방법**: 
        *   최초 실행 시 `data_manager.py`가 OWID의 `csv` 파일을 `data/` 폴더로 다운로드합니다.
        *   이후에는 로컬 캐시 파일을 사용하여 속도를 높입니다.
        *   **주의**: 파일 크기가 크므로 Git에는 포함되지 않습니다 (`.gitignore` 처리됨).

---

## 🎨 Hynex Design System

이번 업데이트를 통해 프로젝트에 일관된 UI/UX를 위한 **Hynex Design System**이 적용되었습니다.
별도의 CSS 작업 없이도 아름다운 대시보드를 만들 수 있도록 `style.py` 모듈과 가이드 페이지를 제공합니다.

### 1. 디자인 철학 (Core Values)
*   **Modern Dark UI**: 눈의 피로를 줄이고 데이터에 집중할 수 있는 다크 모드 기반입니다.
*   **Semantic Colors**: 색상만으로도 데이터의 의미(긍정/부정/정보)를 파악할 수 있습니다.
*   **Compact Sidebar**: 콘텐츠 영역을 극대화하기 위해 50px 너비의 '아이콘 사이드바'를 사용합니다.

### 2. 사용 방법 (How to Use)
모든 페이지에서 `style.py`를 임포트하여 일관된 스타일을 적용하세요.

```python
import style

# 1. 스타일 적용 (페이지 최상단, st.set_page_config 이후)
style.apply_hynex_style()

# 2. 색상 사용 (하드코딩 대신 변수 사용 권장)
st.markdown(f"<h1 style='color: {style.COLORS['primary']}'>Hello World</h1>", unsafe_allow_html=True)
```

### 3. 컬러 팔레트 (Color Palette)
| Key | Color | Role | 사용 예시 |
|---|---|---|---|
| `primary` | `#7B61FF` (Purple) | **Main Identity** | 강조 텍스트, 확진자 그래프 |
| `success` | `#05CD99` (Mint) | **Positive** | 완치자, 백신 접종률, 상승세 |
| `danger` | `#FF5B5B` (Red) | **Negative/Risk** | 사망자, 경고 배지, 하락세 |
| `warning` | `#FFB547` (Orange) | **Caution** | 위중증 환자, 주의 사항 |
| `text_sub`| `#A3AED0` (Gray) | **Description** | 보조 설명, 라벨 |

### 4. 디자인 가이드 페이지 (Design Guide)
UI 컴포넌트(배지, 카드, 차트 등)의 소스 코드가 필요하신가요?
앱 실행 후 사이드바의 **팔레트 아이콘(🎨)**을 클릭하여 **Design Guide** 페이지로 이동하세요.
*   원하는 컴포넌트의 코드를 **'Copy Code'** 버튼으로 복사하여 바로 사용할 수 있습니다.

---

## 🚀 개발 환경 설정 (Setup Guide)

모든 팀원은 **Docker**를 사용하여 동일한 환경에서 개발합니다.

### 사전 준비물
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치 및 실행

### 1. 프로젝트 실행 (Windows & Mac 공통)
터미널에서 프로젝트 폴더로 이동 후 아래 명령어를 입력하세요.

```bash
# 이미지 빌드 및 컨테이너 실행
docker-compose up --build
```

실행이 완료되면 브라우저에서 아래 주소로 접속합니다:
👉 **http://localhost:8501**

### 2. 개발 작업 가이드
*   **코드 수정**: 로컬의 `app.py` 등을 수정하고 저장하면, 웹페이지에서 'Rerun' 버튼을 눌러 즉시 변경 사항을 확인할 수 있습니다. (Volume 연결됨)
*   **라이브러리 추가**: `requirements.txt`에 패키지를 추가한 경우, 반드시 `docker-compose up --build`를 다시 실행해야 적용됩니다.

### 3. 데이터 초기화 문제 해결
앱 최초 실행 시 OWID 데이터를 다운로드하느라 약 **1~2분 정도 로딩**이 걸릴 수 있습니다.
만약 다운로드가 실패한다면 다음 명령어로 로그를 확인하세요.

```bash
docker-compose logs -f
```

---

## 📂 프로젝트 구조

```text
Streamlit/
├── app.py              # 메인 대시보드 UI
├── data_manager.py     # 데이터 수집 및 전처리 모듈 (API/CSV 처리)
├── style.py            # Hynex 디자인 시스템 모듈 (New)
├── pages/              # 추가 페이지 디렉토리
│   └── design_guide.py # 디자인 시스템 가이드 페이지
├── .streamlit/         # Streamlit 설정 (테마 등)
├── Dockerfile          # Docker 이미지 빌드 설정
├── docker-compose.yml  # 컨테이너 오케스트레이션 설정
├── requirements.txt    # 파이썬 의존성 목록
└── data/               # 데이터 저장소 (Docker Volume으로 관리됨)
```

## ⚠️ Git 커밋 시 주의사항
*   `data/` 폴더 내의 CSV 파일은 용량이 크므로 커밋하지 않습니다 (`.gitignore`에 자동 포함).
*   API Key 등 민감 정보가 필요해질 경우 `.env` 파일을 활용하세요 (현재는 Open API라 불필요).