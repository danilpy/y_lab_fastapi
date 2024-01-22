# Запуск проекта
1. Склонируйте репозиторий
git clone https://github.com/danilpy/y_lab_fastapi
2. Подготовьте базу данных (PostgreSQL)
создайте пользователя, создайте базу данных
3. Создайте файл .env в дериктории проекта и заполните
его по примеру файла .env.example
4. Создайте виртуальное окружение в дериктории проекта и активируйте его
```python
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```
5. Установите все зависимости
```
pip install -r requirements.txt
```
6. Примените миграцию
```
alembic upgrade head
```
7. Запустите сервер
```python
python main.py
```
или
```python
uvicorn main:app --reload
```
