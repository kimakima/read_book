# -*- coding: utf-8 -*-

# ToDo
# add args check -> 10/14 sat done
# add usage -> 10/16 mon done
# cache func. -> 10/18 wed done
# cache save(csv) -> 10/19 thu done
# file open with "with" statement -> 10/19 thu

# error message with "with" statement
# google api err handling
# cache database(sqlite)
# i18n
# add __name__ == '__main__'

import argparse
import sys
import datetime
import math
import urllib
import json
import csv

st_desc = "sample desc."
st_usage = "python read_book.py <yyyy-mm-dd> <isbn> <read_pages>"
parser = argparse.ArgumentParser(description=st_desc, usage=st_usage)
parser.add_argument('sd')
parser.add_argument('isbn', type=int)
parser.add_argument('pages', type=int)
args = parser.parse_args()
#print(args)

def save_cache(dic_new_book_data):
    print type(dic_new_book_data),dic_new_book_data
    with open('book_db.csv', mode = 'a') as fp_book_db:
         fp_book_db.write(str(dic_new_book_data['isbn'])+','+dic_new_book_data['title'].encode('utf-8')+','+str(dic_new_book_data['pp'])+'\n')

def search_isbn(isbn):
    #try:
    with open('book_db.csv', 'rb') as fp_book_db:
        data_reader = csv.DictReader(fp_book_db)
        #print data_reader

        flg_book_cache = False
        for row in data_reader:
            #print type(row),row
            if row['isbn'] == isbn:
                print 'i have cache data'
                title = row['title']
                page_count = row['pp']
                flg_book_cache = True
    #except Exception as ex:
        #print('i have no cache file')
        #sys.exit()

    if flg_book_cache == False:
        print 'i have no cache data'
        data = get_book_data(isbn)
        title = data["items"][0]["volumeInfo"]["title"]
        page_count = data["items"][0]["volumeInfo"]["pageCount"]
        dic_new_book_data = {}
        dic_new_book_data['isbn'] = isbn
        dic_new_book_data['title'] = title
        dic_new_book_data['pp'] = page_count
        save_cache(dic_new_book_data)

    return [title, page_count]

def get_book_data(isbn):
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn
    paramStr = ""
    readObj = urllib.urlopen(url + paramStr)
    res = readObj.read()
    res_json = json.loads(res)

    return res_json

args = sys.argv

start_date = args[1]
isbn = args[2]
read_pages = float(args[3])

title, page_count = search_isbn(isbn)

if False:
    data = get_book_data(isbn)

    title = data["items"][0]["volumeInfo"]["title"]
    page_count = data["items"][0]["volumeInfo"]["pageCount"]
else:
    pass

total_pages = float(page_count)

dt_start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
dt_today = datetime.date.today()
num_of_days_read =  (dt_today - dt_start_date.date()).days +1
pages_per_day = round(read_pages/(dt_today - dt_start_date.date()).days,2)
num_of_days_complete = math.floor((total_pages / pages_per_day) +1)
left_days = num_of_days_complete - num_of_days_read
dt_scheduled_date = dt_today + datetime.timedelta(days=left_days)

print "title: " + title,
print "(total pages: " + str(total_pages) + ")"
print "start date: " + start_date,
print " / ",
print dt_today,
print "(elapsed:" + str(num_of_days_read) + " days)"
print "read pages: " + str(read_pages) + " (" + str(round(read_pages/total_pages,2)) + ")",
print "avg: pp." + str(pages_per_day) + "/day"
#print "number of date to complete: " + str(num_of_days_complete) + " days"
print "scheduled date: " + dt_scheduled_date.strftime("%Y-%m-%d"),
print "/ left days: " + str(left_days) + " days"
