from .llm_client import LLMClient

class QueryRefiner:
    """
    ユーザーのクエリを洗練し、検索に適したクエリーを生成するクラス。
    """
    def __init__(self):
        """
        プロンプトを初期化する。
        """
        self.prompt_template = """あなたはWebの扱いに長けた優秀な英語教育アナリストです。
下記のユーザーのクエリー（高校入試や教科書からの英文を含む可能性があります）にたいして、その英文や関連する英語教育の観点からの解説を与えるのに適した簡潔な検索クエリーを一つ作ってください。
なお、作成にあたっては下記を守って下さい。

- 英語教育の観点からの解説に繋がるクエリーをつくること
- あなたの作ったクエリーは可能な限りユーザーが作ったクエリーの意図と過不足なく一致させること
- クエリーは日本語で作成すること
- Web検索に最適化すること
- 簡潔であること

ユーザーのクエリー: {user_query}
"""
        self.llm_client = LLMClient()

    def refine(self, user_query: str) -> str:
        """
        ユーザーのクエリを受け取り、プロンプトに基づいて洗練された検索クエリを生成する。

        Args:
            user_query: ユーザーからの初期クエリ

        Returns:
            洗練された検索クエリ
        """
        try:
            full_prompt = self.prompt_template.format(user_query=user_query)
            refined_query = self.llm_client.generate_text(full_prompt, max_tokens=500, temperature=0.3)
            
            # レスポンスの妥当性をチェック
            if self.llm_client.validate_response(refined_query):
                print(f"Refining query for: {user_query}")
                print(f"Refined query: {refined_query}")
                return refined_query.strip()
            else:
                # フォールバック: 仮実装
                print(f"LLM response validation failed, using fallback for: {user_query}")
                return f'「{user_query}」に関する英語教育の観点からの解説'
                
        except Exception as e:
            print(f"Error in query refinement: {e}")
            # エラー時のフォールバック
            return f'「{user_query}」に関する英語教育の観点からの解説'
