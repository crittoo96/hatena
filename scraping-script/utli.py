import yaml
import json
import codecs
import pymysql
import os

def open_json(filename):
  with open(filename, 'r') as f:
    yaml_data = json.load(f)
    return yaml_data

def get_config():
  config = open_json('config.json')
  return config

def create_connection():
  db_config = get_config()['db']

  connection = pymysql.connect(host=db_config['host'],
                                user=db_config['user'],
                                password=db_config['password'],
                                db=db_config['db'],
                                charset=db_config['charset'],
                                cursorclass=pymysql.cursors.DictCursor)
  return connection

def close_connection(connection=None):
  if not connection:
    return
  else:
    connection.commit()
    connection.close()