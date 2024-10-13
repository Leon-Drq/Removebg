import asyncio
import websockets
import json
import base64
import io
import logging
from PIL import Image
from rembg import remove
import os
from concurrent.futures import ThreadPoolExecutor

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 配置
HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 5001))
MAX_SIZE = int(os.getenv('MAX_SIZE', 10 * 1024 * 1024))  # 10 MB

# 创建线程池
executor = ThreadPoolExecutor(max_workers=os.cpu_count())

def process_image(image_data):
    """在线程池中处理图像"""
    input_image = Image.open(io.BytesIO(image_data))
    output_image = remove(input_image)
    buffered = io.BytesIO()
    output_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

async def remove_background(websocket, path):
    """处理WebSocket连接"""
    client_id = id(websocket)  # 为每个连接生成唯一ID
    logger.info(f"New connection established: {client_id}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if data['type'] == 'remove_background':
                    logger.info(f"Received remove_background request from {client_id}")
                    
                    # 检查图像大小
                    image_data = base64.b64decode(data['image'].split(',')[1])
                    if len(image_data) > MAX_SIZE:
                        raise ValueError("Image size exceeds maximum allowed size")

                    # 在线程池中处理图像
                    img_str = await asyncio.get_event_loop().run_in_executor(executor, process_image, image_data)

                    response = {
                        'type': 'processed_image',
                        'image': f'data:image/png;base64,{img_str}'
                    }
                    await websocket.send(json.dumps(response))
                    logger.info(f"Sent processed image to {client_id}")
                else:
                    raise ValueError("Unsupported request type")
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from {client_id}")
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': "Invalid JSON format"
                }))
            except ValueError as ve:
                logger.error(f"Value error for {client_id}: {str(ve)}")
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': str(ve)
                }))
            except Exception as e:
                logger.error(f"Unexpected error for {client_id}: {str(e)}", exc_info=True)
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': "An unexpected error occurred"
                }))
    finally:
        logger.info(f"Connection closed: {client_id}")

async def main():
    """主函数"""
    server = await websockets.serve(
        remove_background, 
        HOST, 
        PORT,
        max_size=MAX_SIZE,  # 限制WebSocket消息大小
        ping_interval=30,   # 每30秒发送一次ping
        ping_timeout=10     # 10秒内没有接收到pong就断开连接
    )
    logger.info(f"Server started on {HOST}:{PORT}")
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped")