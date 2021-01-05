from utils.db import connect
from utils.api import line
from datetime import datetime
import configparser
import schedule
import time
import logging.config


def job():
    SAVE_PATH = './txtFile'
    toDay = datetime.today().strftime("%Y-%m-%d")

    logging.info({
        'action' : 'job',
        'date' : toDay,
        'status' : 'RUN',
    })

    """Access the sqlite3"""
    path = connect.getToDayData(toDay, SAVE_PATH)

    """Notify by LINE"""
    ACCESS_TOKEN = ini['line']['ACCESS_TOKEN']
    message = line.readTxtFile(path)
    line.sendMsg(ACCESS_TOKEN, message)

    logging.info({
        'action' : 'job',
        'date' : toDay,
        'status' : 'SUCCESS',
    })

    return



"""Read ini file"""
ini = configparser.ConfigParser()
ini.read('./config/config.ini','UTF-8')
logging.config.fileConfig('./config/logging.ini')
logger = logging.getLogger('__name__')


"""Job Schedule"""
schedule.every().day.at("11:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)