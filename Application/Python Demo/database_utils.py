import pymysql 

import re # regex
import requests
from bs4 import BeautifulSoup # for youtube video title


def connect_to_database(host, user, password, db, charset='utf8mb4'):
    return pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)


def search_in_db(connection, URL, tag):
    vid, _ = get_video_info(URL)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM videos WHERE vid = %s AND category = %s"
        cursor.execute(sql, (vid, tag))
        result = cursor.fetchone()
        return bool(result)
        

def insert_into_db(connection, URL, tag):
    vid, title = get_video_info(URL)

    with connection.cursor() as cursor:
        sql = "INSERT INTO videos (title, vid, category) VALUES (%s, %s, %s)"
        cursor.execute(sql, (title, vid, tag))
        connection.commit()



def get_video_info(URL):
    # get video id
    v_id = None
    youtube_regex = (
        r'(https?://)?(www\.)?'
        'youtu(be\.com|\.be)/'
        '(shorts/)?'
        '([^&=%\?]{11})'
    )
    matches = re.search(youtube_regex, URL)
    if matches:
        v_id = matches.group(5) 
    
    # get video title
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, features="html5lib")

    link = soup.find_all(name="title")[0]
    title = str(link)
    title = title.replace("<title>","")
    title = title.replace("</title>","")
    title = title.replace(" - YouTube","")      
    
    return v_id, title
