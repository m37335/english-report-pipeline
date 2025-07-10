import os
import openai
from typing import Optional
from dotenv import load_dotenv
import logging

# 環境変数を読み込み
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    """
    OpenAI APIとの連携を行うクライアントクラス
    """
    
    def __init__(self):
        """LLMクライアントの初期化"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # OpenAIクライアントの初期化
        self.client = openai.OpenAI(api_key=self.api_key)
        logger.info(f"LLMClient initialized with model: {self.model}")
    
    def generate_text(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """
        プロンプトを送信してテキストを生成する
        
        Args:
            prompt: 生成用のプロンプト
            max_tokens: 最大トークン数
            temperature: 生成の多様性（0.0-1.0）
            
        Returns:
            生成されたテキスト
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            generated_text = response.choices[0].message.content
            logger.info(f"Generated text successfully (tokens: {response.usage.total_tokens})")
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise
    
    def generate_structured_output(self, prompt: str, output_format: str = "text") -> str:
        """
        構造化された出力を生成する
        
        Args:
            prompt: 生成用のプロンプト
            output_format: 出力形式（"text", "json", "markdown"など）
            
        Returns:
            生成された構造化テキスト
        """
        # 出力形式に応じてプロンプトを調整
        if output_format == "json":
            prompt += "\n\n出力は有効なJSON形式でお願いします。"
        elif output_format == "markdown":
            prompt += "\n\n出力はMarkdown形式でお願いします。"
        
        return self.generate_text(prompt, max_tokens=3000, temperature=0.5)
    
    def validate_response(self, response: str, expected_format: str = "text") -> bool:
        """
        生成されたレスポンスの妥当性を検証する
        
        Args:
            response: 生成されたレスポンス
            expected_format: 期待される形式
            
        Returns:
            妥当性の結果
        """
        if not response or response.strip() == "":
            return False
        
        if expected_format == "json":
            try:
                import json
                json.loads(response)
                return True
            except:
                return False
        
        return True 