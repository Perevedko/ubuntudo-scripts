# -*- coding: utf-8 -*-
ip = '128.199.40.20'
port = '80'


import xmlrpclib
sock_db = xmlrpclib.ServerProxy('http://{0}:{1}/xmlrpc/db'.format(ip, port))

domain = ip
url = 'http://' + ip + ':' + port
db = 'admin'
username = 'admin'
password = 'admin'

common = xmlrpclib.ServerProxy(url+'/xmlrpc/2/common')
try:
    uid = common.authenticate(db, username, password, {})
except:
    uid = "" #if there is no DB, keep going anyways

models = xmlrpclib.ServerProxy(url+'/xmlrpc/2/object')

#direct DB access
import psycopg2

try:
    direct_db_conn = psycopg2.connect(host=ip, port=5432, dbname=db, user='odoo', password='odoo')
    print "connected"
    direct_db_cur = direct_db_conn.cursor()
except psycopg2.Error as e:
    print "I am unable to connect to the database"
    print e
