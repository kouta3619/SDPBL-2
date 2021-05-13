import calendar
import datetime
import sys
import tkinter as tk            #sudo apt-get install python3-tk (Ubuntu)
from tkinter import messagebox
from tkinter import filedialog
from natsort import natsorted   #pip install natsort(Windows/Ubuntu)

def get_day_of_nth_dow(year, month, nth, dow):
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

        # 予定リスト判定
        if int(task_month) == int(month) and (int(task_day) < 0):
            print("特殊モード")
        if(int(task_month) == int(month) and int(task_day) == int(day)):
            color = "red1"
            if day < 10 and month < 10:
                task_about = "0"+str(task_month)+"月0" +\
                    str(task_day)+"日："+str(task_about)
            elif day < 10:
                task_about = str(task_month)+"月0" +\
                    str(task_day)+"日："+str(task_about)
            elif month < 10:
                task_about = "0"+str(task_month)+"月" +\
                    str(task_day)+"日："+str(task_about)
            else:
                task_about = str(task_month)+"月" +\
                    str(task_day)+"日："+str(task_about)
            printtask = printday = tk.Label(
                cal_print, text=task_about, foreground="black")
            printtask.place(x=500, y=40+(j*20))
            j += 1

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
            task_list = file_read(filepath)
        else:
            task_list = []

        print(task_list)
        
        for i in range(len(task_list)):
            special_day = task_list[i][1]
            special_month = task_list[i][0]
            if int(special_day) <= -1:
                if -7 <= int(special_day) <= -1:
                    nth = 1
                    dow = abs(int(special_day))
                    print(dow)
                elif -14 <= int(special_day) <=-8:
                    nth = 2
                    dow = (abs(int(special_day))%7)
                    print(dow)
                elif -21 <= int(special_day) <=-15:
                    nth = 3
                    dow = (abs(int(special_day))%7)
                    print(dow)
                elif -28 <= special_day <=-22:
                    nth = 4
                    dow = (abs(int(special_day))%7)
                    print(dow)

                task_day = get_day_of_nth_dow(int(year),int(special_month) , nth, dow)
                task_list[i][1] = task_day           
             
       
        print(natsorted(task_list))

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

            if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                day = 31
            elif(month == 4 or month == 6 or month == 9 or month == 11):
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

    next_button = tk.Button(setting, text="ファイルを開く(予定を読み込む場合)",
                            command=file_open, width=35, height=2)
    next_button.place(x=20, y=180)
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
