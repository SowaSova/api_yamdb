### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SowaSova/api_yamdb.git

```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейти в каталог

```
cd api_yamdb/
```

Выполнить миграции:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

Импортировать данные:

```
python3 manage.py insert_data
```

Запустить проект:

```
python3 manage.py runserver
```
