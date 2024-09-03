import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_risk_data(num_days=30, num_locations=5):
    """가상의 위험도 데이터를 생성하는 함수"""
    locations = [f'Location {i+1}' for i in range(num_locations)]
    dates = [datetime.now().date() + timedelta(days=i) for i in range(num_days)]
    
    data = []
    for location in locations:
        base_risk = np.random.uniform(20, 80)
        for date in dates:
            risk = base_risk + np.random.normal(0, 10)
            risk = max(0, min(100, risk))  # 위험도를 0-100 범위로 제한
            data.append({'Date': date, 'Location': location, 'Risk': risk})
    
    return pd.DataFrame(data)

def create_animation(df):
    """애니메이션 그래프를 생성하는 함수"""
    fig = go.Figure()

    for location in df['Location'].unique():
        location_data = df[df['Location'] == location]
        fig.add_trace(go.Scatter(
            x=location_data['Date'],
            y=location_data['Risk'],
            name=location,
            mode='lines+markers'
        ))

    fig.update_layout(
        title='시간에 따른 위험도 변화 예측',
        xaxis_title='날짜',
        yaxis_title='위험도',
        yaxis=dict(range=[0, 100])
    )

    fig.update_traces(line=dict(width=2))

    # 애니메이션 설정
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                buttons=[dict(label="재생",
                              method="animate",
                              args=[None, {"frame": {"duration": 100, "redraw": True},
                                           "fromcurrent": True}]),
                         dict(label="일시정지",
                              method="animate",
                              args=[[None], {"frame": {"duration": 0, "redraw": True},
                                             "mode": "immediate",
                                             "transition": {"duration": 0}}])]
            )
        ]
    )

    # 프레임 생성
    frames = [go.Frame(data=[go.Scatter(x=df[df['Date'] <= date]['Date'],
                                        y=df[df['Date'] <= date]['Risk'],
                                        mode='lines+markers')
                             for location in df['Location'].unique()],
                       name=str(date))
              for date in df['Date'].unique()]
    fig.frames = frames

    return fig

def show_accident_prediction():
    st.subheader("사고 예측 시뮬레이션")

    # 데이터 생성
    df = generate_risk_data()

    # 애니메이션 그래프 생성
    fig = create_animation(df)

    # Streamlit에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 테이블 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(df)

if __name__ == "__main__":
    show_accident_prediction()