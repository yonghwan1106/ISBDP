import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def generate_safety_performance_data(num_days=30, num_departments=5):
    """가상의 안전 성과 데이터를 생성하는 함수"""
    departments = [f'부서 {i+1}' for i in range(num_departments)]
    dates = [datetime.now().date() - timedelta(days=i) for i in range(num_days)]
    
    data = []
    for dept in departments:
        incident_rate = np.random.uniform(0, 5)
        compliance_rate = np.random.uniform(80, 100)
        for date in dates:
            incidents = max(0, int(np.random.normal(incident_rate, 1)))
            compliance = min(100, max(0, compliance_rate + np.random.normal(0, 2)))
            data.append({
                'Date': date,
                'Department': dept,
                'Incidents': incidents,
                'Compliance_Rate': compliance,
                'Training_Hours': np.random.randint(0, 8)
            })
    
    return pd.DataFrame(data)

def show_safety_performance_dashboard():
    st.subheader("안전 성과 대시보드")

    # 데이터 생성
    df = generate_safety_performance_data()

    # 전체 통계
    total_incidents = df['Incidents'].sum()
    avg_compliance = df['Compliance_Rate'].mean()
    total_training_hours = df['Training_Hours'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("총 사고 건수", f"{total_incidents}건")
    col2.metric("평균 규정 준수율", f"{avg_compliance:.2f}%")
    col3.metric("총 교육 시간", f"{total_training_hours}시간")

    # 부서별 사고 건수 (Streamlit 내장 차트)
    st.subheader("부서별 사고 건수")
    dept_incidents = df.groupby('Department')['Incidents'].sum().sort_values(ascending=False)
    st.bar_chart(dept_incidents)

    # 시간에 따른 규정 준수율 변화 (Plotly 라인 차트)
    st.subheader("시간에 따른 규정 준수율 변화")
    fig_compliance = px.line(df, x='Date', y='Compliance_Rate', color='Department',
                             title='부서별 규정 준수율 추이')
    st.plotly_chart(fig_compliance)

    # 교육 시간과 사고 건수의 상관관계 (Plotly 산점도)
    st.subheader("교육 시간과 사고 건수의 상관관계")
    df_corr = df.groupby('Department').agg({
        'Training_Hours': 'sum',
        'Incidents': 'sum'
    }).reset_index()
    fig_correlation = px.scatter(df_corr, x='Training_Hours', y='Incidents', 
                                 text='Department', title='교육 시간 vs 사고 건수')
    fig_correlation.update_traces(textposition='top center')
    st.plotly_chart(fig_correlation)

    # 부서별 안전 성과 히트맵 (Plotly 히트맵)
    st.subheader("부서별 안전 성과 히트맵")
    df_heatmap = df.pivot_table(index='Department', columns='Date', values='Incidents', aggfunc='sum')
    fig_heatmap = go.Figure(data=go.Heatmap(
                   z=df_heatmap.values,
                   x=df_heatmap.columns,
                   y=df_heatmap.index,
                   colorscale='Viridis'))
    fig_heatmap.update_layout(title='부서별 일일 사고 발생 현황', 
                              xaxis_title='날짜', 
                              yaxis_title='부서')
    st.plotly_chart(fig_heatmap)

    # 원본 데이터 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(df)

if __name__ == "__main__":
    show_safety_performance_dashboard()