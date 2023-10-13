import requests
import time
from datetime import datetime

url = 'https://blaze.com/api/roulette_games/recent'


def Send_Message_Telegram(message):
    token = '5963411116:AAHeovmtOeDh0-g-L6R6KX4IjoyzP7nHam8'
    chat_id = '-790930643'
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

vitoriaParcial = 0
derrotaParcial = 0
entrar = False
while True:
    if datetime.now().strftime('%H:%M:%S') == '00:00:00':
        vitoriaParcial = 0
        derrotaParcial = 0
        entrar = False
        Send_Message_Telegram('Parciais Resetadas com sucesso')
        time.sleep(2)
    qtdDerrota = 0
    contador = 0
    try:
        response = requests.get(url)
        r = response.json()
    except:
        pass
    corPrevista = ''
    mensagemEnviada = False
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}]:: Aguardando oportunidade de Entrada. ", end= '\r')
    
    
    if QualCor(r[0]['color']) == 'BRANCO':
        print('\n->ATENÇÃO ESTRATÉGIA DO BRANCO')
        Send_Message_Telegram('->ATENÇÃO ESTRATÉGIA DO BRANCO')

        if QualCor(r[1]['color']) == 'VERMELHO': corPrevista = 'PRETO'
        elif QualCor(r[1]['color']) == 'PRETO': corPrevista = 'VERMELHO'   
        elif QualCor(r[1]['color']) == 'BRANCO': 
            print('-> NÃO EFEUTAR OPERAÇÃO, BRANCO DUPLICADO.')
            corPrevista = ''
        if corPrevista != '':
            while True:
                if  contador > 1 and corPrevista == 'PRETO': 
                    corPrevista = 'VERMELHO'
                    contador = 0
                if  contador > 1 and corPrevista == 'VERMELHO': 
                    corPrevista = 'PRETO'
                    contador = 0
                msg = '-> EFETUAR OPERAÇÃO NA COR '+ corPrevista
                print(msg)
                Send_Message_Telegram(msg)
                    
                idAnterior = r[0]['id']
                while idAnterior == r[0]['id']:
                    try:
                        response = requests.get(url)
                        r = response.json()
                    except:
                        pass
                
                if (corPrevista != '' and corPrevista == QualCor(r[0]['color'])):
                    qtdDerrota  = 0
                    vitoriaParcial += 1
                    print('-> ✅ Green')
                    Send_Message_Telegram('-> ✅ Green')
                    mensagemEnviada = True
                    break
                elif (corPrevista != '' and corPrevista != QualCor(r[0]['color'])):
                    qtdDerrota +=1
                    msg = f'->Entrar no Martingale {qtdDerrota}'
                    print(msg)
                    Send_Message_Telegram(msg)
                contador += 1

                if qtdDerrota == 4:
                    qtdDerrota  = 0
                    derrotaParcial += 1
                    print('-> ⛔️ Loss')
                    Send_Message_Telegram('-> ⛔️ Loss')
                    mensagemEnviada = True
                    break
    
    if QualCor(r[0]['color']) == 'PRETO' and r[0]['roll'] == 10:
        print('\n->ATENÇÃO ESTRATÉGIA DO PRETO')
        Send_Message_Telegram('->ATENÇÃO ESTRATÉGIA DO PRETO')
        
        while True:
            corPrevista = 'PRETO'
            msg = '-> EFETUAR OPERAÇÃO NA COR '+ corPrevista
            print(msg)
            Send_Message_Telegram(msg)
                    
            idAnterior = r[0]['id']
            while idAnterior == r[0]['id']:
                try:
                    response = requests.get(url)
                    r = response.json()
                except:
                    pass
            
            if (corPrevista != '' and corPrevista == QualCor(r[0]['color'])):
                qtdDerrota  = 0
                vitoriaParcial += 1
                print('-> ✅ Green')
                Send_Message_Telegram('-> ✅ Green')
                mensagemEnviada = True
                break
            elif (corPrevista != '' and corPrevista != QualCor(r[0]['color'])):
                derrotaParcial +=1
                print('-> ⛔️ Loss')
                Send_Message_Telegram('-> ⛔️ Loss')
                mensagemEnviada = True
                break
            
        
        
    if (vitoriaParcial != 0 or derrotaParcial != 0) and mensagemEnviada == True:
        winrate = int(100*(vitoriaParcial/(vitoriaParcial+derrotaParcial)))
        # msg = f'->PARCIAL: VITÓRIA-> {vitoriaParcial}   DERROTA-> {derrotaParcial}   TAXA DE ACERTO-> {winrate}%'
        msg = f'-> Parcial ✅ = {vitoriaParcial} ⛔️ = {derrotaParcial} 🎯 = {winrate}% de acerto'
        print(msg)
        Send_Message_Telegram(msg)
        print('\n\n')
    