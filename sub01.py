import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import random

def generate_safety_data(num_points=20):
    """가상의 안전 데이터를 생성하는 함수"""
    data = []
    for _ in range(num_points):
        lat = random.uniform(35.5, 35.7)  # 대한민국 중부 위도 범위
        lon = random.uniform(128.5, 128.7)  # 대한민국 동부 경도 범위
        safety_level = random.choice(['안전', '주의', '위험'])
        data.append({'lat': lat, 'lon': lon, 'safety_level': safety_level})
    return pd.DataFrame(data)

def get_color(safety_level):
    """안전 수준에 따른 색상 반환"""
    if safety_level == '안전':
        return 'green'
    elif safety_level == '주의':
        return 'orange'
    else:
        return 'red'

def show_realtime_safety_map():
    st.subheader("실시간 안전 지도")

    # 가상의 안전 데이터 생성
    df = generate_safety_data()

    # 지도 생성 (중심점은 데이터의 평균 위치)
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=12)

    # 데이터포인트를 지도에 추가
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=10,
            popup=row['safety_level'],
            color=get_color(row['safety_level']),
            fill=True,
            fillColor=get_color(row['safety_level'])
        ).add_to(m)

    # Streamlit에 지도 표시
    folium_static(m)

    # 데이터 테이블 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(df)

if __name__ == "__main__":
    show_realtime_safety_map()