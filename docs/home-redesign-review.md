# Home/header redesign review, 2026-10-12

Scope: header toàn site, Home hero và luồng nội dung Home. Anti-Slop during theo lựa chọn của người quản lý; direction và lý do thiết kế ghi trong design-system.md. Đây không phải chứng nhận accessibility toàn website hoặc kiểm tra link ngoài.

## Kiểm tra thực tế

Runtime: `/home/uit2023/LuuTru/Vutm/.conda-envs/UITweb/bin/python`.

- PASS: build sinh 292 trang EN/VI; check_site kiểm tra 150 publication records, 246 missing links thuộc baseline, 0 missing links mới.
- PASS: 52 Python tests; node --check site.js; animation/pagination JS tests; git diff --check.
- PASS: đối chiếu cả 21 featured IDs trong HTML EN/VI với nguồn JSON, đủ tiêu đề, năm, venue và nguồn tác giả nguyên văn (authors hoặc homepage_reference/citation).
- PASS: Firefox headless qua WebDriver BiDi, cache bypass; ảnh team0 và WSI tải thành công trong cả tám trường hợp.
- PASS: Enter mở menu, Escape đóng và trả focus; pager chuyển sang trang 2 và giữ focus; gallery trước/sau đổi ảnh; EN/VI dẫn đến trang tương ứng.
- PASS: click-through Home/header links tới `/vi/research/`, `/vi/team/`, `/vi/papers/`, `/vi/datasets/`, `/vi/tutorials/`, `/vi/conferences/`, `/vi/contact/`, EN Home, và bốn Research anchors. Đã mở trực tiếp cả ba destinations chính ở EN/VI.
- PASS: không có runtime JavaScript error trong context kiểm thử. Có một yêu cầu font bị hủy khi harness chuyển trang nhanh (Firefox status 2152398850); không phải missing asset. Lỗi của context chrome nội bộ Firefox không được tính là lỗi website.

| Language | Viewport width | Horizontal overflow | Hero height | Header height |
|---|---:|---|---:|---:|
| EN | 375 | Không | 687 | 84 |
| VI | 375 | Không | 689 | 84 |
| EN | 768 | Không | 481 | 84 |
| VI | 768 | Không | 454 | 84 |
| EN | 1024 | Không | 430 | 84 |
| VI | 1024 | Không | 401 | 84 |
| EN | 1440 | Không | 476 | 88 |
| VI | 1440 | Không | 476 | 88 |

Viewport height 1000px, devicePixelRatio 1. Ảnh chụp tạm: `/tmp/uit-en-{375,768,1024,1440}.png`, tương tự `uit-vi-*`. Đã xem trực tiếp ảnh desktop/tablet/mobile; ảnh này là output kiểm thử, không phải asset website.

## Anti-Slop Delivery Gate

Các PASS dưới đây chỉ áp dụng phạm vi thay đổi. Các tiêu chí không có component tương ứng ghi rõ không áp dụng.

### Hard Gate

- R-02 PASS: copy UI mới không có em dash; dấu trong citation lịch sử giữ nguyên vì là nội dung nghiên cứu được bảo toàn.
- R-03 PASS: đo scrollWidth so với innerWidth cho cả tám viewport, không tràn; hero một cột mobile, hai cột tablet/desktop.
- R-17 PASS: thống kê vẫn dùng group_stats từ build, không thêm số hay dấu cộng.
- R-18 PASS: không thêm testimonial hoặc người giả; dùng ảnh nhóm có sẵn.
- R-23 PASS: team0 và WSI đã mở xem, kiểm tra dimensions, sử dụng theo yêu cầu; không tạo asset mới.
- R-24 PASS: check_site không có missing link mới và click-through destinations/anchors mới đã qua.
- R-25 PASS: đo computed foreground/background của text hiển thị trong header, hero, publications, research; 12 cặp màu đều từ 5.67:1 đến 11.67:1. Caption ảnh dùng nền navy đặc, không đặt chữ trực tiếp lên ảnh.
- R-26 PASS: menu, EN/VI, pager, gallery và links có hành vi thực tế; không thêm form hoặc nút placeholder.
- R-27 PASS: featured directory là HTML build sẵn, có empty state trong for/else; không thêm fetch hoặc loading/error state giả cho nội dung tĩnh.
- R-28 PASS: không thêm FAQ.
- R-32 PASS: kiểm thử menu bằng Enter/Escape và focus return; focus primary CTA có computed outline 3px solid, caption navy có outline trắng; pager giữ focus.
- R-33 PASS: chỉnh source bằng apply_patch, không inject script/CSS vào output để dựng UI.
- R-34 PASS: không thêm theme toggle; giữ light theme theo direction được chọn.
- R-35 PASS: build, Firefox screenshots, viewport measurements, tương tác và click-through ghi ở trên.
- R-36 PASS: không tạo claim thành tích, accuracy, security hoặc performance; nguồn nội dung lấy từ research partial và JSON hiện có.
- R-37 PASS: direction người quản lý đã chọn và Design Read được ghi trước triển khai; ENERGY 3/5, RHYTHM 3/5, MOTION 1/5.
- R-38 PASS: kiểm tra đủ 21 bài và nguồn tác giả; không thay đổi data files trong lần redesign này.

### Purpose-Gate

- R-01 PASS: nền xanh nhạt phân tách hero/research; khung navy gắn ảnh với nhận diện; hero không gradient/glow/wave/orb.
- R-04 PASS: không thêm icon; logo thật phục vụ nhận diện; hình khoa học thay minh họa portfolio ở phần Research.
- R-06 PASS: system sans hỗ trợ EN/VI; heading mạnh và metadata 14–15px phục vụ đọc citation; caption header VI đã đo 12px.
- R-07 PASS: không dùng background grid/dots/blueprint.
- R-08 PASS: CTA hero không có arrow; các glyph liên kết cũ ngoài phạm vi đầu trang giữ nguyên.
- R-09 PASS: không dùng pill eyebrow hoặc status dot trong hero mới.
- R-10 PASS: không thêm glassmorphism.
- R-12 PASS: không thêm shadow vào các thành phần mới; ảnh dùng khung navy thay elevation giả.
- R-13 PASS: không dùng glow.
- R-14 PASS: publications là danh sách, research là text và figure, không grid card lặp lại.
- R-19 PASS: Home bị loại khỏi reveal targets; gallery chỉ chuyển khi nhấn trước/sau, không tự chạy; không đổi motion trang khác.
- R-22 PASS: ảnh buổi làm việc và WSI trực tiếp liên quan đến nội dung; không thêm stock/AI illustration.

### Liveliness

- Dials PASS: 3/5, 3/5, 1/5 theo brief; mapping sang toolkit ba mức ghi trong design system.
- Composition PASS: screenshot cho thấy hero bất đối xứng có ảnh thật, publication list hai vùng, research panel có figure; nhịp không lặp card.
- Focal point PASS: heading UIT Together dẫn hero, ảnh nhóm tạo visual anchor; công bố ở section tiếp theo có typography riêng.
- Whitespace PASS: section spacing theo clamp; hero không fixed height và giữ nội dung đầu trang trong tầm nhìn desktop.
- Accent PASS: blue dùng cho lĩnh vực/liên kết, navy cho nhận diện và primary CTA; không thêm cyan trang trí.
- Identity PASS: logo thật, ảnh team0, nội dung paper và hình nghiên cứu của repository làm bản sắc.
- Design Read PASS: ghi trong design-system.md và thông báo trước triển khai.

### Craftsmanship và Quality Locks

- C-1 / R-31 PASS: lý do màu, font, khung ảnh, spacing, composition và motion ghi từng mục trong design-system.md.
- C-2 PASS: các tương tác mới/giữ lại đã kiểm thử; không thêm controls giả.
- C-3 / R-05 PASS: Home theo luồng publications → research → thống kê → hoạt động/tài nguyên/tin; dữ liệu quyết định section.
- C-4 PASS: kiểm thử EN/VI và tám viewport, menu keyboard, focus pager; nội dung publication được render sẵn và đọc được khi không chạy JS.
- C-5 PASS: không thay nguồn dữ liệu hoặc tạo claim mới; thống kê vẫn được tính từ dữ liệu.
- R-11 PASS: buttons radius 6px, hình một góc 20px, directory phẳng; không tất cả pill.
- R-15 PASS: primary Publications, secondary Research directions, Members trong caption, Read paper và All publications chỉ rõ thao tác.
- R-16 PASS: copy mới không buzzwords marketing; nội dung nói rõ các bài toán nghiên cứu có trong source.
- R-20 PASS: ảnh buổi làm việc, paper titles/authors và WSI làm nhận diện riêng, không chỉ thay tên/logo trên template.
- R-21 PASS: light theme theo direction học thuật được chọn; không tự thêm dark theme.
- R-29 PASS: navy/blue và neutral/light blue; không thêm core color; màu trong ảnh khoa học không phải palette UI.
- R-30 PASS: composition dựa nội dung UIT Together, không sao chép stylesheet/asset của sản phẩm khác.

## Cần nghiệm thu bổ sung

Screen reader, zoom 200%, bàn phím ảo/touch trên thiết bị thật và các browser ngoài Firefox chưa được kiểm tra. Link ngoài chưa được truy cập để xác minh hoạt động. Các missing links lịch sử vẫn là baseline cần xử lý riêng; PASS phạm vi này không chứng nhận toàn website.
