# Home ba section: báo cáo triển khai và Delivery Gate

Ngày: 2026-10-12. Anti-Slop during, theo session override. Direction: Premium Academic Editorial, ENERGY 3/5, RHYTHM 3/5, MOTION 1/5.

## Kết quả

Home chỉ gồm About UIT Together → Latest News → Research Highlights. Giữ hero ảnh team0 thật; bỏ statistics, research directory chi tiết, gallery, quick links và feed phân trang khỏi Home. Không xóa dữ liệu hoặc assets của các phần này. About nằm trong main để skip link không bỏ qua phần giới thiệu.

News lấy từ news.json, sắp xếp theo date ISO giảm dần, chỉ dùng record verified có nguồn ngày và source_url HTTPS; Home tối đa ba tin, News directory dùng toàn bộ năm tin đã xác minh. Bằng chứng ngày đăng: [thông báo gốc của UIT-Together](https://uit-together.github.io/). Tin gần nhất là 2022-06-15; giao diện ghi rõ ngày gốc, không giả vờ là cập nhật năm 2026.

Link gốc UIT-VinaFruit20 trỏ nhầm UIT-DODV, được giữ trong JSON để đối chiếu; UI dẫn tới News anchor và nguồn thông báo của nhóm. Một số link GitHub gốc không tải được khi kiểm tra nguồn. Không tự sửa các URL nghiên cứu này.

Danh sách `/news/` trước đây dùng nội dung Niemeyer/NRG. Nay danh sách dùng dữ liệu UIT; src/partials/news-content.html cũ còn nguyên nhưng không được include. Các URL bài tin lịch sử vẫn render EN/VI; đây không phải xác nhận chúng thuộc nhóm UIT.

## Files thay đổi trong lần này

| File | Thay đổi |
|---|---|
| scripts/home_content.py | Mới: kiểm tra date/provenance, chọn và sắp xếp news, đọc IDs highlights |
| scripts/build.py | Đưa context Home vào pipeline hiện có |
| src/data/news.json | Thêm ngày ISO, nguồn ngày, trạng thái kiểm duyệt và copy EN/VI; giữ trường gốc |
| src/data/selected_achievements.json | Mới: ba publication IDs theo thứ tự hiển thị |
| src/data/site.json | Thêm News; nhóm ba destination dưới Resources |
| src/layouts/base.html | About hero trong main, phụ đề Research Group, hai câu giới thiệu, About/Research links |
| src/partials/home-content.html | Home chỉ còn News và Highlights dưới About hero |
| src/partials/news-directory.html | Mới: News list từ JSON, anchor ổn định theo ID |
| src/partials/news-note.html | Mới: ghi chú ngày gốc khi kho tin đã cũ |
| src/pages/news/index.html | Dùng directory mới; giữ URL |
| src/partials/header.html | Resources bằng native details, giữ EN/VI |
| src/assets/css/header-home.css | News hierarchy, bỏ styles Home đã nghỉ, footer text reflow, no-JS navigation |
| src/assets/js/site.js | Escape/focus/outside click cho Resources, đóng nhóm khi chuyển trang |
| tests/test_home_content.py | Mới: ngày sai, nguồn thiếu, tin mới, giới hạn ba tin, chọn papers, bảo toàn tác giả/URLs |
| tests/test_group_statistics.py | Đổi kỳ vọng UI: không còn statistics trên Home; giữ tests tính số liệu |
| docs/architecture.md | Luồng build và bảo toàn news lịch sử |
| docs/content-guide.md | Cách thêm tin và chọn highlights không sửa HTML |
| docs/design-system.md | Ghi nhận composition ba section và lý do thiết kế |
| docs/site-check-report.json | Report sinh lại bởi check_site |
| docs/home-structure-review.md | Báo cáo này |

Các thay đổi đã có ở AGENTS.md, .agents/, conferences.json và portfolio.css không bị ghi đè trong lần này. publications.json, members.json, venues.json, featured_publications.json, group_gallery.json và pages.json không thay đổi. dist chỉ được sinh qua build.

## Kiểm tra

Runtime duy nhất: `/home/uit2023/LuuTru/Vutm/.conda-envs/UITweb/bin/python`. Không sửa môi trường Python/Codex khác.

- PASS: build 292 trang; 59 Python tests; node --check site.js; publication_filters, pagination và animations JS tests; git diff --check.
- PASS: build/check_site với base path rỗng và `/UIT-Together`; 150 publication records, 208 missing links baseline, 0 missing links mới. Đã tạo lại build local sau kiểm tra project path.
- PASS: thêm record mới hợp lệ trong test fixture tự đưa tin lên đầu Home và giới hạn ba tin; không ghi tin test vào dữ liệu website.
- PASS: ngày sai/thiếu, thiếu provenance, ID trùng, paper ID sai và chọn cùng paper qua hai ID đều bị từ chối; không tự bổ sung ngày hoặc metadata.
- PASS: Firefox headless/WebDriver BiDi, cache bypass, EN/VI tại 375/768/1024/1440px: đúng ba section, ba tin, ba papers, ảnh tải thành công, không tràn ngang.
- PASS: Menu và Resources bằng Enter/Escape, focus return; news anchors dẫn đúng record; click-through mọi destination nội bộ có trên Home/footer ở EN/VI.
- PASS: các trang About, Research, Members, Papers, Datasets, Tutorials, Conferences, Contact và News mở được; hai URL tenure-emily lịch sử còn tồn tại ở EN/VI.
- PASS: tăng root font lên 200% tại 375px không tràn ở EN/VI; đã sửa footer min-width/wrapping. Đây là kiểm tra resize chữ trong DOM, không phải chứng nhận mọi kiểu browser zoom.
- PASS: fallback CSS khi không có class js giữ nav links và ba highlights hiển thị, ẩn Menu không có handler; native Resources vẫn là HTML details.
- PASS: không có runtime JavaScript errors trong context kiểm thử cuối.
- PASS: đo computed text colors trong header/About/News/Highlights, 10 cặp đều từ 5.87:1 tới 11.67:1; focus 3px trên About CTA, View all news và Resources summary.

| Language | Width | Hero height | Header height | Overflow |
|---|---:|---:|---:|---|
| EN | 375 | 653 | 84 | Không |
| VI | 375 | 677 | 84 | Không |
| EN/VI | 768 | 479 | 84 | Không |
| EN/VI | 1024 | 458 | 84 | Không |
| EN/VI | 1440 | 500 | 88 | Không |

Viewport height 1000px, DPR 1. Ảnh toàn trang tạm: `/tmp/uit-short-en-{375,768,1024,1440}.png` và tương tự `uit-short-vi-*`. Đã xem trực tiếp desktop và mobile; không đưa ảnh kiểm thử thành asset public.

## Delivery Gate: PASS trong phạm vi thay đổi và kiểm tra ghi trên

### Hard Gate

- R-02 PASS: copy mới không em dash; giữ nguyên tên paper có dấu en dash như định danh nghiên cứu.
- R-03 PASS: tám viewport EN/VI không tràn; resize chữ 200% không tràn sau sửa footer.
- R-17 PASS: không hiển thị statistics hoặc thêm số liệu thành tích; số dataset trong news có nguồn thông báo gốc.
- R-18 PASS: không thêm người/testimonial giả.
- R-23 PASS: dùng logo/team0 đã có; không tạo asset mới.
- R-24 PASS: routes/anchors đã check và click-through, 0 missing link mới.
- R-25 PASS: text foreground/background đo trong browser đều vượt 4.5:1; chữ caption trên nền navy đặc.
- R-26 PASS: Menu, Resources, EN/VI và links có hành vi thật; no-JS fallback không để Menu vô tác dụng hiển thị.
- R-27 PASS: News có for/else empty state; nội dung render sẵn, không có fetch/loading giả. Build validation từ chối dữ liệu không hợp lệ trước khi thay artifact.
- R-28 PASS: không thêm FAQ.
- R-32 PASS: Enter/Escape/focus return, focus ring và main skip target đã kiểm tra; About nằm trong main.
- R-33 PASS: chỉnh source bằng apply_patch; không inject code vào output để tạo UI.
- R-34 PASS: giữ light theme được chọn; không thêm toggle thiếu trạng thái.
- R-35 PASS: build, browser screenshots, tương tác và click-through đã thực hiện; links mailto/DOI bên ngoài giữ từ nguồn hiện có, không gửi email hoặc thay metadata.
- R-36 PASS: không thêm claim ranking, thành tích hoặc accuracy; nguồn tin/ngày ghi rõ.
- R-37 PASS: direction của người quản lý, Design Read và dials ghi trước triển khai.
- R-38 PASS: chỉ render news verified và publication IDs có thật; fixture test không đi vào website.

### Purpose-Gate

- R-01 PASS: nền sáng và đường navy ở tin mới nhất phục vụ phân cấp ngày; không wave/orb/glow.
- R-04 PASS: không thêm icon trang trí; marker Resources là điều khiển expand native.
- R-06 PASS: system sans hỗ trợ EN/VI, typography tách title/metadata; không monospace hoặc uppercase tracking mới.
- R-07 PASS: không background grid/dot/blueprint.
- R-08 PASS: CTA mới không arrow trang trí; native marker chỉ trạng thái disclosure.
- R-09 PASS: không pill badge hoặc fake New status.
- R-10 PASS: không glassmorphism.
- R-12 PASS: shadow chỉ ở Resources dropdown nổi trên nội dung; news và papers phẳng theo hierarchy.
- R-13 PASS: không glow.
- R-14 PASS: một news lead và hai rows, publication list; không card grid lặp.
- R-19 PASS: Home không reveal, slideshow, countdown hoặc auto-motion; các trang khác giữ hành vi cũ.
- R-22 PASS: ảnh nhóm thật, không stock/AI illustration.

### Liveliness

- Dials PASS: ENERGY/RHYTHM/MOTION 3/5, 3/5, 1/5 theo brief và design system.
- Composition PASS: hero ảnh bất đối xứng, news lead/rows, highlights editorial list; ba nhịp khác nhau.
- Focal point PASS: tên nhóm và ảnh thật dẫn About; headline news dẫn phần cập nhật.
- Whitespace PASS: section padding theo clamp; bỏ double bottom padding, không fixed-height hero.
- Accent PASS: blue cho lĩnh vực/link, navy cho nhận diện/primary action; cyan chỉ trong logo thật.
- Identity PASS: logo, ảnh làm việc và nội dung dataset/paper của UIT là dấu hiệu riêng.
- Design Read PASS: ghi nhận hướng Premium Academic Editorial trước triển khai.

### Craftsmanship và Quality Locks

- C-1 / R-31 PASS: lý do layout, màu, typography, news hierarchy, dropdown shadow và motion ghi trong design-system.md.
- C-2 PASS: controls thực tế, không placeholder actions.
- C-3 / R-05 PASS: đúng ba section do người quản lý chọn; không miniature directory/template feature grid.
- C-4 PASS: EN/VI, tám viewport, keyboard, resize chữ và fallback styles đã kiểm tra.
- C-5 PASS: ngày gốc/metadata thật, không claim Q1 chưa chứng minh.
- R-11 PASS: button radius 6px, ảnh có góc riêng, lists phẳng; không tất cả pill.
- R-15 PASS: About the group, Research, Members, View all news/publications là thao tác cụ thể được yêu cầu.
- R-16 PASS: copy mới nói nội dung nhóm, không buzzwords marketing.
- R-20 PASS: ảnh nhóm và dữ liệu UIT tạo bản sắc, không dựa vào tên/logo thay thế trên template.
- R-21 PASS: light theme theo direction; không ép dark hoặc thêm toggle không hoàn chỉnh.
- R-29 PASS: navy/blue/neutral, không thêm core colors.
- R-30 PASS: composition theo brief/nội dung UIT; không sao chép sản phẩm khác.

## Q1 và nghiệm thu thủ công

Ba selected journals: Pattern Recognition Letters (paper 2023), IJDAR (paper 2023), Journal of Imaging (paper 2022). Không có evidence quartile đủ hệ thống xếp hạng, năm, category và nguồn trong metadata được dùng. Nhãn Q1 ở homepage_reference lịch sử không được coi là bằng chứng; không hiển thị Q1, Q2 hoặc impact factor trên Home.

Cần kiểm tra thực tế trên Chrome/Safari, touch/bàn phím ảo, screen reader và browser zoom. Cần nguồn quartile theo năm nếu muốn bổ sung ranking sau này. Các URL news legacy và link dataset gốc cần người quản lý kiểm duyệt riêng. PASS này không chứng nhận mọi link lịch sử hoặc toàn website đạt WCAG.

Cập nhật tương lai: thêm record có ngày/nguồn đã xác minh và bản EN/VI vào news.json; chọn 2–3 paper IDs trong selected_achievements.json; chạy build/check_site bằng môi trường Vutm. Không cần sửa Home HTML.
