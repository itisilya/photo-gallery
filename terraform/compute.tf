# Образ ОС (Ubuntu)
data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2204-lts"
}

resource "yandex_compute_instance" "backend-vm" {
  name        = "gallery-backend"
  platform_id = "standard-v3" # Самый экономный вариант (Ice Lake)
  zone        = "ru-central1-a"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = 20
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.gallery-subnet.id
    nat       = true # Нужен для скачивания пакетов и докера
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_ed25519.pub")}"
    user-data = <<-EOF
      #!/bin/bash
      # 1. Установка Docker и Docker Compose
      apt-get update
      apt-get install -y docker.io docker-compose git

      # 2. Клонирование кода
      cd /home/ubuntu
      git clone https://github.com/itisilya/photo-gallery.git
      cd photo-gallery

      # 3. Создание файла .env с данными, которые знает Terraform
      cat <<EOT > .env
      MONGODB_URL=mongodb://admin:password@mongodb:27017
      DB_NAME=gallery_db
      S3_BUCKET_NAME=${yandex_storage_bucket.photo-bucket.bucket}
      S3_ACCESS_KEY=${yandex_iam_service_account_static_access_key.sa-static-key.access_key}
      S3_SECRET_KEY=${yandex_iam_service_account_static_access_key.sa-static-key.secret_key}
      S3_REGION=ru-central1
      S3_ENDPOINT=https://storage.yandexcloud.net
      VITE_API_URL=http://${yandex_alb_load_balancer.gallery-lb.listener.0.endpoint.0.address.0.external_ipv4_address}/api
      EOT

      # 4. Запуск всего проекта
      docker-compose up -d --build
    EOF
  }
}