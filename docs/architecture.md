# Kiến trúc

`src/pages` là Jinja template. `pages.json` khai báo route, title, section và hero. Build đọc JSON, render với StrictUndefined và HTML autoescape rồi copy asset theo allowlist. Không chạy Jekyll, không copy repo vào public. BibTeX có dấu ngoặc kép đã được escape để không bị hiểu là Jinja.

`src/assets` phát ra `/assets/...`, riêng JavaScript phát ra `/js/...` để giữ route cũ. `src/static` giữ tài nguyên dataset/feeds theo route tương ứng. `themes` là Bootstrap/theme vendor hiện có; CSS mới ở site.css. SCSS cũ được lưu trong legacy vì pipeline hiện tại không dùng nó.

`dist` được tạo mới để loại file stale. Lỗi render giữ bản cũ; dev watcher báo lỗi và chờ lần sửa tiếp theo. Dev server phục vụ dist, không directory listing; hỗ trợ URL bỏ `.html` tương tự nginx try_files. Watcher không tự reload browser.

Website công khai là bản tĩnh. Header/footer và hồ sơ thành viên/công bố dùng template chung. Cập nhật trang chủ dùng news.json; datasets, nghiên cứu và trang tin lịch sử vẫn là HTML nội dung được tách riêng để bảo toàn dữ liệu lịch sử chưa xác minh.

Build render mỗi template hai lần (en/vi), rồi scripts/i18n.py xử lý text-node có dictionary và đường dẫn nội bộ. Kết quả có 292 trang và một bộ assets chung. Header có lựa chọn ngôn ngữ không phụ thuộc JavaScript; layout có hreflang en/vi/x-default. check_site kiểm tra cả hai cây URL, so baseline cũ theo route gốc.

Lịch hội nghị nằm ở `src/data/conferences.json`, được copy theo allowlist sang `/assets/data/conferences.json`. `conference-clock.js` tách logic thời gian/đổi kỳ để kiểm thử; `conferences.js` dựng feature Home, directory, phân trang và bộ đếm EN/VI. `scripts/update_conferences.py` kiểm tra nguồn chính thức, chạy định kỳ trong dev server và GitHub Actions; chưa push/kích hoạt workflow từ xa. Trình duyệt tải JSON mới mỗi 5 phút, giữ seed nếu mạng lỗi. Chi tiết: [conference-automation.md](conference-automation.md).

Nội dung được chỉnh trực tiếp trong JSON/template của `src/`; website không có backend quản trị, tài khoản, đăng nhập hoặc form cập nhật nội dung.

GitHub Pages dùng `.github/workflows/deploy-pages.yml`, chỉ xuất bản `dist`. `scripts/site_paths.py` thêm base path cho URL nội bộ của HTML/CSS và redirect. `site-base-path` trong HTML cung cấp prefix cho liên kết/fetch động Conferences. Bản local mặc định prefix rỗng; `--base-path /UIT-Together` phục vụ project site. Check site loại prefix trước khi kiểm tra asset/baseline.
