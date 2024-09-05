
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

def generate_accident_data(days=365):
    """가상의 사고 데이터 생성"""
    dates = [datetime.now().date() - timedelta(days=i) for i in range(days)]
    accidents = np.random.poisson(lam=2, size=days)  # 평균 2건의 사고가 발생한다고 가정
    return pd.DataFrame({'date': dates, 'accidents': accidents})

def predict_accidents(data, future_days=30):
    """간단한 예측 모델"""
    # 이동 평균을 사용한 간단한 예측
    window = 7
    rolling_mean = data['accidents'].rolling(window=window).mean()
    last_mean = rolling_mean.iloc[-1]
    
    future_dates = [data['date'].iloc[-1] + timedelta(days=i+1) for i in range(future_days)]
    future_accidents = [max(0, int(np.random.normal(last_mean, 1))) for _ in range(future_days)]
    
    return pd.DataFrame({'date': future_dates, 'predicted_accidents': future_accidents})

def show_accident_prediction():
    st.subheader("사고 예측 시뮬레이션")

    # 과거 데이터 생성
    data = generate_accident_data()

    # 미래 예측
    future_data = predict_accidents(data)

    # 데이터 시각화
    fig = go.Figure()

    # 과거 데이터
    fig.add_trace(go.Scatter(
        x=data['date'], 
        y=data['accidents'],
        mode='lines+markers',
        name='과거 사고 데이터'
    ))

    # 예측 데이터
    fig.add_trace(go.Scatter(
        x=future_data['date'], 
        y=future_data['predicted_accidents'],
        mode='lines+markers',
        name='예측 사고 데이터',
        line=dict(dash='dash')
    ))

    fig.update_layout(
        title='사고 발생 추이 및 예측',
        xaxis_title='날짜',
        yaxis_title='사고 건수',
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # 예측 결과 요약
    avg_predicted = future_data['predicted_accidents'].mean()
    st.write(f"향후 30일 동안 예상되는 일일 평균 사고 건수: {avg_predicted:.2f}")

    # 주의사항
    st.warning("이 예측은 가상의 데이터를 바탕으로 한 간단한 시뮬레이션입니다. 실제 상황에서는 더 복잡한 모델과 실제 데이터가 필요합니다.")

if __name__ == "__main__":
    show_accident_prediction()
