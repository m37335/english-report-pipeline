from .llm_client import LLMClient
import re

class QueryExpander:
    """
    洗練されたクエリを元に、検索トピックを生成するクラス。
    """
    def __init__(self):
        """
        プロンプトを初期化する。
        """
        self.prompt_template = """あなたは日本の英語教育に精通した専門家です。
下記のクエリー（高校入試や教科書からの英文を含む可能性があります）に関して、事前にWeb検索をして簡単に下調べしてあります。
Web検索結果もふまえ、クエリーに関する英語教育的な解説・分析文書を作成するために必要な情報を検索しようとしています。

解説・分析に必要な情報を適切にヒットさせきるための検索トピックを以下の形式でリストアップしてください。

出力フォーマット：
- xxx
- yyy
- ...
- zzz

検索トピックをリストアップするにあたり、以下の条件を遵守してください。

- クエリーの背景にある英語教育的な論点を深く考察すること
- クエリーに対する解説・分析を行うのに必要な情報（英文の文法構造、語彙の難易度、構文の複雑性、読解のポイント、指導上の留意点、関連する学習指導要領（英語）、第二言語習得論、応用言語学、英語教授法、教材研究、国内外の事例、および入力された英文に含まれる具体的な文法項目（例: 現在完了進行形、関係代名詞、仮定法など）に関する解説）が揃うように検索トピックをリストアップしてください
- 検索トピックは可能な限り互いに重複せず、個別に調査可能な形にしてください。 **self-contained** であるべきです
- 検索トピックは英語教育分野の文脈に準拠した具体的なものにしてください（短文または具体的な専門用語）
- 検索精度を高めるため、第二言語習得論、応用言語学、英語教授法などの専門用語や、関連するキーワードを含めてください
- 検索トピックをナンバリングする必要はありません。
- 検索トピックの個数は多くても10個までにしてください。

クエリー: {refined_query}
"""
        self.llm_client = LLMClient()

    def expand(self, refined_query: str) -> list[str]:
        """
        洗練されたクエリを受け取り、プロンプトに基づいて検索トピックのリストを生成する。

        Args:
            refined_query: 洗練された検索クエリ

        Returns:
            検索トピックのリスト
        """
        try:
            full_prompt = self.prompt_template.format(refined_query=refined_query)
            response_text = self.llm_client.generate_text(full_prompt, max_tokens=1000, temperature=0.4)
            
            # レスポンスの妥当性をチェック
            if self.llm_client.validate_response(response_text):
                # レスポンスから検索トピックを抽出
                search_topics = self._extract_topics(response_text)
                print(f"Expanding query for: {refined_query}")
                print(f"Expanded to topics: {search_topics}")
                return search_topics
            else:
                # フォールバック: 仮実装
                print(f"LLM response validation failed, using fallback for: {refined_query}")
                return self._get_fallback_topics(refined_query)
                
        except Exception as e:
            print(f"Error in query expansion: {e}")
            # エラー時のフォールバック
            return self._get_fallback_topics(refined_query)
    
    def _extract_topics(self, response_text: str) -> list[str]:
        """レスポンステキストから検索トピックを抽出する"""
        topics = []
        lines = response_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            # "- "で始まる行を検索トピックとして抽出
            if line.startswith('- '):
                topic = line[2:].strip()
                if topic:
                    topics.append(topic)
        
        return topics if topics else self._get_fallback_topics("")
    
    def _get_fallback_topics(self, refined_query: str) -> list[str]:
        """フォールバック用の検索トピックを返す"""
        return [
            "英文法 現在完了進行形 解説",
            "現在完了進行形 指導上の留意点",
            "第二言語習得論 継続相",
            "学習指導要領 英語 現在完了進行形",
            "応用言語学 時制と相",
            "英語教材研究 現在完了進行形 導入",
            "have been -ing ニュアンス 違い",
        ]
