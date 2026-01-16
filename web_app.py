import sys
import os
import subprocess
import math

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
        'page_title': "篷房核心计算系统",
        'main_title': "⛺ 篷房核心计算系统",
        'settings': "基础参数",
        'adv_settings': "高级参数",
        'lang_select': "语言选择 / Language",
        'length': "篷房长度 (米)",
        'width': "篷房宽度/跨度 (米)",
        'side_height': "边高 (米)",
        'unit_length': "单元长度 (米)",
        'gable_unit_length': "山墙单元/间隔 (米)",
        'holes_per_base': "基座孔位数量 (个)",
        'roof_pitch_factor': "三角形角度系数",
        
        'calc_note': "依据“篷房核心计算公式”标准进行计算。",
        'overview': "📊 核心指标概览",
        'details': "📝 详细组件清单",
        'visualization': "📈 数据可视化",
        'export': "💾 导出数据",
        'download_btn': "下载计算结果 (CSV)",
        'area_tab': "面积与覆盖",
        'count_tab': "结构组件数量",
        'col_item': "组件名称",
        'col_value': "数值",
        'col_desc': "计算规则/说明",
        'unit_area': "㎡",
        'unit_pcs': "件",
        'unit_sets': "组",
        'unit_m': "米",
        'unit_kmh': "km/h",
        'unit_kn': "kN/㎡",
        
        # Sections
        'sec_basic': "1. 基础参数关系",
        'sec_struct': "2. 结构性组件关系",
        'sec_conn': "3. 连接件与辅助组件",
        'sec_cover': "4. 覆盖物与装饰组件",
        'sec_specs': "技术规格",

        # Items
        'num_units': "单元数量",
        'tent_area': "篷房面积",
        'perimeter': "周长",
        
        'gable_post': "山墙侧柱",
        'gable_mid_post': "山墙中柱 (说明)",
        'upright_support': "边墙承重柱",
        
        'roof_beam': "斜梁",
        'ridge_conn': "屋脊连接角",
        'eave_conn': "屋檐连接角",
        'expansion_screw': "膨胀螺丝",
        'drilling_steel': "钢钎",
        'bearing_count': "承重数量",
        'main_comp_total': "主要构件总数",
        
        'roof_canvas': "顶棚面积",
        'roof_liner': "顶幔面积",
        'roof_cover': "总覆盖面积",
        'glass_wall_m': "玻璃墙 (米)",
        'glass_wall_sqm': "玻璃墙 (平方)",
        'basic_lighting': "基础照明",
        'roof_stretcher': "顶棚紧固器",

        # Descriptions (Formulas)
        'desc_num_units': "长度 / 单元长度",
        'desc_area': "长度 × 宽度",
        'desc_perimeter': "(长度 + 宽度) × 2",
        
        'desc_gable_post': "(宽度 / 山墙间隔 - 1) × 2",
        'desc_gable_mid': "奇数间隔无中柱，偶数有中柱",
        'desc_upright': "(单元数量 + 1) × 2",
        
        'desc_roof_beam': "单元数量 + 1 (组/对)",
        'desc_ridge_conn': "单元数量 + 1",
        'desc_eave_conn': "(单元数量 + 1) × 2",
        'desc_bearing': "(边墙单元数+1)×2 + 山墙柱数",
        'desc_expansion_screw': "(边墙柱数 + 山墙侧柱数) × 基座孔数",
        'desc_drilling_steel': "(边墙柱数 + 山墙侧柱数) × 基座孔数",
        
        'desc_roof_canvas': "篷房面积 × 角度系数",
        'desc_roof_liner': "同顶棚面积",
        'desc_roof_cover': "顶棚面积 + 顶幔面积 + 玻璃墙面积",
        'desc_glass_m': "周长",
        'desc_glass_sqm': "周长 × 边高",
        'desc_basic_lighting': "(单元数量 - 1) × 2",
        'desc_roof_stretcher': "单元数量 × 2",
    },
    'English': {
        'page_title': "Tent Core Calculator",
        'main_title': "⛺ Tent Core Calculator",
        'settings': "Basic Parameters",
        'adv_settings': "Advanced Parameters",
        'lang_select': "Language",
        'length': "Length (m)",
        'width': "Width / Span (m)",
        'side_height': "Side Height (m)",
        'unit_length': "Unit Length (m)",
        'gable_unit_length': "Gable Unit/Bay (m)",
        'holes_per_base': "Holes per Base Plate",
        'roof_pitch_factor': "Angle ratio of triangle",
        
        'calc_note': "Calculated based on Core Tent Formulas.",
        'overview': "📊 Key Metrics",
        'details': "📝 Detailed List",
        'visualization': "📈 Visualization",
        'export': "💾 Export Data",
        'download_btn': "Download Results (CSV)",
        'area_tab': "Area & Cover",
        'count_tab': "Structural Count",
        'col_item': "Component",
        'col_value': "Value",
        'col_desc': "Formula / Rule",
        'unit_area': "㎡",
        'unit_pcs': "pcs",
        'unit_sets': "sets",
        'unit_m': "m",
        'unit_kmh': "km/h",
        'unit_kn': "kN/㎡",

        # Sections
        'sec_basic': "1. Basic Parameters",
        'sec_struct': "2. Structural Components",
        'sec_conn': "3. Connections & Aux",
        'sec_cover': "4. Cover & Decoration",
        'sec_specs': "Tech Specs",

        # Items
        'num_units': "Quantities of tent units",
        'tent_area': "Tent Area",
        'perimeter': "Perimeter",
        
        'gable_post': "Gable support side",
        'gable_mid_post': "Middle gable support (Note)",
        'upright_support': "Side pillars",
        
        'roof_beam': "Main frame / Beam",
        'ridge_conn': "Ridge connector",
        'eave_conn': "Eave connector",
        'expansion_screw': "Expansion screw",
        'drilling_steel': "Drilling steel",
        'bearing_count': "Bearing Count",
        'main_comp_total': "Total main components",
        
        'roof_canvas': "Roof canvas area",
        'roof_liner': "Roof liner area",
        'roof_cover': "Total cover area",
        'glass_wall_m': "Glass wall (Length)",
        'glass_wall_sqm': "Glass wall (Area)",
        'basic_lighting': "Basic lighting",
        'roof_stretcher': "Roof stretching spare parts",

        # Descriptions
        'desc_num_units': "Length / Unit Length",
        'desc_area': "Length × Width",
        'desc_perimeter': "(Length + Width) × 2",
        
        'desc_gable_post': "(Width / Gable Bay - 1) × 2",
        'desc_gable_mid': "No mid post for odd bays",
        'desc_upright': "(Units + 1) × 2",
        
        'desc_roof_beam': "Units + 1 (Sets/Pairs)",
        'desc_ridge_conn': "Units + 1",
        'desc_eave_conn': "(Units + 1) × 2",
        'desc_bearing': "(Side Units + 1)×2 + Gable Cols",
        'desc_expansion_screw': "(Side pillars + Gable support side) × Holes",
        'desc_drilling_steel': "(Side pillars + Gable support side) × Holes",
        
        'desc_roof_canvas': "Area × Angle ratio of triangle",
        'desc_roof_liner': "Same as roof canvas",
        'desc_roof_cover': "Roof canvas + roof liner + glass wall area",
        'desc_glass_m': "Perimeter",
        'desc_glass_sqm': "Perimeter × Height",
        'desc_basic_lighting': "(Units - 1) × 2",
        'desc_roof_stretcher': "Units × 2",
    }
}

class TentCalculator:
    def __init__(self, length, width, side_height, unit_length, gable_unit_length, holes_per_base, roof_pitch_factor):
        self.length = float(length)
        self.width = float(width)
        self.side_height = float(side_height)
        self.unit_length = float(unit_length)
        self.gable_unit_length = float(gable_unit_length)
        self.holes_per_base = int(holes_per_base)
        self.roof_pitch_factor = float(roof_pitch_factor)
        
        # --- 1. Basic Parameters ---
        self.num_units = 0
        if self.unit_length > 0:
            self.num_units = int(self.length / self.unit_length)
        
        self.area = self.length * self.width
        self.perimeter = (self.length + self.width) * 2

    def calculate_all(self):
        results = {}
        
        # --- 2. Structural Components ---
        # Upright Support: (Units + 1) * 2
        results['upright_support'] = (self.num_units + 1) * 2
        
        # Gable Columns: (Width / Gable_Unit - 1) * 2
        # Note: If Width=20, Bay=5, Cols = (4-1)*2 = 6.
        gable_bays = 0
        if self.gable_unit_length > 0:
            gable_bays = int(self.width / self.gable_unit_length)
        
        # Formula: (Width / Unit_Width - 1) * 2
        # We use max(0, ...) to avoid negatives if width < unit
        results['gable_post'] = max(0, (gable_bays - 1) * 2)
        
        # Middle Post Logic (Information only)
        # "Odd bays no middle post, Even bays have middle post"
        has_mid_post = (gable_bays % 2 == 0) and (gable_bays > 0)
        results['has_mid_post'] = has_mid_post
        
        # --- 3. Connections & Aux ---
        # Roof Beam / Main Frame: Units + 1
        results['roof_beam'] = self.num_units + 1
        
        # Ridge Connection: Units + 1
        results['ridge_conn'] = self.num_units + 1
        
        # Eave Connection: (Units + 1) * 2
        results['eave_conn'] = (self.num_units + 1) * 2
        
        # Bearing Count (Total Columns): (Side Units + 1)*2 + Gable Cols
        # Matches the sum of uprights + gable posts
        results['bearing_count'] = results['upright_support'] + results['gable_post']
        results['main_comp_total'] = results['upright_support'] + results['gable_post'] + results['roof_beam']
        
        # Expansion elements: separate counts for expansion screw and drilling steel
        results['expansion_screw'] = results['bearing_count'] * self.holes_per_base
        results['drilling_steel'] = results['bearing_count'] * self.holes_per_base
        
        # --- 4. Cover & Decoration ---
        results['roof_canvas'] = round(self.area * self.roof_pitch_factor, 2)
        results['roof_liner'] = results['roof_canvas']
        results['glass_wall_m'] = round(self.perimeter, 2)
        results['glass_wall_sqm'] = round(self.perimeter * self.side_height, 2)
        results['roof_cover'] = round(results['roof_canvas'] + results['roof_liner'] + results['glass_wall_sqm'], 2)
        results['basic_lighting'] = max(0, (self.num_units - 1) * 2)
        results['roof_stretcher'] = self.num_units * 2

        return results

def main():
    st.set_page_config(
        page_title="Tent Core Calculator",
        page_icon="⛺",
        layout="wide"
    )

    # --- Sidebar ---
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Language
        lang_choice = st.radio("Language / 语言", ["中文", "English"], horizontal=True)
        t = TRANSLATIONS[lang_choice]
        
        st.markdown("---")
        st.subheader(t['settings'])
        
        length = st.number_input(t['length'], min_value=1.0, value=25.0, step=1.0)
        width = st.number_input(t['width'], min_value=1.0, value=20.0, step=1.0)
        side_height = st.number_input(t['side_height'], min_value=1.0, value=3.0, step=0.5)
        
        st.markdown("---")
        with st.expander(t['adv_settings'], expanded=True):
            unit_length = st.number_input(t['unit_length'], min_value=1.0, value=5.0, step=0.5, help="Standard: 5m (BT), 3m (PT)")
            gable_unit_length = st.number_input(t['gable_unit_length'], min_value=1.0, value=5.0, step=0.5)
            holes_per_base = st.number_input(t['holes_per_base'], min_value=1, value=4, step=1)
            roof_pitch_factor = st.number_input(t['roof_pitch_factor'], min_value=1.0, value=1.15, step=0.01, help="Range: 1.1 - 1.2")
        
        st.info(t['calc_note'])

    # --- Main Content ---
    st.title(t['main_title'])
    st.markdown("---")

    # Calculation
    calc = TentCalculator(length, width, side_height, unit_length, gable_unit_length, holes_per_base, roof_pitch_factor)
    res = calc.calculate_all()

    # --- 1. KPI Overview (Top Level) ---
    st.subheader(t['overview'])
    row1 = st.columns(3)
    with row1[0]:
        st.metric(t['roof_cover'], f"{res['roof_cover']} {t['unit_area']}")
    with row1[1]:
        st.metric(t['num_units'], f"{calc.num_units} {t['unit_sets']}")
    with row1[2]:
        st.metric(t['main_comp_total'], f"{res['main_comp_total']} {t['unit_pcs']}")

    row2 = st.columns(3)
    with row2[0]:
        st.metric(t['roof_canvas'], f"{res['roof_canvas']} {t['unit_area']}")
    with row2[1]:
        st.metric(t['roof_liner'], f"{res['roof_liner']} {t['unit_area']}")
    with row2[2]:
        st.metric(t['tent_area'], f"{calc.area} {t['unit_area']}")

    st.markdown("---")

    # --- 2. Detailed Table (Grouped) ---
    st.subheader(t['details'])
    
    def create_row(section, item_key, value, unit, desc_key):
        return {
            "Category": section,
            t['col_item']: t[item_key],
            t['col_value']: f"{value} {unit}",
            t['col_desc']: t[desc_key]
        }

    rows = []
    
    # Sec 1: Basic
    rows.append(create_row(t['sec_basic'], 'num_units', calc.num_units, t['unit_sets'], 'desc_num_units'))
    rows.append(create_row(t['sec_basic'], 'tent_area', calc.area, t['unit_area'], 'desc_area'))
    rows.append(create_row(t['sec_basic'], 'perimeter', calc.perimeter, t['unit_m'], 'desc_perimeter'))
    
    # Sec 2: Structure
    mid_post_status = "✅ YES" if res['has_mid_post'] else "❌ NO"
    rows.append(create_row(t['sec_struct'], 'gable_post', res['gable_post'], t['unit_pcs'], 'desc_gable_post'))
    # Special row for mid post info
    rows.append({
        "Category": t['sec_struct'],
        t['col_item']: t['gable_mid_post'],
        t['col_value']: mid_post_status,
        t['col_desc']: t['desc_gable_mid']
    })
    rows.append(create_row(t['sec_struct'], 'upright_support', res['upright_support'], t['unit_pcs'], 'desc_upright'))
    
    # Sec 3: Connections & Anchoring
    rows.append(create_row(t['sec_conn'], 'roof_beam', res['roof_beam'], t['unit_sets'], 'desc_roof_beam'))
    rows.append(create_row(t['sec_conn'], 'ridge_conn', res['ridge_conn'], t['unit_pcs'], 'desc_ridge_conn'))
    rows.append(create_row(t['sec_conn'], 'eave_conn', res['eave_conn'], t['unit_pcs'], 'desc_eave_conn'))
    rows.append(create_row(t['sec_conn'], 'bearing_count', res['bearing_count'], t['unit_pcs'], 'desc_bearing'))
    rows.append(create_row(t['sec_conn'], 'expansion_screw', res['expansion_screw'], t['unit_pcs'], 'desc_expansion_screw'))
    rows.append(create_row(t['sec_conn'], 'drilling_steel', res['drilling_steel'], t['unit_pcs'], 'desc_drilling_steel'))
    
    # Sec 4: Cover & Decoration
    rows.append(create_row(t['sec_cover'], 'roof_canvas', res['roof_canvas'], t['unit_area'], 'desc_roof_canvas'))
    rows.append(create_row(t['sec_cover'], 'roof_liner', res['roof_liner'], t['unit_area'], 'desc_roof_liner'))
    rows.append(create_row(t['sec_cover'], 'roof_cover', res['roof_cover'], t['unit_area'], 'desc_roof_cover'))
    rows.append(create_row(t['sec_cover'], 'glass_wall_m', res['glass_wall_m'], t['unit_m'], 'desc_glass_m'))
    rows.append(create_row(t['sec_cover'], 'glass_wall_sqm', res['glass_wall_sqm'], t['unit_area'], 'desc_glass_sqm'))
    rows.append(create_row(t['sec_cover'], 'basic_lighting', res['basic_lighting'], t['unit_pcs'], 'desc_basic_lighting'))
    rows.append(create_row(t['sec_cover'], 'roof_stretcher', res['roof_stretcher'], t['unit_pcs'], 'desc_roof_stretcher'))

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- 3. Visualization ---
    st.subheader(t['visualization'])
    
    tab1, tab2 = st.tabs([t['area_tab'], t['count_tab']])
    
    with tab1:
        area_data = [
            {'Type': t['tent_area'], 'Val': calc.area},
            {'Type': t['roof_canvas'], 'Val': res['roof_canvas']},
            {'Type': t['roof_liner'], 'Val': res['roof_liner']},
            {'Type': t['roof_cover'], 'Val': res['roof_cover']},
            {'Type': t['glass_wall_sqm'], 'Val': res['glass_wall_sqm']}
        ]
        area_df = pd.DataFrame(area_data)
        
        base_a = alt.Chart(area_df).encode(x=alt.X('Type', axis=alt.Axis(title=None, labelAngle=0)))
        bars_a = base_a.mark_bar().encode(
            y=alt.Y('Val', axis=alt.Axis(title=t['unit_area'])),
            color=alt.Color('Type', legend=None),
            tooltip=['Type', 'Val']
        )
        text_a = base_a.mark_text(dy=-10).encode(y='Val', text='Val')
        st.altair_chart((bars_a + text_a).properties(height=350), use_container_width=True)
        
    with tab2:
        cnt_items = ['upright_support', 'gable_post', 'roof_beam', 'ridge_conn', 'eave_conn',
                     'expansion_screw', 'drilling_steel', 'basic_lighting', 'roof_stretcher']
        cnt_data = [{'Type': t[k], 'Val': res[k]} for k in cnt_items]
        cnt_df = pd.DataFrame(cnt_data)
        
        base_c = alt.Chart(cnt_df).encode(x=alt.X('Type', axis=alt.Axis(title=None, labelAngle=-45)))
        bars_c = base_c.mark_bar().encode(
            y=alt.Y('Val', axis=alt.Axis(title=t['unit_pcs'])),
            color=alt.Color('Type', legend=None),
            tooltip=['Type', 'Val']
        )
        text_c = base_c.mark_text(dy=-10).encode(y='Val', text='Val')
        st.altair_chart((bars_c + text_c).properties(height=350), use_container_width=True)

    # --- 4. Export ---
    st.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label=t['download_btn'],
        data=csv,
        file_name='tent_core_calc.csv',
        mime='text/csv',
    )

if __name__ == "__main__":
    try:
        if st.runtime.exists():
            main()
        else:
            script_path = os.path.abspath(__file__)
            print(f"Detected direct Python execution. Launching Streamlit on {script_path}...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])
    except Exception as e:
        print(f"Startup error: {e}")
        main()
