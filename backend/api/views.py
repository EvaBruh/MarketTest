import os
import json
import sys
import oauth2 as oauth
import requests

from urllib.request import urlretrieve
from urllib.parse import parse_qsl

from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from .models import SongData, Discogs
from .serializers import TrackInfoSerializer, DiscogsSerializer


def index(request):
    return render(request, 'index.html')


# Принимаем запрос с компонента React AUDD для API AUDD и Genuis
class UploadFileView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SongData.objects.all()
    serializer_class = TrackInfoSerializer

    def post(self, request):

        # берём файл, если есть
        file = request.FILES.get('file')
        if file:
            path = default_storage.save(f'myfiles/{file.name}', file)
            full_path = os.path.join(default_storage.location, path)
        else:
            return HttpResponseBadRequest('Файл не был предоставлен!')

        # API Token AUDD, вставьте свой
        api_token = 'cf02182b4372d0a1cd23d4de1be5c8c4'
        url = f'https://api.audd.io/?api_token={api_token}'
        with open(full_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
        data = response.json()

        # Получаем информацию о треке из ответа API AUDD
        result = data.get('result')
        if result:
            artist = result.get('artist')
            title = result.get('title')
            release_date = result.get('release_date')
            genre = result.get('genre')
            style = result.get('style')
            lyrics = result.get('lyrics')

            # Genius API - https://docs.genius.com/#search-h2
            base_url = "https://api.genius.com"
            access_token = "yzq9snGUyx_nbgGvkOWPeVF6hZt46vo-J-9qoUuj8tHIg4J4UOBWbiW5K5t1-K9U"

            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            respGenuis = requests.get(f"{base_url}/search?q={artist}", headers=headers)

            if respGenuis.status_code == 200:
                dataGenuis = respGenuis.json()
                hits = dataGenuis['response']['hits']
                img = hits[0]['result']['header_image_url']
                tracklist = []
                for hit in hits:
                    gen_title = hit['result']['title']
                    gen_url = hit['result']['url']
                    tracklist.append({'title': gen_title, 'url': gen_url})
            else:
                print(f"An error occurred: {respGenuis.text}")

            # Сохранение в базе, создаём либо возвращаем то что уже есть в базе данных, модель SongData

            song_data, created = SongData.objects.get_or_create(
                artist=artist,
                title=title,
                defaults={
                    'release_date': release_date,
                    'genre': genre,
                    'style': style,
                    'lyrics': lyrics,
                    'gen_tracklist': tracklist,
                    'gen_url': img
                }
            )
            # Очистка полей для проверки модели, в случае чего получаем ValidationError
            song_data.full_clean()
            if created:
                print('Created new SongData object')
            else:
                print('Retrieved existing SongData object')

            serializer = TrackInfoSerializer(song_data)

            return Response(serializer.data)

        return Response({'error': 'Failed to recognize song'})


# Discogs API - https://www.discogs.com/developers#page:home,header:home-quickstart
# Принимаем запрос с компонента React discogs для Discogs API
# Основная часть кода в def post представлена самим Discogs
# Мне пришлось в каждом запросе прокликивать авторизацию и вводить код, таков путь
class DiscogsApi(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DiscogsSerializer
    queryset = Discogs.objects.all()

    def post(self, request):

        # Получаем нужные значения для запроса в API
        artist = request.data.get('artist')
        title = request.data.get('title')

        # Данные из кабинета приложения, дальше процесс логина до строки 174.
        consumer_key = 'OFYYeeCuFKONctjYQWWH'
        consumer_secret = 'xkOKEXLUkpngpgYqLIbvYFrpDeixHOSM'
        request_token_url = 'https://api.discogs.com/oauth/request_token'
        authorize_url = 'https://www.discogs.com/ru/oauth/authorize'
        access_token_url = 'https://api.discogs.com/oauth/access_token'

        user_agent = 'discogs_api_mastertestcase/3.0'

        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)

        resp, content = client.request(request_token_url, 'POST', headers={'User-Agent': user_agent})

        if resp['status'] != '200':
            sys.exit('Invalid response {0}.'.format(resp['status']))

        request_token = dict(parse_qsl(content.decode('utf-8')))

        print(' == Request Token == ')
        print(f'    * oauth_token        = {request_token["oauth_token"]}')
        print(f'    * oauth_token_secret = {request_token["oauth_token_secret"]}')
        print()

        print(f'Please browse to the following URL {authorize_url}?oauth_token={request_token["oauth_token"]}')

        accepted = 'n'
        while accepted.lower() == 'n':
            print()
            accepted = input(
                f'Have you authorized me at {authorize_url}?oauth_token={request_token["oauth_token"]} [y/n] :')

        oauth_verifier = input('Verification code : ')

        token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer, token)

        resp, content = client.request(access_token_url, 'POST', headers={'User-Agent': user_agent})

        access_token = dict(parse_qsl(content.decode('utf-8')))

        print(' == Access Token ==')
        print(f'    * oauth_token        = {access_token["oauth_token"]}')
        print(f'    * oauth_token_secret = {access_token["oauth_token_secret"]}')
        print(' Authentication complete. Future requests must be signed with the above tokens.')
        print()

        token = oauth.Token(key=access_token['oauth_token'],
                            secret=access_token['oauth_token_secret'])
        client = oauth.Client(consumer, token)

        # Здесь мы вступаем в игру и ставим нужные нам значения(title/artist)
        resp, content = client.request(
            f'https://api.discogs.com/database/search?q={title}&artist={artist}&type=release',
            headers={'User-Agent': user_agent})

        if resp['status'] != '200':
            sys.exit('Invalid API response {0}.'.format(resp['status']))

        releases = json.loads(content.decode('utf-8'))

        print(f'\n== Search results for release_title={title}, Artist={artist}==')
        for release in releases['results']:
            print(f'\n\t== discogs-id {release["id"]} ==')
            print(f'\tTitle\t: {release.get("title", "Unknown")}')
            print(f'\tYear\t: {release.get("year", "Unknown")}')
            print(f'\tLabels\t: {", ".join(release.get("label", ["Unknown"]))}')
            print(f'\tCat No\t: {release.get("catno", "Unknown")}')
            print(f'\tFormats\t: {", ".join(release.get("format", ["Unknown"]))}')

        resp, content = client.request(f'https://api.discogs.com/releases/{release["id"]}',
                                       headers={'User-Agent': user_agent})

        if resp['status'] != '200':
            sys.exit(f'Unable to fetch release {releases["id"]}')

         #load the JSON response content into a dictionary.
        release = json.loads(content.decode('utf-8'))
         #extract the first image uri.
        image = release['images'][0]['uri']

        # Сохраняем таблицу БД с данными discogs, модель Discogs
        for release in releases['results']:
            discogs_data = Discogs(title=release.get('title'), artist=artist, year=release.get('year'),
                                   label=', '.join(release.get("label", ["Unknown"])),
                                   catno=release.get("catno", "Unknown"),
                                   format=', '.join(release.get("format", ["Unknown"])))
            # Проверка полей
            discogs_data.full_clean()
            try:
                discogs_data.save()
                print('saved base discogs')
            except:
                print('failed save')

            serializer = DiscogsSerializer(discogs_data)
            return Response(serializer.data)

        try:
            urlretrieve(image, image.split('/')[-1])
        except Exception as e:
            sys.exit(f'Unable to download image {image}, error {e}')

        print(' == API image request ==')
        print(f'    * response status      = {resp["status"]}')
        print(f'    * saving image to disk = {image.split("/")[-1]}')
        return Response({'error': 'Failed to discogs song'})