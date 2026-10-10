# Hướng dẫn nội dung

## Thành viên và khóa

`members.json` là danh sách object: id ổn định, name, image (URL /assets/images/...), url (có thể rỗng), section, notes (mảng chuỗi). Template Team hiện tham chiếu chỉ số danh sách; khi thêm hoặc đổi thứ tự, cập nhật `{% set member = members[n] %}` tại src/pages/team/index.html. Không đổi ID của hồ sơ cũ. `cohorts.json` gồm cohort và names; Team tham chiếu từng nhóm. Dữ liệu không có mốc tham gia/rời nhóm thì để thiếu, không suy đoán.

## Công bố

`publications.json` là object theo ID ổn định. Fields: id, citation (nguyên văn, giữ tác giả đúng thứ tự), year, links, layouts, title/authors/venue/image cho dạng card. Không tự suy ra DOI. Bản ghi có citation nhưng chưa tách chắc chắn title/authors vẫn được hiển thị đầy đủ ở dạng citation.

Hai view dùng chung bản ghi bằng `{% set publication = publications["ID"] %}{% set kind = "citation" %}{% include "partials/publication.html" %}`. Dạng `card` cần title/authors/venue; thêm reference vào đúng nhóm ở Papers và PapersByYear. Sửa cả citation lẫn trường riêng nếu thay nội dung một card. Các bản ghi chỉ gộp khi văn bản trùng chắc chắn, không gộp gần đúng; 150 record không phải số công bố độc nhất đã được khoa học xác minh.

## Trang và tài nguyên

Thêm template src/pages và mục trong pages.json gồm source, url, title, section, hero (3 chuỗi). Tên file mới dùng kebab-case; giữ tên/URL cũ khi đã có link. Dùng UTF-8, JSON hợp lệ, URL nội bộ bắt đầu `/`. Ảnh/PDF đặt trong src/assets; không đưa cấu hình hoặc bí mật vào src/static.

Home, research, datasets và news có HTML partial riêng. Home dùng news.json và featured_publications.json (danh sách ID trong publications.json). Các ghi chú lịch sử homepage_reference/homepage_date_label được giữ nguyên, không suy ra ngày tháng. Chỉ chỉnh nội dung xác minh được. Website hiện giữ tiếng Anh và tutorial tiếng Việt; chưa triển khai đa ngôn ngữ.

Sau sửa: build, check_site; mở local và kiểm tra trang liên quan. Báo cáo missing links phân biệt baseline và regression.
