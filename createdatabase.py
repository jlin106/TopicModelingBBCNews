#!/usr/bin/python

import sqlite3
import sys
import csv

con = sqlite3.connect('news.db')

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS BBCnews (ID INTEGER PRIMARY KEY, Section TEXT, URL TEXT, Time TIMESTAMP, Title TEXT, Article TEXT, Words TEXT);")

with open('bbc-dataset-201601-201607-time.tab', 'r') as file:
	reader = csv.reader(file, delimiter='\t')
	for row in reader:
		cur.execute("INSERT INTO BBCnews VALUES (NULL,?,?,?,?,?,NULL);", (row[0],row[1],row[4],row[2],row[3],))

con.commit()
con.close()