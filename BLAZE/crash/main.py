import requests
import time

url = 'https://blaze.com/api/crash_games/recent'

response = requests.get(url)

r = response.json()

for x in range(len(r)):
    print(r)
    
    # print('RODADA: ', x, 'RETORNO:', r[x]['crash_point'])

