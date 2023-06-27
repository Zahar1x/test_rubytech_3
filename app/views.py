# import os
from datetime import datetime

from flask import jsonify, request
import urllib.parse as urlParser

from app import app, Links_crud, User_crud
from app.models import Links, Status, Params, User
from app.getLog import getLog
import config
from app.sendRequests import send, sendOnce
from app.writeLog import writeLog


@app.route('/api/all', methods=['GET'])
def getAllLinks():
    writeLog(datetime.now(), __file__, ':getAllLinks:getting all urls from DB...')
    links = Links_crud.read_all()
    writeLog(datetime.now(), __file__, ':getAllLinks:got all urls: ' + str(links))
    return jsonify(links)


@app.route('/api/log', methods=['GET'])
def getLastLogs():
    writeLog(datetime.now(), __file__, ':getLastLog:getting last ' + str(config.NUM_LOG_LINES) + ' lines of log')
    logs = getLog(config.NUM_LOG_LINES)
    writeLog(datetime.now(), __file__, ':getLastLog:Last logs ' + str(logs))
    return jsonify(logs)


@app.route('/api/resource', methods=['POST'])
def postLink():
    req = request.get_json()
    user_id = req['user_id']
    link = req['link']
    parsedLink = urlParser.urlsplit(link, scheme='', allow_fragments=True)
    protocol = parsedLink.scheme
    domain = parsedLink.netloc.split('.')[0]
    domainZone = parsedLink.netloc.split('.')[1]
    path = parsedLink.path
    params = parsedLink.query

    print('protocol: ' + protocol)
    print('domain: ' + domain)
    print('domain zone: ' + domainZone)
    print('path: ' + path)
    print('params: ' + str(params))

    pars = storeParams(params)
    print('Stored params: ' + str(pars))
    Params_list = []
    for key, value in pars.items():
        Params_list.append(Params(key, value, 1))
    last_asnwer_code, resource_status, answer_last_time = sendOnce(link)
    status = Status(last_asnwer_code, resource_status, answer_last_time, 1)

    link = Links(domain, protocol, domain, domainZone, path, [status], Params_list)
    result = Links_crud.create(link)
    if result:
        return jsonify(protocol, domain, domainZone, path, params)


@app.route("/api/user", methods=['POST'])
def createUser():
    req = request.get_json()
    email = req['email']
    password = req['password']
    fio = req['fio']
    user = User(email, password, fio)

    res = User_crud.create(user)
    if res:
        return jsonify(res)

def storeParams(para):
    res_dict = {}
    params_str = para.split("&")
    for s in params_str:
        string = s.split('=')
        res_dict[string[0]] = string[1]

    return res_dict
