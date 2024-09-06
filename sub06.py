import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_environmental_data(num_points=400):
    """가상의 환경 데이터를 생성하는 함수"""
    x = np.linspace(0, 100, 20)
    y = np.linspace(0, 100, 20)
    x, y = np.meshgrid(x, y)
    
    data = []
    temperature = 20 + 5 * np.sin(x/10) + 5 * np.cos(y/10) + np.random.rand(20, 20)
    humidity = 50 + 20 * np.sin(x/15) + 20 * np.cos(y/15) + np.random.rand(20, 20)
    co2 = 400 + 50 * np.sin(x/20) + 50 * np.cos(y/20) + np.random.rand(20, 20)
    
    for i in range(20):
        for j in range(20):
            data.append({
                'x': x[i, j],
                'y': y[i, j],
                'Temperature': temperature[i, j],
                'Humidity': humidity[i, j],
                'CO2': co2[i, j]
            })
    
    return pd.DataFrame(data)

def create_3d_surface(df, z_column, title):
    """3D 표면 그래프를 생성하는 함수"""
    try:
        z_data = df[z_column].values.reshape(20, 20)
        fig = go.Figure(data=[go.Surface(z=z_data,
                                         x=df['x'].unique(),
                                         y=df['y'].unique())])
        fig.update_layout(title=title, autosize=False,
                          width=500, height=500,
                          scene=dict(
                              xaxis_title='X',
                              yaxis_title='Y',
                              zaxis_title=z_column
                          ),
                          margin=dict(l=65, r=50, b=65, t=90))
        return fig
    except ValueError as e:
        st.error(f"데이터 형식 오류: {e}")
        return go.Figure()

def show_environmental_data_visualization():
    st.subheader("환경 데이터 시각화")

    # 데이터 생성
    df = generate_environmental_data()

    # 3D 그래프 생성
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_3d_surface(df, 'Temperature', '온도 분포 (°C)'))
    with col2:
        st.plotly_chart(create_3d_surface(df, 'Humidity', '습도 분포 (%)'))

    st.plotly_chart(create_3d_surface(df, 'CO2', 'CO2 농도 분포 (ppm)'), use_container_width=True)

    # 2D 히트맵
    st.subheader("2D 히트맵")
    heatmap_type = st.selectbox("데이터 선택", ['Temperature', 'Humidity', 'CO2'])
    
    fig = go.Figure(data=go.Heatmap(
                    z=df[heatmap_type].values.reshape(20, 20),
                    x=df['x'].unique(),
                    y=df['y'].unique()),
                    )
    fig.update_layout(title=f'{heatmap_type} 히트맵', 
                      xaxis_title='X 좌표', 
                      yaxis_title='Y 좌표')
    st.plotly_chart(fig, use_container_width=True)

    # 상관 관계 분석
    st.subheader("환경 요소 간 상관 관계")
    corr = df[['Temperature', 'Humidity', 'CO2']].corr()
    
    fig = go.Figure(data=go.Heatmap(
                    z=corr.values,
                    x=corr.index,
                    y=corr.columns,
                    colorscale='RdBu',
                    zmin=-1, zmax=1
                    ))
    fig.update_layout(title='상관 관계 히트맵')
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 통계
    st.subheader("데이터 통계")
    st.write(df[['Temperature', 'Humidity', 'CO2']].describe())

    # 원본 데이터 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(df)

if __name__ == "__main__":
    show_environmental_data_visualization()
