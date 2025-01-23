import firebase_admin
from firebase_admin import credentials, storage
import requests
import serial
import datetime
import os
import time

cred = credentials.Certificate("C:/Users/seuuser/pasta/suakey.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'idproject.appspot.com'})
porta_serial = 'COM45'
baud_rate = 115200

def conectar_serial():
    while True:
        try:
            ser = serial.Serial(porta_serial, baud_rate, timeout=1)
            print(f"Conectado à porta serial {porta_serial}")
            return ser
        except serial.SerialException as e:
            print(f"Erro ao conectar na porta serial: {e}")
            time.sleep(5)

ser = conectar_serial()

def is_connected():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def upload_file_to_storage(local_file_path, remote_file_path):
    if not is_connected():
        print(f"Sem conexão com a internet. Verifique sua conexão e tente novamente.")
        return

    try:
        bucket = storage.bucket()  
        blob = bucket.blob(remote_file_path)
        blob.upload_from_filename(local_file_path)
        print(f"Arquivo {local_file_path} enviado para {remote_file_path} no Firebase Storage.")
    except Exception as e:
        print(f"Erro ao enviar arquivo para o Firebase Storage: {e}")

hora_atual = datetime.datetime.now()
ultima_upload = hora_atual

with open('dados_serial.txt', 'a') as arquivo:
    print(f'Arquivo aberto em: {os.path.abspath("dados_serial.txt")}')
    
    while True:
        try:
            if ser.in_waiting > 0:
                dados = ser.readline().decode('utf-8').strip()
                horario_atual = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                
                linha = f'{horario_atual} - {dados}\n'
                print(linha)
                
                arquivo.write(linha)
                arquivo.flush()

            hora_atual = datetime.datetime.now()
            if hora_atual.minute == 0 and hora_atual.second == 0 and hora_atual != ultima_upload:
                ultima_upload = hora_atual
                
                local_file_path = 'dados_serial.txt'
                remote_file_path = f'uploads/{hora_atual.strftime("%d-%m-%Y_%H-%M-%S")}_dados_serial.txt'
                
                upload_file_to_storage(local_file_path, remote_file_path)
        
        except serial.SerialException as e:
            print(f"Conexão com a porta serial perdida: {e}. Tentando reconectar...")
            ser = conectar_serial()
        except KeyboardInterrupt:
            print("Encerrando o script...")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")
