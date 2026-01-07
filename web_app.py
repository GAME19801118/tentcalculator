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
        'count_tab': "组件数量",
        'col_item': "项目",
        'col_value': "数量/面积/参数",
        'col_desc': "说明",
        'unit_area': "㎡",
        'unit_pcs': "件",
        'unit_sets': "组",
        'unit_m': "米",
        'unit_kmh': "km/h",
        'unit_kn': "kN/㎡",
        
        # Sections
        'sec_structure': "🏗️ 主体结构",
        'sec_connection': "🔗 连接系统",
        'sec_fixing': "🔩 固定与张紧",
        'sec_cover': "🎪 篷布与地板",
        'sec_access': "💡 附加设施",
        'sec_specs': "📋 技术规格",

        # Items - Structure
        'upright_support': "边墙承重柱",
        'roof_beam': "斜梁/主框架",
        'gable_post': "山墙柱",
        'eave_purlin': "屋檐支撑杆",
        
        # Items - Connection
        'ridge_conn': "屋脊连接角",
        'eave_conn': "屋檐连接角",
        
        # Items - Fixing
        'expansion_bolt': "膨胀螺丝/钢钎",
        'roof_tensioner': "顶棚张紧器",
        
        # Items - Cover
        'roof_canvas': "顶篷",
        'roof_liner': "顶幔",
        'side_canvas': "四周篷布",
        'side_liner': "四周边幔",
        'flooring': "承重地板",
        
        # Items - Accessories
        'glass_wall': "玻璃墙系统",
        'lighting': "基础照明",
        
        # Items - Specs
        'wind_load': "抗风等级",
        'snow_load': "雪荷载",

        # Descriptions
        'desc_upright': "每组框架2根",
        'desc_roof_beam': "每组框架2根",
        'desc_gable': "两端山墙共6根",
        'desc_purlin': "连接每组框架",
        'desc_ridge_conn': "每组框架顶端1个",
        'desc_eave_conn': "每组框架两侧各1个",
        'desc_bolt': "每立柱4个",
        'desc_tensioner': "每个单元4个",
        'desc_roof': "篷房面积 × 1.05",
        'desc_same_roof': "同顶篷面积",
        'desc_side': "周长 × 边高",
        'desc_same_side': "同四周篷布",
        'desc_light': "(单元数-1) × 2",
        'desc_floor': "长度 × 宽度",
        'desc_glass': "2 × 长度 × 边高",
        'desc_std': "标准参数",
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
        'count_tab': "Component Count",
        'col_item': "Item",
        'col_value': "Qty / Area / Value",
        'col_desc': "Description",
        'unit_area': "㎡",
        'unit_pcs': "pcs",
        'unit_sets': "sets",
        'unit_m': "m",
        'unit_kmh': "km/h",
        'unit_kn': "kN/㎡",

        # Sections
        'sec_structure': "🏗️ Main Structure",
        'sec_connection': "🔗 Connection System",
        'sec_fixing': "🔩 Fixing & Tensioning",
        'sec_cover': "🎪 Cover & Flooring",
        'sec_access': "💡 Accessories",
        'sec_specs': "📋 Technical Specs",

        # Items - Structure
        'upright_support': "Upright Support",
        'roof_beam': "Roof Beam / Main Frame",
        'gable_post': "Gable Post",
        'eave_purlin': "Eave Purlin",
        
        # Items - Connection
        'ridge_conn': "Ridge Connection",
        'eave_conn': "Eave Connection",
        
        # Items - Fixing
        'expansion_bolt': "Expansion Screw / Stake",
        'roof_tensioner': "Roof Tensioner",
        
        # Items - Cover
        'roof_canvas': "Roof Canvas",
        'roof_liner': "Roof Liner",
        'side_canvas': "Side Canvas",
        'side_liner': "Side Liner",
        'flooring': "Flooring",
        
        # Items - Accessories
        'glass_wall': "Glass Wall System",
        'lighting': "Basic Lighting",
        
        # Items - Specs
        'wind_load': "Wind Load",
        'snow_load': "Snow Load",

        # Descriptions
        'desc_upright': "2 per frame",
        'desc_roof_beam': "2 per frame",
        'desc_gable': "Total 6 for gable ends",
        'desc_purlin': "Connects frames",
        'desc_ridge_conn': "1 per frame top",
        'desc_eave_conn': "1 per side per frame",
        'desc_bolt': "4 per column",
        'desc_tensioner': "4 per unit",
        'desc_roof': "Area × 1.05",
        'desc_same_roof': "Same as Roof",
        'desc_side': "Perimeter × Height",
        'desc_same_side': "Same as Side Canvas",
        'desc_light': "(Units-1) × 2",
        'desc_floor': "Length × Width",
        'desc_glass': "2 × Length × Height",
        'desc_std': "Standard Spec",
    }
}

class TentCalculator:
    def __init__(self, length=25.0, width=20.0, side_height=3.0, unit_length=5.0):
        self.length = float(length)
        self.width = float(width)
        self.side_height = float(side_height)
        self.unit_length = float(unit_length)
        self.triangle_angle_ratio = 1.05
        
        # Basic calculations
        self.num_units = 0
        if self.unit_length > 0:
            self.num_units = int(self.length / self.unit_length)
        self.num_frames = self.num_units + 1

    def calculate_all(self):
        results = {}
        
        # --- 1. Structure ---
        results['upright_support'] = self.num_frames * 2
        results['roof_beam'] = self.num_frames * 2
        results['gable_post'] = 6  # Fixed for now as per previous logic
        results['eave_purlin'] = self.num_units * 2  # 2 lines of purlins (left/right)
        
        # --- 2. Connection ---
        results['ridge_conn'] = self.num_frames
        results['eave_conn'] = self.num_frames * 2
        
        # --- 3. Fixing ---
        total_columns = results['upright_support'] + results['gable_post']
        results['expansion_bolt'] = total_columns * 4
        results['roof_tensioner'] = self.num_units * 4
        
        # --- 4. Cover ---
        tent_area = self.length * self.width
        perimeter = 2 * (self.length + self.width)
        
        results['roof_canvas'] = round(tent_area * self.triangle_angle_ratio, 2)
        results['roof_liner'] = results['roof_canvas']
        results['side_canvas'] = round(perimeter * self.side_height, 2)
        results['side_liner'] = results['side_canvas']
        results['flooring'] = round(tent_area, 2)
        
        # --- 5. Accessories ---
        glass_length = 2 * self.length
        results['glass_wall'] = round(glass_length * self.side_height, 2)
        
        lights_per_beam = 2
        results['lighting'] = int(max(0, (self.num_units - 1) * lights_per_beam))
        
        # --- 6. Specs ---
        results['wind_load'] = "80-100"
        results['snow_load'] = "0.5-0.75"
        
        return results

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
    results = calculator.calculate_all()

    # --- KPI Overview ---
    st.subheader(t['overview'])
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label=t['roof_canvas'], value=f"{results['roof_canvas']} {t['unit_area']}")
    with col2:
        st.metric(label=t['upright_support'], value=f"{results['upright_support']} {t['unit_pcs']}")
    with col3:
        st.metric(label=t['flooring'], value=f"{results['flooring']} {t['unit_area']}")
    with col4:
        st.metric(label=t['expansion_bolt'], value=f"{results['expansion_bolt']} {t['unit_pcs']}")

    st.markdown("---")

    # --- Detailed Table ---
    st.subheader(t['details'])
    
    # Helper to create row
    def create_row(section, item_key, value, unit, desc_key):
        return {
            "Category": section,
            t['col_item']: t[item_key],
            t['col_value']: f"{value} {unit}",
            t['col_desc']: t[desc_key]
        }

    table_data = []
    
    # 1. Structure
    table_data.append(create_row(t['sec_structure'], 'upright_support', results['upright_support'], t['unit_pcs'], 'desc_upright'))
    table_data.append(create_row(t['sec_structure'], 'roof_beam', results['roof_beam'], t['unit_pcs'], 'desc_roof_beam'))
    table_data.append(create_row(t['sec_structure'], 'gable_post', results['gable_post'], t['unit_pcs'], 'desc_gable'))
    table_data.append(create_row(t['sec_structure'], 'eave_purlin', results['eave_purlin'], t['unit_pcs'], 'desc_purlin'))
    
    # 2. Connection
    table_data.append(create_row(t['sec_connection'], 'ridge_conn', results['ridge_conn'], t['unit_pcs'], 'desc_ridge_conn'))
    table_data.append(create_row(t['sec_connection'], 'eave_conn', results['eave_conn'], t['unit_pcs'], 'desc_eave_conn'))
    
    # 3. Fixing
    table_data.append(create_row(t['sec_fixing'], 'expansion_bolt', results['expansion_bolt'], t['unit_pcs'], 'desc_bolt'))
    table_data.append(create_row(t['sec_fixing'], 'roof_tensioner', results['roof_tensioner'], t['unit_pcs'], 'desc_tensioner'))
    
    # 4. Cover
    table_data.append(create_row(t['sec_cover'], 'roof_canvas', results['roof_canvas'], t['unit_area'], 'desc_roof'))
    table_data.append(create_row(t['sec_cover'], 'roof_liner', results['roof_liner'], t['unit_area'], 'desc_same_roof'))
    table_data.append(create_row(t['sec_cover'], 'side_canvas', results['side_canvas'], t['unit_area'], 'desc_side'))
    table_data.append(create_row(t['sec_cover'], 'side_liner', results['side_liner'], t['unit_area'], 'desc_same_side'))
    table_data.append(create_row(t['sec_cover'], 'flooring', results['flooring'], t['unit_area'], 'desc_floor'))
    
    # 5. Accessories
    table_data.append(create_row(t['sec_access'], 'glass_wall', results['glass_wall'], t['unit_area'], 'desc_glass'))
    table_data.append(create_row(t['sec_access'], 'lighting', results['lighting'], t['unit_sets'], 'desc_light'))
    
    # 6. Specs
    table_data.append(create_row(t['sec_specs'], 'wind_load', results['wind_load'], t['unit_kmh'], 'desc_std'))
    table_data.append(create_row(t['sec_specs'], 'snow_load', results['snow_load'], t['unit_kn'], 'desc_std'))

    df = pd.DataFrame(table_data)
    
    # Use st.dataframe for better interaction or st.table for static
    # st.table(df) # table displays everything
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- Visualization (Altair) ---
    st.subheader(t['visualization'])
    
    tab1, tab2 = st.tabs([t['area_tab'], t['count_tab']])
    
    with tab1:
        # Filter for area items
        area_items = ['roof_canvas', 'roof_liner', 'side_canvas', 'side_liner', 'flooring', 'glass_wall']
        area_df = pd.DataFrame({
            'Type': [t[k] for k in area_items],
            'Area': [results[k] for k in area_items]
        })
        
        base_area = alt.Chart(area_df).encode(
            x=alt.X('Type', axis=alt.Axis(title=t['col_item'], labelAngle=0))
        )
        bars_area = base_area.mark_bar().encode(
            y=alt.Y('Area', axis=alt.Axis(title=f"{t['col_value']} ({t['unit_area']})")),
            color=alt.Color('Type', legend=None),
            tooltip=['Type', 'Area']
        )
        text_area = base_area.mark_text(dy=-10, color='black').encode(
            y=alt.Y('Area'),
            text=alt.Text('Area')
        )
        st.altair_chart((bars_area + text_area).properties(height=400), use_container_width=True)

    with tab2:
        # Filter for count items (Structure + Connection + Fixing)
        count_items = ['upright_support', 'roof_beam', 'gable_post', 'eave_purlin', 
                       'ridge_conn', 'eave_conn', 'expansion_bolt', 'roof_tensioner', 'lighting']
        count_df = pd.DataFrame({
            'Type': [t[k] for k in count_items],
            'Count': [results[k] for k in count_items]
        })
        
        base_count = alt.Chart(count_df).encode(
            x=alt.X('Type', axis=alt.Axis(title=t['col_item'], labelAngle=-45))
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
        file_name='tent_calculation_full.csv',
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
