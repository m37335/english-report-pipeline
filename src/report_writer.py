class ReportWriter:
    """
    アウトラインと検索結果を元に、完全なレポートを執筆するクラス。
    リード文、本文、関連事項、結論を個別に生成して結合する。
    """
    def __init__(self):
        self.lead_prompt = """あなたは英語教育問題に精通し、分かりやすい解説記事を書くことに定評のある信頼できるライターです。
下記のクエリーに関する調査レポートの、タイトルの直後に表示する簡潔なリード文を生成してください。
リード文は、レポート全体の要旨、特に英語教育的な観点からの主要な論点や分析の方向性を含めた、140〜280文字程度の簡潔な文章にしてください。

クエリー: {refined_query}
"""

        self.section_prompt = """あなたは日本の英語教育に精通し、客観的なデータと英語教育理論に基づいた分かりやすい解説を書くことに定評のある信頼できるライターです。
下記のクエリー（高校入試や教科書からの英文を含む可能性があります）に関するレポートのアウトラインに基づき、各章の本文を執筆してください。
アウトラインの中にある引用番号は漏れることなく必ず参照し、収集された情報源の内容を適切に解釈しながら、各節ごとに400字以上で解説を記載してください。
解説は緻密かつ包括的で、情報源に基づいたものであることが望ましいです。特に、入力された英文がある場合は、その英文の具体的な分析（文法、語彙、構文、読解ポイントなど）を詳細に含めてください。英語教育に詳しくない人向けにわかりやすくかみ砕いて説明することも重要です。必要に応じて、関連する英語教育理論、歴史的背景、国内外の事例、最新の統計データなどを盛り込んでください。
なお、内容の信頼性が重要なので、必ず情報源にあたり、下記指示にあるように引用をするのを忘れないで下さい。
1. アウトラインの"# Title"、"## Title"、"### Title"のタイトルは変更しないでください。
2. 必ず情報源の情報に基づき記載し、ハルシネーションに気をつけること。
   記載の根拠となる参照すべき情報源は "...です[4][1][27]。" "...ます[21][9]。" のように明示してください。
3. 正しく引用が明示されているほどあなたの解説は高く評価されます。
4. 内容に応じて箇条書きを適切に配置し、読者の理解度を深めてください。
5. 日本語の「ですます調」で解説を書いてください。

【情報源】
{search_results_text}

【アウトライン】
{outline}

【クエリー】
{refined_query}
"""

        self.related_topics_prompt = """あなたは英文法に精通した専門家です。
下記の英文を分析し、含まれる主要な文法項目を特定してください。
特定した各文法項目について、以下の形式で簡潔に解説してください。

出力フォーマット：
- **[文法項目名]**: [その文法項目の簡潔な説明]。例: [提供された英文からの該当箇所]

例:
- **現在完了進行形**: 過去のある時点から現在まで継続している動作を表します。例: "We have been discussing it since last week."
- **関係代名詞**: 名詞を修飾する節を導きます。例: "It's a song about friendship." (ここでは関係代名詞が省略されているが、概念として関連する)

検索トピックをリストアップするにあたり、以下の条件を遵守してください。
- 英文に含まれる主要な文法項目を網羅的に特定すること。
- 各文法項目の説明は、高校生が理解できるレベルで簡潔に記述すること。
- 提供された英文中の具体的な箇所を例として引用し、解説と関連付けること。
- 文法項目は、`_GrammarDictionary_Index.md`に記載されているような一般的な文法分類に従うこと。
- 箇条書き形式で出力すること。

【英文】
{initial_query}
"""

        self.conclusion_prompt = """あなたは英語教育問題に精通し、未来志向の提言をすることに定評のある信頼できるライターです。
レポートのドラフトを踏まえて、レポート全体の要約を本文とはできるだけ異なる表現で記載しつつ、英語教育的な観点からの今後の展望や課題、考えられる対策を含んだ結論部を生成します。
最低でも400字以上、可能なら600字以上記載してください。
結論の文章部分のみ生成し、"## 結論" のようなヘッダは入れないでください。

【レポートドラフト】
{draft}
"""

    def _format_search_results(self, search_results: dict[str, str]) -> str:
        """検索結果の辞書を番号付きリストの文字列にフォーマットする"""
        formatted_text = ""
        for i, (topic, result) in enumerate(search_results.items()):
            formatted_text += f"[{i+1}] Topic: {topic}\nResult: {result}\n\n"
        return formatted_text.strip()

    def write(self, outline: str, search_results: dict[str, str], initial_query: str, refined_query: str) -> str:
        """
        アウトラインと検索結果を元に、完全なレポートを生成する。

        Args:
            outline: Markdown形式のアウトライン
            search_results: Web検索結果
            initial_query: ユーザーの初期クエリ
            refined_query: 洗練された検索クエリ

        Returns:
            完全なMarkdownレポート
        """
        print("Writing final report...")
        # search_results_text = self._format_search_results(search_results)

        # 1. リード文生成 (仮実装)
        # lead_text = llm_api.call(self.lead_prompt.format(refined_query=refined_query))
        lead_text = f"この記事では、「{refined_query}」について、英語教育の観点から深く掘り下げ、その指導法や理論的背景を解説します。"
        print("  - Lead section written.")

        # 2. 本文生成 (仮実装)
        # body_text = llm_api.call(self.section_prompt.format(...))
        # アウトラインからタイトルを除いた本文部分を仮作成
        body_text = "\n".join(outline.split("\n")[1:]) + "\n\n(ここに各章の詳細な解説が入ります...)"
        print("  - Body sections written.")

        # 3. 関連文法事項の生成 (仮実装)
        # related_topics_text = llm_api.call(self.related_topics_prompt.format(initial_query=initial_query))
        related_topics_text = "- **主要文法1**: 解説...\n- **主要文法2**: 解説..."
        print("  - Related topics section written.")

        # 4. 結論生成 (仮実装)
        # draft = outline.split('\n')[0] + "\n" + lead_text + "\n" + body_text
        # conclusion_text = llm_api.call(self.conclusion_prompt.format(draft=draft))
        conclusion_text = "本レポートでは...を明らかにし、今後の英語教育における課題と展望を示しました。"
        print("  - Conclusion section written.")

        # 5. 全てのパートを結合
        title = outline.split('\n')[0]
        final_report = (
            f"{title}\n\n"
            f"{lead_text}\n\n"
            f"{body_text}\n\n"
            f"## 関連文法事項\n{related_topics_text}\n\n"
            f"## 結論\n{conclusion_text}"
        )
        print("Final report assembled.")

        return final_report
