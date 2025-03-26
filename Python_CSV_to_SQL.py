import pyodbc
import csv
import os
from datetime import datetime, timedelta
import configparser

with open("log_result.txt", "w") as log: print("start", file = log)


def get_db_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    db_config = {
        'server': config.get('database', 'server'),
        'database': config.get('database', 'database'),
        'username': config.get('database', 'username'),
        'password': config.get('database', 'password'),
        'filePath': config.get('fileData', 'filePath'),
        'filePrefix': config.get('fileData', 'filePrefix'),
        'fileSuccessPath' : config.get('fileData', 'fileSuccessPath'),
        'fileErrorPath' : config.get('fileData', 'fileErrorPath'),
    }
    return db_config


def db_connection(server, database, uid, pwd):
    
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={uid};'
        f'PWD={pwd}'
    )
    return conn

def main():
    try:
        
        db_config = get_db_config()
        con = db_connection(db_config["server"], db_config["database"], db_config["username"], db_config["password"])
        cursor = con.cursor()
        
        fileTestList = os.listdir(db_config["filePath"])
        #filedateshift = str(datetime.now()).strftime('%Y%m%d') + "_" + ( "1" if datetime.now().strftime("%H"))
        print(fileTestList)
        file_case = ''
        unit = 'unit'
        machine = 'Test'
        date_shift = ''
        date = ''
        product = ''
        values = ''
        group = ''
        values = ''
        
        for fileTest in fileTestList:
            file_case = fileTest
            print(fileTest.startswith(db_config["filePrefix"]))
            if (fileTest.startswith(db_config["filePrefix"])):
                with open(db_config["filePath"] + '/' + fileTest) as f:
                    dataUQX = csv.reader(f, delimiter = ';')
                    listdataUQX = list(dataUQX)
                    for data in listdataUQX[1:]:
                        print(db_config["filePrefix"])
                        date = data[0] + data[1].zfill(2) + data[2].zfill(2)
                        date_shift = date + data[3]
                        product = data[4]
                        system = data[7]
                        group = data[8]
                        values = data[15][0:6]
                        cursor.execute('''INSERT INTO [dbo].[Test_CSV]
                           ([unit]
                           ,[date_shift]
                           ,[date]
                           ,[product]
                           ,[test]
                           ,[system]
                           ,[group]
                           ,[values]
                           ,[timestamp]
                           ,[status]
                           ,[file_name])
                        VALUES 
                           (?
                           ,?
                           ,?
                           ,?
                           ,?
                           ,?
                           ,?
                           ,?
                           ,getdate()
                           ,'0'
                           ,?)'''.format(length='multi-line', ordinal='second'),
                            unit
                           ,date_shift
                           ,date
                           ,product
                           ,machine
                           ,system
                           ,group
                           ,values
                           ,fileTest)
                        
                        #print(data[0] + " - " + data[1].zfill(2) + " - " + data[2].zfill(2) + " - " + data[3] + " - " + data[4] + " - " + data[15][0:6] + " - " + data[7] + " - " + data[8])
                        #print(unit + " - " + date_shift + " - " + date + " - " + product + " - " + system + " - " + values + " - " + group + " - " + values)
                        con.commit()
            if(fileTest.startswith("Test export (Shift)_")):
                os.rename((db_config["filePath"] + '\\' + file_case ), (db_config["fileSuccessPath"]  + '\\' + file_case))
        con.close()

    except Exception as e:
        #print(str(e))
        move_error=""
        if(fileTest.startswith(db_config["filePrefix"])):
            try:
                os.rename((db_config["filePath"] + '\\' + file_case ), (db_config["fileErrorPath"]  + '\\' + file_case))
            except Exception as e:
                move_error = e
        with open("log_result.txt", "w") as log:
            print("err" + str(e)  + "\n fileTest: " + file_case + "\n test_id: " + date_shift + "\n execution_date: " + date +
                          "\n product: " + product + "\n values: " + values  + "\n group: " + group +
                          "\n values: " +  values+ " \n" + move_error , file = log)


if __name__ == "__main__":
    main()
