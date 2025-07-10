import streamlit as st
import os
from dotenv import load_dotenv
from src.pipeline_orchestrator import PipelineOrchestrator
import json
from datetime import datetime
import streamlit_markmap as st_markmap
import time

# 環境変数の読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="English Report Pipeline - Lawsy Inspired",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
if 'reports' not in st.session_state:
    st.session_state.reports = []

def main():
    """Lawsyの設計を参考にしたStreamlitアプリケーションのメイン関数"""
    
    # サイドバー
    with st.sidebar:
        st.title("📚 English Report Pipeline")
        st.markdown("*Lawsy-inspired AI Research Tool*")
        st.markdown("---")
        
        # 設定セクション
        st.subheader("⚙️ 設定")
        openai_api_key = st.text_input(
            "OpenAI API Key",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password",
            help="OpenAI APIキーを入力してください"
        )
        
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
            st.success("✅ APIキーが設定されました")
        else:
            st.warning("⚠️ APIキーを設定してください")
        
        # 検索設定
        st.subheader("🔍 検索設定")
        search_mode = st.selectbox(
            "検索モード",
            ["自動", "教育特化", "一般検索", "詳細検索"],
            help="検索戦略を選択してください"
        )
        
        st.markdown("---")
        
        # 履歴セクション
        st.subheader("📋 履歴")
        if st.session_state.reports:
            for i, report in enumerate(st.session_state.reports):
                if st.button(f"📄 {report['title'][:30]}...", key=f"history_{i}"):
                    st.session_state.current_report = report
                    st.rerun()
    
    # メインコンテンツ
    st.title("🎯 English Report Generator")
    st.markdown("**Lawsy-inspired AI Research Tool for English Education**")
    st.markdown("---")
    
    # タブの作成
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🆕 新規レポート", 
        "📊 レポート履歴", 
        "🗺️ マインドマップ", 
        "📈 分析ダッシュボード",
        "ℹ️ 使い方"
    ])
    
    with tab1:
        new_report_tab(search_mode)
    
    with tab2:
        history_tab()
    
    with tab3:
        mindmap_tab()
    
    with tab4:
        analytics_tab()
    
    with tab5:
        help_tab()

def new_report_tab(search_mode="自動"):
    """Lawsyの設計を参考にした新規レポート生成タブ"""
    
    # ヘッダー
    st.subheader("📝 Lawsy-inspired Report Generation")
    st.markdown("**STORM-based Research Pipeline for English Education**")
    
    # クエリ入力セクション
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_area(
            "英語学習に関するリサーチクエリを入力してください",
            placeholder="例: 英語の比較級と最上級の使い方を教えて",
            height=120,
            help="Lawsyの設計に基づき、詳細なリサーチクエリを入力してください"
        )
    
    with col2:
        st.markdown("### 🎯 クエリタイプ")
        query_type = st.selectbox(
            "クエリの種類",
            ["文法解説", "語彙学習", "読解指導", "リスニング", "ライティング", "その他"],
            help="クエリの種類を選択すると、より適切な検索戦略が適用されます"
        )
        
        st.markdown("### 🔍 検索戦略")
        st.info(f"**選択されたモード:** {search_mode}")
    
    # サンプルクエリ
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🎲 サンプルクエリ", type="secondary"):
            sample_queries = [
                "英語の比較級と最上級の使い方を教えて",
                "現在完了形と過去形の違いを説明して",
                "英語の前置詞の使い方をまとめて",
                "英語の仮定法の使い方を教えて",
                "英語の受動態の作り方を説明して"
            ]
            st.session_state.sample_query = sample_queries[0]
            st.rerun()
    
    with col2:
        if st.button("📚 教育特化クエリ", type="secondary"):
            education_queries = [
                "学習指導要領に基づく英語教育の指導法",
                "第二言語習得論における英語学習の理論",
                "応用言語学の観点からの英語教育",
                "英語教授法の最新トレンド",
                "英語教材研究の方法論"
            ]
            st.session_state.sample_query = education_queries[0]
            st.rerun()
    
    # サンプルクエリの表示
    if 'sample_query' in st.session_state:
        st.info(f"💡 サンプルクエリ: {st.session_state.sample_query}")
        query = st.session_state.sample_query
    
    # レポート生成
    if st.button("🚀 Lawsy-inspired レポート生成", type="primary") and query:
        if not os.getenv("OPENAI_API_KEY"):
            st.error("❌ OpenAI APIキーが設定されていません")
            return
        
        # プログレス表示の改善
        progress_container = st.container()
        status_container = st.container()
        metrics_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
        
        with status_container:
            status_text = st.empty()
        
        with metrics_container:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                education_metric = st.metric("教育ドメイン検索", "0")
            with col2:
                general_metric = st.metric("一般検索", "0")
            with col3:
                detailed_metric = st.metric("詳細検索", "0")
            with col4:
                time_metric = st.metric("処理時間", "0s")
        
        try:
            # パイプラインの実行
            orchestrator = PipelineOrchestrator()
            
            # Lawsyの設計に基づくステップ実行
            steps = [
                ("クエリ洗練", "Web検索用にクエリを最適化中..."),
                ("教育ドメイン検索", "英語教育関連サイトを検索中..."),
                ("一般Web検索", "一般的なWeb情報を収集中..."),
                ("クエリ展開", "詳細なリサーチトピックを生成中..."),
                ("詳細検索", "各トピックを詳細に検索中..."),
                ("情報統合", "検索結果を統合中..."),
                ("アウトライン生成", "包括的なアウトラインを作成中..."),
                ("レポート執筆", "リード文、本文、関連事項、結論を執筆中..."),
                ("マインドマップ生成", "構造化されたマインドマップを生成中...")
            ]
            
            start_time = time.time()
            
            for i, (step_name, step_desc) in enumerate(steps):
                progress = (i + 1) / len(steps)
                status_text.text(f"ステップ {i+1}/{len(steps)}: {step_desc}")
                progress_bar.progress(progress)
                time.sleep(0.5)  # 視覚的な進行表示
            
            # 実際のパイプライン実行
            result = orchestrator.run(query)
            
            # メトリクスの更新
            if 'search_stats' in result:
                stats = result['search_stats']
                education_metric.metric("教育ドメイン検索", stats.get('education_results', 0))
                general_metric.metric("一般検索", stats.get('general_results', 0))
                detailed_metric.metric("詳細検索", stats.get('detailed_results', 0))
                time_metric.metric("処理時間", f"{result.get('processing_time', 0):.1f}s")
            
            status_text.text("✅ Lawsy-inspired レポート生成完了！")
            
            # レポートの保存
            report_data = {
                'title': query[:50] + "..." if len(query) > 50 else query,
                'query': query,
                'report': result['report'],
                'mindmap': result['mindmap'],
                'timestamp': datetime.now().isoformat(),
                'id': len(st.session_state.reports),
                'search_stats': result.get('search_stats', {}),
                'processing_time': result.get('processing_time', 0),
                'query_type': query_type
            }
            
            st.session_state.reports.append(report_data)
            st.session_state.current_report = report_data
            
            # レポートの表示
            display_report(report_data)
            
        except Exception as e:
            st.error(f"❌ エラーが発生しました: {str(e)}")
            st.exception(e)

def history_tab():
    """レポート履歴タブ"""
    st.subheader("📊 レポート履歴")
    
    if not st.session_state.reports:
        st.info("📝 まだレポートがありません。新規レポートタブでレポートを生成してください。")
        return
    
    # レポート一覧の表示
    for i, report in enumerate(st.session_state.reports):
        with st.expander(f"📄 {report['title']} - {report['timestamp'][:19]}"):
            st.markdown(f"**クエリ:** {report['query']}")
            st.markdown("---")
            st.markdown(report['report'])

def mindmap_tab():
    """マインドマップタブ"""
    st.subheader("🗺️ マインドマップ")
    
    if not st.session_state.reports:
        st.info("📝 まだレポートがありません。新規レポートタブでレポートを生成してください。")
        return
    
    # 最新のレポートのマインドマップを表示
    latest_report = st.session_state.reports[-1]
    
    if 'mindmap' in latest_report:
        st.markdown("### 📊 最新レポートのマインドマップ")
        
        # マインドマップデータをMarkmap形式に変換
        mindmap_content = create_markmap_content(latest_report['mindmap'])
        
        # Streamlit Markmapで表示
        st_markmap.markmap(mindmap_content, height=600)
        
        # ダウンロードボタン
        st.download_button(
            label="📥 マインドマップをダウンロード",
            data=mindmap_content,
            file_name=f"mindmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    else:
        st.warning("⚠️ このレポートにはマインドマップが含まれていません")

def create_markmap_content(mindmap_data):
    """マインドマップデータをMarkmap形式に変換"""
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

def analytics_tab():
    """Lawsyの設計を参考にした分析ダッシュボードタブ"""
    st.subheader("📈 Lawsy-inspired Analytics Dashboard")
    
    if not st.session_state.reports:
        st.info("📝 まだレポートがありません。新規レポートタブでレポートを生成してください。")
        return
    
    # 統計情報の計算
    total_reports = len(st.session_state.reports)
    total_processing_time = sum([r.get('processing_time', 0) for r in st.session_state.reports])
    avg_processing_time = total_processing_time / total_reports if total_reports > 0 else 0
    
    # クエリタイプの分析
    query_types = {}
    for report in st.session_state.reports:
        query_type = report.get('query_type', 'その他')
        query_types[query_type] = query_types.get(query_type, 0) + 1
    
    # 検索統計の集計
    total_education_searches = sum([r.get('search_stats', {}).get('education_results', 0) for r in st.session_state.reports])
    total_general_searches = sum([r.get('search_stats', {}).get('general_results', 0) for r in st.session_state.reports])
    total_detailed_searches = sum([r.get('search_stats', {}).get('detailed_results', 0) for r in st.session_state.reports])
    
    # メトリクス表示
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("総レポート数", total_reports)
    
    with col2:
        st.metric("平均処理時間", f"{avg_processing_time:.1f}s")
    
    with col3:
        st.metric("総検索回数", total_education_searches + total_general_searches + total_detailed_searches)
    
    with col4:
        st.metric("教育特化検索", total_education_searches)
    
    # グラフ表示
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 クエリタイプ分布")
        if query_types:
            st.bar_chart(query_types)
        else:
            st.info("クエリタイプのデータがありません")
    
    with col2:
        st.subheader("🔍 検索戦略分布")
        search_data = {
            "教育特化検索": total_education_searches,
            "一般検索": total_general_searches,
            "詳細検索": total_detailed_searches
        }
        st.bar_chart(search_data)
    
    # 詳細分析
    st.subheader("📋 詳細分析")
    
    # 最新のレポートの詳細情報
    if st.session_state.reports:
        latest_report = st.session_state.reports[-1]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 最新レポート情報")
            st.write(f"**クエリ:** {latest_report['query']}")
            st.write(f"**クエリタイプ:** {latest_report.get('query_type', '不明')}")
            st.write(f"**処理時間:** {latest_report.get('processing_time', 0):.1f}秒")
            st.write(f"**生成日時:** {latest_report['timestamp'][:19]}")
        
        with col2:
            st.markdown("### 🔍 検索統計")
            stats = latest_report.get('search_stats', {})
            st.write(f"**教育ドメイン検索:** {stats.get('education_results', 0)}件")
            st.write(f"**一般検索:** {stats.get('general_results', 0)}件")
            st.write(f"**詳細検索:** {stats.get('detailed_results', 0)}件")
            st.write(f"**総トピック数:** {stats.get('total_topics', 0)}件")
    
    # パフォーマンス分析
    st.subheader("⚡ パフォーマンス分析")
    
    processing_times = [r.get('processing_time', 0) for r in st.session_state.reports]
    if processing_times:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("最短処理時間", f"{min(processing_times):.1f}s")
        
        with col2:
            st.metric("最長処理時間", f"{max(processing_times):.1f}s")
        
        with col3:
            st.metric("中央値", f"{sorted(processing_times)[len(processing_times)//2]:.1f}s")

def help_tab():
    """Lawsyの設計を参考にした使い方タブ"""
    st.subheader("ℹ️ Lawsy-inspired Usage Guide")
    
    st.markdown("""
    ### 📚 English Report Pipeline - Lawsy Inspired
    
    #### 🎯 概要
    このアプリケーションは、Lawsyの設計を参考にしたAIを活用した英語学習レポート自動生成ツールです。
    STORMベースの処理フローを採用し、英語教育に特化した検索戦略を実装しています。
    
    #### 🔬 STORM-based Research Pipeline
    1. **Synthesis (統合)**: 複数の情報源から情報を収集・統合
    2. **Transformation (変換)**: クエリを最適化し、検索戦略を決定
    3. **Organization (整理)**: 収集した情報を構造化
    4. **Refinement (洗練)**: レポートの品質を向上
    5. **Mapping (マッピング)**: マインドマップで視覚化
    
    #### 📝 レポート生成の手順
    1. **クエリ入力**: 英語学習に関する詳細なリサーチクエリを入力
    2. **検索戦略選択**: 教育特化、一般検索、詳細検索から選択
    3. **STORM処理**: AIが自動的に情報を収集・分析・統合
    4. **結果表示**: 包括的なレポートとマインドマップを表示
    
    #### 🗺️ マインドマップ機能
    - レポートの内容を階層的に視覚化
    - 関連する概念を構造的に表示
    - 学習の理解促進と記憶定着を支援
    
    #### 📊 分析ダッシュボード
    - レポート生成の統計情報を表示
    - 検索戦略の効果を分析
    - パフォーマンス指標を監視
    
    #### ⚙️ 設定
    - OpenAI APIキーの設定が必要
    - 検索モードの選択が可能
    - サイドバーから設定可能
    
    #### 🔍 検索戦略
    - **自動**: システムが最適な戦略を自動選択
    - **教育特化**: 英語教育関連サイトを重点的に検索
    - **一般検索**: 幅広いWeb情報を収集
    - **詳細検索**: 特定のトピックを深く掘り下げ
    """)

def display_report(report_data):
    """レポートの表示"""
    st.subheader("📄 生成されたレポート")
    
    # レポート情報
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**クエリ:** {report_data['query']}")
    
    with col2:
        st.markdown(f"**生成日時:** {report_data['timestamp'][:19]}")
    
    st.markdown("---")
    
    # レポート本文の表示
    st.markdown(report_data['report'])
    
    # マインドマップの表示
    if 'mindmap' in report_data:
        st.markdown("### 🗺️ マインドマップ")
        mindmap_content = create_markmap_content(report_data['mindmap'])
        st_markmap.markmap(mindmap_content, height=400)
    
    # ダウンロードボタン
    report_text = f"""
# English Report Pipeline

## クエリ
{report_data['query']}

## 生成日時
{report_data['timestamp']}

## レポート
{report_data['report']}
    """
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 レポートをダウンロード",
            data=report_text,
            file_name=f"english_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    
    with col2:
        if 'mindmap' in report_data:
            mindmap_content = create_markmap_content(report_data['mindmap'])
            st.download_button(
                label="🗺️ マインドマップをダウンロード",
                data=mindmap_content,
                file_name=f"mindmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main() 