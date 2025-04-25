import requests
import json
import os
import dotenv
import csv
import datetime
import pandas as pd
import time


dotenv.load_dotenv()
API_ALFA = os.getenv("API_ALFA")
CEP_LOCAL = os.getenv("CEP_LOCAL")
faixa_de_pesos_inicial = [1,11,31]
faixa_de_pesos_final = [10,30,50]
hoje = datetime.date.today()
hoje = hoje.strftime("%Y-%m-%d")
ticket_medio = 300

planilha_vtex = []

def read_cep_ranges_from_csv(filename="faixa_cep.csv"):
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:  
        reader = csv.DictReader(csvfile, delimiter=';')  
        for row in reader:
            for i in range(len(faixa_de_pesos_inicial)):
                estado = row["estado"]
                cidade = row["cidade"]
                cep_inicial = row["cep_inicial"]
                cep_final = row["cep_final"]
                dados = calcula_valor_prazo(cep_inicial, faixa_de_pesos_inicial[i])
                if dados != False:
                    diasEntrega, valorTotal = dados
                    planilha_vtex.append({
                        "ZipCodeStart": cep_inicial,
                        "ZipCodeEnd": cep_final,
                        "PolygonName": "",
                        "WeightStart": faixa_de_pesos_inicial[i],
                        "WeightEnd": faixa_de_pesos_final[i],
                        "AbsoluteMoneyCost": valorTotal,
                        "PricePercent": 2,  # Valor padrão, ajustar conforme necessário
                        "PriceByExtraWeight": 0,  # Valor padrão, ajustar conforme necessário
                        "MaxVolume": 0,  # Valor padrão, ajustar conforme necessário
                        "TimeCost": diasEntrega,
                        "Country": "BR",  # Valor padrão para Brasil
                        "MinimumValueInsurance": 0  # Valor padrão, ajustar conforme necessário
                    })
                    time.sleep(1)  


def calcula_valor_prazo(cep, peso):
    url = "https://api.alfatransportes.com.br/cotacao/v1.2/"
    headers = {
        "Content-Type": "application/json",}
    payload = {"idr":f"{API_ALFA}",
               "cliTip":"2",
               "cliCnpj":"",
               "cliCep":f"{cep}",
               "merVlr":f"{ticket_medio}",
               "merPeso":f"{peso}",
               "merM3":"0",
               "merVol":"",
               "quim":"0",
               "dtEmbarque":f"{hoje}",
               "cepRem":f"{CEP_LOCAL}",
               "modoJson":"1"}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        try:
            diasEntrega = data['cotacao']["emissao"]["diasEntrega"]
            diasEntrega = diasEntrega.replace(" DIAS UTEIS", "")
            diasEntrega = int(diasEntrega)
            diasEntrega = f'{diasEntrega}.00:00:00'
            valorTotal = data['cotacao']["emissao"]["valoresCotacao"]["valorTotal"]
            return diasEntrega, valorTotal
        except:
            return False
    return False


def salvar_planilha_excel(dados, nome_arquivo="tabela_fretes_vtex.xlsx"):
    """Converte os dados para um DataFrame do pandas e salva como Excel"""
    if not dados:
        print("Não há dados para salvar na planilha.")
        return
    
    df = pd.DataFrame(dados)
    
    # Garantindo que as colunas estejam na ordem correta
    colunas_desejadas = [
        "ZipCodeStart", "ZipCodeEnd", "PolygonName", "WeightStart", 
        "WeightEnd", "AbsoluteMoneyCost", "PricePercent", 
        "PriceByExtraWeight", "MaxVolume", "TimeCost", 
        "Country", "MinimumValueInsurance"
    ]
    
    # Reordenar colunas se necessário
    colunas_existentes = [col for col in colunas_desejadas if col in df.columns]
    df = df[colunas_existentes]
    
    # Salvar como Excel (certifique-se de ter openpyxl instalado)
    df.to_excel(nome_arquivo, index=False)
    
    print(f"Planilha salva com sucesso como {nome_arquivo}")


# Executar o processo
read_cep_ranges_from_csv(filename="faixa_cep.csv")
salvar_planilha_excel(planilha_vtex)