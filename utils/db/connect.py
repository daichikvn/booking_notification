import logging
import sqlite3


def getToDayData(today, path):
    logger = logging.getLogger('debugLogging')
    logger.info({
        'action' : 'getToDayData',
        'status' : 'RUN',
    })

    path = path + "/{}.txt".format(today)

    logger.debug({
        'action' : 'getToDayData',
        'txtFilePath' : path,
    })

    con = sqlite3.connect('./db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT * FROM SCHEDULE WHERE date = ? ORDER BY time ASC", (today,))

    logger.debug({
        'action' : 'getToDayData',
        'cur' : cur,
    })

    with open(path, 'w') as f:
        print("\n{} の予約\n".format(today), file=f)
        for i, row in enumerate(cur):
            i += 1
            index = "--------------{}--------------".format(i)
            time = "予約時間 : {}".format(row[2])
            name = "{0}様 {1}名".format(row[3], row[4])
            tel = "TEL({})".format(row[5])
            memo = "[備考]\n{}".format(row[6])
            br = "\n"
            s = "\n".join([index, time, name, tel, memo, br])
            f.write(s)

    con.close()

    logger.info({
        'action' : 'getToDayData',
        'status' : 'SUCCESS',
    })

    return path