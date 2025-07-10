import streamlit as st
import os
from dotenv import load_dotenv
from src.pipeline_orchestrator import PipelineOrchestrator
import json
from datetime import datetime

# 環境変数の読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="English Report Pipeline",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
if 'reports' not in st.session_state:
    st.session_state.reports = []

def main():
    """Streamlitアプリケーションのメイン関数"""
    
    # サイドバー
    with st.sidebar:
        st.title("📚 English Report Pipeline")
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
    st.markdown("AIを活用した英語学習レポート自動生成システム")
    
    # タブの作成
    tab1, tab2, tab3 = st.tabs(["🆕 新規レポート", "📊 レポート履歴", "ℹ️ 使い方"])
    
    with tab1:
        new_report_tab()
    
    with tab2:
        history_tab()
    
    with tab3:
        help_tab()

def new_report_tab():
    """新規レポート生成タブ"""
    
    # クエリ入力
    st.subheader("📝 レポート生成")
    
    query = st.text_area(
        "英語学習に関するクエリを入力してください",
        placeholder="例: 英語の比較級と最上級の使い方を教えて",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        generate_button = st.button("🚀 レポート生成", type="primary")
    
    with col2:
        if st.button("🎲 サンプルクエリ"):
            sample_queries = [
                "英語の比較級と最上級の使い方を教えて",
                "現在完了形と過去形の違いを説明して",
                "英語の前置詞の使い方をまとめて",
                "英語の仮定法の使い方を教えて",
                "英語の受動態の作り方を説明して"
            ]
            st.session_state.sample_query = sample_queries[0]
            st.rerun()
    
    # サンプルクエリの表示
    if 'sample_query' in st.session_state:
        st.info(f"💡 サンプルクエリ: {st.session_state.sample_query}")
        query = st.session_state.sample_query
    
    # レポート生成
    if generate_button and query:
        if not os.getenv("OPENAI_API_KEY"):
            st.error("❌ OpenAI APIキーが設定されていません")
            return
        
        with st.spinner("🔄 レポートを生成中..."):
            try:
                # プログレスバーの作成
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # パイプラインの実行
                orchestrator = PipelineOrchestrator()
                
                # 各ステップの進行状況を表示
                status_text.text("ステップ 1/5: クエリを洗練中...")
                progress_bar.progress(20)
                
                status_text.text("ステップ 2/5: 検索トピックを生成中...")
                progress_bar.progress(40)
                
                status_text.text("ステップ 3/5: 外部情報を収集中...")
                progress_bar.progress(60)
                
                status_text.text("ステップ 4/5: アウトラインを作成中...")
                progress_bar.progress(80)
                
                status_text.text("ステップ 5/5: レポートを執筆中...")
                progress_bar.progress(90)
                
                final_report = orchestrator.run(query)
                
                progress_bar.progress(100)
                status_text.text("✅ レポート生成完了！")
                
                # レポートの保存
                report_data = {
                    'title': query[:50] + "..." if len(query) > 50 else query,
                    'query': query,
                    'report': final_report,
                    'timestamp': datetime.now().isoformat(),
                    'id': len(st.session_state.reports)
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

def help_tab():
    """使い方タブ"""
    st.subheader("ℹ️ 使い方")
    
    st.markdown("""
    ### 🎯 このアプリについて
    
    English Report Pipelineは、AIを活用して英語学習に特化したレポートを自動生成するシステムです。
    
    ### 📝 使い方
    
    1. **APIキーの設定**
       - サイドバーでOpenAI APIキーを入力してください
    
    2. **クエリの入力**
       - 英語学習に関する質問やトピックを入力してください
       - 例: "英語の比較級と最上級の使い方を教えて"
    
    3. **レポート生成**
       - "レポート生成"ボタンをクリック
       - AIが自動的に情報を収集し、構造化されたレポートを作成します
    
    4. **結果の確認**
       - 生成されたレポートは履歴に保存されます
       - いつでも過去のレポートを確認できます
    
    ### 🔧 技術仕様
    
    - **AIモデル**: OpenAI GPT-4
    - **フレームワーク**: Streamlit
    - **アーキテクチャ**: モジュラー設計（Lawsy設計思想採用）
    
    ### 📚 対応トピック
    
    - 英文法の解説
    - 英語表現の使い方
    - 英語学習のコツ
    - 英語試験対策
    - その他英語学習関連
    
    ### 🚀 今後の予定
    
    - マインドマップ機能の追加
    - 音声読み上げ機能
    - 学習進捗の追跡
    - カスタマイズ可能なテーマ
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
    
    st.download_button(
        label="📥 レポートをダウンロード",
        data=report_text,
        file_name=f"english_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )

if __name__ == "__main__":
    main() 