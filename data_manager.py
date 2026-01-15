import pandas as pd
import requests
import os
from datetime import datetime

# 데이터 저장 경로
DATA_DIR = "data"
OWID_FILE = os.path.join(DATA_DIR, "owid-covid-data.csv")
OWID_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def download_owid_data():
    """OWID Github에서 대용량 CSV 데이터를 다운로드합니다."""
    ensure_data_dir()
    print("Downloading OWID data... (This may take a while)")
    try:
        response = requests.get(OWID_URL, stream=True)
        response.raise_for_status()
        with open(OWID_FILE, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Download complete: {OWID_FILE}")
        return True
    except Exception as e:
        print(f"Error downloading data: {e}")
        return False

def load_history_data(country_code="KOR"):
    """
    로컬에 저장된 OWID CSV 파일을 읽어옵니다.
    파일이 없으면 다운로드를 시도합니다.
    """
    ensure_data_dir()
    
    if not os.path.exists(OWID_FILE):
        success = download_owid_data()
        if not success:
            return pd.DataFrame() # 빈 데이터프레임 반환

    try:
        # 전체를 다 읽으면 느리므로, 필요한 컬럼만 읽거나 로딩 후 필터링
        # (최적화를 위해 전체 로딩 후 필터링 방식을 사용하되, 캐싱은 app.py에서 처리)
        df = pd.read_csv(OWID_FILE)
        df['date'] = pd.to_datetime(df['date'])
        
        # 특정 국가 필터링 (기본: 대한민국 iso_code='KOR')
        if country_code:
            df = df[df['iso_code'] == country_code]
            
        return df.sort_values('date')
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return pd.DataFrame()

def fetch_realtime_api(country="South Korea"):
    """
    Disease.sh API를 통해 실시간 데이터를 가져옵니다.
    """
    api_url = f"https://disease.sh/v3/covid-19/countries/{country}?strict=true"
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"API Connection Error: {e}")
    return None
