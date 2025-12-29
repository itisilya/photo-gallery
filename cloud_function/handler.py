import boto3
import os
from io import BytesIO
from PIL import Image

# Настройки S3 (в облаке функция может брать их из переменных окружения)
s3_endpoint = 'https://storage.yandexcloud.net'


def handler(event, context):
    s3 = boto3.client(
        service_name='s3',
        endpoint_url=s3_endpoint,
        # Внутри Yandex Cloud ключи часто не нужны, если привязана роль,
        # но для начала укажем их в переменных функции
    )

    # Получаем информацию о загруженном файле из события (event)
    for record in event.get('messages', []):
        bucket_name = record['details']['bucket_id']
        object_key = record['details']['object_id']

        # Чтобы не уйти в бесконечный цикл (не обрабатывать уже созданные превью)
        if object_key.startswith('thumb_'):
            continue

        print(f"Обработка файла: {object_key} из бакета {bucket_name}")

        # 1. Скачиваем файл из S3 в память
        file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = file_obj['Body'].read()

        # 2. Обрабатываем через Pillow (делаем Thumbnail)
        img = Image.open(BytesIO(file_content))
        img.thumbnail((200, 200))  # Размер превью

        buffer = BytesIO()
        img.save(buffer, format=img.format)
        buffer.seek(0)

        # 3. Сохраняем превью обратно в S3 с префиксом thumb_
        thumb_key = f"thumb_{object_key}"
        s3.put_object(
            Bucket=bucket_name,
            Key=thumb_key,
            Body=buffer,
            ACL='public-read',
            ContentType=file_obj['ContentType']
        )
        print(f"Превью сохранено: {thumb_key}")

    return {'statusCode': 200}