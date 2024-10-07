import os, sys, socket
import asyncio
import time
new_work_dir = os.path.abspath(os.path.join(__file__ ,"../.."))
sys.path.append(new_work_dir)
from datetime import datetime
from tabulate import tabulate
from async_hardware_monitor import HardWareMonitor
import data_operation

class Canvas():
    def __init__(self):
        self.template = self.set_default_template()
        self.hw_usage_template = None
        
        # тут запускаются асинхронно функции которые требуют некоторое время для своего выполнения
        asyncio.run(self.wait_data())

    def set_default_template(self):
        pc_name = f'Host name: {socket.gethostname()}' # Получим имя ПК
        cur_date_time = f"Current date/time {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        self.template.update({1:pc_name,
                              2:cur_date_time})
    
    def get_txt_template(self):
        txt=''
        for block in self.template:
              txt += f"{self.template[block]}\n\n"
        return txt
    
    async def wait_data(self):
        ''' Запускает задачи которые требуют времени ожидания
        '''
        get_hw_usage_template_task = asyncio.create_task(self.get_output_hw_data())
        self.hw_usage_template = await asyncio.gather(get_hw_usage_template_task)

    def set_txt_tamplate(self):
        display_map = dict()
        pc_name = f'Host name: {socket.gethostname()}' # Получим имя ПК
        cur_date_time = f"Current date/time {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    
        display_map.update({"1":pc_name, 
                            "2":cur_date_time,})
        
        if self.hw_usage_template:
            display_map.update(self.hw_usage_template)

        txt = str()

        for block in display_map:
              txt += f"{display_map[block]}\n\n"

        self.template = txt




    def print_progress_bar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent_value = 100*(iteration / float(total))
        percent = ("{0:." + str(decimals) + "f}").format(percent_value)
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        bar_body = f'{prefix} |{bar}| {suffix}'
        return bar_body

    def get_output_hw_data(self):
        # Получим данные из длительной задачи
        result = HardWareMonitor().to_dict()

        # Сохраним данные в CSV
        data = round(result['ram_free']), round(result['cpu_usage']), result['network_usage']
        # data_operation.create_telemerty_data()
        # data_operation.update_telemerty_data(data)

        #Подготавливаем строки для отображения на холсте
        ram_data, cpu_data, network_usage_data = data
        normilize_str = lambda x: str(x) if len(str(x)) > 1 else f'0{x}'
        otput_ram_info_str = f'RAM usage (RAM free {normilize_str(ram_data)}%)   {self.print_progress_bar(100-ram_data, 100, length=30)}'
        cpu_info_ouput_str = f'CPU usage {normilize_str(cpu_data)}%              {self.print_progress_bar(cpu_data, 100, length=30)}'
            
        network_info = []
        for net_adapter in network_usage_data:
            if network_usage_data[net_adapter]['up']>1 or network_usage_data[net_adapter]['down']:
                network_info.append([net_adapter,
                                     round(network_usage_data[net_adapter]['down']*0.000008,2),
                                     round(network_usage_data[net_adapter]['up']*0.000008,2)])
        # Создаим таблицу для отображения данных сетевых интерфейсов
        headers = ['Net adater', 'DOWNLOAD, Mbit/sec', 'UPLOAD, Mbit/sec']
        net_adapters_table_object = tabulate(network_info, headers, tablefmt="github")

        # Условно разделим холст на блоки 
        output_hw_data = {"3":otput_ram_info_str,
                          "4":cpu_info_ouput_str,
                          "5":net_adapters_table_object
                          }

        return output_hw_data

