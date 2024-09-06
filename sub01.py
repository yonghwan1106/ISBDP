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

def create_safety_map(df):
    """안전 지도를 생성하는 함수"""
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=10)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=10,
            popup=row['safety_level'],
            color=get_color(row['safety_level']),
            fill=True,
            fillColor=get_color(row['safety_level']),
            fillOpacity=0.7
        ).add_to(m)

    return m

def show_realtime_safety_map():
    st.subheader("실시간 안전 지도")

    # 안전 레벨 색상 안내
    st.write("안전 레벨 색상 안내:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.color_picker("안전", "#00FF00", disabled=True)
    
    with col2:
        st.color_picker("주의", "#FFA500", disabled=True)
  
    with col3:
        st.color_picker("위험", "#FF0000", disabled=True)
    

    # 가상의 안전 데이터 생성
    df = generate_safety_data()

    # 지도 생성
    m = create_safety_map(df)

    # Streamlit에 지도 표시
    folium_static(m)

    # 통계 정보 표시
    st.subheader("안전 현황 요약")
    safety_counts = df['safety_level'].value_counts()
    st.write(f"안전: {safety_counts.get('안전', 0)}개 지역")
    st.write(f"주의: {safety_counts.get('주의', 0)}개 지역")
    st.write(f"위험: {safety_counts.get('위험', 0)}개 지역")

    # 데이터 테이블 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(df)

if __name__ == "__main__":
    show_realtime_safety_map()
