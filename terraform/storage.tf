# Статический ключ доступа для S3
resource "yandex_iam_service_account_static_access_key" "sa-static-key" {
  service_account_id = yandex_iam_service_account.sa-admin.id
}

resource "yandex_storage_bucket" "photo-bucket" {
  bucket     = "my-gallery-unique-name-${var.folder_id}" # Имя должно быть глобально уникальным
  access_key = yandex_iam_service_account_static_access_key.sa-static-key.access_key
  secret_key = yandex_iam_service_account_static_access_key.sa-static-key.secret_key

  anonymous_access_flags {
    read = true
    list = false
  }
}