# Tự động cập nhật hội nghị

`scripts/update_conferences.py` cập nhật duy nhất `src/data/conferences.json`, bằng Python 3.10 standard library. Dữ liệu seed khai báo nguồn chính thức cho 14 hội nghị; không đọc ai-deadlines, WikiCFP hoặc danh sách cộng đồng. Mỗi hội nghị được kiểm tra tối đa 5 trang, timeout từng request 8 giây, giới hạn mỗi response 2 MiB; tối đa 4 hội nghị chạy đồng thời.

```bash
python scripts/update_conferences.py
python -m unittest discover -s tests -p test_conference_updates.py -v
python scripts/build.py
python scripts/check_site.py
```

Updater dùng JSON-LD Event trước; địa điểm HTML chỉ nhận các nhãn rõ `Location:`, `Venue:` hoặc `Conference Venue:`, bỏ footer/contact/TBA. Sau đó tìm ngày trong hàng bảng/đoạn văn có bằng chứng về kỳ hội nghị và nhãn nộp bài chính/full/regular/research. Hỗ trợ các trang Dates của CVF, ICLR, NeurIPS; HTML chính thức của AAAI, SIGIR, ICMR, ACM MM, MMM, MICCAI, KSE, RIVF và ECIR. Chỉ mở HTTPS trên allowlist riêng của từng hội nghị; redirect đến domain khác bị chặn. Link Dates/CFP/important-dates cùng nguồn chính thức được khám phá tự động trong giới hạn trang.

Các deadline được gộp theo loại/vòng qua nhiều trang; bài Short giữ riêng với Main/Full/Regular và không làm mất các deadline khác đã xác minh.

Các URL theo năm được tạo từ adapter hoặc `source_template` đã qua allowlist. URL dự đoán chỉ là địa chỉ để kiểm tra: không tự tạo ngày, thành phố hay trạng thái confirmed. Hội nghị chuyển domain ngoài allowlist cần bổ sung domain sau khi xác minh từ nguồn chính thức; updater sẽ báo pending/stale thay vì theo domain tùy ý.

Ngày phải đúng năm của kỳ hội nghị, hoặc năm liền trước đối với deadline. Parser bỏ nội dung gạch bỏ (`s`, `del`, `strike`), workshop, abstract, camera-ready, notification và các trường có nhiều ngày chưa rõ nghĩa. Nhãn proposed/tentative được giữ. `at` chỉ có giá trị khi nguồn viết giờ và timezone/offset rõ ràng; chỉ ngày AoE được lưu `date` và `zone: "AoE"`, với `at: null`. Không suy đoán giờ 23:59 từ một ngày đơn thuần. Frontend có thể giải thích quy ước hết ngày AoE riêng, nhưng không được trình bày đó là giờ do nguồn công bố.

Khi `ends_on` đã qua hết ngày AoE (UTC−12), để tránh chuyển kỳ quá sớm khi giờ địa phương chưa rõ, updater chuyển sang năm tiếp theo, xóa ngày/location/deadline cũ và chuyển sang pending. ICCV có cadence 2 năm; các hội nghị khác mặc định 1 năm. `cadence` có thể ghi rõ trong seed. Nếu chưa xác minh ngày kết thúc thì không tự cho rằng hội nghị đã kết thúc.

Lỗi mạng/parser giữ nguyên dữ liệu đã xác minh và đánh dấu stale; kỳ mới chưa có thông tin được đánh dấu pending. Thành công một phần được đánh dấu partial. Ngày từ nguồn chính thức không thống nhất được ẩn và ghi `sync_status: "conflicting"`, `date_status: "unannounced"`. Khoảng ngày toàn hội nghị bao trùm khoảng main sessions được hợp nhất, không coi là mâu thuẫn. Deadline chính mâu thuẫn bị ẩn. `checked_at` là lần thử kiểm tra; `last_success_at` là lần có bằng chứng ngày đọc được, không bảo đảm mọi trường đã được làm mới.

Ghi JSON bằng file tạm rồi replace; input sai hoặc lỗi trước khi ghi giữ nguyên file. CLI trả 0 khi nguồn offline nhưng giữ dữ liệu usable/stale, trả 1 khi cấu trúc input hoặc thao tác file lỗi. CLI từ chối đường dẫn output khác. Không sửa trang, backend, `dist` hoặc các dữ liệu khác.

`.github/workflows/update-conferences.yml` chạy mỗi 6 giờ và cho phép workflow_dispatch trên default branch. Workflow chạy tests, updater, build và check trước khi commit **chỉ conferences.json** bằng github-actions bot. Workflow deploy riêng chạy khi cập nhật nguồn hoàn tất thành công. Repo cần cho phép Actions ghi contents; branch protection có thể chặn bot push, khi đó workflow báo lỗi và không bỏ qua bảo vệ nhánh. Lịch GitHub có thể trễ; đây không phải dịch vụ thời gian thực. Workflow sẽ chạy sau khi người quản trị đưa các file này lên repo; quá trình triển khai local không push/activate workflow từ xa.

Dev server gọi cùng updater lúc khởi động và mỗi 6 giờ; lỗi cập nhật không xóa website đang chạy. Updater vẫn cần truy cập Internet để làm mới dữ liệu. Tests dùng HTML fixtures và mock network, không gọi live API. Trong môi trường phát triển hiện tại, kiểm tra trực tiếp bằng urllib gặp lỗi DNS; vì vậy đã kiểm thử logic parser và giữ dữ liệu khi offline, chưa xác minh thành công toàn bộ 14 website từ CLI. Các trang dùng JavaScript để tải nội dung, chống bot, PDF-only, đổi layout hoặc định dạng ngày không hỗ trợ sẽ giữ ngày cũ/pending và cần cập nhật adapter. Không có parser HTML nào bảo đảm tự cập nhật được mọi thay đổi từ bên tổ chức.

Nguồn tham chiếu trực tiếp cho format adapter: [CVPR Dates](https://cvpr.thecvf.com/Conferences/2027/Dates), [NeurIPS Dates](https://neurips.cc/Conferences/2026/Dates), [ICLR Dates](https://iclr.cc/Conferences/2027/Dates). Đây là bằng chứng định dạng tại thời điểm kiểm tra, không phải cam kết layout sẽ giữ nguyên.

Website có bộ đếm cập nhật mỗi giây theo giờ Việt Nam, tải lại dữ liệu mỗi 5 phút. Trang Home và Conferences tự chọn deadline nộp bài gần nhất, đồng thời giới thiệu hội nghị sắp diễn ra gần nhất. Ngày chưa có giờ/múi giờ chỉ có bộ đếm đến ngày lịch, kèm nhãn rõ ràng; không coi đó là thời hạn nộp bài chính xác. `--no-conference-sync` tắt kiểm tra mạng khi sửa web offline.
