# tools/nutrition_analyzer.py
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class NutritionAnalyzer:
    """营养分析工具"""
    
    def __init__(self, llm):
        self.llm = llm
        self.analysis_chain = self._create_analysis_chain()
    
    def _create_analysis_chain(self):
        template = """
        请对以下食谱进行营养分析：
        
        食谱名称：{recipe_name}
        食材列表：{ingredients}
        制作步骤：{steps}
        健康目标：{health_goals}
        
        请返回一个JSON格式的营养分析报告，所有字段必须符合严格JSON语法。
        数字字段直接返回数字，具体数据根据对当前食谱的食材用量和做法分析结果填写。示例："calories": 320    
        文本字段必须使用双引号包裹，具体数据根据对当前食谱的食材用量和做法分析结果填写。示例："vitamins": "富含维生素C"
        禁止省略字符串两侧的双引号。
        返回内容必须能被 Python json.loads() 直接解析。
        营养分析报告包含以下字段：
        - calories: 总热量（千卡）
        - protein: 蛋白质含量（克）
        - carbs: 碳水化合物含量（克）
        - fat: 脂肪含量（克）
        - fiber: 膳食纤维含量（克）
        - vitamins: 维生素含量摘要
        - minerals: 矿物质含量摘要
        - health_score: 健康评分（1-10分）
        - recommendations: 改进建议
        - reference_guide: 参考中国居民膳食指南说明
        
        你的用户是人类，分析人类的营养需求。请注意保护用户隐私，不要存储或记录任何个人健康信息，不要输出解释性文字，不要使用markdown代码块，不要输出特殊字符，不要输出成分单位，要说中文。
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的营养师，善于分析食物的营养价值。"),
            ("human", template)
        ])
        
        return prompt | self.llm | StrOutputParser()
    
    def analyze_nutrition(self, recipe: Dict, health_goals: str) -> Dict:
        """分析食谱营养"""
        result = self.analysis_chain.invoke({
            "recipe_name": recipe["name"],
            "ingredients": ", ".join(recipe["ingredients"]),
            "steps": "; ".join(recipe["steps"]),
            "health_goals": health_goals
        })
        
        try:
            response_text = result
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            import json
            analysis_data = json.loads(json_str)
            return analysis_data
        except Exception as e:
            print(f"JSON解析失败: {e}")
            print(f"llm原始输出: {result}")
            return {
                "calories": 0,
                "protein": 0,
                "carbs": 0,
                "fat": 0,
                "fiber": 0,
                "vitamins": "待分析",
                "minerals": "待分析",
                "health_score": 0,
                "recommendations": "无建议",
                "reference_guide": "参考中国居民膳食指南"
            }