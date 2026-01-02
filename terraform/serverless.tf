# Упаковываем код функции в ZIP
data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../cloud_function"
  output_path = "${path.module}/function.zip"
}

resource "yandex_function" "photo-resizer" {
  name               = "photo-resizer"
  description        = "Функция для создания превью"
  user_hash          = data.archive_file.function_zip.output_base64sha256
  runtime            = "python312"
  entrypoint         = "handler.handler"
  memory             = 128
  execution_timeout  = "10"
  service_account_id = yandex_iam_service_account.sa-admin.id

  content {
    zip_filename = data.archive_file.function_zip.output_path
  }

  environment = {
    S3_ENDPOINT           = "https://storage.yandexcloud.net"
    S3_BUCKET_NAME        = yandex_storage_bucket.photo-bucket.bucket
    AWS_ACCESS_KEY_ID     = yandex_iam_service_account_static_access_key.sa-static-key.access_key
    AWS_SECRET_ACCESS_KEY = yandex_iam_service_account_static_access_key.sa-static-key.secret_key
  }
}

# Триггер: запускать функцию при создании объекта в бакете
resource "yandex_function_trigger" "s3-trigger" {
  name        = "photo-s3-trigger"
  description = "Trigger for S3 uploads"

  # Блок для вызова функции
  function {
    id                 = yandex_function.photo-resizer.id
    service_account_id = yandex_iam_service_account.sa-admin.id
  }

  # Настройки источника событий (S3)
  object_storage {
    bucket_id = yandex_storage_bucket.photo-bucket.id
    create    = true

    # Эти параметры теперь обязательны в новых версиях провайдера
    batch_cutoff = "1"   # Максимальное время ожидания (в секундах) перед вызовом функции
    batch_size   = "1"   # Количество событий, которые функция может обработать за раз
  }
}