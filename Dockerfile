# Используем образ Python
FROM python:3.9

# Устанавливаем рабочую директорию в /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Копируем requirements.txt в текущую директорию образа
COPY requirements.txt .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы из текущей директории (где находится Dockerfile) в /app в образе
COPY . .

# Выполняем миграции
RUN python manage.py makemigrations && python manage.py migrate


# Заполняем базу данных с использованием фикстур
RUN ./load_fixtures.sh

# Создаем администатора
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@myproject.com', 'password')" | python manage.py shell

# Указываем, что приложение будет доступно на порту 8000
EXPOSE 8000

# Запускаем приложение
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
