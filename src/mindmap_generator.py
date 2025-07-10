from typing import Dict, List, Any
import json
from .llm_client import LLMClient

class MindmapGeneratorModule:
    """マインドマップ生成モジュール"""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.prompt_template = """あなたは英語教育の専門家で、レポート内容を構造化してマインドマップを作成するのが得意です。
以下のレポート内容を分析し、階層構造を持つマインドマップデータをJSON形式で生成してください。

マインドマップの構造は以下の形式に従ってください：
- メインノード（レポートのタイトル）
- サブノード（主要な章やセクション）
- さらに細かいノード（詳細な内容）

出力は有効なJSON形式で、以下の構造にしてください：
{
  "name": "メインノード名",
  "children": [
    {
      "name": "サブノード名",
      "children": [
        {"name": "詳細ノード名", "children": []},
        {"name": "詳細ノード名2", "children": []}
      ]
    }
  ]
}

レポート内容：
{report_content}
"""
    
    def generate_mindmap(self, report_content: str) -> Dict[str, Any]:
        """
        レポート内容からマインドマップデータを生成
        
        Args:
            report_content: レポートの内容
            
        Returns:
            マインドマップ用の階層構造データ
        """
        try:
            # LLMでマインドマップデータを生成
            prompt = self.prompt_template.format(report_content=report_content[:2000])  # 長すぎる場合は切り詰める
            response = self.llm_client.generate_structured_output(prompt, output_format="json")
            
            # JSON文字列をパース
            mindmap_data = json.loads(response)
            
            # 基本的な構造チェック
            if self._validate_mindmap_structure(mindmap_data):
                return mindmap_data
            else:
                return self._create_default_mindmap(report_content)
            
        except Exception as e:
            print(f"Error generating mindmap: {e}")
            # エラー時はデフォルトのマインドマップ構造を返す
            return self._create_default_mindmap(report_content)
    
    def _validate_mindmap_structure(self, mindmap_data: Dict[str, Any]) -> bool:
        """マインドマップ構造の妥当性をチェック"""
        try:
            if not isinstance(mindmap_data, dict):
                return False
            
            if 'name' not in mindmap_data:
                return False
            
            if 'children' in mindmap_data and not isinstance(mindmap_data['children'], list):
                return False
            
            return True
        except:
            return False
    
    def _create_default_mindmap(self, report_content: str) -> Dict[str, Any]:
        """デフォルトのマインドマップ構造を作成"""
        # レポート内容からタイトルを抽出
        lines = report_content.split('\n')
        title = "English Learning Report"
        
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        return {
            "name": title,
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