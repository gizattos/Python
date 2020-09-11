# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date.today()
delta = datetime.timedelta(days=1)
dfBolsonaro = pd.DataFrame(columns = ['atores_politicos','compromisso','local','horaInicial','horaFinal','data'])
dfGuedes = pd.DataFrame(columns = ['atores_politicos','compromisso','local','horaInicial','horaFinal','data'])


while start_date <= end_date:
    start_date += delta
    try:
        page = requests.get(f'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica/{start_date}')
        soup = BeautifulSoup(page.text, 'html.parser')
        compromisso = soup.find_all('h4', attrs={'class':'compromisso-titulo'})
        horaInicio = soup.find_all('time', attrs={'class':'compromisso-inicio'})
        horaFim = soup.find_all('time', attrs={'class':'compromisso-fim'})       
        local = soup.find_all('div', attrs={'class':'compromisso-local'})
        for x in range(len(horaInicio)):
            dfBolsonaro = dfBolsonaro.append({'atores_politicos' : 'Jair Bolsonaro',
                            'compromisso': compromisso[x].string,
                            'local': local[x].string,
                            'horaInicial': horaInicio[x].string,
                            'horaFinal': horaFim[x].string,
                            'data': start_date}, ignore_index=True)
    except:
        continue
    try:
        page = requests.get(f'http://antigo.economia.gov.br/Economia/agendas/gabinete-do-ministro/ministro-da-economia/paulo-guedes/{start_date}')
        # Criar o objeto BeautifulSoup
        soup = BeautifulSoup(page.text, 'html.parser')
        compromisso = soup.find_all('h4', attrs={'class':'comprimisso-titulo'})
        horaInicio = soup.find_all('time', attrs={'class':'comprimisso-inicio'})
        local = soup.find_all('p', attrs={'class':'comprimisso-local'})
        for x in range(len(horaInicio)):
            dfGuedes = dfGuedes.append({'atores_politicos' : 'Paulo Guedes',
                            'compromisso': compromisso[x].string,
                            'local': local[x].text[8:],
                            'horaInicial': horaInicio[x].string,
                            'data': start_date}, ignore_index=True)
    except:
        continue

df_unico = pd.concat([dfBolsonaro,dfGuedes], axis=0, ignore_index=True)
df_unico.to_csv('AgendaAtores.csv', sep=';', index=False, encoding='utf-8')
##dfGuedes.to_csv('guedesAgenda.csv', sep=';', index=False, encoding='utf-8')


