# Kế hoạch tái cấu trúc và cải thiện UI/UX

Ngày ghi nhận: 2026-10-10. Ưu tiên hiện tại: sửa website local. Đã triển khai cấu trúc, template, dữ liệu members/cohorts/publications, UI chung và local tooling. Các giới hạn và phần nội dung cần xác minh ghi ở content-review.md; chưa nghiệm thu visual bằng browser hoặc deploy public.

## Mục tiêu và nguyên tắc

Website giới thiệu UIT-Together, hướng nghiên cứu, công bố khoa học và thành viên qua các khóa/giai đoạn. Tổ chức lại repo để dễ sửa nội dung và dùng giao diện học thuật hiện đại, dễ đọc, dễ tra cứu.

- Chuyển cấu trúc trước, đổi giao diện sau; mỗi giai đoạn có bản local kiểm tra được.
- Bảo toàn nội dung, thứ tự tác giả, liên kết bài báo/thành viên và URL hiện tại, kể cả `/PapersByYear/`.
- Không phỏng đoán DOI, hồ sơ, thời gian tham gia hoặc thông tin nhóm. Đánh dấu dữ liệu chưa xác minh.
- Một nguồn dữ liệu chính, một đầu ra tự động; không sửa tay đầu ra.
- Backup trước migration vì `.git` cũ đã được xóa. Không xóa file chỉ vì tên gợi ý là cũ.

## Hiện trạng đã đọc

Repo trộn HTML chạy trực tiếp, nguồn Jekyll (`_layouts`, `_includes`, `_my_team`, `_projects`, `_plugins`), `_site` cũ, `deploy/public` và repo công cụ `ANOTHER_REPO`. CSS nằm nhiều nơi; header/footer/metadata lặp lại. Bài báo xuất hiện ở trang chủ, Papers và PapersByYear; thành viên viết trong HTML. Còn nội dung/metadata Niemeyer. Menu trang chủ có target không khớp ID, link rỗng/`#`, Datasets dùng title Research. Giao diện thực tế và danh mục liên kết đầy đủ còn cần audit.

## Kiến trúc dự kiến

Website tĩnh: HTML template + JSON + script Python nhẹ. Chọn engine template sau khi xác minh nhu cầu; khai báo dependency nếu dùng thư viện, không tự viết engine template phức tạp.

```text
UIT-Together/
├── README.md
├── AGENTS.md
├── .gitignore
├── src/
│   ├── pages/          # Home, About, Team, Papers, PapersByYear, Research…
│   ├── layouts/        # Khung trang
│   ├── partials/       # Header, footer, metadata, thành phần lặp
│   ├── data/           # site, members, publications, research, datasets, news
│   └── assets/         # css, js, images, fonts, pdfs, vendor
├── scripts/            # build.py, dev.py, check_site.py
├── docs/               # Tài liệu phát triển
├── tools/skills/       # taste-skill, ui-ux-pro-max-skill
├── legacy/jekyll/      # Nguồn/config cũ đã đối chiếu
├── deploy/             # Cấu hình triển khai, đang tạm gác
└── dist/               # Artifact tự động, không sửa tay
```

`docs/` hiện chứa các trang website cũ. Phân biệt chúng với tài liệu phát triển: giữ URL công khai đang dùng bằng cách chuyển nguồn trang sang `src/pages/docs/` khi migration. Kiểm kê cả Funding, Software, Projects, news và mọi trang chi tiết trước quyết định vị trí.

## Giai đoạn 1: Audit và phục hồi

- Sao lưu ngoài thư mục public; ghi manifest và cách phục hồi.
- Kiểm kê trang, asset, route, anchor, link và dependency, gồm CSS url(), font, PDF, các trang ít được menu dẫn tới.
- Xác định nguồn có hiệu lực và nội dung khác nhau giữa HTML, Jekyll, `_site`, deploy.
- Chụp/kiểm tra giao diện desktop/mobile khi browser khả dụng; ghi giới hạn nếu không có browser.
- Tạo `docs/migration-map.md`: file cũ → nguồn mới → URL đầu ra; baseline nội dung và lỗi có sẵn.

Nghiệm thu: danh mục đầy đủ, backup phục hồi được và route map.

## Giai đoạn 2: Di chuyển, giữ hành vi

- Gom nguồn đang dùng vào src; giữ đường dẫn public tương thích hoặc tạo alias đã kiểm tra.
- Di chuyển skill và cập nhật tham chiếu; giữ tài liệu giấy phép của bên thứ ba.
- Lưu Jekyll/CI cũ vào legacy sau khi xác định phụ thuộc; không chạy build Jekyll cũ ghi đè nguồn mới.
- Build theo allowlist vào dist; xử lý file đầu ra đã bị xóa ở nguồn, tránh stale file. Không copy công cụ/bí mật.
- Dev server theo dõi thay đổi nguồn và phục vụ dist, có lỗi build dễ hiểu. Chạy cổng từ terminal SSH thật nếu môi trường agent chặn socket.
- Điều chỉnh deploy để dùng dist sau này; không mở public trong giai đoạn này.

Nghiệm thu: local hoạt động, URL và nội dung giữ nguyên; thư mục public không chứa công cụ/cấu hình riêng.

## Giai đoạn 3: Template và dữ liệu

- Layout/partials chung cho navigation, footer và metadata.
- site.json: thông tin nhóm và navigation đã xác minh.
- members.json: ID ổn định, tên, vai trò, ảnh, khóa, trạng thái, link; mốc thời gian chỉ khi có bằng chứng.
- publications.json: ID, tiêu đề, tác giả đúng thứ tự, năm, loại, venue, DOI, link/PDF; đối chiếu trùng bằng DOI hoặc đánh dấu chưa chắc chắn.
- Các trang Papers/PapersByYear/trang chủ dùng chung dữ liệu; thống kê tính tự động.
- Data validation: ID trùng, năm sai, đường dẫn thiếu; escape nội dung khi render. Phân biệt dữ liệu thiếu/rỗng.

Nghiệm thu: cập nhật một dữ liệu ở một nơi sinh đúng các trang liên quan; đối chiếu đủ nội dung trước/sau.

## Giai đoạn 4: Design system

Áp dụng repo ui-ux-pro-max-skill cùng taste-skill đã được yêu cầu trước đó theo ngữ cảnh. Đã đọc các SKILL.md design/design-system/brand/ui-styling liên quan và chạy search.py --design-system cho UIT-Together. Kết quả gợi ý Swiss Modernism, grid và màu xanh học thuật; đây là đầu vào tham khảo, không phải thiết kế đã nghiệm thu.

- Định hướng: nhóm nghiên cứu học thuật hiện đại, nội dung rõ, dễ tra cứu, chuyển động nhẹ.
- Nền sáng, một màu xanh nhấn, ảnh và logo thật; xem asset hiện có trước khi chốt palette/font.
- Typography hỗ trợ tiếng Việt, self-host khi phù hợp, lưu giấy phép.
- CSS variables theo primitive → semantic → component; scale khoảng cách, bo góc và trạng thái thống nhất.
- Một hệ icon; không ép chuyển React/Tailwind chỉ vì skill có ví dụ cho stack đó.
- Ghi quyết định và component states trong docs/design-system.md.

Nghiệm thu: tokens và thành phần dùng chung đủ cho trang chính, đáp ứng keyboard/contrast/reduced motion.

## Giai đoạn 5: Các trang

- Home: giới thiệu, hướng nghiên cứu, công bố nổi bật, tin tức phân cấp rõ; số liệu chỉ từ dữ liệu xác minh.
- Team: thành viên hiện tại, sinh viên theo khóa, alumni khi có dữ liệu; hình ảnh và vai trò nhất quán.
- Papers: tìm theo tiêu đề/tác giả, lọc năm/loại; DOI/PDF rõ; giữ thứ tự tác giả và liên kết.
- PapersByYear: giữ URL, dùng chung nguồn và nhóm theo năm.
- Research: hướng nghiên cứu/dự án và công bố liên quan có căn cứ.
- Datasets: mô tả và link truy cập; không tự gán giấy phép.
- Tutorials/News/About/Contact và trang phụ: dùng layout chung, sửa metadata, đánh dấu nội dung chưa rõ.
- Tìm kiếm/bộ lọc: trạng thái không có kết quả, reset, keyboard; nội dung chính đọc được khi JavaScript tắt.

## Giai đoạn 6: Nghiệm thu toàn bộ

- So sánh danh mục trang, thành viên, công bố và link trước/sau; phân biệt lỗi baseline và regression.
- Kiểm tra href/src, CSS assets, anchors, ảnh/font/PDF và route cũ.
- Kiểm tra menu, filter/search, footer, viewport 375/768/1024/1440, nội dung dài và không tràn ngang.
- Keyboard/focus, alt text, contrast, reduced motion; không tuyên bố đạt accessibility toàn diện chỉ từ kiểm tra tự động.
- Tối ưu ảnh/kích thước ảnh, script cần thiết và font; kiểm tra console khi browser khả dụng.
- Title/description/lang/favicon đúng; canonical chờ domain thật. Link ngoài bị chặn chưa đồng nghĩa bị hỏng.
- Chạy kiểm tra bảo mật artifact; báo rõ phần không kiểm tra được do môi trường.

## README và tài liệu bàn giao

README: mục đích/stack, cây thư mục, requirements, một lệnh chạy local, build/check, thêm thành viên/bài báo/khóa, quy tắc ID/file/asset, không sửa dist, vị trí skill/legacy, lỗi thường gặp và deploy đang tạm gác. docs/content-guide.md giải thích schema và ví dụ; docs/architecture.md giải thích build/route.

Lệnh dự kiến: `python3 scripts/dev.py --host 0.0.0.0 --port 8080`. Đây chưa phải lệnh đã tồn tại; host/cổng lựa chọn theo cách truy cập local/VPN/SSH forwarding.

## Thứ tự bàn giao

1. Repo sạch và local tương đương hiện tại.
2. Template/dữ liệu tập trung và README đủ để tự sửa.
3. Home/Team/Papers giao diện mới.
4. Trang còn lại và kiểm tra toàn bộ.

Triển khai public sẽ theo [kế hoạch bảo mật](public-deployment-security-plan.md) ở giai đoạn riêng. Trước khi thực hiện, đọc lại skill từ vị trí thực tế và ghi mọi thay đổi phạm vi trong tài liệu này.
