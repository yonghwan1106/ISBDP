import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def generate_compliance_data(num_departments=10, num_rules=15):
    """가상의 안전 규정 준수 데이터를 생성하는 함수"""
    departments = [f'부서 {i+1}' for i in range(num_departments)]
    rules = [f'규정 {i+1}' for i in range(num_rules)]
    
    data = []
    for dept in departments:
        for rule in rules:
            compliance = np.random.choice([0, 1], p=[0.1, 0.9])  # 90% 확률로 준수
            data.append({
                'Department': dept,
                'Rule': rule,
                'Compliance': compliance,
                'LastChecked': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(0, 30))
            })
    
    return pd.DataFrame(data)

def create_compliance_bar_chart(df):
    """부서별 준수율 막대 그래프를 생성하는 함수"""
    dept_compliance = df.groupby('Department')['Compliance'].mean().sort_values(ascending=False)
    fig = go.Figure(data=[
        go.Bar(x=dept_compliance.index, y=dept_compliance.values * 100,
               text=[f'{val:.1f}%' for val in dept_compliance.values * 100],
               textposition='auto')
    ])
    fig.update_layout(title='부서별 안전 규정 준수율',
                      xaxis_title='부서',
                      yaxis_title='준수율 (%)',
                      yaxis=dict(range=[0, 100]))
    return fig

def show_safety_compliance_dashboard():
    st.subheader("안전 규정 준수율 대시보드")

    # 데이터 생성
    df = generate_compliance_data()

    # 전체 준수율 계산
    overall_compliance = df['Compliance'].mean() * 100
    st.metric("전체 안전 규정 준수율", f"{overall_compliance:.1f}%")

    # 부서별 준수율 막대 그래프
    st.plotly_chart(create_compliance_bar_chart(df), use_container_width=True)

    # 규정별 준수율
    st.subheader("규정별 준수율")
    rule_compliance = df.groupby('Rule')['Compliance'].mean().sort_values(ascending=False)
    fig = px.bar(x=rule_compliance.index, y=rule_compliance.values * 100,
                 labels={'x': '규정', 'y': '준수율 (%)'},
                 title='규정별 준수율')
    fig.update_traces(text=[f'{val:.1f}%' for val in rule_compliance.values * 100], textposition='outside')
    fig.update_layout(yaxis=dict(range=[0, 100]))
    st.plotly_chart(fig, use_container_width=True)

    # 부서 선택
    selected_dept = st.selectbox("부서 선택", df['Department'].unique())

    # 선택된 부서의 규정 준수 현황
    st.subheader(f"{selected_dept} 규정 준수 현황")
    dept_data = df[df['Department'] == selected_dept]
    fig = go.Figure(data=[
        go.Table(
            header=dict(values=['규정', '준수 여부', '마지막 점검일'],
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[dept_data['Rule'], 
                               dept_data['Compliance'].map({1: '준수', 0: '미준수'}),
                               dept_data['LastChecked'].dt.strftime('%Y-%m-%d')],
                       fill_color=['white', 
                                   dept_data['Compliance'].map({1: 'lightgreen', 0: 'lightsalmon'})],
                       align='left'))
    ])
    st.plotly_chart(fig, use_container_width=True)

    # 미준수 항목 분석
    st.subheader("미준수 항목 분석")
    non_compliance = df[df['Compliance'] == 0].groupby('Rule').size().sort_values(ascending=False)
    if not non_compliance.empty:
        fig = px.bar(x=non_compliance.index, y=non_compliance.values,
                     labels={'x': '규정', 'y': '미준수 횟수'},
                     title='가장 많이 미준수된 규정')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("모든 규정이 준수되었습니다.")

    # 원본 데이터 표시 (옵션)
    if st.checkbox("원본 데이터 보기"):
        st.write(df)

if __name__ == "__main__":
    show_safety_compliance_dashboard()