# UIT Together: nghiệm thu UI toàn site, 2026-10-12

Anti-Slop active: during (session override). Direction: Premium Academic Editorial, ENERGY 3/5, RHYTHM 3/5, MOTION 1/5; tương ứng toolkit 2/3, 2/3, 1/3. Design Read trước sửa: giữ Home đã duyệt, bổ sung thống kê có nguồn, giảm điều hướng trùng và dùng cùng hệ thống cho các trang đọc sâu.

## Phạm vi và bảo toàn

Home giữ hero/copy/ảnh team0, ba tin và ba highlights đã duyệt. Thứ tự hiện hành: Hero → Statistics → Latest News → Research Highlights → footer. Số liệu được đọc từ `group_stats`, không ghi số cố định vào template. News vẫn kiểm tra ngày ISO/provenance và sắp xếp lúc build. Không sửa dữ liệu thành viên, papers/authors/DOI/venue, news hoặc conferences trong phiên này; không bổ sung nhãn Q1. Không tạo asset, cài package, đổi framework hoặc deploy. `dist/` chỉ được tạo bằng build.

Git status đã có thay đổi từ trước, gồm AGENTS, conferences.json, site.js, các tài liệu và phần Home/data-driven News. Những thay đổi này được bảo toàn; danh sách bên dưới chỉ mô tả phần thực hiện trong phiên này.

## File chỉnh trong phiên

| File | Thay đổi |
|---|---|
| `src/partials/home-content.html` | Statistics từ group_stats; bỏ View all news |
| `src/partials/header.html` | Không hiển thị News/Tutorials; giữ các destination khác |
| `src/partials/footer.html` | Footer academic không navigation, email verified từ contacts, phòng A108 từ About/Contact |
| `scripts/home_content.py` | Copyright year theo ngày build, không đổi news selection |
| `src/layouts/base.html` | Một stylesheet chung, page title/copy EN/VI, bỏ hộp icon placeholder |
| `src/assets/css/site.css` | Tokens, shared components, styles Home/header/footer được hợp nhất; page headers, publication list, research, datasets, tutorials và responsive/focus |
| `src/assets/css/members.css` | Tokens/radii/focus/nav reflow, giữ grouping/search/motion riêng |
| `src/assets/css/conferences.css` | Tokens/radii/contrast/cỡ chữ, wrap spotlight và typography countdown; giữ clock/filter/update |
| `src/assets/css/header-home.css` | Giai đoạn 1 thêm stats/footer; sau giai đoạn 2 file này không còn tải, style hiện hành ở site.css |
| `src/partials/datasets-content.html` | Wrapper dataset-list, bỏ container lồng thừa; không đổi headings h4 dùng để đếm datasets |
| `src/partials/publication.html` | Hiện authors nguyên văn nếu có, nhãn năm thiếu rõ ràng |
| `src/partials/research-content.html` | Native video controls, giữ sources/autoplay/reduced-motion logic |
| `src/pages/tutorials/index.html` | Giữ tên mục chưa có URL, thay link # bằng nhãn Link pending EN/VI |
| `tests/test_home_content.py`, `tests/test_group_statistics.py` | Kiểm tra Home bốn sections và số liệu từ build context |
| `tests/test_members.py` | Cấp copyright year cho StrictUndefined render fixture |
| `docs/design-system.md`, `docs/architecture.md`, `docs/content-guide.md` | Direction, composition, CSS ownership và hướng dẫn hiện hành; bảo toàn lịch sử có giá trị |
| `docs/site-check-report.json` | Báo cáo tự sinh bởi check_site |
| `docs/sitewide-ui-review.md` | Báo cáo này |

## Kiểm tra theo giai đoạn

1. Statistics/header/footer: build 292 trang, check_site không có lỗi mới, 59 test Python đạt. Đã sửa fixture render Members thiếu copyright year trước khi chuyển giai đoạn.
2. Hợp nhất CSS: bỏ tải portfolio.css/header-home.css; build, check_site và 59 test đạt trước khi đồng bộ layouts riêng.
3. Đồng bộ pages: build, Python tests và sáu suites JS đạt. Bỏ fade chung khi tải page header, giữ motion đặc thù Members và clock. Native controls cho video; không thay logic dữ liệu.
4. Firefox headless/WebDriver BiDi: kiểm tra thực tế EN/VI, responsive, chức năng và focus. Các lỗi phát hiện khi tăng cỡ chữ hoặc Bootstrap ghi đè focus đã sửa và kiểm tra lại.

Runtime: `/home/uit2023/LuuTru/Vutm/.conda-envs/UITweb/bin/python`. Server preview chỉ phục vụ dist tại localhost; không dùng dev updater và không chỉnh dữ liệu hội nghị.

## Kết quả validation

| Kiểm tra | Kết quả |
|---|---|
| `scripts/build.py` | PASS: 292 trang EN/VI |
| `scripts/check_site.py` | PASS: 150 publication records; 208 missing links trong baseline cũ, 0 mới |
| `python -m unittest discover -s tests` | PASS: 59 tests |
| `node --check src/assets/js/site.js` | PASS |
| animations, pagination, publication_filters, members_motion, conference_clock, conferences_ui JS suites | PASS: cả sáu suites |
| `git diff --check` | PASS |
| Firefox: 9 trang × EN/VI × 375/768/1024/1440 | PASS: 72 trường hợp, 0 document overflow, 0 cặp chữ thiếu tương phản, 0 ảnh bị lỗi trong mẫu |
| 200% root font ở 375px | PASS: cả chín trang EN/VI; đây là tăng cỡ chữ, không phải browser zoom |

Chín trang: Home, Research, Members, Publications, Datasets, Conferences, Contact, News, Tutorials. Đã xem screenshot trực tiếp ở mobile/desktop và bản Home đầy đủ: ảnh nhóm/caption, nhịp sections, danh sách công bố, footer, dataset figures, news rows và trang đọc hướng dẫn.

Artifacts kiểm tra cục bộ: `/tmp/uit-sitewide-matrix.json` (72 cases), `/tmp/uit-sitewide-functions.json` (45 records), `/tmp/uit-final-*.png`, `/tmp/uit-sitewide-home-*-full.png`. Scripts BiDi dùng stdlib trong environment UITweb, không cài dependencies. Đã sửa lỗi đọc WebSocket frame trong công cụ kiểm thử; không tính các lần chạy công cụ lỗi là bằng chứng PASS.

Contrast checker của antislop-human: white/blue 6.38:1; muted/light-blue 5.87:1; footer muted/navy 13.42:1. Browser kiểm tra các cặp màu chữ đang render, áp dụng ngưỡng 4.5 cho chữ thường và 3 cho chữ lớn. Không tuyên bố website đã được chứng nhận WCAG toàn diện.

## Click-through và trạng thái chức năng

| Thành phần | Bằng chứng thực tế |
|---|---|
| Mobile Menu | Enter mở; Escape đóng và trả focus; EN/VI tại cả bốn widths |
| Resources | Enter mở native details; Escape đóng/trả focus; không tràn khi mở |
| Header/Home links | Click brand/Home, Research, Members, Papers, Contact, Datasets, Conferences, EN/VI, About và ba news anchors: đến đúng pathname/hash |
| Latest News | Ba mục Home, năm mục trang News, ngày gốc, source HTTPS; không có View all news; historical note giữ nguyên |
| Publications | 10 bài/trang, Next, type/year filter, search không kết quả, reset, mở Full citation; authors giữ nguyên |
| Members | Search Khang, không kết quả, cohort K2021, reset, anchor Current Members; order/grouping được tests kiểm tra |
| Datasets | Ba mục/trang, Next, trang cuối một mục |
| Conferences | Vietnam clock/counters, search CVPR, empty, status pending/TBA, topic medical và Next; update/offline/rollover có JS/Python tests |
| Research | Direction anchor; video có native controls và pause thực tế; source media giữ nguyên |
| Contact/footer | Hai contact email, không form giả; footer lấy primary verified email và không navigation |
| Tutorials | Trang index và bốn local detail pages EN/VI truy cập được; không tràn ở 375px; mục URL thiếu có nhãn rõ |
| Keyboard focus | Outline 3px trên skip link, Menu, hero CTA, footer email, input/reset, citation summary, pager, subpage region, member chapter và conference controls |
| No-JS fallback | Bỏ class js: navigation vẫn hiển thị; Home/news/highlights/statistics render sẵn. Đây là kiểm tra fallback CSS, không giả nhận là đã tắt JS browser hoàn toàn |

Các link DOI/paper/nguồn bên ngoài giữ nguyên dữ liệu đã có; kiểm tra href và scheme, không xác nhận uptime của mọi website ngoài hoặc thử gửi email.

## Anti-Slop Delivery Gate

Kết quả trong phạm vi UI và controls của phiên này: PASS sau sửa và kiểm tra lại. Không dùng kết quả này để chứng nhận mọi nội dung/208 link legacy của 292 trang lịch sử.

### Hard Gate

| Rule | Status và bằng chứng |
|---|---|
| R-02 | PASS: copy/UI mới không có em dash; placeholder năm dùng nhãn rõ |
| R-03 | PASS: 72 browser cases và 18 cases cỡ chữ 200% không tràn; native code/table cuộn trong vùng riêng |
| R-17 | PASS: bốn metrics từ group_statistics, test so số render với giá trị tính; không fake numbers |
| R-18 | PASS: không testimonials mới hoặc người giả |
| R-23 | PASS: không tạo asset; dùng logo/team0/ảnh nghiên cứu có sẵn và cấu trúc nav người quản lý yêu cầu |
| R-24 | PASS: toàn bộ header destinations và Home internal links đã click tới đúng route; News/Tutorials vẫn truy cập trực tiếp |
| R-25 | PASS: computed contrast 72 cases và contrast checker; có focus riêng trên dark footer |
| R-26 | PASS: Menu/details/filters/pagers/citation/video có behavior thật; tutorial URL thiếu có nhãn rõ |
| R-27 | PASS: search empty/reset, conference TBA/offline/pending, Home news empty fallback được source/tests kiểm tra |
| R-28 | PASS: không thêm FAQ |
| R-32 | PASS: Enter/Escape/focus return, outline 3px cho control/summary/region; sửa Bootstrap focus override |
| R-33 | PASS: source Jinja/CSS là implementation; không dùng runtime/post-build patch để dựng feature |
| R-34 | PASS: chỉ light theme theo direction, không theme toggle giả; dark footer có contrast riêng |
| R-35 | PASS: build/check_site/tests và click-through ở bảng trên; giới hạn external links/mail client được ghi rõ |
| R-36 | PASS: không thêm claim security/compliance/performance hoặc thành tích |
| R-37 | PASS: direction đã được người quản lý duyệt, Design Read/dials ghi trước sửa và trong design-system |
| R-38 | PASS: không thêm research facts, người, tin hoặc nhãn Q1 chưa xác minh |

### Purpose-Gate

| Rule | Status và mục đích |
|---|---|
| R-01 | PASS: không brand gradient/glow mới; gradient nửa ô countdown biểu thị hai mặt lịch lật |
| R-04 | PASS: statistics icons phân biệt participant/papers/venues/datasets; research icons gắn loại nội dung |
| R-06 | PASS: system sans đọc EN/VI không tải font; metadata không wide-tracking uppercase; monospace chỉ code |
| R-07 | PASS: không background grid/dot pattern |
| R-08 | PASS: không thêm mũi tên cho mọi CTA; back-to-top và external indicators có nghĩa điều hướng |
| R-09 | PASS: page header bỏ capsule/dot; conference/member labels biểu thị trạng thái và role thực |
| R-10 | PASS: không glassmorphism |
| R-12 | PASS: cards/footer/filter không shadow; dropdown overlay và ô flip có độ nổi phục vụ chức năng |
| R-13 | PASS: không glow |
| R-14 | PASS: research text/media, venue/publication rows, member profiles, dataset rows, news editorial và clock layouts khác nhau theo nội dung |
| R-19 | PASS: shared header/content hiện ngay; giữ clock/member motions hiện có và reduced-motion; video có pause/control |
| R-22 | PASS: ảnh thật và figures thật, không illustration generic/stock/AI |

### Liveliness

| Item | Status và bằng chứng |
|---|---|
| Dials explicit | PASS: 3/5, 3/5, 1/5; không thêm motion trang trí |
| Dials consistent | PASS: Home balanced density; photo/statistics/news/highlights có nhịp khác nhau |
| Focal point | PASS: wordmark/ảnh nhóm trên Home, page title và nội dung chuyên biệt trên các trang |
| Structural whitespace | PASS: section-space, separator, typography và gutters phân nhóm nội dung |
| Deliberate accent | PASS: blue dùng links/statistics; navy dùng heading/photo frame/footer |
| Identity motif | PASS: navy typographic hierarchy, khung ảnh thật, divider mảnh và nguồn học thuật |
| Design Read | PASS: giữ Home approved, bổ sung có mục đích, đồng bộ trang đọc sâu |

### Craftsmanship và Quality Locks

| Item | Status và bằng chứng |
|---|---|
| C-1 / R-31 | PASS: design-system ghi mục đích màu, khoảng cách, media, stat, hierarchy, radius, elevation và motion |
| C-2 | PASS: controls trong bảng click-through hoạt động, mục thiếu link được ghi rõ |
| C-3 | PASS: Home chỉ có bốn sections được yêu cầu, không nhồi thêm directory/activities/tutorial feed |
| C-4 | PASS: responsive, text scaling, keyboard, empty/filter/pager states và reduced-motion tests |
| C-5 | PASS: dữ liệu thật; không thêm thành tích/quartile |
| R-05 | PASS: photo hero, blue metrics, asymmetric news và editorial highlights; không uniform card template |
| R-11 | PASS: radius 8px phổ biến, nav 4px và khung ảnh bất đối xứng; không pill toàn site |
| R-15 | PASS: About/Research/Members/Publications gọi tên destination; subpage copy cụ thể, bỏ Explore/Get in touch mới |
| R-16 | PASS: không thêm marketing buzzwords |
| R-20 | PASS: nhận diện từ team0, ảnh nghiên cứu, UIT palette và nội dung thật của nhóm |
| R-21 | PASS: light theme giữ nguyên; navy footer là vùng kết thúc có mục đích |
| R-29 | PASS: navy/blue, trắng/light tint; cyan chỉ trong logo có sẵn; màu TBA semantic giữ nguyên |
| R-30 | PASS: không asset/copy/framework của website khác |

## Giới hạn và kiểm tra thủ công

- 208 missing links là baseline lịch sử, không có lỗi mới; chưa sửa hoặc xóa dữ liệu để làm report sạch. Build/check không xác nhận toàn bộ outbound URLs.
- Cần nghiệm thu Chrome/Safari, thiết bị cảm ứng thực, screen reader và browser zoom 200%. Headless/text scaling không thay thế các kiểm tra này.
- Cần kiểm tra việc mở mail client, nguồn DOI/website hội nghị/News/HackMD ngoài mạng local; không thử gửi email.
- Hội nghị vẫn giữ seed/updater/fetch 5 phút. Parser, clock, UI offline/update có tests; phiên này không chạy cập nhật production hoặc thực hiện request cập nhật thay dữ liệu.
- Không xác minh thêm Q1; highlights tiếp tục selected publications, không có badge quartile.
- Public deployment tiếp tục hoãn.
