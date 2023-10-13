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
            
    
    
    if float(r[0]['crash_point'] == 0):
        contador = 0
        while contador != 5:
            # print(contador)
            # print(f"[{datetime.now().strftime('%H:%M:%S')}]:: Aguardando oportunidade de Entrada. ", end= '\r')                     
            idAnterior = r[0]['id']
            while idAnterior == r[0]['id']:
                try:
                    response = requests.get(url)
                    r = response.json()
                except:
                    pass
            # print(contador)
            if contador == 4:entrar = True
            contador += 1
    
    elif float(r[0]['crash_point']) > 9.99: entrar = True

    if entrar:
        msg = f'-> EFETUAR OPERAÇÃO, TIRAR EM 2X, OPERAR COM ATÉ 2 MARTINGALE'
        print('\n'+msg)
        Send_Message_Telegram(msg)
        while True:                        
            idAnterior = r[0]['id']
            while idAnterior == r[0]['id']:
                try:
                    response = requests.get(url)
                    r = response.json()
                except:
                    pass
            if float(r[0]['crash_point']) > 1.99:
                if martingale == 0:
                    vitoriaMFParcial += 1
                elif martingale == 1:
                    vitoriaMG1Parcial += 1
                elif martingale == 2:
                    vitoriaMG2Parcial += 1
                print('-> ✅ Green')
                Send_Message_Telegram('-> ✅ Green')
                mensagemEnviada = True
                martingale  = 0
                auxMaxperda = 0
                break
                
            elif float(r[0]['crash_point']) < 1.99:
                # print('-> ⛔️ Loss')
                martingale +=1
                auxMaxperda += 1
                if maxPerda < auxMaxperda: maxPerda = auxMaxperda
            
                if martingale == 3:
                    print('-> ⛔️ Loss')
                    martingale  = 0
                    derrotaParcial += 1
                    Send_Message_Telegram('-> ⛔️ Loss')
                    mensagemEnviada = True
                    break
                msg = f'->Entrar no Martingale {martingale}'
                print(msg)
                Send_Message_Telegram(msg)
        
  
    if mensagemEnviada == True:
        winrate = round(100*((vitoriaMFParcial + vitoriaMG1Parcial + vitoriaMG2Parcial)/(vitoriaMFParcial + vitoriaMG1Parcial + vitoriaMG2Parcial + derrotaParcial)),2)
        msg = f'-> Parcial ✅ -> MF = {vitoriaMFParcial} ✅ -> MG1 = {vitoriaMG1Parcial}  ✅ -> MG2 = {vitoriaMG2Parcial}  ⛔️ = {derrotaParcial} 🎯 = {winrate}% de acerto'
        # msg = f'-> Parcial ✅ -> MF = {vitoriaMFParcial} ⛔️ -> Loss = {derrotaParcial} 🎯 = {winrate}% de acerto'
        print(msg)
        Send_Message_Telegram(msg)
        print(f'Maior número de perca: {maxPerda}')
        print('\n\n')
        enviarMensagem = False

    