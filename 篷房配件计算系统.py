"""
BT系列篷房配件自动计算系统
版本: 4.0
设计原则: 模块化、可扩展、支持中英双语
"""

class TentCalculator:
    def __init__(self, length=25, width=20, side_height=3, unit_length=5):
        """
        初始化篷房参数
        :param length: 篷房长度 (米)
        :param width: 篷房宽度/跨度 (米)
        :param side_height: 边高 (米)
        :param unit_length: 标准单元长度 (默认5米)
        """
        self.length = length
        self.width = width
        self.side_height = side_height
        self.unit_length = unit_length
        self.triangle_angle_ratio = 1.05  # 三角形角度系数
    
    def calculate_all(self, lang='zh'):
        """计算所有配件数量"""
        results = {}
        
        # 1. 顶篷 Roof Canvas
        results['roof_canvas'] = self._calculate_roof_canvas()
        
        # 2. 顶幔 Roof Liner
        results['roof_liner'] = self._calculate_roof_liner()
        
        # 3. 四周篷布 Side Canvas
        results['side_canvas'] = self._calculate_side_canvas()
        
        # 4. 四周边幔 Side Liner
        results['side_liner'] = self._calculate_side_liner()
        
        # 5. 基础照明 Lighting
        results['lighting'] = self._calculate_lighting()
        
        # 6. 锚固系统 Anchoring
        results['anchoring'] = self._calculate_anchoring()
        
        # 7. 承重地板 Flooring
        results['flooring'] = self._calculate_flooring()
        
        # 8. 玻璃墙 Glass Wall
        results['glass_wall'] = self._calculate_glass_wall()
        
        return self._format_results(results, lang)
    
    def _calculate_roof_canvas(self):
        """计算顶篷面积: 篷房面积 × 三角型角度系数"""
        tent_area = self.length * self.width
        return round(tent_area * self.triangle_angle_ratio, 2)
    
    def _calculate_roof_liner(self):
        """计算顶幔面积: 同顶篷计算方法"""
        return self._calculate_roof_canvas()
    
    def _calculate_side_canvas(self):
        """计算四周篷布: 周长 × 边高"""
        perimeter = 2 * (self.length + self.width)
        return round(perimeter * self.side_height, 2)
    
    def _calculate_side_liner(self):
        """计算四周边幔: 同四周篷布计算方法"""
        return self._calculate_side_canvas()
    
    def _calculate_lighting(self):
        """计算基础照明: (单元数量-1) × 每组斜梁照明数量"""
        units = self.length / self.unit_length
        lights_per_beam = 2  # 每组斜梁2个照明
        return int((units - 1) * lights_per_beam)
    
    def _calculate_anchoring(self):
        """计算锚固系统数量: (单元数量+1)×2 + 山墙柱数量×2"""
        units = self.length / self.unit_length
        gable_posts = 6  # 每个山墙3柱(1中柱+2侧柱)，两个山墙共6柱
        return int((units + 1) * 2 + gable_posts * 2)
    
    def _calculate_flooring(self):
        """计算承重地板面积: 等于篷房面积"""
        return round(self.length * self.width, 2)
    
    def _calculate_glass_wall(self):
        """计算玻璃墙数量(平方米): 玻璃墙长度 × 边高"""
        glass_length = 2 * self.length  # 假设两侧长边使用玻璃墙
        return round(glass_length * self.side_height, 2)
    
    def _format_results(self, results, lang='zh'):
        """格式化输出结果"""
        if lang == 'zh':
            return f"""
篷房配件计算结果 (尺寸: {self.width}m×{self.length}m)
========================================
1. 顶篷面积: {results['roof_canvas']}㎡ (篷房面积×角度系数)
2. 顶幔面积: {results['roof_liner']}㎡ (同顶篷计算)
3. 四周篷布: {results['side_canvas']}㎡ (周长×边高)
4. 四周边幔: {results['side_liner']}㎡ (同四周篷布)
5. 基础照明: {results['lighting']}组 (单元数-1)×2
6. 锚固系统: {results['anchoring']}件 (公式计算)
7. 承重地板: {results['flooring']}㎡ (等于篷房面积)
8. 玻璃墙: {results['glass_wall']}㎡ (长度×边高)
"""
        else:
            return f"""
Tent Accessories Calculation (Size: {self.width}m×{self.length}m)
========================================
1. Roof Canvas: {results['roof_canvas']}㎡ (Area×Angle Ratio)
2. Roof Liner: {results['roof_liner']}㎡ (Same as Roof)
3. Side Canvas: {results['side_canvas']}㎡ (Perimeter×Height)
4. Side Liner: {results['side_liner']}㎡ (Same as Side Canvas)
5. Basic Lighting: {results['lighting']} sets (Units-1)×2
6. Anchoring System: {results['anchoring']} pcs (Formula)
7. Flooring Area: {results['flooring']}㎡ (Equal to Tent Area)
8. Glass Wall: {results['glass_wall']}㎡ (Length×Height)
"""

# 测试用例
if __name__ == "__main__":
    # 标准尺寸测试
    print("=== 标准20×25篷房测试 ===")
    tent1 = TentCalculator(length=25, width=20, side_height=3)
    print(tent1.calculate_all('zh'))
    
    # 非标准尺寸测试
    print("\n=== 非标准18×30篷房测试 ===")
    tent2 = TentCalculator(length=30, width=18, side_height=2.5)
    print(tent2.calculate_all('en'))
