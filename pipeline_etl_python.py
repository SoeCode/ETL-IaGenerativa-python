sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

import pandas as pd

df = pd.read_csv('SDW2023.CSV')
user_ids = df['UserID'].tolist()
display(user_ids)

import requests
import json

def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
display(users)

import openai
openai.api_key = openai_api_key

def gerenate_ai_news(user):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
            "role": "system", 
            "content": "Você é um especialista em Marketing Bancário."
        },
        {
            "role": "user", 
            "content": f"Crie uma mensagem personalizada para {user['name']} sobre a importância do investimento seguro(máximo de 100 carácteres)!"
        }
      ]
    )
    
    return completion.choice[0].message.content.strip('\"')
    
for user in users:
    news = gerenate_ai_news(user)
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
    })

    def update_user(user):
        response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
        return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")