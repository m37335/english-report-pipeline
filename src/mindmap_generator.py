import dspy
from typing import Dict, List, Any
import yaml
import json

class MindmapGenerator(dspy.Signature):
    """マインドマップ生成用のDSPyシグネチャ"""
    
    report_content = dspy.InputField(desc="生成されたレポートの内容")
    
    mindmap_data = dspy.OutputField(desc="マインドマップ用の階層構造データ（JSON形式）")

class MindmapGeneratorModule:
    """マインドマップ生成モジュール"""
    
    def __init__(self):
        self.generator = dspy.ChainOfThought(MindmapGenerator)
    
    def generate_mindmap(self, report_content: str) -> Dict[str, Any]:
        """
        レポート内容からマインドマップデータを生成
        
        Args:
            report_content: レポートの内容
            
        Returns:
            マインドマップ用の階層構造データ
        """
        try:
            # DSPyでマインドマップデータを生成
            result = self.generator(report_content=report_content)
            
            # JSON文字列をパース
            mindmap_data = json.loads(result.mindmap_data)
            
            return mindmap_data
            
        except Exception as e:
            # エラー時はデフォルトのマインドマップ構造を返す
            return self._create_default_mindmap(report_content)
    
    def _create_default_mindmap(self, report_content: str) -> Dict[str, Any]:
        """デフォルトのマインドマップ構造を作成"""
        return {
            "name": "English Learning Report",
            "children": [
                {
                    "name": "Main Topics",
                    "children": [
                        {"name": "Grammar", "children": []},
                        {"name": "Vocabulary", "children": []},
                        {"name": "Usage", "children": []}
                    ]
                },
                {
                    "name": "Key Points",
                    "children": [
                        {"name": "Important Rules", "children": []},
                        {"name": "Examples", "children": []},
                        {"name": "Practice Tips", "children": []}
                    ]
                }
            ]
        }
    
    def create_markmap_content(self, mindmap_data: Dict[str, Any]) -> str:
        """
        マインドマップデータをMarkmap形式に変換
        
        Args:
            mindmap_data: マインドマップデータ
            
        Returns:
            Markmap形式のコンテンツ
        """
        def _convert_node(node):
            if isinstance(node, dict):
                name = node.get('name', '')
                children = node.get('children', [])
                
                if children:
                    return f"# {name}\n" + "\n".join([_convert_node(child) for child in children])
                else:
                    return f"## {name}"
            else:
                return f"## {str(node)}"
        
        return _convert_node(mindmap_data) 