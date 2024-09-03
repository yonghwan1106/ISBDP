import streamlit as st
from sub01 import show_realtime_safety_map
from sub02 import show_accident_prediction
from sub03 import show_safety_performance_dashboard
from sub04 import show_worker_movement_analysis
from sub05 import show_equipment_status_dashboard
from sub06 import show_environmental_data_visualization
from sub07 import show_safety_compliance_dashboard
from sub08 import show_emergency_response_simulator
from sub09 import show_ppe_monitoring_dashboard
from sub10 import show_safety_training_effectiveness

def main():
    st.set_page_config(page_title="산업단지 안전 빅데이터 플랫폼", page_icon="🏭", layout="wide")
    
    st.title("산업단지 안전 빅데이터 플랫폼 (ISBDP)")

    # 사이드바에 기능 선택 메뉴 추가
    menu = [
        "실시간 안전 지도",
        "사고 예측 시뮬레이션",
        "안전 성과 대시보드",
        "작업자 동선 분석",
        "설비 상태 모니터링",
        "환경 데이터 시각화",
        "안전 규정 준수율 대시보드",
        "비상 대응 시뮬레이터",
        "PPE 착용 현황 모니터링",
        "안전 교육 효과성 분석"
    ]
    
    choice = st.sidebar.selectbox("기능 선택", menu)

    # 선택된 기능에 따라 해당 모듈의 함수 호출
    if choice == "실시간 안전 지도":
        show_realtime_safety_map()
    elif choice == "사고 예측 시뮬레이션":
        show_accident_prediction()
    elif choice == "안전 성과 대시보드":
        show_safety_performance_dashboard()
    elif choice == "작업자 동선 분석":
        show_worker_movement_analysis()
    elif choice == "설비 상태 모니터링":
        show_equipment_status_dashboard()
    elif choice == "환경 데이터 시각화":
        show_environmental_data_visualization()
    elif choice == "안전 규정 준수율 대시보드":
        show_safety_compliance_dashboard()
    elif choice == "비상 대응 시뮬레이터":
        show_emergency_response_simulator()
    elif choice == "PPE 착용 현황 모니터링":
        show_ppe_monitoring_dashboard()
    elif choice == "안전 교육 효과성 분석":
        show_safety_training_effectiveness()

    # 푸터 추가
    st.sidebar.markdown("---")
    st.sidebar.info("© 2024 산업단지 안전 빅데이터 플랫폼 (ISBDP). All rights reserved.")

if __name__ == "__main__":
    main()