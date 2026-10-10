# UIT-Together Research Group

Website giới thiệu nhóm nghiên cứu, công bố khoa học, thành viên theo khóa, datasets và tutorials. Website tĩnh dùng **Python 3.10 + Jinja2**, HTML/CSS/JavaScript và Bootstrap 5.0.2 nội bộ. Đã có cấu hình GitHub Actions để tự build và deploy lên GitHub Pages; chưa kích hoạt trên GitHub.

## Chạy local


Môi trường Conda `UITweb` đã được tạo offline tại prefix dưới đây vì môi trường agent không truy cập được máy chủ tải gói:

```bash
cd /home/uit2023/LuuTru/Thanhld/UIT-Together
conda activate /home/uit2023/LuuTru/Thanhld/.codex-local/home/.conda/envs/UITweb
python scripts/dev.py --host 0.0.0.0 --port 8080
```

Nếu Conda trên terminal của bạn đã nhận môi trường, có thể dùng `conda activate UITweb`. Nếu chưa có lệnh activate, khởi tạo shell Conda theo thiết lập hiện tại hoặc chạy Python trực tiếp:

```bash
/home/uit2023/LuuTru/Thanhld/.codex-local/home/.conda/envs/UITweb/bin/python scripts/dev.py --host 0.0.0.0 --port 8080
```

Dừng server Python cũ bằng Ctrl+C trước khi dùng lại cổng 8080. Mở `http://192.168.20.166:8080` trong mạng/VPN phù hợp, hoặc forward cổng qua VS Code Remote SSH và mở `http://localhost:8080`. Script theo dõi `src/`, build lại khi thay đổi; refresh trình duyệt để xem. Bind mặc định là `127.0.0.1` nếu không truyền `--host`. Đây là server phát triển.

Để tạo môi trường trên máy khác:

```bash
conda env create -f environment.yml
conda activate UITweb
```

## Cấu trúc

```text
src/
  pages/       Template cho từng URL hiện có
  layouts/     Khung HTML dùng chung
  partials/    Header, footer, member, publication, nội dung trang
  data/        site, pages, publications, members, cohorts, news, featured (JSON)
  assets/      css, js, images, fonts, pdfs, themes bên thứ ba
  static/      Tài nguyên giữ URL cũ: dataset media, feeds
scripts/       Build, dev server, kiểm tra dữ liệu/link
docs/         Tài liệu phát triển và báo cáo kiểm tra
tools/skills/ taste-skill và ui-ux-pro-max-skill
legacy/       Nguồn cũ để đối chiếu, không phục vụ web
deploy/       Cấu hình triển khai tạm gác, sử dụng dist
dist/         Website sinh tự động; không chỉnh sửa tại đây
```

## Sửa nội dung

- Thông tin nhóm/menu: `src/data/site.json`.
- Hồ sơ thành viên: `src/data/members.json`; danh sách khóa: `src/data/cohorts.json`.
- Công bố (PapersByYear chuyển tiếp về Papers): `src/data/publications.json`; trang tự gom theo venue và hỗ trợ lọc năm/loại/venue.
- Nội dung trang chủ/tin tức/hướng nghiên cứu/datasets: `src/partials/*-content.html`; bài tutorial và trang chi tiết: `src/pages/`.
- Cover/logo venue: `src/assets/images/venues/`; nguồn tải trong [hướng dẫn ảnh](docs/venue-image-sources.md).
- Liên hệ: `src/data/contacts.json`, trang `/contact/`.
- Giao diện nền: `src/assets/css/site.css`; giao diện theo template Bootstrap: `src/assets/css/portfolio.css`; tương tác: `src/assets/js/site.js`.
- Thêm trang phải khai báo trong `src/data/pages.json`.

Xem [hướng dẫn nội dung](docs/content-guide.md) và [kiến trúc](docs/architecture.md) để thêm dữ liệu/route đúng cách.

## Build và kiểm tra

```bash
python scripts/build.py
python scripts/check_site.py
node --check src/assets/js/site.js
```

Build không cần Node; lệnh Node chỉ kiểm tra cú pháp JS. `check_site` thất bại nếu có link thiếu mới so với baseline; báo cáo vẫn liệt kê các link thiếu đã có từ trước. Một số trang cũ còn nội dung Niemeyer và chưa được xác minh: xem [ghi chú nội dung](docs/content-review.md). Không coi baseline là chứng nhận mọi link đều hoạt động.

## Tài liệu và phục hồi

- [Kế hoạch giao diện theo template Bootstrap](docs/bootstrap-template-redesign-plan.md)
- [Kế hoạch clean/UI/UX](docs/restructure-ui-ux-plan.md)
- [Design system](docs/design-system.md)
- [Migration map](docs/migration-map.md)
- [Bảo mật public](docs/public-deployment-security-plan.md)
- [Báo cáo kiểm tra](docs/site-check-report.json)

Bản sao trước migration: `/home/uit2023/LuuTru/Thanhld/UIT-Together-backups/before-clean-20261010.tar.gz`. Giải nén vào thư mục riêng để đối chiếu/phục hồi; không giải đè bản làm việc khi chưa lưu thay đổi mới.

## License

[MIT](http://opensource.org/licenses/MIT). Giữ thông tin giấy phép riêng của thư viện, font và các skill đi kèm. Chưa xác minh quyền phân phối lại toàn bộ ảnh/PDF; không tự gán giấy phép mới cho dữ liệu nghiên cứu.

Trang chủ chung tại `/`: UIT Together, Computer Vision và Machine Learning. `/homes/` chuyển tiếp về `/`; menu chỉ còn Home.

## English / Tiếng Việt

- Tiếng Anh mặc định: `http://localhost:8080/`.
- Tiếng Việt: `http://localhost:8080/vi/`.
- Chọn EN / VI trên header để đổi ngôn ngữ và giữ trang đang xem.
- Bản dịch: `src/data/translations.json` và `src/data/tutorial-translations.json`. Tên bài báo, tác giả, venue, DOI và code giữ nguyên. Build sinh 292 trang từ 146 template, dùng chung ảnh/CSS/JS.

## Lịch hội nghị tự động

Mở `/conferences/` hoặc `/vi/conferences/`; trang Home cũng hiển thị deadline gần nhất và hội nghị sắp diễn ra. Bộ đếm lật lịch cập nhật mỗi giây, hiển thị theo giờ Việt Nam. Kỳ đã kết thúc tự chuyển sang kỳ tiếp theo; thông tin chưa công bố hiển thị TBA thay vì tái sử dụng lịch cũ.

`scripts/dev.py` kiểm tra nguồn chính thức lúc khởi động và mỗi 6 giờ. GitHub Actions trong `.github/workflows/update-conferences.yml` làm tương tự sau khi được đưa lên nhánh mặc định và Actions có quyền ghi. Trình duyệt nhận dữ liệu mới mỗi 5 phút, kể cả khi website tĩnh chưa được build lại. Lỗi nguồn giữ dữ liệu đã xác minh và hiện trạng thái chờ cập nhật. Hướng dẫn, giới hạn parser và quy tắc múi giờ: [docs/conference-automation.md](docs/conference-automation.md).

Trang Member gồm Supervisor, Current Members (K2023 trở đi) và Former Members (K2022 trở về trước), cuộn liên tục, không phân trang. Sửa `bio_en`/`bio_vi` trong `src/data/members.json` để cập nhật giới thiệu ngắn. Bố cục, thứ tự và hiệu ứng: [docs/member-layout-plan.md](docs/member-layout-plan.md).

## Deploy tự động lên GitHub Pages

Repo hiện có remote `https://github.com/leducthanh041/UIT-Together.git`. Trong GitHub, vào **Settings → Pages → Build and deployment → Source: GitHub Actions** (không chọn Deploy from a branch vì source cần build bằng Jinja2). Sau đó commit và push các thay đổi lên `main`:

```bash
git add .
git commit -m "Prepare GitHub Pages deployment"
git push origin main
```

Workflow **Deploy GitHub Pages** build, chạy kiểm thử/check link, rồi chỉ upload `dist/`. Không cần commit `dist` hoặc chạy server Ubuntu liên tục. URL dự kiến khi chưa dùng custom domain: **https://leducthanh041.github.io/UIT-Together/**. Bản tiếng Việt: `/UIT-Together/vi/`. Có thể chạy lại từ **Actions → Deploy GitHub Pages → Run workflow**. Đây là cấu hình chuẩn bị trong repo; chưa push hoặc bật Pages từ phiên này.

Build tự nhận base path từ `actions/configure-pages`. Khi dùng custom domain hoặc repository `USERNAME.github.io`, base path rỗng; domain khai báo ở Settings → Pages, bật HTTPS khi GitHub xác nhận DNS. Hướng dẫn chính thức: [GitHub custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Kiểm tra cấu hình project-site tại local:

```bash
python scripts/build.py --base-path /UIT-Together
python scripts/check_site.py --base-path /UIT-Together
# Sau kiểm tra, tạo lại bản local:
python scripts/build.py
```

Lịch hội nghị vẫn đồng bộ mỗi 6 giờ trên GitHub Actions. Deploy chạy sau khi workflow đồng bộ hoàn tất thành công, vì commit do `GITHUB_TOKEN` không kích hoạt một workflow `push` khác. Branch protection có thể cần cho phép bot cập nhật hoặc chuyển sang Pull Request; workflow không bỏ qua bảo vệ nhánh. Xem [GitHub workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

Số liệu Home được tính lúc build từ dữ liệu hiện tại: **140 Participants**, **105 Research Papers**, **42 Conferences & Journals** và **13 Public Datasets**. Participants là tên duy nhất trong hồ sơ và danh sách khóa (chuẩn hóa Unicode/khoảng trắng/hoa thường; chưa tự ghép các tên viết khác nhau). Papers là 105 công bố hiển thị sau gộp trùng từ 150 bản ghi lịch sử. Venue gồm 21 journal và 21 conference có bài của nhóm; không phải số lần tham dự sự kiện. Datasets là 13 tên được giới thiệu trên trang Datasets. Không thêm dấu `+` vì đây là số đếm của dữ liệu hiện có. Cập nhật source sẽ tự tính lại khi build; logic ở `scripts/group_statistics.py`.
