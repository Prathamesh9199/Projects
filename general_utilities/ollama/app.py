from ollama import chat, embed
from ollama import ChatResponse
import configparser
import base64

class ConfigLoader:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = None
    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config

class ChatModel:
    def __init__(self, config_loader: ConfigLoader):
        self.config = config_loader.load_config()
        
    def get_response(self, message):
        self.model_name = self.config['chat']['model_name']

        response: ChatResponse = chat(model=self.model_name, messages=[
            {
                'role': 'user',
                'content': message,
            },
        ])
        return response

class EmbedModel:
    def __init__(self, config_loader: ConfigLoader):
        self.config = config_loader.load_config()

    def get_embedding(self, text):
        self.model_name = self.config['embedding']['model_name']
        response = embed(model=self.model_name, input=text)
        return response['embeddings'][0]

class VisionModel:
    def __init__(self, config_loader: ConfigLoader):
        self.config = config_loader.load_config()

    def _encode_image(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    def ask_about_image(self, image_path, prompt):
        self.model_name = self.config['vision']['model_name']

        response = chat(
            model=self.model_name,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                    'images': [image_path]  # ✅ just pass image path here
                }
            ]
        )
        return response

if __name__ == "__main__":
    config_loader = ConfigLoader()
    chat_model = ChatModel(config_loader)
    embed_model = EmbedModel(config_loader)
    vision_model = VisionModel(config_loader)

    # #
    # user_message = "Hello, how are you?"

    # response = chat_model.get_response(user_message)    
    # print(f"Response from model: {response.message.content}")
    
    # embedded_message = embed_model.get_embedding(user_message)
    # print(f"Embedded message: {embedded_message}")

     # Image + prompt
    image_path = r"E:\\Images\\pexels-didsss-2467229.jpg"
    image_prompt = "Describe what you see in this image."
    vision_response = vision_model.ask_about_image(image_path, image_prompt)
    print(f"Vision response: {vision_response.message.content}")