output "balancer_ip" {
  value = yandex_vpc_address.gallery-ip.external_ipv4_address.0.address
}

output "bucket_name" {
  value = yandex_storage_bucket.photo-bucket.bucket
}