#!/usr/bin/env python3
"""
智能搜索优化器
基于上下文和历史优化搜索查询
"""

import re
import json
from typing import List, Dict, Optional
import os

class SearchOptimizer:
    def __init__(self, knowledge_base_path: Optional[str] = None):
        """
        初始化搜索优化器
        
        Args:
            knowledge_base_path: 知识库文件路径
        """
        self.context_history = []
        self.search_patterns = self._load_search_patterns()
        
        if knowledge_base_path and os.path.exists(knowledge_base_path):
            self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        else:
            self.knowledge_base = {}
    
    def _load_search_patterns(self) -> Dict:
        """加载搜索模式"""
        patterns = {
            "technical": [
                "best practices", "tutorial", "guide", "documentation",
                "examples", "performance", "optimization", "troubleshooting"
            ],
            "business": [
                "strategy", "market analysis", "competition", "growth",
                "revenue", "profit", "scaling", "investment"
            ],
            "academic": [
                "research", "study", "paper", "thesis", "analysis",
                "methodology", "results", "conclusion"
            ],
            "news": [
                "latest", "update", "news", "announcement", "release",
                "trend", "forecast", "prediction"
            ]
        }
        return patterns
    
    def _load_knowledge_base(self, path: str) -> Dict:
        """加载知识库"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def add_context(self, context: str):
        """添加上下文"""
        self.context_history.append(context)
        # 保持最近10条上下文
        if len(self.context_history) > 10:
            self.context_history = self.context_history[-10:]
    
    def extract_keywords(self, query: str) -> List[str]:
        """
        提取关键词
        
        Args:
            query: 原始查询
            
        Returns:
            关键词列表
        """
        # 移除标点符号
        clean_query = re.sub(r'[^\w\s]', ' ', query)
        
        # 分割为单词
        words = clean_query.lower().split()
        
        # 移除停用词
        stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were',
            '的', '了', '在', '和', '与', '或', '但', '对', '为', '关于'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 1]
        
        return keywords
    
    def expand_with_context(self, keywords: List[str]) -> List[str]:
        """
        基于上下文扩展关键词
        
        Args:
            keywords: 基础关键词
            
        Returns:
            扩展后的关键词列表
        """
        expanded = keywords.copy()
        
        if not self.context_history:
            return expanded
        
        # 从最近上下文提取关键词
        recent_context = " ".join(self.context_history[-3:])
        context_keywords = self.extract_keywords(recent_context)
        
        # 添加相关的上下文关键词
        for word in context_keywords:
            if word not in expanded:
                expanded.append(word)
        
        return expanded
    
    def semantic_expansion(self, keywords: List[str]) -> List[str]:
        """
        语义扩展关键词
        
        Args:
            keywords: 基础关键词
            
        Returns:
            语义扩展后的关键词列表
        """
        expanded = keywords.copy()
        
        # 简单的同义词映射（实际应用中可以使用更复杂的NLP）
        synonym_map = {
            'python': ['programming', 'code', 'script', 'development'],
            'ai': ['artificial intelligence', 'machine learning', 'deep learning'],
            'search': ['query', 'lookup', 'find', 'discover'],
            'optimize': ['improve', 'enhance', 'boost', 'accelerate'],
            'problem': ['issue', 'challenge', 'difficulty', 'obstacle'],
            'solution': ['answer', 'resolution', 'fix', 'remedy'],
            'github': ['repository', 'repo', 'code hosting', 'version control'],
            'openclaw': ['ai assistant', 'automation', 'toolkit', 'framework']
        }
        
        for keyword in keywords:
            if keyword in synonym_map:
                for synonym in synonym_map[keyword]:
                    if synonym not in expanded:
                        expanded.append(synonym)
        
        return expanded
    
    def add_search_patterns(self, keywords: List[str], query_type: str = "technical") -> List[str]:
        """
        添加搜索模式关键词
        
        Args:
            keywords: 基础关键词
            query_type: 查询类型（technical/business/academic/news）
            
        Returns:
            添加模式后的关键词列表
        """
        expanded = keywords.copy()
        
        if query_type in self.search_patterns:
            patterns = self.search_patterns[query_type]
            for pattern in patterns:
                if pattern not in expanded:
                    expanded.append(pattern)
        
        return expanded
    
    def detect_query_type(self, query: str) -> str:
        """
        检测查询类型
        
        Args:
            query: 查询字符串
            
        Returns:
            查询类型
        """
        query_lower = query.lower()
        
        type_keywords = {
            "technical": ['python', 'code', 'programming', 'software', 'technical', 'bug', 'error', 
                         'github', 'docker', 'api', 'database', 'server', '配置', '优化', '性能',
                         '异步', '编程', '错误', '问题', '安装', '运行'],
            "business": ['business', 'market', 'revenue', 'profit', 'strategy', 'growth', '商业',
                        '增长', '策略', '分析', '市场', '收入', '利润', '公司', '用户', '客户',
                        '留存', '预算', '成本', '投资'],
            "academic": ['research', 'study', 'paper', 'thesis', 'academic', 'scholarly', '研究',
                        '学术', '论文', '学习', '教育', '理论', '方法', '分析'],
            "news": ['news', 'latest', 'update', 'announcement', 'trend', 'forecast', '新闻',
                    '最新', '更新', '趋势', '预测', '动态', '发展']
        }
        
        scores = {}
        for qtype, keywords in type_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in query_lower:
                    score += 1
            scores[qtype] = score
        
        # 找到最高分
        max_score = max(scores.values())
        if max_score > 0:
            for qtype, score in scores.items():
                if score == max_score:
                    return qtype
        
        return "general"
    
    def optimize_search_query(self, query: str, use_context: bool = True) -> str:
        """
        优化搜索查询
        
        Args:
            query: 原始查询
            use_context: 是否使用上下文
            
        Returns:
            优化后的查询字符串
        """
        # 1. 提取基础关键词
        keywords = self.extract_keywords(query)
        
        # 2. 检测查询类型
        query_type = self.detect_query_type(query)
        
        # 3. 基于上下文扩展
        if use_context:
            keywords = self.expand_with_context(keywords)
        
        # 4. 语义扩展
        keywords = self.semantic_expansion(keywords)
        
        # 5. 添加搜索模式
        keywords = self.add_search_patterns(keywords, query_type)
        
        # 6. 去重并生成查询字符串
        unique_keywords = list(set(keywords))
        
        # 确保原始查询的核心词在前
        core_keywords = self.extract_keywords(query)
        sorted_keywords = []
        
        # 先添加核心关键词
        for word in core_keywords:
            if word in unique_keywords:
                sorted_keywords.append(word)
                unique_keywords.remove(word)
        
        # 添加其他关键词
        sorted_keywords.extend(unique_keywords)
        
        # 生成查询字符串
        optimized_query = " ".join(sorted_keywords)
        
        return optimized_query
    
    def generate_search_report(self, original_query: str, optimized_query: str) -> Dict:
        """
        生成搜索优化报告
        
        Args:
            original_query: 原始查询
            optimized_query: 优化后的查询
            
        Returns:
            优化报告
        """
        original_keywords = self.extract_keywords(original_query)
        optimized_keywords = self.extract_keywords(optimized_query)
        
        added_keywords = [k for k in optimized_keywords if k not in original_keywords]
        removed_keywords = [k for k in original_keywords if k not in optimized_keywords]
        
        report = {
            "original_query": original_query,
            "optimized_query": optimized_query,
            "original_keywords": original_keywords,
            "optimized_keywords": optimized_keywords,
            "added_keywords": added_keywords,
            "removed_keywords": removed_keywords,
            "improvement_ratio": len(optimized_keywords) / max(1, len(original_keywords)),
            "query_type": self.detect_query_type(original_query)
        }
        
        return report

# 使用示例
if __name__ == "__main__":
    # 创建优化器实例
    optimizer = SearchOptimizer()
    
    # 添加上下文
    optimizer.add_context("我们在讨论AI助手的自主搜索能力")
    optimizer.add_context("需要提高问题解决的效率")
    
    # 测试查询优化
    test_queries = [
        "Python异步编程问题",
        "AI助手搜索优化",
        "GitHub仓库创建失败",
        "商业增长策略分析"
    ]
    
    print("搜索优化测试:")
    print("=" * 50)
    
    for query in test_queries:
        optimized = optimizer.optimize_search_query(query)
        report = optimizer.generate_search_report(query, optimized)
        
        print(f"原始查询: {query}")
        print(f"优化查询: {optimized}")
        print(f"查询类型: {report['query_type']}")
        print(f"改进比例: {report['improvement_ratio']:.2f}x")
        print(f"新增关键词: {', '.join(report['added_keywords'])}")
        print("-" * 50)