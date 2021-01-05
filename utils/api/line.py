from datetime import datetime
import logging
import requests


def readTxtFile(path):
    logger = logging.getLogger('debugLogging')
    logger.info({
        'action' : 'readTxtFile',
        'status' : 'RUN',
    })

    with open(path, 'r') as f:
        msg = f.read()

    logger.info({
        'action' : 'readTxtFile',
        'status' : 'SUCCESS',
    })
    logger.debug({
        'action' : 'readTxtFile',
        'msg' : msg,
    })

    return msg


def sendMsg(access_token, message):
    logger = logging.getLogger('debugLogging')
    logger.info({
        'action' : 'sendMsg',
        'status' : 'RUN',
    })

    url = "https://notify-api.line.me/api/notify"
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    payload = {
        'message': message
    }
    resp = requests.post(url, headers=headers , params=payload)

    if resp.status_code == 200:
        logger.info({
            'action' : 'sendMsg',
            'status_code' : resp.status_code,
        })

        limit = resp.headers.get("X-RateLimit-Limit")
        remaining = resp.headers.get("X-RateLimit-Remaining")
        resetTime = resp.headers.get("X-RateLimit-Reset")
        resetTime = datetime.fromtimestamp(int(resetTime))

        logger.debug({
            'action' : 'sendMsg',
            'call上限回数(1H)' : limit,
            'call可能残回数' : remaining,
            'リセット時刻' : resetTime,
        })

    else:
        logger.critical({
            'action' : 'sendMsg',
            'error' : resp.status_code,
        })

    logger.info({
        'action' : 'sendMsg',
        'status' : 'SUCCESS',
    })

    return