# UIT-Together design system

Academic modern, light theme, navy/blue accent, native CSS + Bootstrap hiện có. DESIGN_VARIANCE 4, MOTION_INTENSITY 2, VISUAL_DENSITY 4. Áp dụng taste-skill và ui-ux-pro-max theo nhu cầu website nghiên cứu, không chuyển framework vì ví dụ của skill.

Tokens ba lớp primitive/semantic/component nằm ở src/assets/css/site.css. Font sans hệ thống hỗ trợ tiếng Việt, tránh yêu cầu tải font ngoài. Giữ logo thật, grid rõ; gradient và trang trí chỉ dùng khi có mục đích identity, hierarchy hoặc usability được ghi nhận. Header dùng link text, menu mobile có ARIA/Escape; footer không cố định che nội dung.

Paper/member và danh sách dùng spacing thống nhất; tìm kiếm bỏ dấu tiếng Việt, trạng thái không kết quả và clear filters. Nội dung vẫn có khi tắt JS. Bảng và code tutorial cuộn trong phạm vi riêng; ảnh responsive. Gallery Team hiển thị tĩnh thay carousel phụ thuộc jQuery.

Focus rõ, reduced-motion, mobile styles có trong CSS. Chưa có nghiệm thu visual tự động: Firefox headless crash do môi trường; cần kiểm tra local ở 375/768/1024/1440 px và keyboard trước public. Icon decoration FontAwesome cũ chưa được tải; navigation không phụ thuộc icon.

## Tham chiếu CORE Lab — cập nhật 2026-10-10

Đã đọc các HTML local trong core-lab-source, đặc biệt trang chủ. Đây là HTML xuất từ Next.js; CSS chunks được tham chiếu nhưng không có trong thư mục, nên không tuyên bố đã sao chép stylesheet hoặc xem đầy đủ bản render. Thiết kế UIT-Together tham khảo header compact, hero hai cột, typography phân cấp và các nhóm nội dung rõ.

Palette mới: navy #10386b, blue #145ac4, nền #f6f9ff, chữ #233e61. Font system sans hỗ trợ tiếng Việt. Hero dùng ảnh nhóm team0 có sẵn, không dùng artwork/asset của CORE. Footer navy, thẻ nội dung trắng, vùng cuộn giữ nguyên và có keyboard focus. Mobile hero thành một cột. Không thêm dependency hoặc chuyển Next.js.

## Home và header: Premium Academic Editorial, 2026-10-12

Direction do người quản lý chọn: Modern Academic Research Lab / Premium Academic Editorial; academic, intelligent, modern, credible, visually engaging. ENERGY 3/5, RHYTHM 3/5, MOTION 1/5. Quy đổi toolkit ba mức: ENERGY 2/3, RHYTHM 2/3, MOTION 1/3. Các dials này thay thế thiết lập Home trước đây; không đổi hành vi các trang khác.

Design Read: website nhóm nghiên cứu cho nhà nghiên cứu, sinh viên và đối tác; bố cục editorial bất đối xứng, nhịp nội dung cân bằng và chuyển động tối thiểu.

- Navy giữ nhận diện học thuật và khung ảnh; blue phân biệt liên kết và lĩnh vực nghiên cứu. Nền xanh rất nhạt phân tách hero với publication directory; cyan chỉ có trong logo thật.
- System sans hỗ trợ tiếng Việt và không cần tải font; heading lớn tạo thứ bậc, metadata 14–15px giữ khả năng đọc citation.
- Hero hai cột từ tablet, tỷ lệ 0.9/1.1 trên desktop: tên nhóm dẫn câu chuyện, ảnh buổi làm việc cho thấy hoạt động có thật. Mobile xếp text trước ảnh và không cố định chiều cao.
- team0.jpg đã xem trực tiếp, 1303×582; giữ tỷ lệ ngang để không cắt mất người. Caption nằm ngoài ảnh; khung navy và góc bo bất đối xứng gắn ảnh với nhận diện, không phải placeholder logo.
- Header dùng logo 52px (44px mobile), chữ navy; underline active phân biệt vị trí hiện tại, focus tương phản rõ phục vụ keyboard.
- Navigation chuyển sang Menu dưới 1200px: browser xác nhận hàng navigation đầy đủ bị tràn ở 1024px. Giữ desktop navigation khi đủ chiều rộng và cùng breakpoint trong JS/CSS.
- Publications xuất hiện ngay sau hero, dùng danh sách thay card: tiêu đề, tác giả nguyên văn, venue/năm và nguồn đọc. Khi authors trống dùng homepage_reference nguyên văn hoặc citation đầy đủ; không suy diễn metadata. Giữ toàn bộ featured IDs và phân trang ba bài.
- Research dùng danh sách liên kết đến các anchor có thật và hình WSI hiện có, không gán thêm kết quả hoặc accuracy. Composition khác publications để tạo nhịp nội dung.
- Spacing lớn giữa các section và nhỏ trong citation giúp phân nhóm nội dung; thống kê từ build nằm sau nghiên cứu, đóng vai trò thông tin phụ.
- Home không scroll reveal hoặc tự chuyển ảnh. Gallery vẫn giữ toàn bộ ảnh và nút trước/sau; các trang khác giữ hành vi hiện có.
- CSS header/Home có một nguồn ở header-home.css; hero dùng class lab-hero riêng để không kế thừa các lớp hero portfolio cũ. Không thêm framework hoặc asset mới.

Đường dẫn runtime hiện tại: /home/uit2023/LuuTru/Vutm/.conda-envs/UITweb/bin/python. Build và check_site dùng môi trường này; không sử dụng prefix Thanhld trong README cũ.

## Home ba section: direction trước lần đồng bộ toàn site, 2026-10-12

Theo yêu cầu mới, Home chỉ gồm About UIT Together → Latest News → Research Highlights. Các mô tả composition Home ở mục trước là lịch sử; palette, typography, ảnh thật, responsive và quy tắc focus vẫn áp dụng. ENERGY/RHYTHM/MOTION tiếp tục là 3/5, 3/5, 1/5.

- About dùng hero editorial hai cột với team0, phụ đề Research Group, đơn vị trực thuộc và hai câu giới thiệu dựa trên Research/publications/datasets đã có; liên kết About/Research/Members phục vụ đọc sâu.
- News dùng một tin chính có nền sáng và đường ngang navy, hai tin phụ dạng editorial rows. Thứ bậc này phản ánh ngày mới nhất, không phải decoration; không thêm ảnh minh họa hoặc card grid lặp.
- Ngày ISO và ghi chú archive giữ độ tin cậy của tin 2021–2022; không dùng badge New hoặc fake recency.
- Research Highlights dùng danh sách ba journal papers lấy từ cấu hình IDs; venue/year/DOI và tác giả nguyên văn là bằng chứng, không thêm nhãn Q1 chưa xác minh.
- Resources gom Datasets/Tutorials/Conferences bằng native details để thêm News mà header không dài hơn. Dropdown có shadow nhẹ vì nằm trên nội dung; các section thường không shadow. Enter/Space toggle, Escape đóng và trả focus; click ra ngoài đóng.
- Statistics, Research Directions chi tiết, gallery, directory và feed dài được bỏ khỏi composition Home; dữ liệu, assets và trang chi tiết giữ nguyên.
- Hero nằm trong main để skip link đưa người dùng đến phần giới thiệu thay vì bỏ qua About. Home không có pagination hay motion tự chạy; tin và highlights render sẵn khi tắt JS.

## Đồng bộ toàn site: direction hiện hành, 2026-10-12

Premium Academic Editorial tiếp tục áp dụng: ENERGY 3/5, RHYTHM 3/5, MOTION 1/5. Design Read: giữ composition Home đã duyệt, dùng ảnh hoạt động thật và thứ bậc nghiên cứu làm điểm tựa, bổ sung tín hiệu quy mô gọn và đồng bộ trang đọc sâu. Không có asset mới.

- Home: About → Group Statistics → Latest News → Research Highlights → footer. Hero/copy/news/highlights giữ nguyên. Khối statistics blue tách khỏi hero nền nhạt; icons biểu thị bốn loại dữ liệu thật, đường phân chia thể hiện nhóm số liệu. Desktop bốn cột, mobile hai cột khi đủ chỗ và tự reflow khi chữ lớn.
- Ranh giới section dùng nền hero, khối blue statistics, khoảng cách `--section-space` và divider mảnh giữa News/Highlights. Tin đầu có viền navy để biểu thị thứ tự; không thêm wave, orb hoặc đường kẻ dày sau mọi section.
- Tokens/components hiện hành ở site.css, container `--layout-width:1180px`, radius thường 8px, control tối thiểu 44px. System sans hỗ trợ tiếng Việt; heading navy, link blue, metadata muted. Input border dùng muted để phân biệt control rõ hơn nền trắng.
- Page headers có nền #f6f9ff, title rõ và mô tả cụ thể; bỏ hộp icon lớn và eyebrow capsule cũ. Nội dung hiện ngay thay vì fade chung khi tải. Members giữ behavior reveal riêng đã có; flip countdown biểu thị thay đổi thời gian, reduced-motion loại animation, video có controls và được pause theo preference.
- Research giữ ảnh/video uncropped và bố cục text/media; caption dùng separator mảnh. Members giữ nhóm/thứ tự/search và crop chân dung. Publications dùng venue header + rows, authors nguyên văn nếu có, citation details và DOI; không suy diễn metadata thiếu. Dataset dùng hàng ảnh/text ở desktop và xếp dọc trên mobile. Conferences giữ spotlight/countdown/TBA/filter/update; navy tạo thứ bậc deadline gần nhất, gradient nửa ô biểu thị cấu trúc flip calendar. Contact dùng thông tin đã xác minh, News dùng dated rows, Tutorials giữ tài liệu và cấu trúc đọc.
- Footer navy #071c36, chỉ có tên nhóm, lĩnh vực, đơn vị, primary verified email, Room A108 từ About/Contact và copyright năm build. Không navigation hoặc CTA lặp; hai cột desktop, một cột mobile.
- Header bỏ News/Tutorials; Resources giữ Datasets/Conferences. Các URL cũ vẫn hoạt động. Shadow chỉ dùng dropdown đang nổi phía trên nội dung và chiều sâu ô flip; không dùng shadow cho mọi card.
- portfolio.css/header-home.css không còn được tải. Chỉnh style chung trong site.css; CSS Members/Conferences chỉ giữ chuyên biệt, dùng tokens chung. Các phần direction phía trên ghi lịch sử, mục này ưu tiên khi có khác biệt.

Kết quả nghiệm thu có căn cứ và giới hạn kiểm chứng: [sitewide-ui-review.md](sitewide-ui-review.md).

## Tinh chỉnh Statistics, navigation và Research, 2026-10-12

Statistics là dải thông tin phụ trên Home: dùng token nền UIT blue nhạt, chữ số navy, icon nhỏ, divider mảnh và bốn cột desktop/tối đa hai cột mobile. Giữ khoảng đệm gọn để khối số liệu hỗ trợ nhịp đọc thay vì cạnh tranh hero. Nguồn số luôn là `group_stats`.

Header dùng các liên kết trực tiếp Home, Research, Member, Publications, Datasets, Conferences và Contact; News/Tutorials vẫn có public routes nhưng không chiếm chỗ trong điều hướng chính. Mobile menu giữ cùng destinations, trạng thái active, Escape và trả focus.

Page header dùng nền xanh rất nhạt, divider dưới, không ép min-height; H1 dùng clamp 34–42px và mô tả sát tiêu đề. Research directions dùng partial chung `research-direction.html` với dữ liệu title, paragraph EN/VI, media type/source, alt text và caption EN/VI. Desktop ưu tiên text/media 45/55; mobile chuyển thành một cột với nội dung trước media. Ảnh khoa học giữ tỷ lệ tự nhiên và `object-fit: contain`; video giữ controls, không phát âm thanh tự động và tuân theo reduced-motion.

Kết quả nghiệm thu tinh chỉnh: [research-navigation-refinement-review.md](research-navigation-refinement-review.md).
