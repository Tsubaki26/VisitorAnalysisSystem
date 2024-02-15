import mysql.connector
import datetime
import matplotlib.pyplot as plt

area_threthold = 0.99
plt.rcParams['font.family'] = 'MS Gothic'

class DB_controller():
    def __init__(self):
        self.conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='mysqlkeito1340@',
        db='visitordb'
        )
        self.cursor = self.conn.cursor()

    #データベースに格納
    def insert_db(self,results,path,dt):
        area = results['area'][0]
        area_accuracy = results['area'][1]
        num1 = results['num1']
        kana = results['kana']
        num2 = results['num2']

        if area_accuracy < area_threthold*100:
            area = 'other'

        date = str(dt.date())
        year, month, day = date.split('-')
        year, month, day = int(year), int(month), int(day)
        time = dt.time()
        #ex. 2023-11-12 23:11:03.900627

        #地名DBから地名IDを取得
        self.cursor.execute('select area_id from area where area_name="{}"'.format(area))
        a = self.cursor.fetchall()
        for row in a:
            area_id = row[0]

        #ナンバープレートDBで同一ナンバーを検索
        self.cursor.execute('select license_plate_id from license_plate where area_id={} and class_number="{}" \
            and kana="{}" and serial_number="{}"'.format(area_id,num1,kana,num2))
        a = self.cursor.fetchall()
        #同一ナンバーが存在した場合
        if a != []:
            for row in a:
                #ナンバープレートIDを取得
                license_plate_id = row[0]
            self.cursor.execute('select leave_time from access where license_plate_id={}'.format(license_plate_id))
            a = self.cursor.fetchall()

            #最新のアクセスを確認し，退場時間にデータが存在しない場合に以下を実行
            if a[0][0] == None:
                self.cursor.execute('update access set leave_time="{}" where license_plate_id={}'.format(time,license_plate_id))
                self.cursor.execute('update access set image_path_2="{}" where license_plate_id={}'.format(path,license_plate_id))
            else:
                self.cursor.execute('insert into access(license_plate_id, year, month, day, enter_time, image_path_1)\
                    value({},{},{},{},"{}","{}")'.format(license_plate_id,year,month,day,time,path))

        #同一ナンバーが存在しない場合
        else:
            self.cursor.execute('insert into license_plate(area_id,class_number,kana,serial_number)\
                value("{}","{}","{}","{}")'.format(area_id,num1,kana,num2))
            license_plate_id = self.cursor.lastrowid
            self.cursor.execute('insert into access(license_plate_id, year, month, day, enter_time, image_path_1)\
                value({},{},{},{},"{}","{}")'.format(license_plate_id,year,month,day,time,path))

        self.conn.commit()

    def show_db(self):
        self.cursor.execute('select * from license_plate')
        for row in self.cursor.fetchall():
            print(row)

    def generate_daily_graph(self, include_tottori, year, month, day):
        #地名リストを作成
        area_list = {}
        if include_tottori:
            self.cursor.execute('select area_name from area')
            for row in self.cursor.fetchall():
                area = row[0]
                area_list[area] = 0

            self.cursor.execute('select area_name from license_plate, access, area where access.year={} and access.month={} and access.day={} and\
                license_plate.license_plate_id=access.license_plate_id and license_plate.area_id=area.area_id'.format(year, month, day))
        else:
            self.cursor.execute('select area_name from area where area_name != "鳥取"')
            for row in self.cursor.fetchall():
                area = row[0]
                area_list[area] = 0

            self.cursor.execute('select area_name from license_plate, access, area where access.year={} and access.month={} and access.day={} and\
                license_plate.license_plate_id=access.license_plate_id and license_plate.area_id=area.area_id and\
                area.area_name != "鳥取"'.format(year, month, day))

        for row in self.cursor.fetchall():
            area_name = row[0]
            area_list[area_name] += 1

        x = []
        for i in range(len(area_list)):
            x.append(i)
        plt.xlabel('地名')
        plt.ylabel('台数')
        plt.bar(x, area_list.values(), tick_label=list(area_list.keys()))
        plt.title(f'{year}年 {month}月 {day}日')
        plt.savefig('./images/output_images/daily_bar_graph.png')
        plt.clf()
        plt.close()

    def generate_monthly_graph(self, include_tottori, year, month):
        #地名リストを作成
        area_list = {}
        if include_tottori:
            self.cursor.execute('select area_name from area')
            for row in self.cursor.fetchall():
                area = row[0]
                area_list[area] = 0

            self.cursor.execute('select area_name from license_plate, access, area where access.year={} and access.month={} and\
                license_plate.license_plate_id=access.license_plate_id and license_plate.area_id=area.area_id'.format(year, month))

        else:
            self.cursor.execute('select area_name from area where area_name != "鳥取"')
            for row in self.cursor.fetchall():
                area = row[0]
                area_list[area] = 0

            self.cursor.execute('select area_name from license_plate, access, area where access.year={} and access.month={} and\
                license_plate.license_plate_id=access.license_plate_id and license_plate.area_id=area.area_id and\
                area.area_name != "鳥取"'.format(year, month))

        for row in self.cursor.fetchall():
            area_name = row[0]
            area_list[area_name] += 1

        x = []
        for i in range(len(area_list)):
            x.append(i)
        plt.xlabel('地名')
        plt.ylabel('台数')
        plt.bar(x, area_list.values(), tick_label=list(area_list.keys()))
        plt.title(f'{year}年 {month}月')
        plt.savefig('./images/output_images/monthly_bar_graph.png')
        plt.clf()
        plt.close()

    def generate_yearly_graph(self,include_tottori, year):
        #地名リストを作成
        area_list = {}
        if include_tottori:
            self.cursor.execute('select area_name from area')
            for row in self.cursor.fetchall():
                area = row[0]
                area_list[area] = 0

            self.cursor.execute('select area_name from license_plate, access, area where access.year={} and\
                license_plate.license_plate_id=access.license_plate_id and license_plate.area_id=area.area_id'.format(year))
        else:
            self.cursor.execute('select area_name from area where area_name != "鳥取"')
            for row in self.cursor.fetchall():
                area = row[0]
                area_list[area] = 0

            self.cursor.execute('select area_name from license_plate, access, area where access.year={} and\
                license_plate.license_plate_id=access.license_plate_id and license_plate.area_id=area.area_id and\
                area.area_name != "鳥取"'.format(year))

        for row in self.cursor.fetchall():
            area_name = row[0]
            area_list[area_name] += 1

        x = []
        for i in range(len(area_list)):
            x.append(i)
        plt.xlabel('地名')
        plt.ylabel('台数')
        plt.bar(x, area_list.values(), tick_label=list(area_list.keys()))
        plt.title(f'{year}年')
        plt.savefig('./images/output_images/yearly_bar_graph.png')
        plt.clf()
        plt.close()

if __name__ == '__main__':
    #test
    db_controller = DB_controller()
    results = {
        'area':['鳥取',0.99],
        'num1':'590',
        'kana':'あ',
        'num2':'12-34'
    }
    dt = '2023-11-12 23:11:03.900627'
    db_controller.insert_db(results,'c:/a/b/c.png',dt)