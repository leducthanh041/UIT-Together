# Kiến trúc

`src/pages` là Jinja template. `pages.json` khai báo route, title, section và hero. Build đọc JSON, render với StrictUndefined và HTML autoescape rồi copy asset theo allowlist. Không chạy Jekyll, không copy repo vào public. BibTeX có dấu ngoặc kép đã được escape để không bị hiểu là Jinja.

`src/assets` phát ra `/assets/...`, riêng JavaScript phát ra `/js/...` để giữ route cũ. `src/static` giữ tài nguyên dataset/feeds theo route tương ứng. `themes` là Bootstrap/theme vendor hiện có; CSS mới ở site.css. SCSS cũ được lưu trong legacy vì pipeline hiện tại không dùng nó.

`dist` được tạo mới để loại file stale. Lỗi render giữ bản cũ; dev watcher báo lỗi và chờ lần sửa tiếp theo. Dev server phục vụ dist, không directory listing; hỗ trợ URL bỏ `.html` tương tự nginx try_files. Watcher không tự reload browser.

Header render destinations trực tiếp từ navigation data, lọc News/Tutorials khỏi menu chính nhưng giữ nguyên route. Research directions được khai báo một lần theo schema trong `src/partials/research-content.html` và render qua `src/partials/research-direction.html`; schema chứa bản dịch, nguồn media, loại media, alt text và caption để nội dung EN/VI cùng dùng một layout.

Website công khai là bản tĩnh. Header/footer và hồ sơ thành viên/công bố dùng template chung. Cập nhật trang chủ dùng news.json; datasets, nghiên cứu và trang tin lịch sử vẫn là HTML nội dung được tách riêng để bảo toàn dữ liệu lịch sử chưa xác minh.

Home gồm About UIT Together (hero trong main), Group Statistics, Latest News và Research Highlights. Statistics đọc `group_stats` do `scripts/group_statistics.py` tính lúc build, không lưu số đếm trong HTML. `scripts/home_content.py` kiểm tra ngày ISO/provenance, chọn tối đa ba tin đã xác minh theo ngày giảm dần và đọc 2–3 publication IDs từ `src/data/selected_achievements.json`. Build render kết quả EN/VI; không cần JS để sắp xếp hoặc đọc nội dung. `/news/` dùng cùng dữ liệu, giữ danh sách đầy đủ và anchor theo news ID. Partial news-content.html cũ của Niemeyer còn nguyên để đối chiếu nhưng không được include vào danh sách UIT. URL bài tin lịch sử không đổi. Không trích quartile từ citation hoặc homepage_reference để tạo nhãn thành tích.

Nhận diện và components chung tải từ `src/assets/css/site.css`; base layout không còn tải portfolio.css hoặc header-home.css. Hai file cũ được giữ lại để bảo toàn lịch sử source, không phải nơi chỉnh UI hiện hành. Members và Conferences chỉ tải stylesheet riêng cho cấu trúc/hành vi đặc thù, tham chiếu tokens chung. Page header và footer dùng base/partials chung; footer không có navigation. News/Tutorials vẫn build EN/VI theo route cũ nhưng không xuất hiện trong navigation chính; Home không có View all news.

Build render mỗi template hai lần (en/vi), rồi scripts/i18n.py xử lý text-node có dictionary và đường dẫn nội bộ. Kết quả có 292 trang và một bộ assets chung. Header có lựa chọn ngôn ngữ không phụ thuộc JavaScript; layout có hreflang en/vi/x-default. check_site kiểm tra cả hai cây URL, so baseline cũ theo route gốc.

Lịch hội nghị nằm ở `src/data/conferences.json`, được copy theo allowlist sang `/assets/data/conferences.json`. `conference-clock.js` tách logic thời gian/đổi kỳ để kiểm thử; `conferences.js` dựng feature Home, directory, phân trang và bộ đếm EN/VI. `scripts/update_conferences.py` kiểm tra nguồn chính thức, chạy định kỳ trong dev server và GitHub Actions; chưa push/kích hoạt workflow từ xa. Trình duyệt tải JSON mới mỗi 5 phút, giữ seed nếu mạng lỗi. Chi tiết: [conference-automation.md](conference-automation.md).

Nội dung được chỉnh trực tiếp trong JSON/template của `src/`; website không có backend quản trị, tài khoản, đăng nhập hoặc form cập nhật nội dung.

GitHub Pages dùng `.github/workflows/deploy-pages.yml`, chỉ xuất bản `dist`. `scripts/site_paths.py` thêm base path cho URL nội bộ của HTML/CSS và redirect. `site-base-path` trong HTML cung cấp prefix cho liên kết/fetch động Conferences. Bản local mặc định prefix rỗng; `--base-path /UIT-Together` phục vụ project site. Check site loại prefix trước khi kiểm tra asset/baseline.
