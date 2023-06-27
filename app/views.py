# import os

from flask import jsonify, request
import urllib.parse as urlParser

from app import app, Links_crud
from app.models import Links
from app.getLog import getLog
import config
from app.sendRequests import send, sendOnce


@app.route('/api/all', methods=['GET'])
def getAllLinks():
    links = Links_crud.read_all()
    return jsonify(links)


@app.route('/api/log', methods=['GET'])
def getLastLogs():
    logs = getLog(config.NUM_LOG_LINES)
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
    status = sendOnce(link)
    link = Links(user_id, protocol, domain, domainZone, path, status, params)
    result = Links_crud.create(link)
    if result:
        return jsonify(protocol, domain, domainZone, path, params)
