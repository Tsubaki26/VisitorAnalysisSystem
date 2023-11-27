import mysql.connector

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
        num1 = results['num1']
        kana = results['kana']
        num2 = results['num2']
        
        # date = dt.split(' ')[0]
        # time = dt.split(' ')[1].split('.')[0]
        date = str(dt.date())
        time = dt.time()
        #ex. 2023-11-12 23:11:03.900627
        self.cursor.execute('select license_plate_ID from license_plate where area="{}" and classification_number="{}" \
            and kana="{}" and serial_number="{}"'.format(area,num1,kana,num2))
        a = self.cursor.fetchall()
        print(a)
        if a != []:
            print("aaa")
            for row in a:
                license_plate_ID = row[0]
            print(license_plate_ID)
            self.cursor.execute('select leave_time from access where license_plate_ID={}'.format(license_plate_ID))
            a = self.cursor.fetchall()
            print(a)
            if a[0][0] == None:
                self.cursor.execute('update access set leave_time="{}" where license_plate_ID={}'.format(time,license_plate_ID))
            else:
                print("kakunou")
                self.cursor.execute('insert into license_plate(area,classification_number,kana,serial_number,image_path)\
                    value("{}","{}","{}","{}","{}")'.format(area,num1,kana,num2,path))
                license_plate_ID = self.cursor.lastrowid
                self.cursor.execute('insert into access(license_plate_ID, date, enter_time)\
                    value({},"{}","{}")'.format(license_plate_ID,date,time))
        else:
            print("kakunou")
            self.cursor.execute('insert into license_plate(area,classification_number,kana,serial_number,image_path)\
                value("{}","{}","{}","{}","{}")'.format(area,num1,kana,num2,path))
            license_plate_ID = self.cursor.lastrowid
            self.cursor.execute('insert into access(license_plate_ID, date, enter_time)\
                value({},"{}","{}")'.format(license_plate_ID,date,time))
        
        self.conn.commit()

    def show_db(self):
        self.cursor.execute('select * from license_plate')
        for row in self.cursor.fetchall():
            print(row)

if __name__ == '__main__':
    db_controller = DB_controller()
    results = {
        'area':['鳥取',0.99],
        'num1':'590',
        'kana':'あ',
        'num2':'12-34'
    }
    dt = '2023-11-12 23:11:03.900627'
    db_controller.insert_db(results,'c:/a/b/c.png',dt)
    # db_controller.show_db()