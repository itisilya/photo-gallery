# Группа целевых ресурсов (наша VM с бэкендом)
resource "yandex_alb_target_group" "gallery-tg" {
  name = "gallery-target-group"

  target {
    subnet_id = yandex_vpc_subnet.gallery-subnet.id
    ip_address = yandex_compute_instance.backend-vm.network_interface.0.ip_address
  }
}

resource "yandex_vpc_address" "gallery-ip" {
  name = "gallery-static-ip"
  external_ipv4_address {
    zone_id = "ru-central1-a"
  }
}

# Группа бэкендов
resource "yandex_alb_backend_group" "gallery-bg" {
  name = "gallery-backend-group"

  http_backend {
    name             = "fastapi-backend"
    weight           = 1
    port             = 80 # Порт вашего FastAPI
    target_group_ids = [yandex_alb_target_group.gallery-tg.id]
    load_balancing_config {
      panic_threshold = 50
    }
    healthcheck {
      timeout  = "2s"
      interval = "2s"
      http_healthcheck {
        path = "/" # Проверяем корень фронтенда (порт 80)
      }
    }
  }
}

# HTTP роутер
resource "yandex_alb_http_router" "gallery-router" {
  name = "gallery-router"
}

resource "yandex_alb_virtual_host" "gallery-host" {
  name           = "gallery-host"
  http_router_id = yandex_alb_http_router.gallery-router.id
  route {
    name = "main-route"
    http_route {
      http_route_action {
        backend_group_id = yandex_alb_backend_group.gallery-bg.id
        timeout          = "3s"
      }
    }
  }
}

# Сам балансировщик
resource "yandex_alb_load_balancer" "gallery-lb" {
  name               = "gallery-load-balancer"
  network_id         = yandex_vpc_network.gallery-net.id
  allocation_policy {
    location {
      zone_id   = "ru-central1-a"
      subnet_id = yandex_vpc_subnet.gallery-subnet.id
    }
  }

  listener {
    name = "http-listener"
    endpoint {
      address {
        external_ipv4_address {
          address = yandex_vpc_address.gallery-ip.external_ipv4_address.0.address # Ссылка на статический IP
        }
      }
      ports = [80]
    }
    http {
      handler {
        http_router_id = yandex_alb_http_router.gallery-router.id
      }
    }
  }
}