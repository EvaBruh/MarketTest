
# Market Radio TestCase

## Запуск и установка:

<ul>
  <li>В терминале перейдите в <code>backend</code>:</li>
</ul>

<code>cd backend</code>

<ul> <li>Установите необходимые зависимости:</li> </ul>

  <code>pip install -r requirements.txt</code>
  
<li>Запустите сервер:</li>

  <code>python manage.py runserver</code>
  
<li>Сервер будет доступен по адресу http://127.0.0.1:8000.</li>

<li>Перейдите в папку <code>frontend</code>:</li>
  <li><code>cd ..</code></li>
  <li><code>cd frontend</code></li>
  
<li>React:</li>
<li>Перейдите в папку <code>my-app</code> установите зависимости и запустите сервер разработки:</li>

  <li><code>cd my-app</code></li>
  <li><code>npm install</code></li>
  <li><code>npm start</code></li>
  
  ## Описание, что делаем.
  
  <p>У нас имеется backend на Django + DRF API и frontend на React. <br>
  Реализован доступ к данным API сервисов AUDD, Discogs, Genuis <br>
  <h4>Цикл user-experience:<br></h4>
  Наш сервис предлагает юзеру найти информацию о музыке, в разных формах(файл, название).
  Перед нами 2 формы, одна для Audd & Genuis, вторая для discogs. В первую мы загружаем mp3 файл, немного погодя нам показывается инфо о треке с полями.<br>
  Во второй форме мы вводим название и исполнителя трека, получаем информацию по базе discogs.
  ![image](https://user-images.githubusercontent.com/86770909/226099918-dd888836-cd8e-48d7-b876-7ee34ed1ac3a.png)</p>
<p>Результат загрузки файла в первую форму. ![image](https://user-images.githubusercontent.com/86770909/226099956-3dd147a6-bc20-40a6-86fe-1a3542db425c.png)<br></p>
Результат загрузки данных во вторую форму. ![image](https://user-images.githubusercontent.com/86770909/226100009-a421a137-ef76-4f66-8f93-c1a335ee4a29.png)<br>
Обратите внимание, что при нажатии поиска в Discogs, вам нужно свернуться в терминал, так как там вам будет предложено верифицировать ваш запрос путём ввода спец. кода из ссылки, которую вам предоставят.
  
  ## Как работает.
  
  <p>React компоненты AUDD и discogs отправляют запросы с помощью axios либы на API Django-сервера<br>
  Для AUDD <code>127.0.0.1:8000/api/audd/</code><br>
  Для discogs <code>127.0.0.1:8000/api/discogs/</code><br>
  Django принимает post запрос, реализация в файле views.py приложения api.<br>
  <code>class UploadFileView</code> отвечает за AUDD & Genuis, и соответственно <code>/api/audd/</code><br>
  <code>class DiscogsApi</code> отвечает за Discogs, и соответственно <code>/api/discogs</code><br>
  Принимая запрос, Django отправляет свой запрос с данными полученными от frontend в API нужных сервисов.<br>
  Далее мы оперируем с этими данными, сохраняем их в нашу базу данных(не плодим одинаковые объекты, а проверяем есть ли уже в базе такие данные, если есть даем их) и вконце возвращаем полученные данные обратно в React компонент. Этот ответ появляется в нашем API и Админке.<br>
  React разбирает на кусочки полученный запрос и вставляет их в нужные места.</p>
  
