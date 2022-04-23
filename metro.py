#!/usr/bin/env python3
import string
import sys
import requests
import json
import urllib3

import os
import errno

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# WIP - maybe dictionary for -help? and add names
station_id_codes = ['AM','AF','AH','AL','AS','AX','AN','AE','AR','AV','BC','BV','CR','CS','CG','CP','CA','CH','CU','CM','EC','IN','JZ','LA','LU','MP','MM','OD','OL','OS','OR','PA','PI','PO','PE','QC','RA','RE','RM','RO','SA','SP','SS','SR','TE','TP','MO','EN','AP','RB']

destinations = {
  33:'Reboleira',
  34:'Amadora Este',
  35:'Pontinha',
  36:'Colégio Militar/Luz',
  37:'Laranjeiras',
  38:'São Sebastião',
  39:'Avenida',
  40:'Baixa-Chiado',
  41:'Terreiro do Paço',
  42:'Santa Apolónia',
  43:'Odivelas',
  44:'Lumiar',
  45:'Campo Grande',
  46:'Campo Pequeno',
  48:'Rato',
  50:'Telheiras',
  51:'Alvalade',
  52:'Alameda',
  53:'Martim Moniz',
  54:'Cais do Sodré',
  56:'Bela Vista',
  57:'Chelas',
  59:'Moscavide',
  60:'Aeroporto'
}


def station_codes():
  return station_id_codes


def generate_token():

  # with open("metro/credentials.json", "r") as f:
  # credentials = json.load(f)

  # headers = {
  #     'Authorization': 'Basic ' + credentials["consumer_encoded"],
  # }

  # data = {
  #   'grant_type': 'password',
  #   'username': credentials["username"],
  #   'password': credentials["password"]
  # }

  headers = {
      'Authorization': 'Basic ' + 'bmJMOGYzQWlJZWI1cWZkTU1mdVZXdlBHZzJ3YToxMVVmX3plQ2E1RnBqb3QzOWtYTk5yaVJrZkVh',
  }

  data = {
    'grant_type': 'password',
    'username': 'MetroBot',
    'password': 'MetroB0t'
  }

  response = requests.post('https://api.metrolisboa.pt:8243/token', headers=headers, data=data, verify=False)

  # WIP - HTTPSConnectionPool(host='api.metrolisboa.pt', port=8243): Max retries exceeded with url: /token
  return response.json()['access_token']


def request(token,station_id_code):
  headers = {
      'accept': 'application/json',
      'Authorization': 'Bearer ' + token,
  }

  return requests.get('https://api.metrolisboa.pt:8243/estadoServicoML/1.0.1/tempoEspera/Estacao/' + station_id_code, headers=headers, verify=False)


def format_time(time):
  time = int(time)
  return  "{:02d}".format(time//60) + ':' + "{:02d}".format(time - time//60*60)


def format(response):
  formatted = ""
  for train in json.loads(json.dumps(response.json()['resposta'])):
    formatted += destinations[int(train['destino'])] + ' -> ' +\
          format_time(train['tempoChegada1']) + ' - ' + format_time(train['tempoChegada2']) + ' - ' + format_time(train['tempoChegada3'])
    formatted += "\n"
  return formatted


def request_time(station_id_code, token):
  error = False
  if type(station_id_code) != str:
    print('Error! Usage: metro.py [station_id_code].')
    error = True;
  if station_id_code not in station_id_codes:
    print('Error! ' + station_id_code + ' is not a station id code.')
    error = True;
  if not error:
    response = request(token, station_id_code)
    print(response)
    return format(response)
  return 'Error! ' + station_id_code + ' is not a station id code'
