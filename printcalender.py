import calendar
import sys
import tkinter as tk            #sudo apt-get install python3-tk (Ubuntu)
from tkinter import messagebox
from tkinter import filedialog
from natsort import natsorted   #pip install natsort(Windows/Ubuntu)
from functools import partial

def lastweek(year, month, dow):
    n = calendar.monthrange(year, month)[1]
    l = range(n - 6, n + 1)
    w = calendar.weekday(year, month, l[0])
    w_l = [i % 7 for i in range(w, w + 7)]
    return l[w_l.index(dow)]

def nthweek(year, month, nth, dow):
    if nth < 1 or dow < 0 or dow > 6:
        return None

    first_dow, n = calendar.monthrange(year, month)
    day = 7 * (nth - 1) + (dow - first_dow) % 7 + 1

    return day if day <= n else None

def file_read(filepath):
    # ファイルを開く
    task_list=[]
    if len(filepath) != 0:
        fp = open(filepath,  'r', encoding="utf-8_sig")
        for line in fp:
            line = line.strip()
            line = line.replace("\n","")
            line = line.split(",")
            task_list.append(line)
        return task_list
    else:
        fp = ""
        return

def zeller(year, month, day):
    # 1月1日または月初めの曜日判定
    if month <= 2:
        year -= 1
        month += 10
    else:
        month -= 2
    w = day + int((13 * month - 1) / 5) + year + \
        int(year / 4) - int(year / 100) + int(year / 400)
    x = w % 7
    return x


def isleap(year):
    # うるう年判定
    if year % 100 == 0 and year % 400 != 0:
        return 0
    elif year % 4 == 0:
        return 1
    else:
        return 0


def printmonth(month,  month_day, weekday, task_list,  j, xmonth, ymonth, cal_print, sat_mode, sun_mode):
    # 月表示(月,月の日数,初日の曜日までの空白,予定リスト,予定リストの番目数,表示X座標,表示Y座標,表示ウィンドウ名,土曜着色,日曜着色)
    # その月のカレンダー表示
    block = 0
    i = 0
    i += 1
    newy = 40 + ymonth
    newx = 20 + xmonth
    # 月の初日曜日までの空白作成
    for i in range(0, weekday):
        printday = tk.Label(cal_print, text="  ")
        printday.place(x=newx, y=newy)
        block += 1
        newx += 20

    for day in range(1,month_day+1):
        # 予定リスト確認
        task_month = 0
        task_day = 0

        if j < len(task_list):
            # 予定リスト１行取得して配列に分割
            # [月,日,内容]
            task_month = task_list[j][0]
            task_day = task_list[j][1]
            task_about = task_list[j][2]
            flag = 0
            # 予定リスト判定
            if (int(task_month) == (1 or 3 or 5 or 7 or 8 or 10 or 12)):
                if(-35<=int(task_day)<=31):
                    flag = 0
                else:
                    flag = 1
            elif (int(task_month) == (4 or 6 or 9 or 11)):
                if(-35<=int(task_day)<=30):
                    flag = 0
                else:
                    flag = 1
            elif (int(task_month) == 2):
                if(-35<=int(task_day)<=int(month_day)):
                    flag = 0
                else:
                    flag = 1

            if flag == 1:
                task_list.remove(task_list[j])

        if(int(task_month) == int(month) and int(task_day) == int(day)):
            color = "red1"
            if  int(task_day)< 10 and int(task_month) < 10:
                task_print = "0"+str(task_month)+"月0" +\
                    str(task_day)+"日："+str(task_about)
            elif int(task_day) < 10:
                task_print = str(task_month)+"月0" +\
                    str(task_day)+"日："+str(task_about)
            elif int(task_month) < 10:
                task_print = "0"+str(task_month)+"月" +\
                    str(task_day)+"日："+str(task_about)
            else:
                task_print = str(task_month)+"月" +\
                    str(task_day)+"日："+str(task_about)
            
            print_task = tk.Label(
                cal_print, text=task_print, foreground="black")
            print_task.place(x=500, y=40+(j*20))
            
            while 1:
                if j+1 < len(task_list) != "":
                    task_print=""
                    print_task=""
                    next_task_month = task_list[j+1][0]
                    next_task_day = task_list[j+1][1]
                    next_task_about = task_list[j+1][2]

                    if not((int(task_month) == int(next_task_month)) and (int(task_day) == int(next_task_day))):
                        j += 1
                        break
                    else:
                        j += 1
                        if int(next_task_day) < 10 and int(next_task_month) < 10:
                            task_print = "0"+str(next_task_month)+"月0" +\
                            str(next_task_day)+"日："+str(next_task_about)
                        elif int(next_task_day) < 10:
                            task_print = str(next_task_month)+"月0" +\
                                str(next_task_day)+"日："+str(next_task_about)
                        elif int(next_task_month) < 10:
                            task_print = "0"+str(next_task_month)+"月" +\
                                str(next_task_day)+"日："+str(next_task_about)
                        else:
                            task_print = str(next_task_month)+"月" +\
                                str(next_task_day)+"日："+str(next_task_about)
                        print_task = tk.Label(
                        cal_print, text=task_print, foreground="black")
                        print_task.place(x=500, y=40+(j*20))

                else:
                    break
                    

        elif(block % 7 == 6 and sat_mode == 0):
            # 土曜日を青色に着色
            color = "darkBlue"
        elif(block % 7 == 0 and sun_mode == 0):
            # 日曜日を赤色に着色
            color = "red3"
        else:
            # 予定もなく普通の日は黒色に着色
            color = "black"
            
        printday = tk.Label(cal_print, text=day, foreground=color)
        printday.place(x=newx, y=newy)

        newx += 20
        if (6 == block % 7):
            newx = 20 + xmonth
            newy += 20
        block += 1
    weekday = block % 7
    return (weekday, j)


def exit():
    ans = messagebox.askyesno("確認", "このアプリを終了しますか？")
    if ans == True:
        sys.exit()

def make_file(i):
    if i == 0:
        ftype = [("テキストファイル", "*.txt")]
        filepath = tk.filedialog.askopenfilename(filetypes=ftype)
        if filepath != "":
            print("ファイルを開きました")
            task_txt = file_read(filepath)
        else:
            task_txt = []
        i += 1
    print(task_txt)
    make_window = tk.Tk()
    make_window.title("ファイル作成")
    make_window.geometry("600x600")
    about = tk.Label(make_window, text="ここでは読み込み用ファイルを作成できます。")
    about.place(x=20, y=20)

    about_month = tk.Label(make_window, text="予定・月(必須)")
    about_month.place(x=20, y=40)

    entry_month = tk.Entry(make_window)
    entry_month.place(x=20, y=70)

    about_day = tk.Label(make_window, text="予定・日(必須)")
    about_day.place(x=20, y=100)
    about_day_2 = tk.Label(make_window,text="特別な日を設定する場合は右のメニューから選択してください。")
    about_day_2.place(x=20, y=120)

    entry_day = tk.Entry(make_window)
    entry_day.place(x=20, y=150)

    task_about = tk.Label(make_window, text="予定の内容(任意)")
    task_about.place(x=20, y=180)

    entry_about = tk.Entry(make_window,width=20)
    entry_about.place(x=20, y=210)
    
    def view_file():
        print(task_txt)
        view_list = tk.Tk()
        view_list.title("ファイルの内容")
        view_list.geometry("300x600")
        about = tk.Label(view_list, text="現在のファイルの内容です")
        about.place(x=20, y=20)
        for i in range(0,len(task_txt)):
            list_month = task_txt[i][0]
            list_day = task_txt[i][1]
            list_about = task_txt[i][2]
            if int(list_day) < 0 and int(list_month)<10:
                task_print = "0"+str(list_month)+"月" +\
                    "特殊日："+str(list_about)
            elif  int(list_day)< 10 and int(list_month) < 10:
                task_print = "0"+str(list_month)+"月0" +\
                    str(list_day)+"日："+str(list_about)
            elif int(list_day) < 10:
                task_print = str(list_month)+"月0" +\
                    str(list_day)+"日："+str(list_about)
            elif int(list_month) < 10:
                task_print = "0"+str(list_month)+"月" +\
                    str(list_day)+"日："+str(list_about)
            else:
                task_print = str(list_month)+"月" +\
                    str(list_day)+"日："+str(list_about)
            
            print_task = tk.Label(
                view_list, text=task_print, foreground="black")
            print_task.place(x=20, y=40+(i*20))

        def view_close():
            view_list.destroy() 

        exit_button = tk.Button(view_list, text="閉じる", command=view_close, width=15, height=2)
        exit_button.place(x=20, y=530)
        tk.mainloop()



    def add_file():
        add_list=[]
        flag = 0
        task_month = entry_month.get()        
        task_day = entry_day.get()
        task_about = entry_about.get()

        add_list.append(task_month)
        add_list.append(task_day)
        add_list.append(task_about)
        task_txt.append(add_list)
        print(task_txt)



    def remove_file():
        add_list=[]
        task_month = entry_month.get()
        add_list.append(task_month)
        
        task_day = entry_day.get()
        add_list.append(task_day)

        task_about = entry_about.get()
        add_list.append(task_about)

        task_txt.remove(add_list)
        print(task_txt)

    def force_save_file():
        save_txt = natsorted(task_txt)
        types = [("テキストファイル", ".txt")]
        filename = filedialog.asksaveasfilename(filetypes=types)
        if filename != "":
            fp = open(filename,"w",encoding="utf-8_sig")
            fp.write("")
            fp.close()

            fp = open(filename,"a",encoding="utf-8_sig")
            for i in range(0,len(save_txt)):
                line = save_txt[i][0] + ","+save_txt[i][1]+","+save_txt[i][2]+"\n"
                fp.writelines(line)              
            fp.close()
        else:
            return

    def save_file():
        save_txt = natsorted(task_txt)
        types = [("テキストファイル", ".txt")]
        filename = filedialog.asksaveasfilename(filetypes=types)
        if filename != "":
            fp = open(filename,"a",encoding="utf-8_sig")
            for i in range(0,len(save_txt)):
                line = save_txt[i][0] + ","+save_txt[i][1]+","+save_txt[i][2]+"\n"
                fp.writelines(line)              
            fp.close()

    def close():
        ret = messagebox.askyesno('確認','このモードを終了しますか？')
        if ret == False:
            return
        make_window.destroy()
    
    view_button = tk.Button(make_window, text="予定確認",
                            command=view_file, width=15, height=2)
    view_button.place(x=20, y=320)

    add_button = tk.Button(make_window, text="予定追加",
                            command=add_file, width=15, height=2)
    add_button.place(x=20, y=390)

    remove_button = tk.Button(make_window, text="予定削除", command=remove_file, width=15, height=2)
    remove_button.place(x=20, y=390)

    add_button = tk.Button(make_window, text="予定追加", command=add_file, width=15, height=2)
    add_button.place(x=210, y=390)

    force_save_button = tk.Button(make_window, text="上書き保存",
                            command=force_save_file, width=15, height=2)
    force_save_button.place(x=20, y=460)

    save_button = tk.Button(make_window, text="追記保存",
                            command=save_file, width=15, height=2)
    save_button.place(x=210, y=460)

    open_button = tk.Button(make_window, text="ファイルを開く", command=close, width=15, height=2)
    open_button.place(x=20, y=530)

    exit_button = tk.Button(make_window, text="終了する", command=close, width=15, height=2)
    exit_button.place(x=210, y=530)

    tk.mainloop()

def start_month():
    # 1か月のカレンダー作成
    setting = tk.Tk()
    setting.title("カレンダー設定")
    setting.geometry("440x500")

    about_year = tk.Label(setting, text="作成する年(西暦,必須)")
    about_year.place(x=20, y=20)

    entry_year = tk.Entry(setting)
    entry_year.place(x=20, y=50)

    month_list = ["", "1月", "2月", "3月", "4月", "5月", "6月",
                  "7月", "8月", "9月", "10月", "11月", "12月"]

    about_month = tk.Label(setting, text="作成する月(西暦,必須)")
    about_month.place(x=20, y=80)

    month_var = tk.IntVar()

    for i in range(1, len(month_list)):
        entry_month = tk.Radiobutton(
            setting, value=i, variable=month_var, text=month_list[i])
        entry_month.place(x=20, y=100+((i-1)*25))

    about_sunday = tk.Label(setting, text="日曜日赤色表示")
    about_sunday.place(x=220, y=20)

    about_saturday = tk.Label(setting, text="土曜日赤色表示")
    about_saturday.place(x=220, y=20)

    saturday_mode_list = ["ON", "OFF"]

    saturday_mode_var = tk.IntVar()

    for i in range(0, len(saturday_mode_list)):
        entry_month = tk.Radiobutton(
            setting, value=i, variable=saturday_mode_var, text=saturday_mode_list[i])
        entry_month.place(x=220, y=40+(i*25))

    about_sunday = tk.Label(setting, text="日曜日赤色表示")
    about_sunday.place(x=320, y=20)

    sunday_mode_list = ["ON", "OFF"]

    sunday_mode_var = tk.IntVar()

    for i in range(0, len(sunday_mode_list)):
        entry_month = tk.Radiobutton(
            setting, value=i, variable=sunday_mode_var, text=sunday_mode_list[i])
        entry_month.place(x=320, y=40+(i*25))


    def btn_start():
        year = entry_year.get()
        month = month_var.get()
        sat_mode = saturday_mode_var.get()
        sun_mode = sunday_mode_var.get()
        task_list = []
        ret = messagebox.askyesno(
            '確認', year + '年' + month_list[month] + 'を作成しますか？')
        if not(0 <= int(year) <= 9999):
            return
        if ret == False:
            return
        else:
            weekday = zeller(int(year), int(month), 1)
            leap = isleap(int(year))
            cal_print = tk.Tk()
            cal_print.title("生成結果")
            cal_print.geometry("190x280")
            printyear = str(year) + "年" + str(month) + "月"
            mon = tk.Label(cal_print, text=printyear)
            mon.place(x=50, y=20)

            week_list = ["日", "月", "火", "水", "木", "金", "土"]
            for i in range(len(week_list)):
                week = tk.Label(cal_print, text=week_list[i])
                week.place(x=20+(20*i), y=40)

            ymonth = 20
            xmonth = 0
        if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
            day = 31
        elif(month == 4 or month == 6 or month == 9 or month == 11):
            day = 30
        elif(leap == 1):
            day = 29
        else:
            day = 28

        printmonth(int(month),  int(day), weekday, task_list,  0, xmonth, ymonth, cal_print, sat_mode, sun_mode)

        def month_close():
            cal_print.destroy()

        close = tk.Button(
            cal_print, text="閉じる", command=month_close, width=15, height=2)
        close.place(x=20, y=200)
        tk.mainloop()

    next_button = tk.Button(setting, text="カレンダーを作る",
                            command=btn_start, width=15, height=2)
    next_button.place(x=20, y=420)

    exit_button = tk.Button(
        setting, text="終了する", command=exit, width=15, height=2)
    exit_button.place(x=175, y=420)

    tk.mainloop()


def start_year():
    # 1年のカレンダー作成
    setting = tk.Tk()
    setting.title("カレンダー設定")
    setting.geometry("440x320")

    about_year = tk.Label(setting, text="生成する年(西暦,必須)")
    about_year.place(x=20, y=20)

    about_saturday = tk.Label(setting, text="土曜日赤色表示")
    about_saturday.place(x=220, y=20)

    saturday_mode_list = ["ON", "OFF"]

    saturday_mode_var = tk.IntVar()

    for i in range(0, len(saturday_mode_list)):
        entry_month = tk.Radiobutton(
            setting, value=i, variable=saturday_mode_var, text=saturday_mode_list[i])
        entry_month.place(x=220, y=40+(i*25))

    about_sunday = tk.Label(setting, text="日曜日赤色表示")
    about_sunday.place(x=320, y=20)

    sunday_mode_list = ["ON", "OFF"]

    sunday_mode_var = tk.IntVar()

    for i in range(0, len(sunday_mode_list)):
        entry_month = tk.Radiobutton(
            setting, value=i, variable=sunday_mode_var, text=sunday_mode_list[i])
        entry_month.place(x=320, y=40+(i*25))

    entry_year = tk.Entry(setting)
    entry_year.place(x=20, y=50)

    def btn_start():
        year = entry_year.get()
        sat_mode = saturday_mode_var.get()
        sun_mode = sunday_mode_var.get()
        filepath = entry_path.get()
        if filepath != "":
            tasklist = file_read(filepath)
        else:
            tasklist = []
        
        for i in range(len(tasklist)):
            special_day = tasklist[i][1]
            special_month = tasklist[i][0]
            if int(special_day) <= -1:
                lastweek_mode = 1
                dow = (abs(int(special_day))%7)
                if -7 <= int(special_day) <= -1:
                    nth = 1
                elif -14 <= int(special_day) <=-8:
                    nth = 2    
                elif -21 <= int(special_day) <=-15:
                    nth = 3
                elif -28 <= int(special_day) <=-22:
                    nth = 4
                else:
                    lastweek_mode = 0
                    task_day = lastweek(int(year), int(special_month), dow)
                
                if lastweek_mode == 1:
                    task_day = nthweek(int(year),int(special_month) , nth, dow)
                
                tasklist[i][1] = str(task_day)      

        task_list = natsorted(tasklist)

        ret = messagebox.askyesno(
            '確認', year + '年を作成しますか？')
        if not(0 <= int(year) <= 9999):
            return
        if ret == False:
            return
        else:
            weekday = zeller(int(year), 1, 1)
            leap = isleap(int(year))
            cal_print = tk.Tk()
            cal_print.title("生成結果")
            cal_print.geometry("780x780")
            printyear = str(year) + "年"
            mon = tk.Label(cal_print, text=printyear)
            mon.place(x=20, y=20)

            ymonth = 40
            xmonth = 0
            xweek = 20
            yweek = 60
            xnew = 70
            ynew = 40
            j = 0
            printtask = tk.Label(
                cal_print, text="予定一覧", foreground="black")
            printtask.place(x=500, y=20)
        
        for month in range(1, 13):
            month_list = ["", "1月", "2月", "3月", "4月", "5月", "6月",
                          "7月", "8月", "9月", "10月", "11月", "12月"]
            mon = tk.Label(cal_print, text=month_list[month])
            mon.place(x=xnew, y=ynew)

            week_list = ["日", "月", "火", "水", "木", "金", "土"]
            for i in range(len(week_list)):
                week = tk.Label(cal_print, text=week_list[i])
                week.place(x=xweek+(20*i), y=yweek)

            if (month == (1 or 3 or 5 or 7 or 8 or 10 or 12)):
                day = 31
            elif(month == (4 or 6 or 9 or 11)):
                day = 30
            elif(leap == 1):
                day = 29
            else:
                day = 28
            c = printmonth(int(month),  int(day), int(
                weekday), task_list,  j, xmonth, ymonth, cal_print, sat_mode, sun_mode)
            weekday = c[0]
            j = c[1]
            xmonth += 160
            xweek += 160
            xnew = xnew + 160
            if(month % 3 == 0):
                xmonth = 0
                xnew = 70
                xweek = 20
                ymonth += 160
                yweek += 160
                ynew = ynew + 160

        def year_close():
            cal_print.destroy()

        close = tk.Button(
            cal_print, text="閉じる", command=year_close, width=15, height=2)
        close.place(x=20, y=700)
        tk.mainloop()

    file_about = tk.Label(setting, text="読み込むファイル(任意)")
    file_about.place(x=20, y=100)
    entry_path = tk.Entry(setting, width=39)
    entry_path.place(x=20, y=130)

    def file_open():
        ftype = [("テキストファイル", "*.txt")]
        filepath = tk.filedialog.askopenfilename(filetypes=ftype)
        if filepath != "":
            entry_path.delete(0, tk.END)
            entry_path.insert(tk.END, filepath)
            print("ファイルを開きました")
        return

    fileopen_button = tk.Button(setting, text="ファイルを開く",
                            command=file_open, width=15, height=2)
    fileopen_button.place(x=20, y=180)

    filemake_button = tk.Button(setting, text="読み込みファイル作成",
                            command=partial(make_file, 0), width=15, height=2)
    filemake_button.place(x=180, y=180)

    next_button = tk.Button(setting, text="カレンダーを作る",
                            command=btn_start, width=15, height=2)
    next_button.place(x=20, y=250)

    exit_button = tk.Button(
        setting, text="終了する", command=exit, width=15, height=2)
    exit_button.place(x=180, y=250)

    tk.mainloop()


def start():
    num = cal_mode_var.get()
    ret = messagebox.askyesno('確認', cal_mode[num]+'を作成しますか？')
    if ret == False:
        return
    root.destroy()
    if num == 0:
        start_year()
    else:
        start_month()


# メインウィンドウ
root = tk.Tk()
root.title("カレンダー作成")
root.geometry("380x230")
about = tk.Label(root, text="このプログラムはカレンダーを作成することができます。")
about.place(x=20, y=20)
mode_about = tk.Label(root, text="使用するモードを選択してください。")
mode_about.place(x=20, y=40)
cal_mode = ['1年のカレンダー', '1ヶ月のカレンダー']
# ラジオボタンの状態
cal_mode_var = tk.IntVar()

for i in range(len(cal_mode)):
    rdo = tk.Radiobutton(
        root, value=i, variable=cal_mode_var, text=cal_mode[i])
    rdo.place(x=80, y=80 + (i * 25))

next_button = tk.Button(root, text="カレンダーを作る",
                        command=start, width=15, height=2)
next_button.place(x=20, y=160)

exit_button = tk.Button(root, text="終了する", command=exit, width=15, height=2)
exit_button.place(x=210, y=160)

tk.mainloop()
