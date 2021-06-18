import base64
from io import BytesIO

from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from PIL import Image

from MyMongoClient import MyMongoClient

app = Flask(__name__)


@app.route('/show')
def show():

    myMongoClient = MyMongoClient()
    myCollection = myMongoClient.collection
    naver_movies = myCollection.find()
    movie_list = []

    for movie in naver_movies:
        movie_list.append(movie)

    return render_template('movie_list.html', movie_list=movie_list)


@app.route('/')
def get_naver_movie():

    myMongoClient = MyMongoClient()
    myCollection = myMongoClient.collection
    total_count = myCollection.count()
    if total_count > 0:
        myCollection.drop()

    uri = 'https://movie.naver.com/movie/running/current.nhn'
    response = requests.get(uri)
    soup = BeautifulSoup(response.content, 'html.parser')

    ul = soup.find('ul', class_='lst_detail_t1')
    li = ul.find_all('li')

    seq = 0
    error = 0
    size = (450, 450)

    for item in li:

        seq += 1

        try:
            img = item.find('img')
            img_src = img.get('src')
            img_data = requests.get(img_src)
            b = BytesIO(img_data.content)

            img = Image.open(b)
            img.thumbnail(size)     # 작은 그림

            img_file = BytesIO()
            img.save(img_file, format="png")
            img_bytes = img_file.getvalue()     # img_bytes: image in binary format
            img_b64 = base64.b64encode(img_bytes)
            img_b64_decode = img_b64.decode()

            # with open(img_src, 'rb') as image_file:
            #     encoded_data = base64.b64encode(image_file.read())
            #     print(encoded_data)
        except:
            pass

        try:
            age = item.select('dl > dt > span')
            age = age[0].text
        except:
            pass

        try:
            title = item.select('dl > dt > a')
            title = title[0].text
        except:
            pass

        try:
            star_num = item.select('dl > dd.star > dl.info_star > dd > div > a > span.num')
            star_num = star_num[0].text
        except:
            pass
        try:
            booking_rate = item.select('dl > dd.star > dl.info_exp > dd > div > span.num')
            booking_rate = booking_rate[0].text
        except:
            pass

        try:
            genre = item.select('dl > dd:nth-child(3) > dl > dd:nth-child(2) > span.link_txt > a')
            genre = genre[0].text
        except:
            pass

        try:
            director = item.select('dl > dd:nth-child(3) > dl > dd:nth-child(4) > span > a')
            director = director[0].text
        except:
            pass

        myDocument = {'seq': seq, 'img_b64_decode': img_b64_decode, 'age': age, 'title': title, 'star_num': star_num, 'booking_rate': booking_rate, 'genre': genre, 'director': director}
        myCollection.insert_one(myDocument)
        print(myDocument)

    return '네이버 영화 빅데이터 수집'




if __name__ == '__main__':
    app.run()
