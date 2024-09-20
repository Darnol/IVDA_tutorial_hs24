import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

class GroqClient:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"

    def generate_poem(self, company_name, prompt_file_path):

        # # DEBUG
        # import os
        # print("This is the current directory:")
        # print(os.getcwd())
        # print("This is GROQ_API_KEY from the env:")
        # print(os.environ['GROQ_API_KEY'])

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Load prompt file
        with open(prompt_file_path, 'r') as file:
            messages_data = json.load(file)

        # Replace {company_name} in the prompt
        for message in messages_data["messages"]:
            message["content"] = message["content"].replace("{company_name}", company_name)

        # # DEBUG
        # print("This is the url:")
        # print(url)
        # print("This is the headers:")
        # print(headers)

        # Make the API request
        response = requests.post(url, json={"model": "llama3-8b-8192", "messages": messages_data["messages"]}, headers=headers)

        # # DEBUG
        # from pprint import PrettyPrinter
        # pp = PrettyPrinter(indent = 2)
        # print("This is the response:")
        # print(pp.pprint(response.json()))
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}"

    def generate_funfact(self, company_name, company_category, company_founding_year, prompt_file_path):

        # # DEBUG
        # import os
        # print("This is the current directory:")
        # print(os.getcwd())
        # print("This is GROQ_API_KEY from the env:")
        # print(os.environ['GROQ_API_KEY'])

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Load prompt file
        with open(prompt_file_path, 'r') as file:
            messages_data = json.load(file)

        # Replace company_name, category and founding_year in the prompt
        for message in messages_data["messages"]:
            message["content"] = message["content"].replace("{company_name}", company_name)
            message["content"] = message["content"].replace("{company_category}", company_category)
            message["content"] = message["content"].replace("{company_founding_year}", company_founding_year)

        # # DEBUG
        # print("This is the url:")
        # print(url)
        # print("This is the headers:")
        # print(headers)

        # Make the API request
        response = requests.post(url, json={"model": "llama3-8b-8192", "messages": messages_data["messages"]}, headers=headers)

        # # DEBUG
        # from pprint import PrettyPrinter
        # pp = PrettyPrinter(indent = 2)
        # print("This is the response:")
        # print(pp.pprint(response.json()))
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}"
