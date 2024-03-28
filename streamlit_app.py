import telepot
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
from tqdm import tqdm
import requests


from telepot.loop import MessageLoop


def get_data_and_classify(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendChatAction(chat_id, 'typing')
    
    try:
    
        organizations_and_csv = {'211': '1',
                             "421": '2', 
                             "908": '3', 
                             "38": '4', 
                             "896": '5',
                             "219": '6',
                             "902": '7',
                             "887": '8',
                             "2287": '9'}

    
        last_values = {}
        results = []

    
        t1 = time.time()
        edge_driver_path = '\msedgedriver.exe'
    #driver = webdriver.Edge(executable_path=edge_driver_path)
        driver = webdriver.Edge()

        username = 'mtq-ms'
        password = 'mtq-ms2017'

        
        url = 'https://sistema.kajoo.com.br/'
        driver.get(url)
        time.sleep(30)
        driver.find_element(By.ID, 'input_0').send_keys(username)
        driver.find_element(By.ID, 'input_1').send_keys(password, Keys.RETURN)
        time.sleep(20)

        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
        historical_data = {}
        historical = {}
        organization_data = {}

        total_organizations = len(organizations_and_csv)

    
        message = bot.sendMessage(chat_id, "Iniciando processamento...\n`[░░░░░░░░░░░░░░░░░░░░░░░░░░░░]`", parse_mode='Markdown')
        message_id = message['message_id']

        for idx, (org_id, csv_path) in enumerate(tqdm(organizations_and_csv.items(), desc="Progresso", position=0, leave=False)):
        
        
    
            new_url = f'https://sistema.kajoo.com.br/#/admin/statistics?organization_id={org_id}'
            driver.get(new_url)
            driver.execute_script(f"window.location.href = '{new_url}';")
            driver.execute_script("location.reload();")
            time.sleep(20)
            driver.find_element(By.XPATH, '//button[@ng-click="vm.openStatisticsTable()"]').click()
            time.sleep(10)
            table = driver.find_element(By.XPATH, '//*[@id="statistics-table"]/md-content/div[2]')
            table_data = [[cell.text for cell in row.find_elements(By.TAG_NAME, 'td')] for row in table.find_elements(By.TAG_NAME, 'tr')]

            
            for i in range(1, len(table_data)):
                for j in range(len(table_data[i])):
                    if table_data[i][j] == '':
                        table_data[i][j] = 0  
                        try:
                           table_data[i][j] = int(table_data[i][j])
                        except ValueError:
                            table_data[i][j] = 0  

            hist_df = pd.DataFrame(table_data[1:]).iloc[:, :-2]
            org_df = pd.DataFrame(table_data[1:]).iloc[:, [-1]]
            org_df.columns = [""]
            historical_data[org_id] = hist_df.T
            organization_data[org_id] = org_df.T
        
            current_progress = idx + 1
            progress = int((current_progress / total_organizations) * 20)
            enviar_mensagem_com_barra_de_progresso(chat_id, message_id, progress)

        mensagem_conclusao = "Concluído!\n`[████████████████████████]` (100%)"
        bot.editMessageText((chat_id, message_id), mensagem_conclusao, parse_mode='Markdown')
    
        combined_data = pd.concat(organization_data, axis=1)
        historico_data = pd.concat(historical_data, axis=1)
    


    #historico_data = historico_data.iloc[:,:]

        
        combined_data.insert(0, 'Hora', timestamp)
    
        
        
        
        with open('HistoricalData.csv', 'w', newline='') as f:
            historico_data.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')

        with open('Historico_BI.csv', 'w', newline='') as f:
            historico_data.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')
        
        with open('Combinado_BI.csv', 'a', newline='') as f:
            combined_data.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')

        with open('CombinedData.csv', 'w', newline='') as f:
            combined_data.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')
        # Fechar o driver
        driver.quit()

        print(f'Banco de dados atualizado às {time.strftime("%H:%M:%S", time.localtime(t1))} com total de {time.time() - t1} segundos.')
        mensagem = f'Banco de dados atualizado às {time.strftime("%H:%M:%S", time.localtime(t1))} com total de {time.time() - t1} segundos.'   
        
        time.sleep(1)
        bot.editMessageText((chat_id, message_id), mensagem, parse_mode='Markdown')
        return combined_data, historico_data, mensagem
    except Exception as e:
        error_message = f"Ocorreu um erro: {str(e)}"
        enviar_mensagem(error_message)
        bot.sendMessage(chat_id, 'Erro durante a execução do código.')
        return combined_data, historico_data, mensagem


def enviar_mensagem(texto):
    TELEGRAM_BOT_TOKEN = '6756572199:AAF1PBY8MeS7ajC31mjotFSZvlHXbL9VLpE'
    CHAT_ID = '988668946'
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {'chat_id': CHAT_ID, 'text': texto}
    requests.post(url, params=params)

def enviar_mensagem_com_barra_de_progresso(chat_id, message_id, progress):
    bar_length = 20
    progress_bar = "█" * progress + "░" * (bar_length - progress)
    mensagem = f"Iniciando processamento...\n`[{progress_bar}]` ({progress * (100 // bar_length)}%)"
    bot.editMessageText((chat_id, message_id), mensagem, parse_mode='Markdown')


# Função para processar mensagens
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        command = msg['text']
        if command == '/executar':
            
            for i in range(1,144):
                
                i = time.time()
                x, y, z = get_data_and_classify(msg)  
                dif = time.time() - i
                bot.sendMessage(chat_id, 'Código executado com sucesso!')
                if dif < 600:
                    time.sleep(600 - dif)
                else:
                    time.sleep(10)



token = '6756572199:AAF1PBY8MeS7ajC31mjotFSZvlHXbL9VLpE'


bot = telepot.Bot(token)

MessageLoop(bot, {'chat': handle}).run_as_thread()

