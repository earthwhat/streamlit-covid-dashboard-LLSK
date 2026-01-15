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
├── Dockerfile          # Docker 이미지 빌드 설정
├── docker-compose.yml  # 컨테이너 오케스트레이션 설정
├── requirements.txt    # 파이썬 의존성 목록
└── data/               # 데이터 저장소 (Docker Volume으로 관리됨)
```

## ⚠️ Git 커밋 시 주의사항
*   `data/` 폴더 내의 CSV 파일은 용량이 크므로 커밋하지 않습니다 (`.gitignore`에 자동 포함).
*   API Key 등 민감 정보가 필요해질 경우 `.env` 파일을 활용하세요 (현재는 Open API라 불필요).
