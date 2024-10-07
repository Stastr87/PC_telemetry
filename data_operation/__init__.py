import os
from datetime import datetime
import time
import csv



def create_telemerty_data(data_file='data.csv'):
    '''Создает пустой CSV файл в пепке хранения телеметрии
    '''
    folder_name = os.path.abspath(os.path.join('telemetry',datetime.now().strftime('%d-%m-%Y')))
    file_path = os.path.join(folder_name,data_file)
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        # Таймер для того что бы создалась директория
        time.sleep(0.2)
        with open(file_path, mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            file_writer.writerow(['time', 'cpu_usage', 'ram_free','network_adapter','net_usage_up','net_usage_down'])

def update_telemerty_data(data, data_file='data.csv'):
    ''' Добавляет данные в существующий CSV файл
    '''
    cpu_usage, ram_free, network_usage = data
    
    
    folder_name = os.path.abspath(os.path.join('telemetry',datetime.now().strftime('%d-%m-%Y')))
    file_path = os.path.join(folder_name, data_file)
    
    #Если папка существует но в ней нет файла, то его нужно создать с указанной шапкой
    if not os.path.exists(file_path):
        with open(file_path, mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            file_writer.writerow(['time', 'cpu_usage', 'ram_free','network_adapter','net_usage_up','net_usage_down'])

    with open(file_path, mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
        for net_adaptor in list(network_usage.keys()):
            file_writer.writerow([datetime.now(),
                                  round(float(cpu_usage)),
                                  round(float(ram_free)),
                                  net_adaptor,
                                  round(float(network_usage[net_adaptor]["up"])),
                                  round(float(network_usage[net_adaptor]["down"]))])

def create_channel_record_data(data_file='channel_record_telemetry.csv'):
    '''Создает пустой CSV файл в пепке хранения телеметрии
    '''
    folder_name = os.path.abspath(os.path.join('telemetry',datetime.now().strftime('%d-%m-%Y')))
    file_path = os.path.join(folder_name,data_file)
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        # Таймер для того что бы создалась директория
        time.sleep(0.2)
        with open(file_path, mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            file_writer.writerow(['time', 'channel_name', 'is_record_error'])

def update_channel_record_data(data, data_file='channel_record_telemetry.csv'):
    ''' Добавляет данные в существующий CSV файл
    '''
    folder_name = os.path.abspath(os.path.join('telemetry',datetime.now().strftime('%d-%m-%Y')))
    file_path = os.path.join(folder_name, data_file)

    #Если папка существует но в ней нет файла, то его нужно создать с указанной шапкой
    if not os.path.exists(file_path):
        with open(file_path, mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            file_writer.writerow(['time', 'channel_name', 'is_record_error'])

    with open(file_path, mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
        for channel_data in data:
            file_writer.writerow([datetime.now(),
                                  channel_data[0],
                                  channel_data[1]
                                  ])
