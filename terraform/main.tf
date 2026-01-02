terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  # Для федеративных аккаунтов лучше создать Service Account Key и указать путь к JSON
  service_account_key_file = "key.json"
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  zone                     = var.zone
}

# Виртуальная сеть (VPC)
resource "yandex_vpc_network" "gallery-net" {
  name = "gallery-network"
}

resource "yandex_vpc_subnet" "gallery-subnet" {
  name           = "gallery-subnet-a"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.gallery-net.id
  v4_cidr_blocks = ["10.0.0.0/24"]
}

# Сервисный аккаунт для всей системы (пункт №10 ТЗ)
resource "yandex_iam_service_account" "sa-admin" {
  name        = "gallery-admin-sa"
  description = "SA для управления S3 и функциями"
}

# Назначаем права
resource "yandex_resourcemanager_folder_iam_member" "sa-editor" {
  folder_id = var.folder_id
  role      = "editor"
  member    = "serviceAccount:${yandex_iam_service_account.sa-admin.id}"
}