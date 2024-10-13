# #This is an example that uses the websockets api and the SaveImageWebsocket node to get images directly without
# #them being saved to disk

# import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
# import uuid
# import json
# import urllib.request
# import urllib.parse

# server_address = "127.0.0.1:8188"
# client_id = str(uuid.uuid4())

# def queue_prompt(prompt):
#     p = {"prompt": prompt, "client_id": client_id}
#     data = json.dumps(p).encode('utf-8')
#     req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
#     return json.loads(urllib.request.urlopen(req).read())

# def get_image(filename, subfolder, folder_type):
#     data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
#     url_values = urllib.parse.urlencode(data)
#     with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
#         return response.read()

# def get_history(prompt_id):
#     with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
#         return json.loads(response.read())

# def get_images(ws, prompt):
#     prompt_id = queue_prompt(prompt)['prompt_id']
#     output_images = {}
#     current_node = ""
#     while True:
#         out = ws.recv()
#         if isinstance(out, str):
#             message = json.loads(out)
#             if message['type'] == 'executing':
#                 data = message['data']
#                 if data['prompt_id'] == prompt_id:
#                     if data['node'] is None:
#                         break #Execution is done
#                     else:
#                         current_node = data['node']
#         else:
#             if current_node == 'save_image_websocket_node':
#                 images_output = output_images.get(current_node, [])
#                 images_output.append(out[8:])
#                 output_images[current_node] = images_output

#     return output_images

# prompt_text = """
# {
#     "3": {
#         "class_type": "KSampler",
#         "inputs": {
#             "cfg": 8,
#             "denoise": 1,
#             "latent_image": [
#                 "5",
#                 0
#             ],
#             "model": [
#                 "4",
#                 0
#             ],
#             "negative": [
#                 "7",
#                 0
#             ],
#             "positive": [
#                 "6",
#                 0
#             ],
#             "sampler_name": "euler",
#             "scheduler": "normal",
#             "seed": 8566257,
#             "steps": 20
#         }
#     },
#     "4": {
#         "class_type": "CheckpointLoaderSimple",
#         "inputs": {
#             "ckpt_name": "v1-5-pruned-emaonly.ckpt"
#         }
#     },
#     "5": {
#         "class_type": "EmptyLatentImage",
#         "inputs": {
#             "batch_size": 1,
#             "height": 512,
#             "width": 512
#         }
#     },
#     "6": {
#         "class_type": "CLIPTextEncode",
#         "inputs": {
#             "clip": [
#                 "4",
#                 1
#             ],
#             "text": "masterpiece best quality girl"
#         }
#     },
#     "7": {
#         "class_type": "CLIPTextEncode",
#         "inputs": {
#             "clip": [
#                 "4",
#                 1
#             ],
#             "text": "bad hands"
#         }
#     },
#     "8": {
#         "class_type": "VAEDecode",
#         "inputs": {
#             "samples": [
#                 "3",
#                 0
#             ],
#             "vae": [
#                 "4",
#                 2
#             ]
#         }
#     },
#     "save_image_websocket_node": {
#         "class_type": "SaveImageWebsocket",
#         "inputs": {
#             "images": [
#                 "8",
#                 0
#             ]
#         }
#     }
# }
# """

# prompt = json.loads(prompt_text)
# #set the text prompt for our positive CLIPTextEncode
# prompt["6"]["inputs"]["text"] = "masterpiece best quality man"

# #set the seed for our KSampler node
# prompt["3"]["inputs"]["seed"] = 5

# ws = websocket.WebSocket()
# ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
# images = get_images(ws, prompt)

# #Commented out code to display the output images:

# # for node_id in images:
# #     for image_data in images[node_id]:
# #         from PIL import Image
# #         import io
# #         image = Image.open(io.BytesIO(image_data))
# #         image.show()

# This is an example that uses the websockets API and the SaveImageWebsocket node to get images directly without
# them being saved to disk

import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import urllib.error
import time

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

# Function to queue a prompt to the server
# This function sends a prompt to the server and returns the server's response
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    req.add_header('Content-Type', 'application/json')  # Adding Content-Type header
    try:
        response = urllib.request.urlopen(req)
        response_data = json.loads(response.read())
        print("[DEBUG] queue_prompt response: ", response_data)
        return response_data
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
        print("Request Data:", json.dumps(p, indent=4))
        raise

# Function to retrieve an image from the server
# This is used to get an image by specifying its filename, subfolder, and type
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    try:
        with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
        raise

# Function to get the history of a prompt execution from the server
# It retrieves information about the specified prompt ID
def get_history(prompt_id):
    try:
        with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
        raise

# Function to retrieve images from the WebSocket connection
# This function listens to messages from the WebSocket and extracts image data
def get_images(ws, prompt):
    queue_response = queue_prompt(prompt)
    if 'prompt_id' not in queue_response:
        print("[ERROR] No prompt_id found in response from queue_prompt.")
        return {}
    
    prompt_id = queue_response['prompt_id']
    output_images = {}
    current_node = ""
    print("[DEBUG] Waiting for images...")
    while True:
        try:
            out = ws.recv()  # Receive data from WebSocket
        except websocket.WebSocketTimeoutException:
            print("[ERROR] WebSocket timeout occurred. No response from server.")
            break
        
        if isinstance(out, str):
            message = json.loads(out)
            print("[DEBUG] Received message: ", message)
            if message['type'] == 'executing':
                data = message['data']
                if data['prompt_id'] == prompt_id:
                    if data['node'] is None:
                        print("[DEBUG] Execution completed.")
                        break  # Execution is done
                    else:
                        current_node = data['node']
        else:
            if current_node == 'save_image_websocket_node':
                images_output = output_images.get(current_node, [])
                images_output.append(out[8:])  # Get image data
                output_images[current_node] = images_output

    return output_images

# The prompt JSON that defines the image generation workflow
# This specifies various nodes like sampler, model, latent image, etc.
prompt_text = """
{
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "cfg": 8,
            "denoise": 1,
            "latent_image": [
                "5",
                0
            ],
            "model": [
                "4",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "sampler_name": "euler",
            "scheduler": "normal",
            "seed": 440491169669868,
            "steps": 20
        }
    },
    "4": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {
            "ckpt_name": "majicmixRealistic_betterV2V25.safetensors"
        }
    },
    "5": {
        "class_type": "EmptyLatentImage",
        "inputs": {
            "batch_size": 1,
            "height": 512,
            "width": 512
        }
    },
    "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "beautiful scenery nature glass bottle landscape, purple galaxy bottle"
        }
    },
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "text, watermark"
        }
    },
    "8": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "4",
                2
            ]
        }
    },
    "save_image_websocket_node": {
        "class_type": "SaveImageWebsocket",
        "inputs": {
            "images": [
                "8",
                0
            ]
        }
    }
}
"""

# Load the prompt from the text and modify specific parts for customization
prompt = json.loads(prompt_text)
#set the text prompt for our positive CLIPTextEncode
prompt["6"]["inputs"]["text"] = "beautiful scenery nature glass bottle landscape, purple galaxy bottle"

#set the seed for our KSampler node
prompt["3"]["inputs"]["seed"] = 440491169669868

# Connect to WebSocket server
# Establish a connection to the WebSocket server to receive generated images
ws = websocket.WebSocket()
try:
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    ws.settimeout(10)  # Set a timeout for WebSocket response
    # Get images
    images = get_images(ws, prompt)
    # Display the output images (uncomment if needed)
    if images:
        for node_id in images:
            for image_data in images[node_id]:
                from PIL import Image
                import io
                image = Image.open(io.BytesIO(image_data))
                image.show()
    else:
        print("[ERROR] No images received.")
except websocket.WebSocketException as e:
    print("WebSocket Error:", e)
finally:
    ws.close()