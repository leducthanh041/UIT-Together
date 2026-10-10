# Hướng dẫn nội dung

## Thành viên và khóa

`members.json` là danh sách object: id ổn định, name, image (URL /assets/images/...), url (có thể rỗng), section, notes (mảng chuỗi). Template Team hiện tham chiếu chỉ số danh sách; khi thêm hoặc đổi thứ tự, cập nhật `{% set member = members[n] %}` tại src/pages/team/index.html. Không đổi ID của hồ sơ cũ. `cohorts.json` gồm cohort và names; Team tham chiếu từng nhóm. Dữ liệu không có mốc tham gia/rời nhóm thì để thiếu, không suy đoán.

## Công bố

`publications.json` là object theo ID ổn định. Giữ nguyên citation, thứ tự tác giả, year, links và dữ liệu lịch sử. Metadata hiển thị gồm display_title, venue_id, venue_name, publication_type và doi. Chỉ điền DOI đã xác minh; nguồn đối chiếu lưu ở doi_source. paper_url là trang bài báo chính thức khi chưa có DOI.

Trang Papers dựng tự động từ JSON; không thêm bài trực tiếp vào template. Build gộp những bản ghi trùng chính xác tiêu đề/venue/năm cho hiển thị, giữ toàn bộ source ID và citation. Bản ghi needs_metadata_review không tự gộp. Khi đổi venue, sửa venues.json và metadata bài để giữ bộ lọc nhất quán. 150 record gốc không đồng nghĩa150 công bố độc nhất.

## Trang và tài nguyên

Thêm template src/pages và mục trong pages.json gồm source, url, title, section, hero (3 chuỗi). Tên file mới dùng kebab-case; giữ tên/URL cũ khi đã có link. Dùng UTF-8, JSON hợp lệ, URL nội bộ bắt đầu `/`. Ảnh/PDF đặt trong src/assets; không đưa cấu hình hoặc bí mật vào src/static.

Home, research, datasets và news có HTML partial riêng. Home dùng news.json và featured_publications.json (danh sách ID trong publications.json). Các ghi chú lịch sử homepage_reference/homepage_date_label được giữ nguyên, không suy ra ngày tháng. Chỉ chỉnh nội dung xác minh được. Website có hai bản tĩnh: tiếng Anh mặc định ở `/`, tiếng Việt ở `/vi/`. Các nút EN / VI chuyển sang cùng trang ở ngôn ngữ còn lại.

Sau sửa: build, check_site; mở local và kiểm tra trang liên quan. Báo cáo missing links phân biệt baseline và regression.

## Công bố gọn và Contact (2026-10-10)

`/papers/` là trang chung cho công bố và năm; `/PapersByYear/` chuyển tiếp. Dropdown năm, loại (journal/conference) và venue kết hợp với tìm kiếm. Venue được chuẩn hóa trong `src/data/venues.json`; mỗi venue dùng một cover/logo cho cả nhóm bài, không lặp ảnh trên từng hàng.

Publication thêm `display_title`, `venue_id`, `venue_name`, `publication_type`, `doi`, `needs_metadata_review`. Giữ `citation`, tác giả và link nguồn. `doi` chỉ chứa định danh `10...`, không gồm prefix URL. Có thể để rỗng. Không suy luận DOI từ số IEEE document hoặc tên bài. Build gộp chính xác tiêu đề/venue/năm cho hiển thị, giữ mọi source ID và citation; bản ghi cần review không tự gộp.

Tải cover/logo từ các nguồn trong `venue-image-sources.md` và lưu `src/assets/images/venues/<venue_id>.webp` (hoặc png/jpg/jpeg/svg). Build tự nhận file theo slug khi `venues.json.image` rỗng; cũng có thể khai báo `image` rõ ràng. Không dùng ảnh minh họa của paper làm bìa journal. Chạy lại build sau khi thêm ảnh.

Contact dùng `src/data/contacts.json`; email trống không tạo link mailto. Khanh Duy Nguyen đã được người dùng xác nhận danh tính; ảnh dùng từ hồ sơ thành viên hiện có. Email chưa được xác minh nên để trống.

Kiểm tra bổ sung: `python -m unittest discover -s tests`.

Kiểm tra bộ lọc kết hợp: `node tests/publication_filters.test.js` (mô phỏng DOM; không thay thế kiểm tra trình duyệt). DOI được đối chiếu web có `doi_source`; `paper_url` là trang nguồn chính thức cho bài chưa xác minh DOI. Xem `doi-research.md` và `doi-older-research.md`.

## Ngôn ngữ

`src/data/translations.json` chứa các map `en` và `vi`: khóa là nguyên văn nội dung, giá trị là bản dịch. `src/data/tutorial-translations.json` dịch nội dung tutorial tiếng Việt sang tiếng Anh; build sử dụng map đảo chiều cho bản Việt. Khi thêm nội dung, bổ sung bản dịch phù hợp; không sửa trực tiếp dist. Khoảng trắng trong khóa được chuẩn hóa khi so khớp. `scripts/i18n.py` dịch các text-node và nhãn accessibility, giữ code/pre/script/style và các vùng `translate="no"`. Tên tác giả, tên bài báo, DOI và venue giữ nguyên. Ảnh và JS/CSS dùng chung cho hai ngôn ngữ; không nhân đôi assets.

Mỗi template trong pages.json được build ra cả URL gốc và URL có prefix `/vi`. Không cần viết lại 145 template. Liên kết điều hướng, tutorial và chuyển hướng đi theo ngôn ngữ; link DOI, email, PDF và tài nguyên ngoài giữ nguyên. Cập nhật vai trò Hiệu trưởng / Phó Giáo sư, Tiến sĩ của Nguyen Tan Tran Minh Khang và email khanhnd@uit.edu.vn theo thông tin người dùng cung cấp.

## Hướng nghiên cứu

Trang Research dùng `src/partials/research-content.html`, nội dung EN/VI theo biến language. Giới thiệu AI medical (Sparse-View CT Reconstruction, WSI classification/survival risk), Anomaly Detection; Object Detection trong điều kiện clean, fog, rain, snow (video `Object_detection/object_detection.mp4`). Media gốc ở `src/assets/images/research/`; `anomaly-detection-web.mp4` là bản H.264 chuyển từ video gốc để tương thích trình duyệt. Các video tự chạy lặp, tắt tiếng và ẩn controls như GIF; tôn trọng reduced motion qua JS. Không gắn hình minh họa với kết quả hay độ chính xác chưa xác minh.

## Phân trang và ảnh động

Các danh sách có `data-paginate`/`data-page-item`; Publications và People dùng `data-page-size` kết hợp bộ lọc. Đổi bộ lọc trả về trang 1; nhóm venue/cohort trống được ẩn. Không JavaScript vẫn đọc được toàn bộ nội dung. Website dùng MP4 H.264 nén (tối đa 960px, 20fps, không tiếng); MKV là bản cùng codec cho tải/lưu trữ, không dùng làm video trình duyệt. Bản gốc nằm ngoài repo trong UIT-Together-backups.

Slideshow trang chủ dùng 9 ảnh từ gallery People, đổi ảnh mỗi 4,5 giây khi đang trong màn hình. Có trước/sau/tạm dừng; dừng tự chuyển khi hover, focus, tab ẩn hoặc reduced motion. Scroll reveal đặt lại trạng thái khi phần tử rời màn hình để xuất hiện lại khi cuộn quay lại. Tiêu đề UI được Title Case sau dịch và bỏ dấu chấm cuối; bảo vệ tên riêng, paper, venue, code và translate=no.

Thanh phân trang nằm ở đầu mỗi danh sách và sticky dưới header; chuyển trang giữ focus nhưng không gọi scrollIntoView. Chú thích media dùng nền/viền xanh và chữ có tương phản cao; chú thích slideshow nền xanh đậm.
