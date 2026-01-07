import sys
import os
import subprocess

# 尝试导入依赖库，如果失败则提示安装
try:
    import streamlit as st
    import pandas as pd
    import altair as alt
    from streamlit.runtime.scriptrunner import get_script_run_ctx
except ImportError as e:
    print(f"\n❌ 错误: 缺少必要的库 ({e})")
    print("请运行以下命令安装:")
    print(f"{sys.executable} -m pip install streamlit pandas altair")
    sys.exit(1)

# --- 翻译字典 / Translation Dictionary ---
TRANSLATIONS = {
    '中文': {
        'page_title': "篷房配件计算系统",
        'main_title': "⛺ 篷房配件计算系统",
        'settings': "参数设置",
        'lang_select': "语言选择 / Language",
        'length': "篷房长度 (米)",
        'width': "篷房宽度/跨度 (米)",
        'side_height': "边高 (米)",
        'unit_length': "标准单元长度 (米)",
        'calc_note': "调整上方参数，右侧结果将实时更新。",
        'overview': "📊 概览",
        'details': "📝 详细清单",
        'visualization': "📈 数据可视化",
        'export': "💾 导出数据",
        'download_btn': "下载计算结果 (CSV)",
        'area_tab': "面积分布",
        'count_tab': "数量统计",
        'col_item': "项目",
        'col_value': "数量/面积",
        'col_desc': "说明",
        'unit_area': "㎡",
        'unit_pcs': "件",
        'unit_sets': "组",
        # Items
        'roof_canvas': "顶篷",
        'roof_liner': "顶幔",
        'side_canvas': "四周篷布",
        'side_liner': "四周边幔",
        'flooring': "承重地板",
        'glass_wall': "玻璃墙",
        'lighting': "基础照明",
        'anchoring': "锚固系统",
        # Descriptions
        'desc_roof': "篷房面积 × 1.05",
        'desc_same_roof': "同顶篷面积",
        'desc_side': "周长 × 边高",
        'desc_same_side': "同四周篷布",
        'desc_light': "(单元数-1) × 2",
        'desc_anchor': "(单元数+1)×2 + 山墙柱×2",
        'desc_floor': "长度 × 宽度",
        'desc_glass': "2 × 长度 × 边高",
    },
    'English': {
        'page_title': "Tent Accessories Calculator",
        'main_title': "⛺ Tent Accessories Calculator",
        'settings': "Settings",
        'lang_select': "Language",
        'length': "Length (m)",
        'width': "Width / Span (m)",
        'side_height': "Side Height (m)",
        'unit_length': "Unit Length (m)",
        'calc_note': "Adjust parameters above to update results.",
        'overview': "📊 Overview",
        'details': "📝 Detailed List",
        'visualization': "📈 Visualization",
        'export': "💾 Export Data",
        'download_btn': "Download Results (CSV)",
        'area_tab': "Area Distribution",
        'count_tab': "Count Statistics",
        'col_item': "Item",
        'col_value': "Qty / Area",
        'col_desc': "Description",
        'unit_area': "㎡",
        'unit_pcs': "pcs",
        'unit_sets': "sets",
        # Items
        'roof_canvas': "Roof Canvas",
        'roof_liner': "Roof Liner",
        'side_canvas': "Side Canvas",
        'side_liner': "Side Liner",
        'flooring': "Flooring",
        'glass_wall': "Glass Wall",
        'lighting': "Basic Lighting",
        'anchoring': "Anchoring System",
        # Descriptions
        'desc_roof': "Area × 1.05",
        'desc_same_roof': "Same as Roof",
        'desc_side': "Perimeter × Height",
        'desc_same_side': "Same as Side Canvas",
        'desc_light': "(Units-1) × 2",
        'desc_anchor': "(Units+1)×2 + Gable×2",
        'desc_floor': "Length × Width",
        'desc_glass': "2 × Length × Height",
    }
}

class TentCalculator:
    def __init__(self, length=25.0, width=20.0, side_height=3.0, unit_length=5.0):
        self.length = float(length)
        self.width = float(width)
        self.side_height = float(side_height)
        self.unit_length = float(unit_length)
        self.triangle_angle_ratio = 1.05
    
    def get_raw_results(self):
        results = {}
        results['roof_canvas'] = self._calculate_roof_canvas()
        results['roof_liner'] = self._calculate_roof_liner()
        results['side_canvas'] = self._calculate_side_canvas()
        results['side_liner'] = self._calculate_side_liner()
        results['lighting'] = self._calculate_lighting()
        results['anchoring'] = self._calculate_anchoring()
        results['flooring'] = self._calculate_flooring()
        results['glass_wall'] = self._calculate_glass_wall()
        return results
    
    def _calculate_roof_canvas(self):
        tent_area = self.length * self.width
        return round(tent_area * self.triangle_angle_ratio, 2)
    
    def _calculate_roof_liner(self):
        return self._calculate_roof_canvas()
    
    def _calculate_side_canvas(self):
        perimeter = 2 * (self.length + self.width)
        return round(perimeter * self.side_height, 2)
    
    def _calculate_side_liner(self):
        return self._calculate_side_canvas()
    
    def _calculate_lighting(self):
        if self.unit_length <= 0: return 0
        units = self.length / self.unit_length
        lights_per_beam = 2
        return int(max(0, (units - 1) * lights_per_beam))
    
    def _calculate_anchoring(self):
        if self.unit_length <= 0: return 0
        units = self.length / self.unit_length
        gable_posts = 6
        return int((units + 1) * 2 + gable_posts * 2)
    
    def _calculate_flooring(self):
        return round(self.length * self.width, 2)
    
    def _calculate_glass_wall(self):
        glass_length = 2 * self.length
        return round(glass_length * self.side_height, 2)

def main():
    st.set_page_config(
        page_title="Tent Accessories Calculator",
        page_icon="⛺",
        layout="wide"
    )

    # --- Sidebar & Language Selection ---
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Language Selector
        lang_choice = st.radio("Language / 语言", ["中文", "English"], horizontal=True)
        t = TRANSLATIONS[lang_choice]
        
        st.markdown("---")
        st.header(t['settings'])
        
        length = st.number_input(t['length'], min_value=1.0, value=25.0, step=1.0)
        width = st.number_input(t['width'], min_value=1.0, value=20.0, step=1.0)
        side_height = st.number_input(t['side_height'], min_value=1.0, value=3.0, step=0.5)
        unit_length = st.number_input(t['unit_length'], min_value=1.0, value=5.0, step=0.5)
        
        st.markdown("---")
        st.info(t['calc_note'])

    # --- Main Content ---
    st.title(t['main_title'])
    st.markdown("---")

    # Calculation
    calculator = TentCalculator(length, width, side_height, unit_length)
    results = calculator.get_raw_results()

    # --- KPI Overview ---
    st.subheader(t['overview'])
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label=t['roof_canvas'], value=f"{results['roof_canvas']} {t['unit_area']}")
    with col2:
        st.metric(label=t['side_canvas'], value=f"{results['side_canvas']} {t['unit_area']}")
    with col3:
        st.metric(label=t['flooring'], value=f"{results['flooring']} {t['unit_area']}")
    with col4:
        st.metric(label=t['anchoring'], value=f"{results['anchoring']} {t['unit_pcs']}")

    st.markdown("---")

    # --- Detailed Table ---
    st.subheader(t['details'])
    
    table_data = [
        {t['col_item']: t['roof_canvas'], t['col_value']: f"{results['roof_canvas']} {t['unit_area']}", t['col_desc']: t['desc_roof']},
        {t['col_item']: t['roof_liner'], t['col_value']: f"{results['roof_liner']} {t['unit_area']}", t['col_desc']: t['desc_same_roof']},
        {t['col_item']: t['side_canvas'], t['col_value']: f"{results['side_canvas']} {t['unit_area']}", t['col_desc']: t['desc_side']},
        {t['col_item']: t['side_liner'], t['col_value']: f"{results['side_liner']} {t['unit_area']}", t['col_desc']: t['desc_same_side']},
        {t['col_item']: t['lighting'], t['col_value']: f"{results['lighting']} {t['unit_sets']}", t['col_desc']: t['desc_light']},
        {t['col_item']: t['anchoring'], t['col_value']: f"{results['anchoring']} {t['unit_pcs']}", t['col_desc']: t['desc_anchor']},
        {t['col_item']: t['flooring'], t['col_value']: f"{results['flooring']} {t['unit_area']}", t['col_desc']: t['desc_floor']},
        {t['col_item']: t['glass_wall'], t['col_value']: f"{results['glass_wall']} {t['unit_area']}", t['col_desc']: t['desc_glass']},
    ]
    
    df = pd.DataFrame(table_data)
    st.table(df)

    # --- Visualization (Altair) ---
    st.subheader(t['visualization'])
    
    tab1, tab2 = st.tabs([t['area_tab'], t['count_tab']])
    
    with tab1:
        area_df = pd.DataFrame({
            'Type': [t['roof_canvas'], t['roof_liner'], t['side_canvas'], t['side_liner'], t['flooring'], t['glass_wall']],
            'Area': [results['roof_canvas'], results['roof_liner'], results['side_canvas'], results['side_liner'], results['flooring'], results['glass_wall']]
        })
        
        # Base chart
        base_area = alt.Chart(area_df).encode(
            x=alt.X('Type', axis=alt.Axis(title=t['col_item'], labelAngle=0))
        )

        # Colorful Bar Chart
        bars_area = base_area.mark_bar().encode(
            y=alt.Y('Area', axis=alt.Axis(title=f"{t['col_value']} ({t['unit_area']})")),
            color=alt.Color('Type', legend=None), # Different color per bar
            tooltip=['Type', 'Area']
        )
        
        # Text Labels
        text_area = base_area.mark_text(dy=-10, color='black').encode(
            y=alt.Y('Area'),
            text=alt.Text('Area')
        )
        
        st.altair_chart((bars_area + text_area).properties(height=400), use_container_width=True)

    with tab2:
        count_df = pd.DataFrame({
            'Type': [t['lighting'], t['anchoring']],
            'Count': [results['lighting'], results['anchoring']]
        })
        
        # Base chart
        base_count = alt.Chart(count_df).encode(
            x=alt.X('Type', axis=alt.Axis(title=t['col_item'], labelAngle=0))
        )
        
        bars_count = base_count.mark_bar().encode(
            y=alt.Y('Count', axis=alt.Axis(title=t['col_value'])),
            color=alt.Color('Type', legend=None),
            tooltip=['Type', 'Count']
        )
        
        text_count = base_count.mark_text(dy=-10, color='black').encode(
            y=alt.Y('Count'),
            text=alt.Text('Count')
        )
        
        st.altair_chart((bars_count + text_count).properties(height=400), use_container_width=True)

    # --- Export ---
    st.markdown("---")
    st.subheader(t['export'])
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label=t['download_btn'],
        data=csv,
        file_name='tent_calculation_results.csv',
        mime='text/csv',
    )

if __name__ == "__main__":
    try:
        if st.runtime.exists():
            main()
        else:
            print("Detected direct Python execution. Launching Streamlit...")
            sys.argv = ["streamlit", "run", sys.argv[0]]
            subprocess.run([sys.executable, "-m", "streamlit", "run", sys.argv[0]])
    except Exception as e:
        print(f"Startup error: {e}")
        main()
