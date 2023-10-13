import requests
import time
from datetime import datetime

url = 'https://blaze.com/api/roulette_games/recent'


def Send_Message_Telegram(message):
    token = '5963411116:AAHeovmtOeDh0-g-L6R6KX4IjoyzP7nHam8'
    chat_id = '-812829830'
    try:
        data = {"chat_id": chat_id, "text": message}
        urlTelegram = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(urlTelegram, data)
    except Exception as e:
        print("Erro no sendMessage:", e)

def QualCor(aux):
    if  aux == 0: return 'BRANCO'
    elif aux == 1: return 'VERMELHO'
    elif aux == 2: return 'PRETO'

vitoriaMFParcial = 0
vitoriaMG1Parcial = 0
vitoriaMG2Parcial = 0
vitoriaBrancoParcial = 0
derrotaParcial = 0
entrar = False
auxMaxperda = 0
maxPerda = 0
lucro = 0
ValorEntrada = 2
while True:
    if datetime.now().strftime('%H') == '00':
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
    if (int(r[2]['roll']) - 1 == r[0]['roll']) or (int(r[2]['roll']) + 1 == r[0]['roll']):corPrevista = 'BRANCO'
    else:corPrevista = ''
    
    if corPrevista != '':
        msg = f'-> EFETUAR OPERAÇÃO NA COR {corPrevista}'
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
                    
            if (corPrevista == QualCor(r[0]['color'])):
                lucro = lucro + (ValorEntrada*14)
                vitoriaMFParcial += 1
                print('-> ✅ Green')
                Send_Message_Telegram('-> ✅ Green')
                mensagemEnviada = True
                martingale  = 0
                auxMaxperda = 0
                break
            
            elif (corPrevista != QualCor(r[0]['color'])):
                # print('-> ⛔️ Loss')
                martingale +=1
                auxMaxperda += 1
                if maxPerda < auxMaxperda: maxPerda = auxMaxperda
                lucro = lucro - ValorEntrada
                if martingale == 5:
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
            winrate = int(100*((vitoriaMFParcial + vitoriaMG1Parcial + vitoriaMG2Parcial + vitoriaBrancoParcial)/(vitoriaMFParcial + vitoriaMG1Parcial + vitoriaMG2Parcial + vitoriaBrancoParcial+derrotaParcial)))
            # msg = f'-> Parcial ✅ -> MF = {vitoriaMFParcial} ✅ -> MG1 = {vitoriaMG1Parcial}  ✅ -> MG2 = {vitoriaMG2Parcial}  ⛔️ = {derrotaParcial} 🎯 = {winrate}% de acerto'
            msg = f'-> Parcial: ✅ -> MF = {vitoriaMFParcial} | ⛔️ = {derrotaParcial} | 🎯 = {winrate}% de acerto'
            print(msg)
            print(f'Lucro Atual: R${lucro}')
            print(f'Maior número de perca: {maxPerda}')
            Send_Message_Telegram(msg)
            print('\n\n')

    