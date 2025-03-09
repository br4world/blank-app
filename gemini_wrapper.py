import pandas as pd
import os
import random
import google.generativeai as genai

class GeminiWrapper:
    def __init__(self,temp:int=0,keys:list[str]=None,models:list[str]=None):
        if(keys == None):
            keys = ["AIzaSyDr_v2E4GPxVftyaySXqS5USaKkLoOIjuWg", "AIzaSyA1OZblo-Yc4klundcSIPKmh0tpVW2vDFtXpM" ]
            # "AIzaSyDpg66kaCdZwWnMluIy4hgQzH7b0Bc-7O4LhZA" #paid
        if(models == None):
            models = ["gemini-2.0-flash-exp","gemini-1.5-flash"]
            
        
        self.key = random.choice(keys)
        self.model = random.choice(models)

        genai.configure(api_key=self.key)  ##random.choice(keys)
        self.generation_config = {"temperature": temp,"top_p": 0.95,"top_k": 40, "max_output_tokens": 8192, "response_mime_type": "application/json"}
       
 
    def get_thinking_model_data(self,system_prompt:str,user_prompt:str):
        generation_config = self.generation_config
        thinking_model = "gemini-2.0-flash-thinking-exp-01-21"
        generation_config["response_mime_type"] =  "text/plain"
        prompt = f"{system_prompt} \r\n#User Prompt:\r\n{user_prompt}"
        gen = genai.GenerativeModel( model_name=thinking_model, generation_config=self.generation_config )
        response_stream = gen.generate_content( prompt, generation_config=self.generation_config,stream=True)
        full_markdown = ""
        for chunk in response_stream:
            full_markdown += chunk.text
            html = full_markdown
            yield html 
    
    def get_results(self,instructions:str,data:str):
        prompt = f"{instructions} \r\n#Input Data:\r\n{data}"
        gen = genai.Generativegen( model_name=self.model, generation_config=self.generation_config )
        result = gen.generate_content( prompt, generation_config=self.generation_config)
        return result
