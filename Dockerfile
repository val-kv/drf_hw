# Используем официальный образ Python в качестве базового образа
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы requirements.txt и Dockerfile в контейнер
COPY requirements.txt ./
COPY Dockerfile ./

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Мигрируем базу данных
RUN python manage.py migrate

# Запускаем команду для запуска проекта
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]