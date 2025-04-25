import requests
import json
import os
import dotenv
import csv
import datetime

dotenv.load_dotenv()
API_ALFA = os.getenv("API_ALFA")
CEP_LOCAL = os.getenv("CEP_LOCAL")
faixa_de_pesos_inicial = [0,11,31]
faixa_de_pesos_final = [10,30,50]
hoje = datetime.date.today()
hoje = hoje.strftime("%Y-%m-%d")
ticket_medio = 300

def read_cep_ranges_from_csv(filename="faixa_cep.csv"):
    cep_ranges = []
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:  
        reader = csv.DictReader(csvfile, delimiter=';')  
        for row in reader:
            estado = row["estado"]
            cidade = row["cidade"]
            cep_inicial = row["cep_inicial"]
            cep_final = row["cep_final"]



def calcula_valor_prazo(cep, peso):
    url = "https://api.alfatransportes.com.br/cotacao/v1.2/"
    headers = {
        "Content-Type": "application/json",}
    payload = f'{"idr":"{API_ALFA}",
               "cliTip":"2",
               "cliCnpj":"",
               "cliCep":"{cep}",
               "merVlr":"{ticket_medio}",
               "merPeso":"{peso}",
               "merM3":"0",
               "merVol":"",
               "quim":"0",
               "dtEmbarque":"{hoje}",
               "cepRem":"{CEP_LOCAL}",
               "modoJson":"1"}'
