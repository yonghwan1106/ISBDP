import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def generate_ppe_data(num_workers=100, num_days=30):
    """가상의 PPE 착용 데이터를 생성하는 함수"""
    ppe_types = ['안전모', '안전화', '보안경', '장갑', '마스크']
    departments = ['생산부', '정비부', '품질관리부', '연구개발부', '물류부']
    
    data = []
    for _ in range(num_workers):
        worker_id = f'W{np.random.randint(1000, 9999)}'
        department = np.random.choice(departments)
        for day in range(num_days):
            date = datetime.now().date() - timedelta(days=num_days-day-1)
            for ppe in ppe_types:
                wearing = np.random.choice([True, False], p=[0.95, 0.05])  # 95% 확률로 착용
                data.append({
                    'Date': date,
                    'Worker_ID': worker_id,
                    'Department': department,
                    'PPE_Type': ppe,
                    'Wearing': wearing
                })
    
    return pd.DataFrame(data)

def show_ppe_monitoring_dashboard():
    st.subheader("PPE 착용 현황 모니터링 대시보드")

    # 데이터 생성
    df = generate_ppe_data()

    # 최신 날짜의 데이터만 선택
    latest_date = df['Date'].max()
    latest_df = df[df['Date'] == latest_date]

    # 전체 PPE 착용률 계산
    overall_compliance = latest_df['Wearing'].mean() * 100

    # 메트릭 표시
    st.metric("전체 PPE 착용률", f"{overall_compliance:.2f}%")

    # PPE 종류별 착용률
    st.subheader("PPE 종류별 착용률")
    ppe_compliance = latest_df.groupby('PPE_Type')['Wearing'].mean().sort_values(ascending=False)
    fig_ppe = px.bar(x=ppe_compliance.index, y=ppe_compliance.values * 100,
                     labels={'x': 'PPE 종류', 'y': '착용률 (%)'},
                     title='PPE 종류별 착용률')
    fig_ppe.update_traces(text=[f'{val:.1f}%' for val in ppe_compliance.values * 100], textposition='outside')
    st.plotly_chart(fig_ppe, use_container_width=True)

    # 부서별 PPE 착용률
    st.subheader("부서별 PPE 착용률")
    dept_compliance = latest_df.groupby('Department')['Wearing'].mean().sort_values(ascending=False)
    fig_dept = px.bar(x=dept_compliance.index, y=dept_compliance.values * 100,
                      labels={'x': '부서', 'y': '착용률 (%)'},
                      title='부서별 PPE 착용률')
    fig_dept.update_traces(text=[f'{val:.1f}%' for val in dept_compliance.values * 100], textposition='outside')
    st.plotly_chart(fig_dept, use_container_width=True)

    # 시간에 따른 PPE 착용률 변화
    st.subheader("시간에 따른 PPE 착용률 변화")
    daily_compliance = df.groupby('Date')['Wearing'].mean()
    fig_trend = px.line(x=daily_compliance.index, y=daily_compliance.values * 100,
                        labels={'x': '날짜', 'y': '착용률 (%)'},
                        title='일별 PPE 착용률 추이')
    st.plotly_chart(fig_trend, use_container_width=True)

    # PPE 미착용 근로자 목록
    st.subheader("PPE 미착용 근로자 목록")
    non_compliant = latest_df[latest_df['Wearing'] == False].groupby(['Worker_ID', 'Department', 'PPE_Type']).size().reset_index(name='Count')
    if not non_compliant.empty:
        st.write(non_compliant)
    else:
        st.write("모든 근로자가 PPE를 착용하고 있습니다.")

    # PPE 착용 현황 히트맵
    st.subheader("PPE 착용 현황 히트맵")
    heatmap_data = latest_df.pivot_table(values='Wearing', index='Department', columns='PPE_Type', aggfunc='mean')
    fig_heatmap = go.Figure(data=go.Heatmap(
                   z=heatmap_data.values * 100,
                   x=heatmap_data.columns,
                   y=heatmap_data.index,
                   colorscale='Viridis'))
    fig_heatmap.update_layout(title='부서별 PPE 종류 착용률 (%)', 
                              xaxis_title='PPE 종류', 
                              yaxis_title='부서')
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # 원본 데이터 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(df)

if __name__ == "__main__":
    show_ppe_monitoring_dashboard()