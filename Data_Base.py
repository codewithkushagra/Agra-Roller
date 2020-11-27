import mysql.connector
db=mysql.connector.connect(host="localhost",user="agraroller",passwd="root12345678",database="agraroller_database")

cursor=db.cursor()


def create_tables():
    cursor.execute("DROP TABLE IF EXISTS LOGIN_INFO")
    cursor.execute("DROP TABLE IF EXISTS LOCATION_DATA")
    cursor.execute("DROP TABLE IF EXISTS ALLOT")
    cursor.execute("DROP TABLE IF EXISTS IMEI")
    cursor.execute("DROP TABLE IF EXISTS HEART_BEAT")
    db.commit()
    cursor.execute("CREATE TABLE IMEI(IMEI VARCHAR(20))")
    cursor.execute("CREATE TABLE HEART_BEAT(TERMINAL_INFO TEXT,VOLTAGE_LEVEL TEXT,GSM_SIGNAL TEXT,SNO TEXT)")
    cursor.execute("CREATE TABLE ALLOT(SNO INT(11) NOT NULL AUTO_INCREMENT,EMPLOPYEE_NAME VARCHAR(30),IMEI VARCHAR(20),PRIMARY KEY (SNO))")
    cursor.execute("CREATE TABLE LOGIN_INFO(TERMINAL_ID TEXT,INFORMATION_SERIAL_NUMBER TEXT)")
    cursor.execute("CREATE TABLE LOCATION_DATA(TERMINAL_ID TEXT, DATE_TIME TIMESTAMP,LATITUDE INTEGER,LONGITUDE INTEGER,COURSE_STATUS TEXT,MCC TEXT,MNC TEXT,LAC TEXT,CELL_ID TEXT,DATA_UPLOAD_MODE TEXT,REUPLOAD TEXT,SERIAL_NUMBER TEXT)")
    return

def login_insert(terminal_id,serial_number):
    cursor.execute("INSERT INTO LOGIN_INFO(TERMINAL_ID,INFORMATION_SERIAL_NUMBER)VALUES(%s,%s)",(terminal_id,serial_number))
    db.commit()
    return

def location_insert(terminal_id,date_time,latitude,longitude,course_status,mcc,mnc,lac,cell_id,data_upload_mode,reupload,serial_number):
    cursor.execute("INSERT INTO LOCATION_DATA(TERMINAL_ID,DATE_TIME,LATITUDE,LONGITUDE,COURSE_STATUS,MCC,MNC,LAC,CELL_ID,DATA_UPLOAD_MODE,REUPLOAD,SERIAL_NUMBER)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(terminal_id,date_time,latitude,longitude,course_status,mcc,mnc,lac,cell_id,data_upload_mode,reupload,serial_number))
    db.commit()
    return

def heartbeat_insert(terminal_info,voltage_level,gsm_signal,sno):
    cursor.execute("INSERT INTO HEART_BEAT(TERMINAL_INFO,VOLTAGE_LEVEL,GSM_SIGNAL,SNO)VALUES(%s,%s,%s,%s)",(terminal_info,voltage_level,gsm_signal,sno))
    db.commit()
    return



def update(employee_name,imei):
    cursor.execute("UPDATE ALLOT SET IMEI = %s WHERE EMPLOPYEE_NAME = %s",(imei,employee_name))
    db.commit()
    return

def getAlldata_allot():
    cursor.execute("SELECT * FROM ALLOT")
    result=cursor.fetchall()
    return result
def getLastdata_location_data():
    cursor.execute("SELECT * FROM LOCATION_DATA WHERE DATE_TIME=(SELECT MAX(DATE_TIME) FROM LOCATION_DATA) LIMIT 1")
    result=cursor.fetchall()
    return result
def getIMEI():
    cursor.execute("SELECT * FROM IMEI")
    result=cursor.fetchall()
    return result
#cursor.execute("INSERT INTO ALLOT(EMPLOPYEE_NAME)VALUES('Ambuj')")
#db.commit()

#create_tables()

