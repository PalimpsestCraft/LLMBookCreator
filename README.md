# LLM Book Creator
- LLM Book Creator は、指定したテーマに基づいて本を生成するためのウェブアプリケーションです。このツールは、教科書、チャット形式の対話、理解度チェックなど、多様なフォーマットでコンテンツを作成できます。A4で20ページ、50円前後で出力されます。
- LLM Book Creator is a web application designed to generate books based on specified themes. This tool can create content in various formats, such as textbooks, chat-based dialogues, and comprehension checks. The output is approximately 20 pages in A4 size and costs around $0.50.
## 特徴/ Features
- **多様なフォーマット**:
  - 教科書形式 (Textbook)
  - チャット形式 (Chat)
  - 冗談を交えたチャット形式 (Chat with Comedy)
  - 理解度チェック形式 (QA Check)
  - 同じテーマで教科書形式→チャット形式→理解度チェック形式と読み進めることで効率的・印象的な理解を実現！
- **リアルタイムレンダリング**:
  - MathJax を使用して数式をきれいに表示
- **柔軟なカスタマイズ**:
  - テーマとフォーマットを自由に選択可能
- **キャラクター対応**:
  - ずんだもん・ずん子のセリフ付きチャット表示に対応
- **Various Formats**:
  - Textbook Format
  - Chat Format
  - Chat with Comedy
  - QA Check Format
  - Achieve efficient and impactful understanding by progressing through the same theme in Textbook → Chat → QA Check formats!
- **Real-Time Rendering**:
  - Beautifully display mathematical equations using MathJax.
- **Flexible Customization**:
  - Freely select themes and formats.
- **Character Support**:
  - Supports chat displays with dialogue from Zundamon and Zunko.

## セットアップ / Set Up
1. Open AI API Keyを設定(app.py) / Set Open AI API Key in app.py
   ```bash
   api_key=""
   ```
3. 必要な依存ライブラリをインストールしてください / Please install the required dependency libraries.
   ```bash
   pip install flask openai
   ```
4. Flaskサーバーを起動 / Start the Flask server.
   ```bash
   python app.py
   ```
## 実行 / Execution
1. テーマを入力 / Enter a Theme
   - 入力ボックスにテーマを入力します (例: "量子力学" や "AIの基礎")
   - 希望のフォーマットを選択し、送信 ボタンを押します。
   - Input your desired theme into the text box (e.g., "Quantum Mechanics" or "Basics of AI").
   - Select your preferred format and click the "Submit" button.
2. 結果を確認 / Review the Results
   - 生成された内容は画面に表示されます。
   - 必要に応じて内容をコピーして利用できます。
   - The generated content will be displayed on the screen.
   - You can copy and use the content as needed.
   

