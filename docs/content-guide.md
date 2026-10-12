# Hướng dẫn nội dung

## Thành viên và khóa

`members.json` là danh sách object: id ổn định, name, image (URL /assets/images/...), url (có thể rỗng), section, notes (mảng chuỗi). Template Team lọc theo section và giữ thứ tự hồ sơ trong danh sách. Không đổi ID của hồ sơ cũ. `cohorts.json` gồm cohort và names; Team tham chiếu từng nhóm. Dữ liệu không có mốc tham gia/rời nhóm thì để thiếu, không suy đoán.

## Công bố

`publications.json` là object theo ID ổn định. Giữ nguyên citation, thứ tự tác giả, year, links và dữ liệu lịch sử. Metadata hiển thị gồm display_title, venue_id, venue_name, publication_type và doi. Chỉ điền DOI đã xác minh; nguồn đối chiếu lưu ở doi_source. paper_url là trang bài báo chính thức khi chưa có DOI.

Trang Papers dựng tự động từ JSON; không thêm bài trực tiếp vào template. Build gộp những bản ghi trùng chính xác tiêu đề/venue/năm cho hiển thị, giữ toàn bộ source ID và citation. Bản ghi needs_metadata_review không tự gộp. Khi đổi venue, sửa venues.json và metadata bài để giữ bộ lọc nhất quán. 150 record gốc không đồng nghĩa150 công bố độc nhất.

## Trang và tài nguyên

Thêm template src/pages và mục trong pages.json gồm source, url, title, section, hero (3 chuỗi). Tên file mới dùng kebab-case; giữ tên/URL cũ khi đã có link. Dùng UTF-8, JSON hợp lệ, URL nội bộ bắt đầu `/`. Ảnh/PDF đặt trong src/assets; không đưa cấu hình hoặc bí mật vào src/static.

Home, research, datasets và news có HTML partial riêng. Home dùng news.json và selected_achievements.json (2–3 ID trong publications.json); featured_publications.json được giữ nguyên nhưng không còn điều khiển Home. Các ghi chú lịch sử homepage_reference/homepage_date_label được giữ nguyên, không suy ra ngày tháng. Chỉ chỉnh nội dung xác minh được. Website có hai bản tĩnh: tiếng Anh mặc định ở `/`, tiếng Việt ở `/vi/`. Các nút EN / VI chuyển sang cùng trang ở ngôn ngữ còn lại.

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

Các danh sách có `data-paginate`/`data-page-item`; Publications dùng `data-page-size` kết hợp bộ lọc; Member chỉ tìm/lọc, không phân trang. Đổi bộ lọc trả về trang 1; nhóm venue/cohort trống được ẩn. Không JavaScript vẫn đọc được toàn bộ nội dung. Website dùng MP4 H.264 nén (tối đa 960px, 20fps, không tiếng); MKV là bản cùng codec cho tải/lưu trữ, không dùng làm video trình duyệt. Bản gốc nằm ngoài repo trong UIT-Together-backups.

Home dùng ảnh team0 tĩnh; slideshow không còn được hiển thị trên Home. Dữ liệu group_gallery.json và ảnh gốc giữ nguyên. Style chung hiển thị nội dung ngay, không làm mờ page header khi tải. Members giữ chuyển động riêng của hồ sơ; reduced motion/print không ẩn nội dung. Video nghiên cứu có native controls để dừng/phát, giữ logic reduced-motion. Tiêu đề UI được Title Case sau dịch và bỏ dấu chấm cuối; bảo vệ tên riêng, paper, venue, code và translate=no.

Thanh phân trang nằm ở cuối mỗi danh sách; chuyển trang giữ focus và cuộn ngay lên đầu danh sách vừa cập nhật. Tutorials hiển thị tất cả hướng dẫn, không phân trang; mục chưa có URL hiện nhãn Link pending/Chưa có liên kết. Caption nghiên cứu dùng chữ muted trên nền trắng, ngăn bằng viền mảnh; caption ảnh Home nằm trong khung navy.

Kho ảnh group_gallery.json gồm src, caption_en, caption_vi; giữ 32 ảnh hoạt động team0–team20 và LeTN2022, dùng chung asset, không sao chép ảnh. Thêm ảnh vào kho không tự tạo section mới trên Home.

## Tin tức và research highlights trên Home

Sửa `src/data/news.json` để thêm tin, không chỉnh HTML. Mỗi record có ID duy nhất; `title`, `description` và `date` ISO YYYY-MM-DD bắt buộc. `date` phải là ngày đăng có bằng chứng, không phải ngày migration hoặc ngày build. Các ngày năm 2021–2022 hiện tại đã đối chiếu thông báo trên https://uit-together.github.io/ và khớp date_label gốc.

- `verified: true` cho phép hiển thị sau khi người biên tập xác minh nội dung và ngày.
- `date_source` ghi nguồn và bằng chứng ngày đăng; `source_url` là HTTPS URL nguồn chính thức được mở từ News.
- `title_vi`, `summary_en`, `summary_vi` cung cấp tiêu đề Việt và mô tả ngắn song ngữ. Nếu thiếu bản Việt, giao diện dùng nội dung EN có lang=en, không tự dịch hoặc tạo thông tin.
- Các trường `date_label`, `url`, `description`, `links` gốc giữ nguyên để đối chiếu. URL UIT-VinaFruit20 gốc đang trỏ nhầm UIT-DODV; UI dùng source_url thông báo của nhóm, không tự sửa link nghiên cứu chưa kiểm duyệt.
- `scripts/home_content.py` kiểm tra ngày/IDs/provenance; sắp xếp giảm dần, Home lấy ba tin đầu, `/news/` lấy tất cả tin verified. Khi thêm record hợp lệ và build lại, thứ tự cập nhật tự động.
- Không có tin được xác minh thì hiển thị empty state. Nếu tin mới nhất đã hơn một năm so với ngày build, UI nêu ngày gốc của tin gần nhất; không giả vờ đó là cập nhật hiện tại.

Thay danh sách 2–3 ID trong `src/data/selected_achievements.json` để chọn Research Highlights theo thứ tự hiển thị. ID phải tồn tại, không trùng cùng một paper, có title/venue/year và DOI/paper link. Metadata và tác giả đọc trực tiếp từ publications.json, không sửa hoặc rút gọn dữ liệu gốc. Nếu thiếu authors, UI dẫn đến citation trong Publications.

Home hiện không hiển thị quartile/impact factor từ citation hoặc homepage_reference. Muốn thêm Q1 phải có bằng chứng quartile, hệ thống xếp hạng, năm và category tương ứng, được biên tập xác minh riêng; không dùng danh tiếng venue hoặc nhãn Q1 lịch sử làm chứng cứ.

`src/partials/news-content.html` cũ được giữ nguyên để đối chiếu; danh sách News dùng news-directory.html và news.json. Các URL `/news/*.html` lịch sử vẫn còn, nhưng không dùng nội dung Niemeyer làm tin UIT.

Trang Member không phân trang. `members.json` chứa các hồ sơ `section: "Supervisor"` hoặc `"Current Members"`; giữ ID ổn định, thứ tự hồ sơ chính là thứ tự thẻ trên desktop hai cột. `role` chỉ hiển thị Leader/Collaborator trong thẻ đầu; `cohort` ghi K2023 trở đi nếu đã xác nhận. `bio_en`/`bio_vi` là giới thiệu ngắn cho Current Member; để trống thì hiện thông báo sẽ cập nhật. Không dùng học vị hoặc tiểu sử giả.

`cohorts.json` giữ tên theo từng khóa: K2022 trở về trước hiển thị Former Members; K2023 trở đi hiển thị Current Members. Tên đã có thẻ không lặp lại trong danh sách cùng khóa. Thêm thành viên 2024/2025 bằng hồ sơ và cohort tương ứng. Ảnh trống dùng chữ viết tắt của tên. CSS/JS Member chỉ tải ở `/team/` và `/vi/team/`; trang dùng cuộn toàn tài liệu, không scroll snap, từng thẻ hiện dần 1 giây khi cuộn xuống và hiện ngay khi cuộn lên và điều hướng anchor theo ba nhóm. Tìm tên/khóa tiếp tục hoạt động nhưng không tạo pager. Reduced motion/print không ẩn nội dung.

## Hội nghị và deadline

`src/data/conferences.json` chứa kỳ hiện tại, địa điểm, khoảng ngày tổ chức và các deadline có nguồn chính thức. `at` chỉ ghi khi có giờ kèm múi giờ; `date`/`zone` giữ trường hợp chỉ công bố ngày. Không suy đoán địa điểm hoặc deadline cho kỳ mới. ICCV cách hai năm; `cadence` điều khiển đổi kỳ. `checked_at` ghi lần thử đồng bộ, `last_success_at` ghi lần đọc được bằng chứng. Website hiển thị theo `Asia/Ho_Chi_Minh`.

Updater tự chuyển kỳ sau hết ngày kết thúc AoE, xóa lịch cũ và dò nguồn chính thức kỳ tiếp theo. TBA hoặc nguồn mâu thuẫn không có bộ đếm giờ giả. Thêm hội nghị/domain mới phải khai báo seed và allowlist trong updater rồi chạy test parser, test clock, build/check. Xem [conference-automation.md](conference-automation.md).

Các `data-page-item` phải độc lập, không lồng vào nhau. Datasets có 13 mục, 3 mục/trang: 5 trang, trang cuối có 1 mục. Kiểm thử cấu trúc phân trang rà toàn bộ HTML đã build ở cả EN/VI.
