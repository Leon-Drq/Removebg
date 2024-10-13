import asyncio
import websockets
import json
import base64
import io
from PIL import Image
from rembg import remove

async def remove_background(websocket, path):
    try:
        # 接收客户端发送的消息
        message = await websocket.recv()
        data = json.loads(message)

        if data['type'] == 'remove_background':
            # 从 base64 字符串解码图像数据
            image_data = base64.b64decode(data['image'].split(',')[1])
            input_image = Image.open(io.BytesIO(image_data))

            # 使用 rembg 移除背景
            output_image = remove(input_image)

            # 将处理后的图像转换为 base64 字符串
            buffered = io.BytesIO()
            output_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # 发送处理后的图像给客户端
            response = {
                'type': 'processed_image',
                'image': f'data:image/png;base64,{img_str}'
            }
            await websocket.send(json.dumps(response))
        else:
            raise ValueError("Unsupported request type")

    except Exception as e:
        # 如果发生错误，发送错误消息给客户端
        error_response = {
            'type': 'error',
            'message': str(e)
        }
        await websocket.send(json.dumps(error_response))

# 启动 WebSocket 服务器
start_server = websockets.serve(remove_background, "localhost", 5001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()