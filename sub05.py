import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

def generate_equipment_data(num_equipment=6):
    """가상의 설비 상태 데이터를 생성하는 함수"""
    equipment_types = ['Pump', 'Compressor', 'Motor', 'Valve', 'Tank', 'Heat Exchanger']
    data = []
    for i in range(num_equipment):
        equipment_type = equipment_types[i % len(equipment_types)]
        temperature = np.random.uniform(50, 80)
        pressure = np.random.uniform(2, 5)
        vibration = np.random.uniform(0, 2)
        efficiency = np.random.uniform(70, 95)
        last_maintenance = datetime.now() - timedelta(days=np.random.randint(0, 365))
        status = np.random.choice(['정상', '주의', '경고'], p=[0.7, 0.2, 0.1])
        data.append({
            'Equipment_ID': f'EQ-{i+1:03d}',
            'Type': equipment_type,
            'Temperature': temperature,
            'Pressure': pressure,
            'Vibration': vibration,
            'Efficiency': efficiency,
            'Last_Maintenance': last_maintenance,
            'Status': status
        })
    return pd.DataFrame(data)

def create_gauge(value, title, min_value, max_value, threshold_values):
    """게이지 차트를 생성하는 함수"""
    color = 'green' if value < threshold_values[0] else 'yellow' if value < threshold_values[1] else 'red'
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        gauge = {
            'axis': {'range': [min_value, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [min_value, threshold_values[0]], 'color': "lightgray"},
                {'range': [threshold_values[0], threshold_values[1]], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold_values[1]
            }
        }
    ))
    fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10))
    return fig

def show_equipment_status_dashboard():
    st.subheader("설비 상태 모니터링 대시보드")

    # 데이터 생성
    df = generate_equipment_data()

    # 설비 선택
    equipment_id = st.selectbox("설비 선택", df['Equipment_ID'])
    equipment_data = df[df['Equipment_ID'] == equipment_id].iloc[0]

    # 설비 정보 표시
    col1, col2, col3 = st.columns(3)
    col1.metric("설비 ID", equipment_data['Equipment_ID'])
    col2.metric("설비 유형", equipment_data['Type'])
    col3.metric("상태", equipment_data['Status'], 
                delta="정상" if equipment_data['Status'] == '정상' else ("주의" if equipment_data['Status'] == '주의' else "경고"),
                delta_color="normal" if equipment_data['Status'] == '정상' else ("off" if equipment_data['Status'] == '주의' else "inverse"))

    # 게이지 차트 생성
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_gauge(equipment_data['Temperature'], '온도 (°C)', 0, 100, [60, 75]), use_container_width=True)
        st.plotly_chart(create_gauge(equipment_data['Pressure'], '압력 (bar)', 0, 10, [3, 6]), use_container_width=True)
    with col2:
        st.plotly_chart(create_gauge(equipment_data['Vibration'], '진동 (mm/s)', 0, 5, [1, 3]), use_container_width=True)
        st.plotly_chart(create_gauge(equipment_data['Efficiency'], '효율 (%)', 0, 100, [80, 90]), use_container_width=True)

    # 마지막 정비 일자 및 다음 정비 예정일
    last_maintenance = equipment_data['Last_Maintenance']
    next_maintenance = last_maintenance + timedelta(days=90)  # 예: 3개월마다 정비
    col1, col2 = st.columns(2)
    col1.metric("마지막 정비 일자", last_maintenance.strftime('%Y-%m-%d'))
    col2.metric("다음 정비 예정일", next_maintenance.strftime('%Y-%m-%d'))

    # 전체 설비 상태 요약
    st.subheader("전체 설비 상태 요약")
    status_summary = df['Status'].value_counts()
    fig_summary = go.Figure(data=[go.Pie(labels=status_summary.index, values=status_summary.values, hole=.3)])
    fig_summary.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_summary, use_container_width=True)

    # 원본 데이터 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(df)

if __name__ == "__main__":
    show_equipment_status_dashboard()