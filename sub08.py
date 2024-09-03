import streamlit as st
import folium
from streamlit_folium import folium_static
import random
import numpy as np

def generate_emergency_scenarios():
    """비상 상황 시나리오를 생성하는 함수"""
    return {
        "화재": {"위험도": "높음", "대피시간": "5분", "영향범위": "100m"},
        "화학물질 유출": {"위험도": "매우 높음", "대피시간": "즉시", "영향범위": "500m"},
        "지진": {"위험도": "중간", "대피시간": "2분", "영향범위": "전체"},
        "폭발": {"위험도": "높음", "대피시간": "즉시", "영향범위": "200m"},
        "태풍": {"위험도": "중간", "대피시간": "30분", "영향범위": "전체"}
    }

def generate_evacuation_routes(center_lat, center_lon):
    """가상의 대피 경로를 생성하는 함수"""
    routes = []
    for _ in range(3):  # 3개의 대피 경로 생성
        route = []
        current_lat, current_lon = center_lat, center_lon
        for _ in range(5):  # 각 경로는 5개의 지점으로 구성
            current_lat += random.uniform(-0.001, 0.001)
            current_lon += random.uniform(-0.001, 0.001)
            route.append((current_lat, current_lon))
        routes.append(route)
    return routes

def create_emergency_map(center_lat, center_lon, scenario, routes):
    """비상 상황 지도를 생성하는 함수"""
    m = folium.Map(location=[center_lat, center_lon], zoom_start=15)

    # 비상 상황 발생 지점 표시
    folium.Marker(
        [center_lat, center_lon],
        popup=f"비상 상황: {scenario}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    # 대피 경로 표시
    colors = ['blue', 'green', 'purple']
    for route, color in zip(routes, colors):
        folium.PolyLine(
            route,
            weight=5,
            color=color,
            opacity=0.8
        ).add_to(m)

    return m

def show_emergency_response_simulator():
    st.subheader("비상 대응 시뮬레이터")

    # 시나리오 선택
    scenarios = generate_emergency_scenarios()
    selected_scenario = st.selectbox("비상 상황 시나리오 선택", list(scenarios.keys()))

    # 선택된 시나리오 정보 표시
    st.write(f"선택된 시나리오: {selected_scenario}")
    st.write(f"위험도: {scenarios[selected_scenario]['위험도']}")
    st.write(f"권장 대피 시간: {scenarios[selected_scenario]['대피시간']}")
    st.write(f"예상 영향 범위: {scenarios[selected_scenario]['영향범위']}")

    # 가상의 산업단지 중심 좌표 (대한민국 울산의 좌표를 사용)
    center_lat, center_lon = 35.5383773, 129.3113596

    # 대피 경로 생성
    routes = generate_evacuation_routes(center_lat, center_lon)

    # 지도 생성
    m = create_emergency_map(center_lat, center_lon, selected_scenario, routes)

    # 지도 표시
    folium_static(m)

    # 대피 지침
    st.subheader("대피 지침")
    st.markdown("""
    1. 침착하게 행동하세요.
    2. 가장 가까운 비상구를 통해 대피하세요.
    3. 엘리베이터를 사용하지 말고 계단을 이용하세요.
    4. 지정된 대피 장소로 이동하세요.
    5. 안전 요원의 지시를 따르세요.
    """)

    # 비상 연락처
    st.subheader("비상 연락처")
    st.markdown("""
    - 비상 대응팀: 080-1234-5678
    - 소방서: 119
    - 경찰서: 112
    - 병원: 1339
    """)

if __name__ == "__main__":
    show_emergency_response_simulator()