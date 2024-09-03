import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

def generate_safety_training_data(num_departments=20, num_months=12):
    """가상의 안전 교육 및 사고 데이터를 생성하는 함수"""
    np.random.seed(42)  # 재현 가능성을 위한 시드 설정
    
    data = []
    for i in range(num_departments):
        dept_name = f'부서 {i+1}'
        base_training_hours = np.random.uniform(10, 50)
        base_accident_rate = np.random.uniform(5, 20)
        
        for month in range(num_months):
            training_hours = max(0, base_training_hours + np.random.normal(0, 5))
            accident_rate = max(0, base_accident_rate - 0.2 * training_hours + np.random.normal(0, 2))
            
            data.append({
                'Department': dept_name,
                'Month': month + 1,
                'Training_Hours': round(training_hours, 2),
                'Accident_Rate': round(accident_rate, 2)
            })
    
    return pd.DataFrame(data)

def calculate_correlation(df):
    """교육 시간과 사고율 간의 상관관계를 계산하는 함수"""
    correlation, p_value = stats.pearsonr(df['Training_Hours'], df['Accident_Rate'])
    return correlation, p_value

def show_safety_training_effectiveness():
    st.subheader("안전 교육 효과성 분석 도구")

    # 데이터 생성
    df = generate_safety_training_data()

    # 전체 상관관계 계산
    correlation, p_value = calculate_correlation(df)

    # 상관관계 결과 표시
    st.write(f"전체 상관계수: {correlation:.4f}")
    st.write(f"p-값: {p_value:.4f}")

    # 해석 추가
    if p_value < 0.05:
        if correlation < 0:
            st.write("안전 교육 시간과 사고율 사이에 통계적으로 유의미한 음의 상관관계가 있습니다.")
        else:
            st.write("안전 교육 시간과 사고율 사이에 통계적으로 유의미한 양의 상관관계가 있습니다.")
    else:
        st.write("안전 교육 시간과 사고율 사이에 통계적으로 유의미한 상관관계가 없습니다.")

    # 산점도 그래프
    st.subheader("교육 시간과 사고율의 상관관계")
    fig = px.scatter(df, x='Training_Hours', y='Accident_Rate', 
                     color='Department', hover_data=['Month'],
                     labels={'Training_Hours': '교육 시간 (시간)', 
                             'Accident_Rate': '사고율 (%)'},
                     title='교육 시간 vs 사고율')
    
    # 추세선 추가
    fig.add_trace(go.Scatter(x=df['Training_Hours'], y=np.poly1d(np.polyfit(df['Training_Hours'], df['Accident_Rate'], 1))(df['Training_Hours']),
                             mode='lines', name='추세선'))
    
    st.plotly_chart(fig, use_container_width=True)

    # 부서별 평균 교육 시간과 사고율
    st.subheader("부서별 평균 교육 시간과 사고율")
    dept_avg = df.groupby('Department').agg({
        'Training_Hours': 'mean',
        'Accident_Rate': 'mean'
    }).reset_index()

    fig_dept = px.scatter(dept_avg, x='Training_Hours', y='Accident_Rate', 
                          text='Department', 
                          labels={'Training_Hours': '평균 교육 시간 (시간)', 
                                  'Accident_Rate': '평균 사고율 (%)'},
                          title='부서별 평균 교육 시간 vs 평균 사고율')
    fig_dept.update_traces(textposition='top center')
    st.plotly_chart(fig_dept, use_container_width=True)

    # 시간에 따른 교육 시간과 사고율 변화
    st.subheader("시간에 따른 교육 시간과 사고율 변화")
    time_trend = df.groupby('Month').agg({
        'Training_Hours': 'mean',
        'Accident_Rate': 'mean'
    }).reset_index()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=time_trend['Month'], y=time_trend['Training_Hours'],
                                   mode='lines+markers', name='평균 교육 시간'))
    fig_trend.add_trace(go.Scatter(x=time_trend['Month'], y=time_trend['Accident_Rate'],
                                   mode='lines+markers', name='평균 사고율', yaxis='y2'))
    fig_trend.update_layout(title='월별 평균 교육 시간과 사고율 추이',
                            xaxis_title='월',
                            yaxis_title='평균 교육 시간 (시간)',
                            yaxis2=dict(title='평균 사고율 (%)', overlaying='y', side='right'))
    st.plotly_chart(fig_trend, use_container_width=True)

    # 원본 데이터 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(df)

if __name__ == "__main__":
    show_safety_training_effectiveness()