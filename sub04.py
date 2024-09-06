import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_worker_movement_data(num_workers=5, num_points=100):
    """가상의 작업자 동선 데이터를 생성하는 함수"""
    data = []
    for worker in range(num_workers):
        lat, lon, alt = 35.6 + np.random.random() * 0.1, 128.5 + np.random.random() * 0.1, 0
        for i in range(num_points):
            lat += np.random.normal(0, 0.0001)
            lon += np.random.normal(0, 0.0001)
            alt = max(0, alt + np.random.normal(0, 0.5))
            timestamp = (datetime.now() + timedelta(minutes=i*5)).isoformat()
            data.append({
                'worker_id': f'Worker {worker+1}',
                'timestamp': timestamp,
                'latitude': float(lat),
                'longitude': float(lon),
                'altitude': float(alt)
            })
    return pd.DataFrame(data)

def create_pydeck_chart(df):
    """PyDeck을 사용하여 3D 동선 차트를 생성하는 함수"""
    worker_colors = {worker: [int(r), int(g), 0] for worker, (r, g) in 
                     zip(df['worker_id'].unique(), np.random.randint(0, 255, size=(len(df['worker_id'].unique()), 2)))}
    df['color'] = df['worker_id'].map(worker_colors)

    layer = pdk.Layer(
        "PathLayer",
        df.to_dict('records'),
        get_path=["longitude", "latitude", "altitude"],
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

    df = generate_worker_movement_data()
    chart = create_pydeck_chart(df)
    st.pydeck_chart(chart)

    selected_worker = st.selectbox("작업자 선택", df['worker_id'].unique())
    filtered_df = df[df['worker_id'] == selected_worker]

    distances = np.sqrt(
        np.diff(filtered_df['latitude'])**2 + 
        np.diff(filtered_df['longitude'])**2 +
        np.diff(filtered_df['altitude'])**2
    )
    total_distance = float(np.sum(distances) * 111000)  # Convert to float

    st.metric(f"{selected_worker}의 총 이동 거리", f"{total_distance:.2f} 미터")

    st.subheader(f"{selected_worker}의 시간대별 고도 변화")
    chart_data = pd.DataFrame({
        'timestamp': pd.to_datetime(filtered_df['timestamp']),
        'altitude': filtered_df['altitude']
    }).set_index('timestamp')
    st.line_chart(chart_data)

    if st.checkbox("원본 데이터 보기"):
        st.write(filtered_df)

if __name__ == "__main__":
    show_worker_movement_analysis()
