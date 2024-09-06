import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_worker_movement_data(num_workers=5, num_points=100):
    """가상의 작업자 동선 데이터를 생성하는 함수"""
    data = []
    for worker in range(num_workers):
        # 작업자의 시작 위치 (위도, 경도, 고도)
        lat, lon, alt = 35.6 + np.random.random() * 0.1, 128.5 + np.random.random() * 0.1, 0
        for i in range(num_points):
            # 시간 경과에 따른 위치 변화
            lat += np.random.normal(0, 0.0001)
            lon += np.random.normal(0, 0.0001)
            alt = max(0, alt + np.random.normal(0, 0.5))  # 고도는 음수가 되지 않도록
            timestamp = datetime.now() + timedelta(minutes=i*5)
            data.append({
                'worker_id': f'Worker {worker+1}',
                'timestamp': timestamp,
                'latitude': lat,
                'longitude': lon,
                'altitude': alt
            })
    return pd.DataFrame(data)

def create_pydeck_chart(df):
    """PyDeck을 사용하여 3D 동선 차트를 생성하는 함수"""
    # 색상 매핑을 미리 계산
    worker_colors = {worker: [r, g, 0] for worker, (r, g) in 
                     zip(df['worker_id'].unique(), np.random.randint(0, 255, size=(len(df['worker_id'].unique()), 2)))}
    df['color'] = df['worker_id'].map(worker_colors)

    layer = pdk.Layer(
        "PathLayer",
        df,
        get_path="[longitude, latitude, altitude]",
        get_color="color",
        width_scale=20,
        width_min_pixels=2,
        get_width=5,
        pickable=True,
        auto_highlight=True
    )

    view_state = pdk.ViewState(
        latitude=df['latitude'].mean(),
        longitude=df['longitude'].mean(),
        zoom=14,
        pitch=45,
        bearing=0
    )

    return pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{worker_id}\nTime: {timestamp}"},
        map_style="mapbox://styles/mapbox/dark-v9"
    )

def show_worker_movement_analysis():
    st.subheader("작업자 동선 분석")

    # 데이터 생성
    df = generate_worker_movement_data()

    # PyDeck 차트 생성
    chart = create_pydeck_chart(df)

    # Streamlit에 차트 표시
    st.pydeck_chart(chart)

    # 작업자 선택 옵션
    selected_worker = st.selectbox("작업자 선택", df['worker_id'].unique())

    # 선택된 작업자의 데이터만 필터링
    filtered_df = df[df['worker_id'] == selected_worker]

    # 선택된 작업자의 이동 거리 계산
    distances = np.sqrt(
        np.diff(filtered_df['latitude'])**2 + 
        np.diff(filtered_df['longitude'])**2 +
        np.diff(filtered_df['altitude'])**2
    )
    total_distance = np.sum(distances) * 111000  # 대략적인 미터 단위 변환

    st.metric(f"{selected_worker}의 총 이동 거리", f"{total_distance:.2f} 미터")

    # 시간대별 고도 변화 그래프
    st.subheader(f"{selected_worker}의 시간대별 고도 변화")
    st.line_chart(filtered_df.set_index('timestamp')['altitude'])

    # 원본 데이터 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(filtered_df)

if __name__ == "__main__":
    show_worker_movement_analysis()
