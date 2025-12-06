from ollama import chat
from ollama import ChatResponse
import configparser

class ConfigLoader:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = None
    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config
    
class ChatModel:
    def __init__(self, config_file='config.ini'):
        config_loader = ConfigLoader(config_file)
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
    
if __name__ == "__main__":
    
    chat_model = ChatModel()
    
    user_message = "Hello, how are you?"

    response = chat_model.get_response(user_message)    
    print(f"Response from model: {response.message.content}")