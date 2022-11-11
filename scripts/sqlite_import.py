from pymongo import MongoClient
import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

ROOT = Path().resolve().parent

def fetch_phrases():
  # mongo
  client = MongoClient()
  client = MongoClient("mongodb://localhost:27017/")
  collection = client['vantu']['phrases']
  # get data
  print("count_documents={}".format(collection.count_documents({})))
  cursor = collection.find()
  phrases = []
  for record in cursor:
    han = record["han"]
    content = json.dumps(record["content"])
    info = json.dumps(record["info"])
    # svg

    phrases.append([han, content, info])
  # sort
  phrases.sort(key=lambda x: x[0])
  return phrases

def read_phrases():
  f = open(os.path.join(ROOT, "data", "export.json"), "r")
  lines = f.readlines()
  f.close
  phrases = []
  for line in lines:
    p = json.loads(line)
    han = p["han"]
    content = json.dumps(p["content"])
    info = json.dumps(p["info"])
    svg = json.dumps(p["svg"])
    phrases.append([han, content, info, svg])
  return phrases

def import_phrases(phrases):
  # sqlite3
  conn = sqlite3.connect('../data/vantu.sqlite.db')
  cur = conn.cursor()
  # create table
  sql_create_phrases_table = """ CREATE TABLE phrases (
      id int not null primary key,
      han varchar(100),
      content text,
      info text,
      svg text
  ); """
  cur.execute(sql_create_phrases_table)
  # insert data
  count = 0
  bulk = []
  bulk_size = 10000
  start = datetime.now()
  for idx, phrase in enumerate(phrases):
    # print("phrase={}".format(phrase))
    bulk.append((idx, phrase[0], phrase[1], phrase[2], phrase[3]))
    count = count + 1
    # bulk insert
    if count == bulk_size:
      # print("size={}, bulk={}".format(len(bulk), bulk))
      cur.executemany("insert into phrases (id, han, content, info, svg) values (?, ?, ?, ?, ?);", bulk);
      count = 0
      bulk = []
      conn.commit()
  # last bulk
  if bulk:
    cur.executemany("insert into phrases (id, han, content, info, svg) values (?, ?, ?, ?, ?)", bulk);
    conn.commit()
  end = datetime.now()
  print("time={}".format(end-start))

def run():
  # phrases = fetch_phrases()
  phrases = read_phrases()
  import_phrases(phrases)
  # print(phrases[0])

run()
