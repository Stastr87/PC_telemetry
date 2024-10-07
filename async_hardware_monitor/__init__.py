from datetime import datetime
import psutil
import asyncio
import time

class HardWareMonitor():
    def __init__(self, monitor_period=5):
        '''Init HardWareMonitor object

        Arguments:
        monitor_period - period (sec) to check hardware usege (default = 5)
         '''
        self.monitor_period = monitor_period
        self.set_ram_free()
        self.cpu_usage = None
        self.network_usage = None
        # тут запускаются асинхронно функции которые требуют некоторое время для своего выполнения
        asyncio.run(self.wait_data())
        

    def to_dict(self):
        return {"ram_free":self.ram_free,
                "cpu_usage":self.cpu_usage[0],
                "network_usage":self.network_usage[0]}

    
    async def wait_data(self):
        ''' Запускает задачи которые требуют времени ожидания
        '''
        # tasks = []
        # tasks.append(asyncio.create_task(self.get_network_usage()))
        # tasks.append(asyncio.create_task(self.get_cpu_usage()))
        # self.network_usage = await asyncio.gather(*tasks)

        get_network_usage_task = asyncio.create_task(self.get_network_usage())
        get_cpu_usage_task = asyncio.create_task(self.get_cpu_usage())
        self.network_usage = await asyncio.gather(get_network_usage_task)
        self.cpu_usage = await asyncio.gather(get_cpu_usage_task)




        # self.network_usage = await self.get_network_usage()
        # self.cpu_usage = await self.get_cpu_usage()
    
    def set_ram_free(self):
        ''' Задает:
            атрибут класса - процент свободной памяти ram_free
        '''
        self.ram_free = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    
    async def get_cpu_usage(self):
        ''' Задает: 
            атрибут класса - нагрузка ЦП за указанный промежуток времени cpu_usage
        '''
        # print(f"get_cpu_usage called {time.strftime('%X')}")
        # Статиска потребления ЦП требует временного лага
        # await asyncio.sleep(self.monitor_period)
        cpu_usage = psutil.cpu_percent(interval=self.monitor_period)
        # print (f'cpu_usage {cpu_usage}')
        # print(f"get_cpu_usage finished {time.strftime('%X')}")
        return cpu_usage


    async def get_network_usage(self):
        ''' Задает:
            атрибут класса - статискика передачи данных всех сетевых интерфейсов network_usage
        '''
        # print(f"get_network_usage called {time.strftime('%X')}")
        # Статистика сети
        previous_state = {"data":psutil.net_io_counters(pernic=True),
                          "timestamp":datetime.now()}
        await asyncio.sleep(self.monitor_period)
        # Обновим статистику сети
        current_state = {"data":psutil.net_io_counters(pernic=True),
                         "timestamp":datetime.now()}
        network_usage = dict()
        for adapter in current_state["data"]:
            down_diff = getattr(current_state["data"][adapter], 'bytes_recv')-getattr(previous_state["data"][adapter], 'bytes_recv')
            up_diff = getattr(current_state["data"][adapter], 'bytes_sent')-getattr(previous_state["data"][adapter], 'bytes_sent')
            time_diff = current_state["timestamp"] - previous_state["timestamp"]
            time_diff_in_seconds = time_diff.total_seconds()
            #Подсчитали колличество байт за указанный промежуток
            down = down_diff / time_diff_in_seconds
            up = up_diff / time_diff_in_seconds
            network_usage.update({adapter:{"up":up,
                                           "down":down}})

        # print(f'network_usage::: {network_usage}')
        # print(f"get_network_usage finished {time.strftime('%X')}")
        return network_usage