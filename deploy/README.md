# Triển khai UIT-Together trên server

Chạy từ thư mục repo:

```bash
python3 deploy/prepare.py
docker compose -f deploy/compose.yaml up -d web
curl -I http://127.0.0.1:8080
```

Website được chuẩn bị từ HTML hiện tại, không dùng bản `_site` cũ. Chỉ thư mục `dist` được phục vụ; mã công cụ và cấu hình repo không nằm trong thư mục public.

## Tên miền và Cloudflare Tunnel

1. Thêm tên miền vào tài khoản Cloudflare và hoàn tất cấu hình nameserver.
2. Tạo Cloudflare Tunnel, chọn connector Docker.
3. Sao chép `.env.example` thành `.env`, đặt token của tunnel vào `TUNNEL_TOKEN`. Không commit hoặc chia sẻ token.
4. Tạo published application cho tên miền mong muốn, đặt service là `http://web:80`. Không thêm yêu cầu đăng nhập nếu website dành cho mọi người.
5. Chạy:

```bash
docker compose --env-file deploy/.env -f deploy/compose.yaml --profile public up -d
docker compose --env-file deploy/.env -f deploy/compose.yaml logs --tail=50
```

Kiểm tra tên miền bằng HTTPS từ mạng ngoài. Server cần Docker Compose, kết nối Internet cho container và phải luôn bật. Cập nhật nội dung bằng cách chạy lại `python3 deploy/prepare.py`. Build tạo lại toàn bộ dist để loại file stale.

Dừng dịch vụ:

```bash
docker compose --env-file deploy/.env -f deploy/compose.yaml down
```
