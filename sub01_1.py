import streamlit as st
import pydeck as pdk
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
        return [0, 255, 0, 160]
    elif safety_level == '주의':
        return [255, 165, 0, 160]
    else:
        return [255, 0, 0, 160]

def show_realtime_safety_map():
    st.subheader("실시간 안전 지도")

    # 가상의 안전 데이터 생성
    df = generate_safety_data()
    
    # 색상 데이터 추가
    df['color'] = df['safety_level'].apply(get_color)

    # pydeck 레이어 생성
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=['lon', 'lat'],
        get_color='color',
        get_radius=300,
        pickable=True
    )

    # 뷰 상태 설정
    view_state = pdk.ViewState(
        latitude=df['lat'].mean(),
        longitude=df['lon'].mean(),
        zoom=10,
        pitch=0
    )

    # pydeck 차트 생성
    chart = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{safety_level}"}
    )

    # Streamlit에 차트 표시
    st.pydeck_chart(chart)

    # 데이터 테이블 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(df)

if __name__ == "__main__":
    show_realtime_safety_map()
