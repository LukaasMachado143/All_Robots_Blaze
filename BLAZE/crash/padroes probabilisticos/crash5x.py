import requests
import time
from datetime import datetime

url = 'https://blaze.com/api/crash_games/recent'


def Send_Message_Telegram(message):
    token = '5983576053:AAGuggU_hhyacB_0qyaG30LW60EkdDB5OEk'
    chat_id = '-817325975'
    try:
        data = {"chat_id": chat_id, "text": message}
        urlTelegram = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(urlTelegram, data)
    except Exception as e:
        print("Erro no sendMessage:", e)


vitoriaMFParcial = 0
vitoriaMG1Parcial = 0
vitoriaMG2Parcial = 0
vitoriaBrancoParcial = 0
derrotaParcial = 0
entrar = False
auxMaxperda = 0
maxPerda = 0
mensagemEnviada = False
valorEntrada = 2
lucro = 0
while True:
    if datetime.now().strftime('%H:%M:%S') == '00:00:00':
        vitoriaMFParcial = 0
        vitoriaMG1Parcial = 0
        vitoriaMG2Parcial = 0
        vitoriaBrancoParcial = 0
        derrotaParcial = 0
        entrar = False
        maxPerda = 0
        # Send_Message_Telegram('Parciais Resetadas com sucesso')
        time.sleep(2)
    martingale = 0
    try:
        response = requests.get(url)
        r = response.json()
    except:
        pass
    idAnterior = r[0]['id']
    while idAnterior == r[0]['id']:
        print(f"[{datetime.now().strftime('%H:%M:%S')}]:: Aguardando oportunidade de Entrada. ", end= '\r')
        time.sleep(1)
        try:
            response = requests.get(url)
            r = response.json()
        except:
            pass
            
    
    
    if r[0]['crash_point'] == 0 or r[0]['crash_point'] == '0': entrar = True


    if entrar:
        msg = f'-> EFETUAR OPERAÇÃO, ATÉ 5 CASAS APÓS O 1.00X'
        print('\n'+msg)
        Send_Message_Telegram(msg)
        contador = 0
        while contador != 5:             
            idAnterior = r[0]['id']
            while idAnterior == r[0]['id']:
                try:
                    response = requests.get(url)
                    r = response.json()
                except:
                    pass
            if float(r[0]['crash_point']) > 4.99:
                lucro = lucro + (valorEntrada*5)
                vitoriaMFParcial += 1
                print('-> ✅ Green')
                Send_Message_Telegram('-> ✅ Green')
                mensagemEnviada = True
                auxMaxperda = 0
                
            elif float(r[0]['crash_point']) < 4.99:
                lucro = lucro - valorEntrada
                print('-> ⛔️ Loss')
                auxMaxperda += 1
                if maxPerda < auxMaxperda: maxPerda = auxMaxperda
                derrotaParcial += 1
                Send_Message_Telegram('-> ⛔️ Loss')
                mensagemEnviada = True
            contador += 1
        entrar = False
  
    if mensagemEnviada == True:
        winrate = round(100*((vitoriaMFParcial + vitoriaMG1Parcial + vitoriaMG2Parcial)/(vitoriaMFParcial + vitoriaMG1Parcial + vitoriaMG2Parcial + derrotaParcial)),2)
        msg = f'-> Parcial ✅ -> MF = {vitoriaMFParcial} ✅ -> MG1 = {vitoriaMG1Parcial}  ✅ -> MG2 = {vitoriaMG2Parcial}  ⛔️ = {derrotaParcial} 🎯 = {winrate}% de acerto'
        # msg = f'-> Parcial ✅ -> MF = {vitoriaMFParcial} ⛔️ -> Loss = {derrotaParcial} 🎯 = {winrate}% de acerto'
        print(msg)
        Send_Message_Telegram(msg)
        print(f'Lucro Atual: R${lucro}')
        print(f'Maior número de perca Seguida: {maxPerda}')
        print('\n\n')
        mensagemEnviada = False

    