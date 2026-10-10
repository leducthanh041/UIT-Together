# Kế hoạch bảo mật khi triển khai public

Ngày ghi nhận: 2026-10-10. Trạng thái: kế hoạch, tạm gác triển khai public để ưu tiên chỉnh sửa local. Chưa xác minh đầy đủ cấu hình mạng và quyền quản trị server 192.168.20.166; tài liệu này không chứng nhận server đã an toàn.

## Kiến trúc đề xuất

Người xem → HTTPS/Cloudflare → Cloudflare Tunnel → Nginx → thư mục website tĩnh `dist/` chỉ đọc.

Tunnel tạo kết nối đi ra ngoài, tránh yêu cầu mở cổng web inbound. Website vẫn cần bảo vệ dù origin không có IP public. Nếu server chứa dữ liệu nghiên cứu quan trọng, ưu tiên VM riêng cho website; container dùng chung kernel với host.

## Các lớp bảo vệ

1. **Phạm vi public:** chỉ đưa HTML, CSS, JavaScript, ảnh và PDF đã duyệt vào `dist/`. Không phục vụ cả repo, skill, backup, `.env`, khóa hoặc dữ liệu nghiên cứu nội bộ. Quét artifact trước phát hành.
2. **Mạng:** Tunnel chỉ được truy cập Nginx. Không publish cổng container ra Internet; cổng debug chỉ mở khi cần, ưu tiên loopback/SSH forwarding. Kiểm tra cả IPv4 và IPv6. Docker có thể xử lý cổng publish ngoài luồng UFW, nên cần kiểm tra từ mạng ngoài.
3. **Nginx:** tắt directory listing; chỉ phục vụ file tĩnh; chặn file riêng; giới hạn phương thức, timeout và tài nguyên phù hợp. Không bật PHP/CGI. Kiểm tra cấu hình trước reload.
4. **Container:** user không đặc quyền, website mount read-only, giảm capabilities, `no-new-privileges`, giới hạn CPU/RAM/PID và log. Root filesystem read-only khi đã bố trí vùng ghi cần thiết. Không mount Docker socket, home hoặc dữ liệu nghiên cứu. Đánh giá rootless Docker nếu phù hợp.
5. **Host:** cập nhật bản vá, kiểm kê dịch vụ, firewall theo nhu cầu thực tế, tài khoản vận hành riêng và quyền tối thiểu. Không thay đổi dịch vụ nghiên cứu ngoài phạm vi website.
6. **SSH:** dùng khóa; giới hạn VPN/mạng quản trị khi khả thi. Xác minh đăng nhập bằng khóa và quyền truy cập dự phòng trước khi tắt password/root login hoặc thay firewall. Fail2ban chỉ bổ sung khi SSH có nhu cầu tiếp xúc mạng ngoài.
7. **Bí mật và tài khoản:** MFA cho DNS/Cloudflare/GitHub; token quyền tối thiểu, lưu ngoài public và không commit. Có quy trình thu hồi/thay token. Không ghi token vào log hoặc tài liệu.

## Bảo vệ mã phía trình duyệt

- Kiểm kê thư viện/CDN và inline script/style hiện có; loại bỏ phần không dùng, cập nhật phần cần thiết, cố định phiên bản.
- Ưu tiên tài nguyên self-hosted có giấy phép rõ; dùng kiểm tra tính toàn vẹn khi phù hợp với CDN.
- Escape dữ liệu khi render HTML; tránh chèn dữ liệu chưa xử lý bằng `innerHTML` trong tìm kiếm/bộ lọc.
- Thêm `X-Content-Type-Options`, `Referrer-Policy` và chống nhúng trang phù hợp.
- Triển khai CSP Report-Only trước; xử lý vi phạm rồi bật enforcement. Bố trí nơi nhận báo cáo nếu sử dụng report endpoint.
- Bật HSTS sau khi HTTPS ổn định; không tự bật preload/includeSubDomains trước khi kiểm kê các subdomain.

## Lưu lượng bất thường

- Cache tại Cloudflare, chọn WAF/rate limiting theo tính năng thực tế của gói tài khoản.
- Quan sát lưu lượng trước khi chặn; tránh ảnh hưởng người dùng chung mạng trường và tải ảnh/PDF.
- Nếu limit theo IP ở Nginx, chỉ tin header IP từ proxy đã xác định; không tin header tùy ý của client. Không gom toàn bộ người dùng thành IP của connector.
- Có thể dùng rate-limit dry-run trước enforcement. Không áp CAPTCHA/đăng nhập toàn website học thuật theo mặc định.
- Giới hạn tại origin không thay thế chống DDoS ở phía nhà cung cấp.

## Trình tự triển khai và nghiệm thu

1. Khảo sát OS, bản vá, dịch vụ/cổng, Docker, SSH, firewall, IPv6 và dữ liệu dùng chung trên server thật.
2. Backup và kiểm tra đường khôi phục; giữ phiên quản trị đang hoạt động khi thay SSH/firewall.
3. Cô lập web trong VM hoặc container theo kết quả khảo sát.
4. Kiểm tra local: trang hoạt động; dịch vụ không sửa được artifact hoặc truy cập dữ liệu ngoài phạm vi.
5. Kết nối tên miền, Tunnel và HTTPS.
6. Kiểm tra từ mạng ngoài: cổng mở, khả năng bypass origin, file riêng, headers, CSP, tải bình thường và tải vượt ngưỡng.
7. Thử restart, rollback, khôi phục backup ngoài server và thay token.
8. Bật cảnh báo uptime, tài nguyên và lỗi bất thường; cấu hình log rotation/thời gian lưu phù hợp.

## Sự cố và bảo trì

Khi nghi ngờ xâm nhập: ngắt route Tunnel để hạn chế tiếp xúc, bảo toàn log, thu hồi bí mật liên quan, xác định phạm vi ảnh hưởng, phục hồi từ bản sạch. Không xóa bằng chứng trước khi đánh giá.

Cập nhật image/dependency có kiểm tra và khả năng rollback; tránh dùng tag trôi nổi cho bản production đã nghiệm thu. Lưu tài liệu vận hành và diễn tập phục hồi định kỳ. Không có cấu hình nào bảo đảm miễn nhiễm hoàn toàn.

## Tài liệu chính thức

- [Cloudflare Tunnel](https://developers.cloudflare.com/tunnel/)
- [Docker security](https://docs.docker.com/engine/security/)
- [Docker rootless](https://docs.docker.com/engine/security/rootless/)
- [Docker firewall](https://docs.docker.com/engine/network/packet-filtering-firewalls/)
- [Nginx request limiting](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)
- [OWASP HTTP headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)
- [OWASP CSP](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
