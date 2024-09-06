
import streamlit as st
import importlib

def import_module(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

# 모듈 임포트
sub01 = import_module('sub01')
sub02 = import_module('sub02')
sub03 = import_module('sub03')
sub04 = import_module('sub04')
sub05 = import_module('sub05')
sub06 = import_module('sub06')
sub07 = import_module('sub07')
sub08 = import_module('sub08')
sub09 = import_module('sub09')
sub10 = import_module('sub10')

def main():
    st.set_page_config(page_title="산업단지 안전 빅데이터 플랫폼", page_icon="🏭", layout="wide")
    
    st.title("📋 산업단지 안전 빅데이터 플랫폼 (ISBDP)")

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

    modules = [sub01, sub02, sub03, sub04, sub05, sub06, sub07, sub08, sub09, sub10]
    functions = ['show_realtime_safety_map', 'show_accident_prediction', 'show_safety_performance_dashboard',
                 'show_worker_movement_analysis', 'show_equipment_status_dashboard', 'show_environmental_data_visualization',
                 'show_safety_compliance_dashboard', 'show_emergency_response_simulator', 'show_ppe_monitoring_dashboard',
                 'show_safety_training_effectiveness']

    for i, module in enumerate(modules):
        if choice == menu[i]:
            if module is not None and hasattr(module, functions[i]):
                getattr(module, functions[i])()
            else:
                st.warning(f"'{choice}' 기능은 아직 구현되지 않았습니다.")

    st.sidebar.markdown("---")
    st.sidebar.info("© 2024 산업단지 안전 빅데이터 플랫폼 (ISBDP: Industrial Safety Big Data Platform). All rights reserved.")

if __name__ == "__main__":
    main()
