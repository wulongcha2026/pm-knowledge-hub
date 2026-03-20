"""
风险识别 Agent - 基于 LangGraph 多步推理
"""
from typing import Dict, List, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from openai import OpenAI
from django.conf import settings
import json
import operator


class RiskState(TypedDict):
    """风险识别状态"""
    project_description: str
    meeting_notes: str
    risk_categories: List[str]
    identified_risks: List[Dict[str, Any]]
    analysis_steps: List[str]


class RiskAgent:
    """风险识别 Agent"""
    
    def __init__(self):
        # 初始化智谱 LLM
        self.llm_client = OpenAI(
            api_key=settings.ZHIPU_API_KEY,
            base_url=settings.ZHIPU_API_BASE
        )
        self.llm_model = settings.ZHIPU_LLM_MODEL
        
        # 预定义风险类别
        self.risk_categories = [
            'technical', 'schedule', 'resource',
            'requirement', 'communication', 'external'
        ]
        
        # 构建 LangGraph 工作流
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """构建 LangGraph 工作流"""
        workflow = StateGraph(RiskState)
        
        # 添加节点
        workflow.add_node("categorize", self._categorize_risks)
        workflow.add_node("analyze_technical", self._analyze_technical_risks)
        workflow.add_node("analyze_schedule", self._analyze_schedule_risks)
        workflow.add_node("analyze_resource", self._analyze_resource_risks)
        workflow.add_node("synthesize", self._synthesize_results)
        
        # 设置入口点
        workflow.set_entry_point("categorize")
        
        # 添加边
        workflow.add_edge("categorize", "analyze_technical")
        workflow.add_edge("analyze_technical", "analyze_schedule")
        workflow.add_edge("analyze_schedule", "analyze_resource")
        workflow.add_edge("analyze_resource", "synthesize")
        workflow.add_edge("synthesize", END)
        
        return workflow.compile()
    
    def _categorize_risks(self, state: RiskState) -> RiskState:
        """步骤 1：风险分类"""
        prompt = f"""分析以下项目描述和会议纪要，识别可能涉及的风险类别。

项目描述：
{state['project_description']}

会议纪要：
{state['meeting_notes']}

可选风险类别：技术风险、进度风险、资源风险、需求风险、沟通风险、外部风险

请返回最相关的 3-5 个风险类别（JSON 数组格式）。"""

        response = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        try:
            categories = json.loads(response.choices[0].message.content)
            state['risk_categories'] = categories
            state['analysis_steps'].append('✓ 完成风险分类')
        except:
            state['risk_categories'] = ['technical', 'schedule', 'resource']
        
        return state
    
    def _analyze_technical_risks(self, state: RiskState) -> RiskState:
        """步骤 2：技术风险分析"""
        risks = self._analyze_category('technical', state)
        state['identified_risks'].extend(risks)
        state['analysis_steps'].append('✓ 完成技术风险分析')
        return state
    
    def _analyze_schedule_risks(self, state: RiskState) -> RiskState:
        """步骤 3：进度风险分析"""
        risks = self._analyze_category('schedule', state)
        state['identified_risks'].extend(risks)
        state['analysis_steps'].append('✓ 完成进度风险分析')
        return state
    
    def _analyze_resource_risks(self, state: RiskState) -> RiskState:
        """步骤 4：资源风险分析"""
        risks = self._analyze_category('resource', state)
        state['identified_risks'].extend(risks)
        state['analysis_steps'].append('✓ 完成资源风险分析')
        return state
    
    def _analyze_category(self, category: str, state: RiskState) -> List[Dict[str, Any]]:
        """分析特定类别的风险"""
        category_names = {
            'technical': '技术风险',
            'schedule': '进度风险',
            'resource': '资源风险',
            'requirement': '需求风险',
            'communication': '沟通风险',
            'external': '外部风险',
        }
        
        prompt = f"""分析以下项目的{category_names.get(category, category)}风险。

项目描述：
{state['project_description']}

会议纪要：
{state['meeting_notes']}

请识别 2-3 个具体的{category_names.get(category, category)}，每个风险包含：
- title: 风险标题（简短）
- description: 风险描述
- probability: 发生概率（1-10）
- impact: 影响程度（1-10）
- mitigation_suggestions: 应对建议

返回 JSON 数组格式。"""

        response = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        
        try:
            risks = json.loads(response.choices[0].message.content)
            for risk in risks:
                risk['category'] = category
            return risks
        except:
            return []
    
    def _synthesize_results(self, state: RiskState) -> RiskState:
        """步骤 5：综合结果"""
        # 计算整体风险等级
        if state['identified_risks']:
            avg_score = sum(
                r.get('probability', 5) * r.get('impact', 5)
                for r in state['identified_risks']
            ) / len(state['identified_risks'])
            
            if avg_score >= 64:
                state['overall_risk_level'] = 'critical'
            elif avg_score >= 36:
                state['overall_risk_level'] = 'high'
            elif avg_score >= 16:
                state['overall_risk_level'] = 'medium'
            else:
                state['overall_risk_level'] = 'low'
        
        state['analysis_steps'].append('✓ 完成风险评估')
        return state
    
    def analyze(self, project_description: str, meeting_notes: str = '') -> Dict[str, Any]:
        """执行风险分析"""
        initial_state: RiskState = {
            'project_description': project_description,
            'meeting_notes': meeting_notes,
            'risk_categories': [],
            'identified_risks': [],
            'analysis_steps': [],
        }
        
        result = self.workflow.invoke(initial_state)
        
        return {
            'overall_risk_level': result.get('overall_risk_level', 'medium'),
            'risk_items': result['identified_risks'],
            'analysis_steps': result['analysis_steps'],
        }


# 单例模式
risk_agent = None

def get_risk_agent() -> RiskAgent:
    """获取风险 Agent 单例"""
    global risk_agent
    if risk_agent is None:
        risk_agent = RiskAgent()
    return risk_agent
