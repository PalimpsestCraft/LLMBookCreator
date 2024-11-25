from flask import Flask, g, render_template, jsonify, Response, send_file, request
from openai import OpenAI
import os
import concurrent.futures

app = Flask(__name__)

api_key=""

client = OpenAI(api_key=api_key)

@app.route("/")
def book():
    return render_template("index.html")


@app.route("/api/structured_headings/", methods=["POST"])
def structured_headings():
    query = request.form["query"]  # ユーザーからの問い合わせを取得
    format_text= request.form["format"]  # ユーザーからの問い合わせを取得
    print("キーワード: " + query)
    total_tokens = 0  # トークンの合計を初期化

    # OpenAIのChat APIを呼び出して、見出しを生成
    try:
        response_index = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "次のテーマを体系的に理解するのに必要な見出しを2階層（大見出しと小見出し）で構造化して日本語で列挙してください。. i.e. # main_heading ## sub_heading",
                },
                {"role": "user", "content": query},
            ],
        )

        # 応答テキストを取得
        structured_text = response_index.choices[0].message.content

        # 最初のAPI呼び出しのトークン数を加算
        total_tokens += response_index.usage.total_tokens

        def fetch_subheading_content(client, format_text, query_subheadings):
            content_templates = {
                "textbook": "次のテーマについて、具体的にかつ滅茶苦茶詳細に日本語で解説してください。もし見出しを付ける場合は1階層目（#）からではなく3階層目（###）からスタートです。",
                "chat_plain": "次のテーマについて、具体的にかつ滅茶苦茶詳細に、二人の対話形式のシットコムで解説してください。登場キャラクターはずんだもんとずん子で、ずんだもんの口調は「～なのだ！」調で愛嬌のある元気なボケ役の子供で、ずん子はクールなツッコミ役な感じの女性です。くだけた雰囲気で。地の文は不要で台詞のみで。一つの台詞は最大2文まで。台詞の「」はつけて。台詞ごとに段落分けして。i.e. ずんだもん: 「・・・」\nずん子: 「・・・」",
                "chat_comedy": "次のテーマについて、具体的にかつ滅茶苦茶詳細に、ふんだんに冗談をまぜて、二人の対話形式のシットコムで解説してください。登場キャラクターはずんだもんとずん子で、ずんだもんの口調は「～なのだ！」調で愛嬌のある元気なボケ役の子供で、ずん子はクールなツッコミ役な感じの女性です。くだけた雰囲気で。地の文は不要で台詞のみで。一つの台詞は最大2文まで。台詞の「」はつけて。台詞ごとに段落分けして。i.e. ずんだもん: 「・・・」\nずん子: 「・・・」",
                "chat_qa": "次のテーマについて、わかっているか10の質問を作ってください。対象は上級者向けです。回答があまり論述的ではなく具体的にこたえられるような質問にしてください。そして、質問だし、シンキングタイム、回答を、具体的にかつ滅茶苦茶詳細に、冗談をまぜて、二人の対話形式のシットコムで解説してください。登場キャラクターはずんだもんとずん子で、ずんだもんの口調は「～なのだ！」調で愛嬌のある元気なボケ役の子供で、ずん子はクールなツッコミ役な感じの女性です。くだけた雰囲気で。地の文は不要で台詞のみで。一つの台詞は最大2文まで。台詞の「」はつけて。台詞ごとに段落分けして。見出しや区切り（---）は不要です。i.e. ずんだもん: 「・・・」\nずん子: 「・・・」"
            }
            content_text = content_templates.get(format_text, "デフォルトのフォーマットエラーです。")

            # APIリクエスト
            response_content = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                    "role": "system",
                    "content": "次のテーマを体系的に理解するのに必要な見出しを2階層（大見出しと小見出し）で構造化して日本語で列挙してください。. i.e. # main_heading ## sub_heading",
                    },
                    {"role": "user", "content": query},
                    {"role": "system", "content": structured_text},
                    {"role": "system", "content": content_text},
                    {"role": "user", "content": query_subheadings},
                ],
            )
            # 各サブ見出し生成に消費されたトークン数を加算
            nonlocal total_tokens
            total_tokens += response_content.usage.total_tokens
            return response_content.choices[0].message.content


        def process_structure(client, structured_text, format_text, query):
            headings = []
            current_heading = None
            subheading_queries = []

            for line in structured_text.split("\n"):
                line = line.strip()
                if not line:
                    continue
                if line.startswith("# "):
                    if current_heading:
                        headings.append(current_heading)
                    current_heading = {"title": line, "subheadings": []}
                elif line.startswith("## "):
                    if current_heading:
                        query_subheadings = f"「{query}」の「{current_heading['title'].replace('# ', '') }」の「{line.replace('## ', '')}」"
                        subheading_queries.append((current_heading, line, query_subheadings))

            if current_heading:
                headings.append(current_heading)

            # 並列処理でAPIリクエストを送る
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_subheading = {
                    executor.submit(fetch_subheading_content, client, format_text, query_subheading): (current_heading, line)
                    for current_heading, line, query_subheading in subheading_queries
                }
                for future in concurrent.futures.as_completed(future_to_subheading):
                    current_heading, line = future_to_subheading[future]
                    try:
                        content = future.result()
                        subheading_entry = {"subheading": line, "content": content}
                        current_heading["subheadings"].append(subheading_entry)
                    except Exception as e:
                        print(f"Error fetching subheading content: {e}")

            structured_output = {"query": query, "headings": headings}
            return structured_output

        structured_output = process_structure(client, structured_text, format_text, query)

        total_price = round(total_tokens * 10 / 1000000 * 150)

        # 消費したトークン数
        print('消費トークン数: ' + str(total_tokens) + '（' + str(total_price) + '円）')

        # 構造化されたレスポンスをJSONで返す
        return jsonify(structured_output)

    except OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return jsonify({"error": "API error occurred"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8887)
