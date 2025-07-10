import streamlit as st
import os
from dotenv import load_dotenv
from src.pipeline_orchestrator import PipelineOrchestrator
import json
from datetime import datetime
import streamlit_markmap as st_markmap

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
    tab1, tab2, tab3, tab4 = st.tabs(["🆕 新規レポート", "📊 レポート履歴", "🗺️ マインドマップ", "ℹ️ 使い方"])
    
    with tab1:
        new_report_tab()
    
    with tab2:
        history_tab()
    
    with tab3:
        mindmap_tab()
    
    with tab4:
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
                status_text.text("ステップ 1/6: クエリを洗練中...")
                progress_bar.progress(17)
                
                status_text.text("ステップ 2/6: 検索トピックを生成中...")
                progress_bar.progress(33)
                
                status_text.text("ステップ 3/6: 外部情報を収集中...")
                progress_bar.progress(50)
                
                status_text.text("ステップ 4/6: アウトラインを作成中...")
                progress_bar.progress(67)
                
                status_text.text("ステップ 5/6: レポートを執筆中...")
                progress_bar.progress(83)
                
                status_text.text("ステップ 6/6: マインドマップを生成中...")
                progress_bar.progress(100)
                
                result = orchestrator.run(query)
                
                status_text.text("✅ レポート生成完了！")
                
                # レポートの保存
                report_data = {
                    'title': query[:50] + "..." if len(query) > 50 else query,
                    'query': query,
                    'report': result['report'],
                    'mindmap': result['mindmap'],
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
       - マインドマップタブで視覚的な学習マップを確認できます
    
    ### 🔧 技術仕様
    
    - **AIモデル**: OpenAI GPT-4
    - **フレームワーク**: Streamlit
    - **アーキテクチャ**: モジュラー設計（Lawsy設計思想採用）
    - **マインドマップ**: Markmap形式で視覚化
    
    ### 📚 対応トピック
    
    - 英文法の解説
    - 英語表現の使い方
    - 英語学習のコツ
    - 英語試験対策
    - その他英語学習関連
    
    ### 🚀 新機能
    
    - **マインドマップ機能**: レポート内容を視覚的に整理
    - **ダウンロード機能**: レポートとマインドマップの保存
    - **履歴管理**: 過去のレポートの再表示
    
    ### 🗺️ マインドマップについて
    
    マインドマップは、レポートの内容を階層構造で視覚化したものです。
    - 主要なトピックを中心に配置
    - 関連する概念を枝分かれで表現
    - 学習の流れを直感的に理解
    
    ### 🚀 今後の予定
    
    - 音声読み上げ機能
    - 学習進捗の追跡
    - カスタマイズ可能なテーマ
    - インタラクティブなマインドマップ
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