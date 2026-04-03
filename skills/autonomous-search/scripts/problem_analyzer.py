#!/usr/bin/env python3
"""
问题分析器
自动分析问题、识别约束、明确目标
"""

import re
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class ProblemAnalyzer:
    def __init__(self, templates_path: Optional[str] = None):
        """
        初始化问题分析器
        
        Args:
            templates_path: 问题模板文件路径
        """
        self.problem_templates = self._load_problem_templates(templates_path)
        self.analysis_history = []
    
    def _load_problem_templates(self, path: Optional[str]) -> Dict:
        """加载问题模板"""
        default_templates = {
            "technical": {
                "patterns": [
                    r"(error|bug|issue|problem|not working|failed).*?(python|code|program|script|api)",
                    r"(how to|how do I|how can I).*?(implement|fix|solve|optimize)",
                    r"(best practice|optimization|performance).*?(for|in|with)"
                ],
                "constraints": ["time", "resources", "compatibility", "security"],
                "goals": ["fix", "optimize", "implement", "debug"]
            },
            "business": {
                "patterns": [
                    r"(growth|revenue|profit|market).*?(strategy|plan|analysis)",
                    r"(competition|competitor|market share).*?(analysis|research)",
                    r"(customer|user).*?(retention|satisfaction|acquisition)"
                ],
                "constraints": ["budget", "time", "team", "market conditions"],
                "goals": ["increase", "improve", "expand", "optimize"]
            },
            "operational": {
                "patterns": [
                    r"(process|workflow|efficiency).*?(improve|optimize|streamline)",
                    r"(automation|manual).*?(task|process|work)",
                    r"(cost|time).*?(reduce|save|optimize)"
                ],
                "constraints": ["budget", "resources", "time", "expertise"],
                "goals": ["automate", "streamline", "reduce", "improve"]
            }
        }
        
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    custom_templates = json.load(f)
                    # 合并默认模板和自定义模板
                    for key in custom_templates:
                        if key in default_templates:
                            default_templates[key].update(custom_templates[key])
                        else:
                            default_templates[key] = custom_templates[key]
            except:
                pass
        
        return default_templates
    
    def classify_problem(self, problem_description: str) -> str:
        """
        分类问题类型
        
        Args:
            problem_description: 问题描述
            
        Returns:
            问题类型
        """
        problem_lower = problem_description.lower()
        
        # 检查每种问题类型的模式
        scores = {}
        
        for ptype, template in self.problem_templates.items():
            score = 0
            patterns = template.get("patterns", [])
            
            for pattern in patterns:
                if re.search(pattern, problem_lower, re.IGNORECASE):
                    score += 1
            
            scores[ptype] = score
        
        # 找到最高分的问题类型
        if scores:
            max_score = max(scores.values())
            if max_score > 0:
                for ptype, score in scores.items():
                    if score == max_score:
                        return ptype
        
        return "general"
    
    def extract_constraints(self, problem_description: str) -> List[str]:
        """
        提取约束条件
        
        Args:
            problem_description: 问题描述
            
        Returns:
            约束条件列表
        """
        constraints = []
        
        # 常见约束关键词
        constraint_keywords = {
            "time": ["deadline", "time limit", "urgent", "asap", "尽快", "马上"],
            "budget": ["budget", "cost", "price", "expensive", "cheap", "预算", "成本"],
            "resources": ["resources", "team", "personnel", "equipment", "资源", "人员"],
            "technical": ["technology", "platform", "compatibility", "技术", "平台"],
            "legal": ["legal", "compliance", "regulation", "法律", "合规"],
            "quality": ["quality", "standard", "requirement", "质量", "标准"]
        }
        
        problem_lower = problem_description.lower()
        
        for constraint_type, keywords in constraint_keywords.items():
            for keyword in keywords:
                if keyword in problem_lower:
                    constraints.append(constraint_type)
                    break
        
        return list(set(constraints))
    
    def extract_goals(self, problem_description: str) -> List[str]:
        """
        提取目标
        
        Args:
            problem_description: 问题描述
            
        Returns:
            目标列表
        """
        goals = []
        
        # 常见目标动词
        goal_verbs = [
            "solve", "fix", "implement", "create", "build", "develop",
            "improve", "optimize", "enhance", "increase", "reduce",
            "automate", "streamline", "simplify", "accelerate",
            "解决", "修复", "实现", "创建", "构建", "开发",
            "改进", "优化", "增强", "增加", "减少", "自动化",
            "提高", "提升", "制定", "分析", "研究", "学习",
            "需要", "要", "应该", "必须"
        ]
        
        # 提取包含目标动词的短语
        sentences = re.split(r'[.!?。！？,，]', problem_description)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for verb in goal_verbs:
                if verb in sentence_lower:
                    # 提取动词后的内容作为目标
                    pattern = rf"{verb}\s*([^.!?。！？,，]+)"
                    match = re.search(pattern, sentence_lower, re.IGNORECASE)
                    if match:
                        goal = match.group(1).strip()
                        if goal and len(goal) > 2:
                            # 清理目标文本
                            goal = re.sub(r'[但|但是|不过|然而].*', '', goal)  # 移除转折词后的内容
                            goal = goal.strip()
                            if goal:
                                goals.append(f"{verb} {goal}")
        
        # 如果没有找到明确目标，使用默认目标
        if not goals:
            problem_type = self.classify_problem(problem_description)
            if problem_type in self.problem_templates:
                default_goals = self.problem_templates[problem_type].get("goals", [])
                goals.extend(default_goals)
            else:
                # 添加通用目标
                goals.append("解决问题")
                goals.append("找到解决方案")
        
        return goals
    
    def estimate_complexity(self, problem_description: str) -> str:
        """
        估计问题复杂度
        
        Args:
            problem_description: 问题描述
            
        Returns:
            复杂度等级（low/medium/high）
        """
        # 简单启发式方法
        word_count = len(problem_description.split())
        constraint_count = len(self.extract_constraints(problem_description))
        goal_count = len(self.extract_goals(problem_description))
        
        complexity_score = (
            (word_count / 50) +  # 描述长度
            (constraint_count * 0.3) +  # 约束数量
            (goal_count * 0.2)  # 目标数量
        )
        
        if complexity_score < 0.5:
            return "low"
        elif complexity_score < 1.5:
            return "medium"
        else:
            return "high"
    
    def identify_subproblems(self, problem_description: str) -> List[Dict]:
        """
        识别子问题
        
        Args:
            problem_description: 问题描述
            
        Returns:
            子问题列表
        """
        subproblems = []
        
        # 常见连接词，可能表示多个问题
        connectors = [
            "and", "also", "additionally", "furthermore", "moreover",
            "besides", "同时", "另外", "此外", "而且", "并且"
        ]
        
        # 按连接词分割
        sentences = re.split(r'[.!?。！？]', problem_description)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # 检查是否包含多个部分
            for connector in connectors:
                if f" {connector} " in f" {sentence.lower()} ":
                    parts = re.split(rf"\b{connector}\b", sentence, flags=re.IGNORECASE)
                    for part in parts:
                        part = part.strip()
                        if part and len(part) > 5:
                            subproblems.append({
                                "description": part,
                                "type": self.classify_problem(part),
                                "complexity": self.estimate_complexity(part)
                            })
                    break
            else:
                # 单个问题
                subproblems.append({
                    "description": sentence,
                    "type": self.classify_problem(sentence),
                    "complexity": self.estimate_complexity(sentence)
                })
        
        return subproblems
    
    def analyze_problem(self, problem_description: str) -> Dict:
        """
        完整分析问题
        
        Args:
            problem_description: 问题描述
            
        Returns:
            分析报告
        """
        # 1. 问题分类
        problem_type = self.classify_problem(problem_description)
        
        # 2. 提取约束
        constraints = self.extract_constraints(problem_description)
        
        # 3. 提取目标
        goals = self.extract_goals(problem_description)
        
        # 4. 估计复杂度
        complexity = self.estimate_complexity(problem_description)
        
        # 5. 识别子问题
        subproblems = self.identify_subproblems(problem_description)
        
        # 6. 生成分析报告
        analysis_report = {
            "timestamp": datetime.now().isoformat(),
            "problem_description": problem_description,
            "problem_type": problem_type,
            "constraints": constraints,
            "goals": goals,
            "complexity": complexity,
            "subproblems": subproblems,
            "subproblem_count": len(subproblems),
            "recommended_approach": self._recommend_approach(problem_type, complexity)
        }
        
        # 保存到历史
        self.analysis_history.append(analysis_report)
        
        return analysis_report
    
    def _recommend_approach(self, problem_type: str, complexity: str) -> str:
        """
        推荐解决方法
        
        Args:
            problem_type: 问题类型
            complexity: 复杂度
            
        Returns:
            推荐方法
        """
        recommendations = {
            ("technical", "low"): "直接搜索解决方案，参考文档和示例代码",
            ("technical", "medium"): "分析问题根本原因，分步调试，参考社区讨论",
            ("technical", "high"): "需要系统分析，可能涉及架构调整，建议分阶段实施",
            ("business", "low"): "市场调研，分析竞争对手，制定简单策略",
            ("business", "medium"): "数据驱动分析，多方案对比，风险评估",
            ("business", "high"): "需要全面战略规划，可能涉及组织调整，建议咨询专家",
            ("operational", "low"): "流程优化，工具自动化，效率提升",
            ("operational", "medium"): "系统分析工作流，识别瓶颈，逐步改进",
            ("operational", "high"): "需要重新设计流程，可能涉及系统集成，建议分阶段实施"
        }
        
        key = (problem_type, complexity)
        return recommendations.get(key, "根据具体情况分析，制定个性化解决方案")
    
    def generate_analysis_summary(self, analysis_report: Dict) -> str:
        """
        生成分析摘要
        
        Args:
            analysis_report: 分析报告
            
        Returns:
            分析摘要
        """
        summary = f"""问题分析报告
================

问题描述: {analysis_report['problem_description']}

📋 分析结果:
• 问题类型: {analysis_report['problem_type']}
• 复杂度: {analysis_report['complexity']}
• 约束条件: {', '.join(analysis_report['constraints']) or '无明确约束'}
• 主要目标: {', '.join(analysis_report['goals'])}

🔍 子问题分析:
"""
        
        for i, subproblem in enumerate(analysis_report['subproblems'], 1):
            summary += f"  {i}. {subproblem['description']} ({subproblem['type']}, {subproblem['complexity']})\n"
        
        summary += f"""
🎯 推荐方法:
{analysis_report['recommended_approach']}

📊 统计信息:
• 子问题数量: {analysis_report['subproblem_count']}
• 分析时间: {analysis_report['timestamp']}
"""
        
        return summary

# 使用示例
if __name__ == "__main__":
    # 创建分析器实例
    analyzer = ProblemAnalyzer()
    
    # 测试问题分析
    test_problems = [
        "我们的Python程序运行很慢，需要优化性能，但时间有限只有一周",
        "公司用户留存率下降，需要制定增长策略，预算有限",
        "GitHub仓库创建失败，显示认证错误，需要尽快解决",
        "工作流程效率低下，需要自动化处理重复任务"
    ]
    
    print("问题分析测试:")
    print("=" * 60)
    
    for problem in test_problems:
        print(f"\n问题: {problem}")
        print("-" * 40)
        
        analysis = analyzer.analyze_problem(problem)
        summary = analyzer.generate_analysis_summary(analysis)
        
        print(summary)
        print("=" * 60)