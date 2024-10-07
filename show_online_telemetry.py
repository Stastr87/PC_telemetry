import curses, canvas_data
from tabulate import tabulate
from datetime import datetime
import asyncio

def draw(canvas):
    # Обычно приложения curses отключают автоматическое отображение клавиш на экране,
    # чтобы иметь возможность читать клавиши и отображать их только при определенных обстоятельствах. 
    # Для этого необходимо вызвать функцию noecho().
    curses.noecho()

    # Приложениям также обычно требуется мгновенно реагировать на клавиши, 
    # не требуя нажатия клавиши Enter; это называется режимом cbreak, 
    # в отличие от обычного режима ввода с буферизацией.
    curses.cbreak()
    
    # Добавим набор стилей для отображения текста
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    
    while True:
        canvas.clear()
        canvas.border()
        # Отключить мигающий курсор
        curses.curs_set(False)

        height,width = canvas.getmaxyx()
        
        # Зададим значение главного отступа для всех строк main_offset
        main_offset = 2

        # Получим данные для отображения на холсте
        display_data = canvas_data.get_txt()

        # Построчно назместим в окне
        rows = display_data.split('\n')
        
        # Для того что бы окно не падало с ошибкой добавим заглушку для отображения
        # Найдем самую длинную строку
        row_len_list = list(map(lambda x: len(x),rows))
        min_width = max(row_len_list)
        
        if width<min_width:
            canvas.addstr(1, 1, f'min widht {min_width}')
        
        else:
            for row in range(len(rows)):
                if row==0 or row==1:
                    canvas.addstr(row+1, main_offset+round(min_width/2)-round(len(rows[row])/2), rows[row])
                else:
                    canvas.addstr(row+1, main_offset, rows[row])

        canvas.refresh()
        # time.sleep(1)
        
        # Обновление холста будет работать автоматически без ожидания нажатий клавиш
        canvas.nodelay(True)
        key = canvas.getch()
        
        if key == 27:
            curses.nocbreak()
            canvas.keypad(False)
            curses.echo()
            # endwin - завершает сессию и возвращает в обычную консоль
            curses.endwin()
            print(f"EXIT")
            quit()


  
if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)