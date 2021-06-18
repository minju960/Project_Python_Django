from django.http import HttpResponse
from django.shortcuts import render

from MyMongoClient import MyMongoClient


class Pharmacy(object):
    def __init__(self):
        self.name = ''
        self.address = ''
        self.latitude: 0.0
        self.longitude: 0.0



def geocode_find(request):
    return render(request, 'pharmacy/geocode_find.html')


def query(request):
    # if request.method == 'POST':

        myMongoClient = MyMongoClient()
        myCollection = myMongoClient.collection
        myCollection.create_index([('location', '2dsphere')])

        # input_address = request.POST['address']
        # print(input_address)

        latlng =request.GET['latlng']
        latlng = latlng.split(",")
        lat = latlng[0].replace("(", "")
        lat = float(lat)
        lng = latlng[1].replace(")", "").replace(" ", "")
        lng = float(lng)

        maxDistance = 1000
        pharmacy = myCollection.find(
            {
                'location':
                    {'$near':
                        {
                            '$geometry': {'type': 'Point',
                                          'coordinates': [lng, lat]},
                            '$minDistance': 0,
                            '$maxDistance': maxDistance
                        }
                    }
            }
        )

        pharmacy_list = []
        for item in pharmacy:
            phar = Pharmacy()
            phar.name = item['pharmacy_name']
            phar.address = item['address']
            phar.latitude = item['location']['coordinates'][1]
            phar.longitude = item['location']['coordinates'][0]
            pharmacy_list.append(phar)

        context = {
            'pharmacy_list': pharmacy_list,
            'lat': lat,
            'lng': lng
        }

        return render(request, 'pharmacy/googlemap.html', context)


def current_location(request):
    return render(request, 'pharmacy/current_location.html')


def my_location(request):
    if request.method == 'GET':
        return render(request, 'pharmacy/my_input.html')

    import requests
    if request.method == 'POST':

        address = request.POST['address']
        radius = int(request.POST['radius'])

        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyDAQCdTZ49zdFnOVyByYUz_eojJT1YDfEc'
        res = requests.get(url)
        data = res.json()
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        print(lat, lng)

        myMongoClient = MyMongoClient()
        myCollection = myMongoClient.collection

        myCollection.create_index([('location', '2dsphere')])

        maxDistance = radius  # 미터
        pharmacy = myCollection.find(
            {
                'location':
                    {'$near':
                        {
                            '$geometry': {'type': 'Point',
                                          'coordinates': [lng, lat]},
                            '$minDistance': 0,
                            '$maxDistance': maxDistance
                        }
                    }
            }
        )

        pharmacy_list = []
        for item in pharmacy:
            phar = Pharmacy()
            phar.name = item['pharmacy_name']
            phar.address = item['address']
            phar.latitude = item['location']['coordinates'][1]
            phar.longitude = item['location']['coordinates'][0]
            pharmacy_list.append(phar)

        context = {
            'pharmacy_list': pharmacy_list,
            'address': address,
            'lat': lat,
            'lng': lng,
            'maxDistance': maxDistance,

        }
        return render(request, 'pharmacy/my_result.html', context)

