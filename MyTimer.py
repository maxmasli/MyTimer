import random
from tkinter import *
from tkinter.messagebox import *
from collections import Counter


class Timer:
    def __init__(self, main):  # вводим переменные
        self.ms = 0
        self.s = 0
        self.m = 0
        self.after_id = ''
        self.night = False
        self.col = None
        self.is_input = False
        self.last_scrs333 = []
        self.last_scrs222 = []
        self.solves333 = []
        self.solves222 = []
        self.solves_sec333 = []
        self.solves_sec222 = []
        self.sol_count333 = 0
        self.sol_count222 = 0
        self.current_event = "333"
        self.in_time = False
        self.col_fg = "black"

        self.text_of_scr = Label(main, text="", bg='lightgray', width=43, font='Calibri 17')  # текст скрамбла
        self.text_of_scr.place(x=157, y=25)

        self.button_gener = Button(main, bg='gray', text=u'Новый скрамбл',
                                   font='Calibri 13')  # создаем кнопку для генерации скера
        self.button_gener.place(x=24, y=25)
        self.button_gener.bind('<Button-1>', self.get_scr)

        self.timer = Label(main, text=u'0:00.00', font='Calibri 100')  # таймер
        self.timer.place(x=200, y=210)

        self.avg5 = Label(main, text='AVG 5: ---', font='Calibri 30')  # авг 5
        self.avg5.place(x=280, y=350)

        self.avg12 = Label(main, text='AVG 12: ---', font='Calibri 30')  # авг 12
        self.avg12.place(x=280, y=410)

        self.scrollbar = Scrollbar(main)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.results = Listbox(main, yscrollcommand=self.scrollbar.set, font='Calibri 16', width=50,
                               height=17, )  # таблица справа
        self.results.place(x=740, y=20)
        self.scrollbar.config(command=self.results.yview)

        self.get_plus2 = Button(main, text='+2', font='Calibri 30', height=1, width=8, bg='gray')  # кнопка +2
        self.get_plus2.place(x=220, y=470)
        self.get_plus2.bind('<Button-1>', self.do_plus2)

        self.get_dnf = Button(main, text='DNF', font='Calibri 30', height=1, width=8, bg='gray')  # кнопка DNF
        self.get_dnf.place(x=420, y=470)
        self.get_dnf.bind('<Button-1>', self.do_dnf)

        self.clear_results = Button(main, text='Сбросить результаты', font='Calibri 13', height=1,
                                    bg='gray')  # кнопка сбросить результаты
        self.clear_results.place(x=24, y=75)
        self.clear_results.bind('<Button-1>', self.clear_res)

        self.clear_one = Button(main, text='Удалить сборку', font='Calibri 9', width=20,
                                bg='gray')  # кнопка удалить сборку
        self.clear_one.place(x=740, y=485)
        self.clear_one.bind('<Button-1>', self.clear_on)

        self.info = Button(main, text='Info', font='Calibri 12', bg='gray')  # кнопка инфо
        self.info.place(x=690, y=25)
        self.info.bind('<Button-1>', self.sinfo)

        self.night_theme = Button(main, text='Ночная тема', font='Calibri 12', bg='gray')  # кнопка ночной темы
        self.night_theme.place(x=24, y=180)
        self.night_theme.bind('<Button-1>', self.nighttheme)

        self.avg50 = Label(main, text='AVG 50: ---', font='Calibri 14')
        self.avg50.place(x=10, y=500)

        self.avg100 = Label(main, text='AVG 100: ---', font='Calibri 14')
        self.avg100.place(x=10, y=525)

        self.count = Label(main, text='Всего сборок: ' + str(self.sol_count333), font='Calibri 14')
        self.count.place(x=10, y=550)

        self.settings = Button(main, text='Настройки', font='Calibri 14', bg='gray')
        self.settings.place(x=24, y=225)
        self.settings.bind("<Button-1>", self.update_settings)

        self.lbl1 = Label(main, text='Entry BG HEX color')
        self.ent1 = Entry(main)
        self.btn1 = Button(main, text='Apply', font='Calibri 10', bg='gray')

        self.lbl2 = Label(main, text='Entry font HEX color')
        self.ent2 = Entry(main)
        self.btn2 = Button(main, text='Apply', font='Calibri 10', bg='gray')

        self.lbl3 = Label(main, text='Entry Button HEX color')
        self.ent3 = Entry(main)
        self.btn3 = Button(main, text='Apply', font='Calibri 10', bg='gray')

        self.btn2.place(x=1250, y=560)
        self.btn1.place(x=1250, y=530)
        self.btn3.place(x=1250, y=500)

        self.ent2.place(x=1120, y=562)
        self.ent1.place(x=1120, y=532)
        self.ent3.place(x=1120, y=502)

        self.lbl2.place(x=1000, y=560)
        self.lbl1.place(x=1008, y=530)
        self.lbl3.place(x=987, y=500)

        self.btn1.bind('<Button-1>', self.change_bg)
        self.btn2.bind('<Button-1>', self.change_fg)
        self.btn3.bind('<Button-1>', self.change_btn)

        self.main_menu = Menu(main)
        main.configure(menu=self.main_menu)

        self.event_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Event", menu=self.event_menu)
        self.event_menu.add_command(label="3x3x3", command=self.change_on_333)
        self.event_menu.add_command(label="2x2x2", command=self.change_on_222)

        self.input_res = Button(root, text='Вводить время', font='Calibri 13', bg='gray')
        self.input_res.place(x=25, y=125)
        self.input_res.bind('<Button-1>', self.change_input)

    def tick(self):  # фукнция тайера
        self.after_id = root.after(10, self.tick)
        self.ms += 1
        if self.ms >= 100:
            self.ms = 0
            self.s += 1
        if self.s >= 60:
            self.m += 1
            self.s = 0
        if len(str(self.s)) < 2:
            if len(str(self.ms)) < 2:
                self.timer.configure(text=str(self.m) + ':' + '0' + str(self.s) + '.' + '0' + str(self.ms))
            else:
                self.timer.configure(text=str(self.m) + ':' + '0' + str(self.s) + '.' + str(self.ms))
        else:
            if len(str(self.ms)) < 2:
                self.timer.configure(text=str(self.m) + ':' + str(self.s) + '.' + '0' + str(self.ms))
            else:
                self.timer.configure(text=str(self.m) + ':' + str(self.s) + '.' + str(self.ms))

    def start_tick(self, event):  # начало таймера
        self.ms = 0
        self.s = 0
        self.m = 0
        self.tick()

    def stop_tick(self, event):  # остановка таймера

        lscr = None
        root.after_cancel(self.after_id)
        if self.current_event == "333":
            self.sol_count333 += 1
            lscr = self.last_scrs333[-1]
            self.solves333.append(str(self.m) + ':' + str(self.s) + '.' + str(self.ms))
            if len(str(self.ms)) < 2:
                self.solves_sec333.append(self.m * 60 + self.s + float('0.0' + str(self.ms)))
            else:
                self.solves_sec333.append(self.m * 60 + self.s + float('0.' + str(self.ms)))
        elif self.current_event == "222":
            self.sol_count222 += 1
            lscr = self.last_scrs222[-1]
            self.solves222.append(str(self.m) + ':' + str(self.s) + '.' + str(self.ms))
            if len(str(self.ms)) < 2:
                self.solves_sec222.append(self.m * 60 + self.s + float('0.0' + str(self.ms)))
            else:
                self.solves_sec222.append(self.m * 60 + self.s + float('0.' + str(self.ms)))
        self.in_time = False

        if self.current_event == "333":
            self.get_333_scr(event)
            self.countAVG5(event, self.solves_sec333)
            self.countAVG12(event, self.solves_sec333)
            self.countAVG50(event, self.solves_sec333)
            self.countAVG100(event, self.solves_sec333)
            self.count.configure(text='Всего сборок: ' + str(self.sol_count333))
        elif self.current_event == "222":
            self.get_222_scr(event)
            self.countAVG5(event, self.solves_sec222)
            self.countAVG12(event, self.solves_sec222)
            self.countAVG50(event, self.solves_sec222)
            self.countAVG100(event, self.solves_sec222)
            self.count.configure(text='Всего сборок: ' + str(self.sol_count222))

        if self.m == 0:
            if len(str(self.ms)) < 2:
                self.results.insert(END, str(self.s) + '.' + '0' + str(self.ms) + ' -- ' + str(lscr))
                self.result_in_txt(str(self.s) + '.' + '0' + str(self.ms) + ' -- ' + str(lscr))
            else:
                self.results.insert(END, str(self.s) + '.' + str(self.ms) + ' -- ' + str(lscr))
                self.result_in_txt(str(self.s) + '.' + str(self.ms) + ' -- ' + str(lscr))
        else:
            if len(str(self.s)) < 2:
                if len(str(self.ms)) < 2:
                    self.results.insert(END,
                                        str(self.m) + ':' + '0' + str(self.s) + '.' + '0' + str(self.ms) + ' -- ' + str(
                                            lscr))
                    self.result_in_txt(
                        str(self.m) + ':' + '0' + str(self.s) + '.' + '0' + str(self.ms) + ' -- ' + str(lscr))
                else:
                    self.results.insert(END,
                                        str(self.m) + ':' + '0' + str(self.s) + '.' + str(self.ms) + ' -- ' + str(lscr))
                    self.result_in_txt(str(self.m) + ':' + '0' + str(self.s) + '.' + str(self.ms) + ' -- ' + str(lscr))
            else:
                if len(str(self.ms)) < 2:
                    self.results.insert(END,
                                        str(self.m) + ':' + str(self.s) + '.' + '0' + str(self.ms) + ' -- ' + str(lscr))
                    self.result_in_txt(str(self.m) + ':' + str(self.s) + '.' + '0' + str(self.ms) + ' -- ' + str(lscr))
                else:
                    self.results.insert(END, str(self.m) + ':' + str(self.s) + '.' + str(self.ms) + ' -- ' + str(lscr))
                    self.result_in_txt(str(self.m) + ':' + str(self.s) + '.' + str(self.ms) + ' -- ' + str(lscr))

    def sinfo(self, event):
        showinfo(title='Информация',
                 message='''
        MyTimer:
        Version - 1.3
        By Макс Бреднев
        ---------------------------------------------------
        Hotkeys:
        Home - new scramble
        * - DNF solve
        + - +2 solve
        Delete - delete last solve
        ---------------------------------------------------
        Если нашли баг, или просто хотите что-либо предложить,
        то писать мне в ВК: https://vk.com/pyrakal
        ''')

    def change_input(self, event):
        if self.is_input == False:
            self.timer.place_forget()
            self.inp_results = Entry(root, width=7, font='Calibri 85', justify=CENTER)
            self.inp_results.place(x=200, y=205)
            self.is_input = True
        else:
            self.timer.place(x=200, y=210)
            self.inp_results.place_forget()
            self.is_input = False

    def from_input_to_res(self, event):
        if self.is_input:
            res = self.inp_results.get()

            try:
                res = int(res)
                res = str(res)
                if len(res) == 1:
                    new_res = float('0.0' + str(res))
                    new_res_non = float(str(new_res))
                elif len(res) == 2:
                    new_res = float('0.' + str(res))
                    new_res_non = float(str(new_res))
                elif len(res) == 3:
                    new_res = float(res[:1] + '.' + res[1:])
                    new_res_non = float(str(new_res))
                elif len(res) == 4:
                    new_res = float(res[:2] + '.' + res[2:])
                    new_res_non = str(new_res)
                elif len(res) == 5:
                    new_res_non = res[:1] + ':' + res[1:3] + '.' + res[3:]
                    m = int(res[0])
                    new_res = float(m * 60 + float(res[1:3] + '.' + res[3:]))

                elif len(res) == 6:
                    new_res_non = res[:2] + ':' + res[2:4] + '.' + res[4:]
                    m = int(res[:2])
                    new_res = float(m * 60 + float(res[2:4] + '.' + res[4:]))

                else:
                    pass
            except ValueError:
                if res.lower() == 'dnf':
                    new_res_non = 'DNF'
                    new_res = 'DNF'
                else:
                    return

            if self.current_event == "333":
                self.sol_count333 += 1
                lscr = self.last_scrs333[-1]
                self.solves_sec333.append(new_res)

                self.get_333_scr(event)
                self.countAVG5(event, self.solves_sec333)
                self.countAVG12(event, self.solves_sec333)
                self.countAVG50(event, self.solves_sec333)
                self.countAVG100(event, self.solves_sec333)
                self.count.configure(text='Всего сборок: ' + str(self.sol_count333))

                self.results.insert(END, str(new_res_non) + ' -- ' + str(lscr))
                self.result_in_txt(str(new_res_non) + ' -- ' + str(lscr))

            elif self.current_event == "222":

                self.sol_count222 += 1
                lscr = self.last_scrs222[-1]
                self.solves_sec222.append(new_res)
                self.get_222_scr(event)
                self.countAVG5(event, self.solves_sec222)
                self.countAVG12(event, self.solves_sec222)
                self.countAVG50(event, self.solves_sec222)
                self.countAVG100(event, self.solves_sec222)
                self.count.configure(text='Всего сборок: ' + str(self.sol_count222))

                self.results.insert(END, str(new_res_non) + ' -- ' + str(lscr))
                self.result_in_txt(str(new_res_non) + ' -- ' + str(lscr))

            self.inp_results.delete(0, END)


        else:
            pass

    def update_settings(self, event):
        self.button_gener.grid_forget()
        


    def clear_res(self, event):
        if self.current_event == "333":
            self.results.delete(0, END)
            self.solves_sec333 = []
            self.countAVG5(event, self.solves_sec333)
            self.countAVG12(event, self.solves_sec333)
            self.countAVG50(event, self.solves_sec333)
            self.countAVG100(event, self.solves_sec333)
            self.sol_count333 = 0
            self.count.configure(text='Всего сборок: ' + str(self.sol_count333))
            self.txt_delete()
        elif self.current_event == "222":
            self.results.delete(0, END)
            self.solves_sec222 = []
            self.countAVG5(event, self.solves_sec222)
            self.countAVG12(event, self.solves_sec222)
            self.countAVG50(event, self.solves_sec222)
            self.countAVG100(event, self.solves_sec222)
            self.sol_count222 = 0
            self.count.configure(text='Всего сборок: ' + str(self.sol_count222))
            self.txt_delete()

    def clear_on(self, event):
        if self.current_event == "333":
            try:
                del self.solves_sec333[-1]
                self.sol_count333 -= 1
            except IndexError:
                pass
            self.results.delete(END)
            self.countAVG5(event, self.solves_sec333)
            self.countAVG12(event, self.solves_sec333)
            self.countAVG50(event, self.solves_sec333)
            self.countAVG100(event, self.solves_sec333)
            self.txt_delete_line()
            self.count.configure(text='Всего сборок: ' + str(self.sol_count333))
        elif self.current_event == "222":
            try:
                del self.solves_sec222[-1]
                self.sol_count222 -= 1
            except IndexError:
                pass
            self.results.delete(END)
            self.countAVG5(event, self.solves_sec222)
            self.countAVG12(event, self.solves_sec222)
            self.countAVG50(event, self.solves_sec222)
            self.countAVG100(event, self.solves_sec222)
            self.txt_delete_line()
            self.count.configure(text='Всего сборок: ' + str(self.sol_count222))

    def do_plus2(self, event):
        if self.current_event == "333":
            try:
                rez = self.solves_sec333[-1]
                rez_up = rez + 2
                self.results.delete(END)
                self.solves_sec333[-1] = rez_up
                round(rez_up, 2)
                if rez_up >= 60:
                    scr = self.last_scrs333[-2]
                    m = rez_up // 60
                    self.results.insert(END, str(int(m)) + ':' + str(round(rez_up - m * 60, 2)) + ' -- ' + str(scr))

                    f = open("results333.txt", 'r')
                    lines = f.readlines()
                    f.close()
                    f = open("results333.txt", 'w')
                    for line in lines[:-1]:
                        f.write(line)
                    f.write(str(int(m)) + ':' + str(round(rez_up - m * 60, 2)) + ' -- ' + str(scr))
                else:
                    scr = self.last_scrs333[-2]
                    self.results.insert(END, str(round(rez_up, 2)) + ' -- ' + str(scr))

                    f = open("results333.txt", 'r')
                    lines = f.readlines()
                    f.close()
                    f = open("results333.txt", 'w')
                    for line in lines[:-1]:
                        f.write(line)
                    f.write(str(round(rez_up, 2)) + ' -- ' + str(scr))

                self.countAVG5(event, self.solves_sec333)
                self.countAVG12(event, self.solves_sec333)
                self.countAVG50(event, self.solves_sec333)
                self.countAVG100(event, self.solves_sec333)

            except TypeError:
                pass

        elif self.current_event == "222":
            try:
                rez = self.solves_sec222[-1]
                rez_up = rez + 2
                self.results.delete(END)
                self.solves_sec222[-1] = rez_up
                round(rez_up, 2)
                if rez_up >= 60:
                    scr = self.last_scrs222[-2]
                    m = rez_up // 60
                    self.results.insert(END, str(int(m)) + ':' + str(round(rez_up - m * 60, 2)) + ' -- ' + str(scr))

                    f = open("results222.txt", 'r')
                    lines = f.readlines()
                    f.close()
                    f = open("results222.txt", 'w')
                    for line in lines[:-1]:
                        f.write(line)
                    f.write(str(int(m)) + ':' + str(round(rez_up - m * 60, 2)) + ' -- ' + str(scr))
                else:
                    scr = self.last_scrs222[-2]
                    self.results.insert(END, str(round(rez_up, 2)) + ' -- ' + str(scr))

                    f = open("results222.txt", 'r')
                    lines = f.readlines()
                    f.close()
                    f = open("results222.txt", 'w')
                    for line in lines[:-1]:
                        f.write(line)
                    f.write(str(round(rez_up, 2)) + ' -- ' + str(scr))

                self.countAVG5(event, self.solves_sec222)
                self.countAVG12(event, self.solves_sec222)
                self.countAVG50(event, self.solves_sec222)
                self.countAVG100(event, self.solves_sec222)

            except TypeError:
                pass

    def do_dnf(self, event):
        if self.current_event == "333":
            self.results.delete(END)
            scr = self.last_scrs333[-2]
            self.solves_sec333[-1] = 'DNF'
            self.results.insert(END, 'DNF' + ' -- ' + str(scr))
            self.countAVG5(event, self.solves_sec333)
            self.countAVG12(event, self.solves_sec333)
            self.countAVG50(event, self.solves_sec333)
            self.countAVG100(event, self.solves_sec333)

            f = open("results333.txt", 'r')
            lines = f.readlines()
            f.close()
            f = open("results333.txt", 'w')
            for line in lines[:-1]:
                f.write(line)
            f.write('DNF' + ' -- ' + str(scr))

        elif self.current_event == "222":
            self.results.delete(END)
            scr = self.last_scrs222[-2]
            self.solves_sec222[-1] = 'DNF'
            self.results.insert(END, 'DNF' + ' -- ' + str(scr))
            self.countAVG5(event, self.solves_sec222)
            self.countAVG12(event, self.solves_sec222)
            self.countAVG50(event, self.solves_sec222)
            self.countAVG100(event, self.solves_sec222)

            f = open("results222.txt", 'r')
            lines = f.readlines()
            f.close()
            f = open("results222.txt", 'w')
            for line in lines[:-1]:
                f.write(line)
            f.write('DNF' + ' -- ' + str(scr))

    def update_timer(self, event):
        if self.is_input == False:
            if self.in_time == False:
                self.start_tick(event)
                self.in_time = True
            else:
                self.stop_tick(event)
        else:
            pass

    def countAVG5(self, event, list):
        if len(list) < 5:
            self.avg5.configure(text='AVG 5: ---')
        else:
            c = Counter(list[-5:])
            if c['DNF'] >= 2:
                self.avg5.configure(text='AVG 5: DNF')
            else:
                copy = list[-5:]
                copy.remove(self.find_biggest(copy))
                copy.remove(self.find_smallest(copy))
                result = sum(copy) / 3
                if result >= 60:
                    min = result // 60
                    self.avg5.configure(text='AVG 5: ' + str(int(min)) + ':' + str(round(result - 60 * min, 3)))
                else:
                    self.avg5.configure(text='AVG 5: ' + str(round(result, 3)))

    def countAVG12(self, event, list):  # lol
        if len(list) < 12:
            self.avg12.configure(text='AVG 12: ---')
        else:
            c = Counter(list[-12:])
            if c['DNF'] >= 2:
                self.avg12.configure(text='AVG 12: DNF')
            else:
                copy = list[-12:]
                copy.remove(self.find_biggest(copy))
                copy.remove(self.find_smallest(copy))
                result = sum(copy) / 10
                if result >= 60:
                    min = result // 60
                    self.avg12.configure(text='AVG 12: ' + str(int(min)) + ':' + str(round(result - 60 * min, 3)))
                else:
                    self.avg12.configure(text='AVG 12: ' + str(round(result, 3)))

    def countAVG50(self, event, list):
        if len(list) < 50:
            self.avg50.configure(text='AVG 50: ---')
        else:
            c = Counter(list[-50:])
            if c['DNF'] >= 2:
                self.avg50.configure(text='AVG 50: DNF')
            else:
                copy = list[-50:]
                copy.remove(self.find_biggest(copy))
                copy.remove(self.find_smallest(copy))
                result = sum(copy) / 48
                if result >= 60:
                    min = result // 60
                    self.avg50.configure(text='AVG 50: ' + str(int(min)) + ':' + str(round(result - 60 * min, 3)))
                else:
                    self.avg50.configure(text='AVG 50: ' + str(round(result, 3)))

    def countAVG100(self, event, list):
        if len(list) < 100:
            self.avg100.configure(text='AVG 100: ---')
        else:
            c = Counter(list[-100:])
            if c['DNF'] >= 2:
                self.avg100.configure(text='AVG 100: DNF')
            else:
                copy = list[-100:]
                copy.remove(self.find_biggest(copy))
                copy.remove(self.find_smallest(copy))
                result = sum(copy) / 98
                if result >= 60:
                    min = result // 60
                    self.avg100.configure(text='AVG 100: ' + str(int(min)) + ':' + str(round(result - 60 * min, 3)))
                else:
                    self.avg100.configure(text='AVG 100: ' + str(round(result, 3)))

    def find_biggest(self, list):
        if 'DNF' in list:
            return 'DNF'
        else:
            biggest = list[0]
            for i in list:
                if i > biggest:
                    biggest = i
            return biggest

    def find_smallest(self, list):
        try:
            smallest = list[0]
            for i in list:
                if i < smallest:
                    smallest = i
            return smallest
        except TypeError:
            list.remove('DNF')
            smallest = list[0]
            for i in list:
                if i < smallest:
                    smallest = i
            return smallest

    def get_333(self):  # выдает скер
        lit = [["F", "F'", "F2"],
               ['B', "B'", 'B2'],
               ['U', "U'", 'U2'],
               ['D', "D'", 'D2'],
               ['R', "R'", 'R2'],
               ['L', "L'", 'L2']]
        scr = []
        temp = []
        temp_int = None
        while True:
            i = random.randrange(0, 6)
            if i in temp or i == temp_int:
                continue
            j = random.randrange(0, 3)
            if len(temp) < 3:
                temp.append(i)
            if len(temp) == 3:
                if (temp[0] in (0, 2, 4) and temp[0] == temp[2] and temp[0] + 1 == temp[1]) or (
                        temp[0] in (1, 3, 5) and temp[0] == temp[2] and temp[0] - 1 == temp[1]):
                    del temp[0]
                    continue
            scr.append(lit[i][j])
            if len(scr) >= 20:
                break
            if len(temp) == 3:
                del temp[0]
        self.text_of_scr.configure(text=scr)
        # del self.last_scrs333[-1]
        self.last_scrs333.append(' '.join(scr) + '\n')

    def get_333_scr(self, event):  # выдает скер
        lit = [["F", "F'", "F2"],
               ['B', "B'", 'B2'],
               ['U', "U'", 'U2'],
               ['D', "D'", 'D2'],
               ['R', "R'", 'R2'],
               ['L', "L'", 'L2']]
        scr = []
        temp = []
        temp_int = None
        while True:
            i = random.randrange(0, 6)
            if i in temp or i == temp_int:
                continue
            j = random.randrange(0, 3)
            if len(temp) < 3:
                temp.append(i)
            if len(temp) == 3:
                if (temp[0] in (0, 2, 4) and temp[0] == temp[2] and temp[0] + 1 == temp[1]) or (
                        temp[0] in (1, 3, 5) and temp[0] == temp[2] and temp[0] - 1 == temp[1]):
                    del temp[0]
                    continue

            scr.append(lit[i][j])
            if len(scr) >= 20:
                break
            if len(temp) == 3:
                del temp[0]
        self.text_of_scr.configure(text=scr)
        self.last_scrs333.append(' '.join(scr) + '\n')

    def get_222(self):
        scr = []

        temp = None

        lit = [["R", "R'", "R2"],
               ["F", "F'", "F2"],
               ["U", "U'", "U2"]]

        while True:
            i = random.randrange(0, 3)
            j = random.randrange(0, 3)
            if temp == i:
                continue
            else:
                temp = i
                scr.append(lit[i][j])
            if len(scr) >= 9:
                break

        self.text_of_scr.configure(text=scr)
        self.last_scrs222.append(' '.join(scr) + '\n')

    def get_222_scr(self, event):
        scr = []

        temp = None

        lit = [["R", "R'", "R2"],
               ["F", "F'", "F2"],
               ["U", "U'", "U2"]]

        while True:
            i = random.randrange(0, 3)
            j = random.randrange(0, 3)
            if temp == i:
                continue
            else:
                temp = i
                scr.append(lit[i][j])
            if len(scr) >= 9:
                break

        self.text_of_scr.configure(text=scr)
        self.last_scrs222.append(' '.join(scr) + '\n')
    
    def get_skewb_scr(self, event):
        scr = []
        
        temp = None
        
        lit = [["R", ]]

    def change_on_222(self):
        self.results.delete(0, END)
        try:
            f = open('results222.txt', 'r')
            while True:
                data = f.readline()
                data = str(data[:-1])
                if data != "":
                    self.results.insert(END, data)
                else:
                    break
            f.close()
        except FileNotFoundError:
            f = open('results222.txt', 'a')
            f.close()

        del self.last_scrs333[-1]
        self.current_event = "222"
        self.get_222()
        self.count.configure(text="Всего сборок: " + str(self.sol_count222))

    def change_on_333(self):
        self.results.delete(0, END)
        f = open('results333.txt', 'r')
        while True:
            data = f.readline()
            data = str(data[:-1])
            if data != "":
                self.results.insert(END, data)
            else:
                break
        f.close()
        del self.last_scrs222[-1]
        self.current_event = "333"
        self.get_333()
        self.count.configure(text="Всего сборок: " + str(self.sol_count333))

    def get_scr(self, event):
        if self.current_event == "333":
            self.get_333_scr(event)
        else:
            self.get_222_scr(event)

    ################################################## функции для (jopa) работы с текстовым файлом
    def result_in_txt(self, rez):
        if self.current_event == "333":
            results_txt = open('results333.txt', 'a+')
            results_txt.write(rez)
            results_txt.close()
        elif self.current_event == "222":
            results_txt = open('results222.txt', 'a+')
            results_txt.write(rez)
            results_txt.close()

    def txt_delete(self):
        if self.current_event == "333":
            f = open('results333.txt', 'w')
            f.close()
        elif self.current_event == "222":
            f = open('results222.txt', 'w')
            f.close()

    def txt_delete_line(self):
        if self.current_event == "333":
            f = open('results333.txt', 'r')
            lines = f.readlines()
            f.close()
            f = open('results333.txt', 'w')
            for i in lines[:-1]:
                f.write(str(i))
            f.close()
        elif self.current_event == "222":
            f = open('results222.txt', 'r')
            lines = f.readlines()
            f.close()
            f = open('results222.txt', 'w')
            for i in lines[:-1]:
                f.write(str(i))
            f.close()

    def podsvetka(self, event):
        if self.in_time == False and self.is_input == False:
            self.timer.configure(fg='green')
        else:
            self.timer.configure(fg=self.col_fg)

    def change_bg(self, event):
        col = self.ent1.get()
        root['bg'] = col
        self.timer.configure(bg=col)
        self.avg5.configure(bg=col)
        self.avg12.configure(bg=col)
        self.avg50.configure(bg=col)
        self.avg100.configure(bg=col)
        self.results.configure(bg=col)
        self.lbl1.configure(bg=col)
        self.lbl2.configure(bg=col)
        self.lbl3.configure(bg=col)
        self.count.configure(bg=col)
        self.ent1.destroy()
        self.ent1 = Entry(root)
        self.ent1.place(x=1120, y=532)

    def change_fg(self, event):
        col = self.ent2.get()
        self.timer.configure(fg=col)
        self.avg5.configure(fg=col)
        self.avg12.configure(fg=col)
        self.avg50.configure(fg=col)
        self.avg100.configure(fg=col)
        self.results.configure(fg=col)
        self.lbl1.configure(fg=col)
        self.lbl2.configure(fg=col)
        self.lbl3.configure(fg=col)
        self.count.configure(fg=col)
        self.ent2.destroy()
        self.ent2 = Entry(root)
        self.ent2.place(x=1120, y=562)
        self.col_fg = col

    def change_btn(self, event):
        col = self.ent3.get()
        self.btn3.configure(bg=col)
        self.btn2.configure(bg=col)
        self.btn1.configure(bg=col)
        self.night_theme.configure(bg=col)
        self.info.configure(bg=col)
        self.clear_one.configure(bg=col)
        self.clear_results.configure(bg=col)
        self.get_dnf.configure(bg=col)
        self.get_plus2.configure(bg=col)
        self.button_gener.configure(bg=col)
        self.ent3.destroy()
        self.ent3 = Entry(root)
        self.ent3.place(x=1120, y=502)

    def nighttheme(self, event):
        if self.night == False:
            root['bg'] = 'black'
            self.timer.configure(bg='black', fg='white')
            self.avg5.configure(bg='black', fg='white')
            self.avg12.configure(bg='black', fg='white')
            self.avg50.configure(bg='black', fg='white')
            self.avg100.configure(bg='black', fg='white')
            self.results.configure(bg='black', fg='white')
            self.count.configure(bg='black', fg='white')
            self.lbl1.configure(bg='black', fg='white')
            self.lbl2.configure(bg='black', fg='white')
            self.lbl3.configure(bg='black', fg='white')
            self.col_fg = 'white'
            self.night = True
        else:
            root['bg'] = 'white'
            self.timer.configure(bg='white', fg='black')
            self.avg5.configure(bg='white', fg='black')
            self.avg12.configure(bg='white', fg='black')
            self.avg50.configure(bg='white', fg='black')
            self.avg100.configure(bg='white', fg='black')
            self.results.configure(bg='white', fg='black')
            self.count.configure(bg='white', fg='black')
            self.lbl1.configure(bg='white', fg='black')
            self.lbl2.configure(bg='white', fg='black')
            self.lbl3.configure(bg='white', fg='black')
            self.col_fg = 'black'
            self.night = False


ch = random.choice(range(0, 100))  # делаем пасхалку
if ch == 99:
    tit = 'захер коч'
else:
    tit = 'MyTimer'

root = Tk()
root.geometry('1320x600')  # ширина 870пкс висота 600пкс
root.title(tit)
q = Timer(root)

try:
    f = open('results333.txt', 'r')
    while True:
        data = f.readline()
        data = str(data[:-1])
        if data != "":
            q.results.insert(END, data)
        else:
            break
    f.close()
except FileNotFoundError:
    f = open('results333.txt', 'a')
    f.close()

f = open('results333.txt', 'r')
lines = f.readlines()
counter_of_spaces = 0
for line in lines:
    counter_of_spaces = 0
    for i in line:
        if i == "-":
            counter_of_spaces += 1
            line = line.replace(i, '')
        elif i == " ":
            line = line[1:]
        else:
            line = line.replace(i, '')
        if counter_of_spaces >= 2:
            line = line[1:]
            break
    q.last_scrs333.append(line)
f.close()

try:
    f = open('results222.txt', 'r')
    lines = f.readlines()
    counter_of_spaces = 0
    for line in lines:
        counter_of_spaces = 0
        for i in line:
            if i == "-":
                counter_of_spaces += 1
                line = line.replace(i, '')
            elif i == " ":
                line = line[1:]
            else:
                line = line.replace(i, '')
            if counter_of_spaces >= 2:
                line = line[1:]
                break
        q.last_scrs222.append(line)
    f.close()
except FileNotFoundError:
    f = open('results222.txt', 'a')
    f.close()

f = open('results333.txt', 'r')
lines = f.readlines()
num = ''
for line in lines:
    for i in line:
        if i != ' ':
            num = num + str(i)
        else:
            break
    try:
        q.solves_sec333.append(float(num))
    except ValueError:
        q.solves_sec333.append(str('DNF'))
    q.sol_count333 += 1
    num = ''
f.close()

f = open('results222.txt', 'r')
lines = f.readlines()
num = ''
for line in lines:
    for i in line:
        if i != ' ':
            num = num + str(i)
        else:
            break
    try:
        q.solves_sec222.append(float(num))
    except ValueError:
        q.solves_sec222.append(str('DNF'))
    q.sol_count222 += 1
    num = ''
f.close()

q.get_333()

##################################################################################### тут все бинды
root.bind('<KeyRelease-space>', q.update_timer)
root.bind('<space>', q.podsvetka)

root.bind('<Home>', q.get_scr)

root.bind('<*>', q.do_dnf)

root.bind('<+>', q.do_plus2)

root.bind('<Delete>', q.clear_on)

root.bind('<Return>', q.from_input_to_res)
####################################################################################

root.mainloop()
