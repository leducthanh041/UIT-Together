# Kiến trúc

`src/pages` là Jinja template. `pages.json` khai báo route, title, section và hero. Build đọc JSON, render với StrictUndefined và HTML autoescape rồi copy asset theo allowlist. Không chạy Jekyll, không copy repo vào public. BibTeX có dấu ngoặc kép đã được escape để không bị hiểu là Jinja.

`src/assets` phát ra `/assets/...`, riêng JavaScript phát ra `/js/...` để giữ route cũ. `src/static` giữ tài nguyên dataset/feeds theo route tương ứng. `themes` là Bootstrap/theme vendor hiện có; CSS mới ở site.css. SCSS cũ được lưu trong legacy vì pipeline hiện tại không dùng nó.

`dist` được tạo mới để loại file stale. Lỗi render giữ bản cũ; dev watcher báo lỗi và chờ lần sửa tiếp theo. Dev server phục vụ dist, không directory listing; hỗ trợ URL bỏ `.html` tương tự nginx try_files. Watcher không tự reload browser.

Không có backend, database, upload hay CMS. Header/footer và hồ sơ thành viên/công bố dùng template chung. Cập nhật trang chủ dùng news.json; datasets, nghiên cứu và trang tin lịch sử vẫn là HTML nội dung được tách riêng để bảo toàn dữ liệu lịch sử chưa xác minh.
