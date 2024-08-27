from flask import Flask, request, send_file
import csv
import json
import io

app = Flask(
  __name__,
  static_folder='public',
  static_url_path='/'
)

# 讀取 CSV 文件並轉換為 JSON
def csv_to_json(file_content):
    json_data = []

    # 使用 io.StringIO 將文件內容轉換為文本流
    text_stream = io.StringIO(file_content)
    csv_reader = csv.DictReader(text_stream)
    for row in csv_reader:
        message_data = []
        for column, content in row.items():
            message_data.append({
                "role": column,
                "content": content
            })

        json_data.append({
            "messages": message_data
        })

    return json_data

# 將 JSON 轉換為 JSONL
def json_to_jsonl(json_data):
    jsonl_data = ""
    for item in json_data:
        jsonl_data += json.dumps(item, ensure_ascii=False) + '\n'
    return jsonl_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 檢查是否有文件上傳
        if 'file' not in request.files:
            return 'No file uploaded.'

        file = request.files['file']

        if file.filename == '':
            return 'No file selected.'

        if file:
            # 讀取文件內容為文本
            file_content = file.read().decode('utf-8-sig')
            
            # 讀取 CSV 文件並轉換為 JSON
            json_data = csv_to_json(file_content)

            # 將 JSON 轉換為 JSONL
            jsonl_data = json_to_jsonl(json_data)

            # 保存 JSONL 文件
            jsonl_filename = 'output.jsonl'
            with open(jsonl_filename, 'w', encoding='utf-8') as jsonl_file:
                jsonl_file.write(jsonl_data)

            return send_file(jsonl_filename, as_attachment=True)

    # 簡單的上傳表單
    return '''
    <!doctype html>
    <a href="/dataset.csv">範例檔案下載</a>
    <title>CSV to JSONL Converter</title>
    <h1>Upload a CSV file to convert to JSONL</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(port=5343)