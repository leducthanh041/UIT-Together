# UIT-Together Research Group

Website giới thiệu nhóm nghiên cứu, công bố khoa học, thành viên theo khóa, datasets và tutorials. Website tĩnh dùng **Python 3.10 + Jinja2**, HTML/CSS/JavaScript và Bootstrap có sẵn. Hiện ưu tiên phát triển local; chưa deploy public.

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
- Công bố trên Papers và PapersByYear: `src/data/publications.json`; vị trí hiển thị được tham chiếu trong các template trang.
- Nội dung trang chủ/tin tức/hướng nghiên cứu/datasets: `src/partials/*-content.html`; bài tutorial và trang chi tiết: `src/pages/`.
- Giao diện: `src/assets/css/site.css`; tương tác: `src/assets/js/site.js`.
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

- [Kế hoạch clean/UI/UX](docs/restructure-ui-ux-plan.md)
- [Design system](docs/design-system.md)
- [Migration map](docs/migration-map.md)
- [Bảo mật public](docs/public-deployment-security-plan.md)
- [Báo cáo kiểm tra](docs/site-check-report.json)

Bản sao trước migration: `/home/uit2023/LuuTru/Thanhld/UIT-Together-backups/before-clean-20261010.tar.gz`. Giải nén vào thư mục riêng để đối chiếu/phục hồi; không giải đè bản làm việc khi chưa lưu thay đổi mới.

## License

[MIT](http://opensource.org/licenses/MIT). Giữ thông tin giấy phép riêng của thư viện, font và các skill đi kèm. Chưa xác minh quyền phân phối lại toàn bộ ảnh/PDF; không tự gán giấy phép mới cho dữ liệu nghiên cứu.
