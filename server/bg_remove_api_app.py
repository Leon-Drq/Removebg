from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import base64

app = Flask(__name__)
CORS(app)

# 从环境变量获取 API 密钥
API_KEY = os.getenv('REMOVE_BG_API_KEY')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # 获取前端发送的图片数据
        data = request.json
        image_data = data['image'].split(',')[1]

        # 调用 Remove.bg API
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            data={
                'image_file_b64': image_data,
            },
            headers={'X-Api-Key': API_KEY},
        )

        if response.status_code == requests.codes.ok:
            # 返回处理后的图片
            return jsonify({'processedImage': 'data:image/png;base64,' + base64.b64encode(response.content).decode('utf-8')})
        else:
            # 处理错误
            return jsonify({'error': 'Background removal failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

