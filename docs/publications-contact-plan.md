# Kế hoạch công bố gọn và Contact

Ngày: 2026-10-10. Đã triển khai UI, bộ lọc, hợp nhất route, Contact và kiểm tra dữ liệu. Cover/logo chờ người dùng tải từ nguồn nghiên cứu; email/định danh thầy Khánh chờ xác nhận.

1. Chuẩn hóa metadata của công bố từ citation và link đã có: tiêu đề, venue, loại journal/conference, DOI. Không suy đoán dữ liệu thiếu; giữ citation đầy đủ để đối chiếu.
2. Research nguồn ảnh/cover/logo chính thức. Mỗi venue dùng một ảnh chung tại src/assets/images/venues; không dùng hình mô hình trong paper làm cover journal. Lưu nguồn và hướng dẫn tải ảnh trong venue-image-sources.md.
3. Gộp Publications/By year vào /papers/, giữ /PapersByYear/ làm link chuyển tiếp. Hiển thị paper gọn theo venue: tiêu đề, năm, DOI/link. Citation đầy đủ được mở khi cần, không xóa tác giả.
4. Giữ tìm kiếm; thêm dropdown loại journal/conference, venue cụ thể và năm. Kết hợp các điều kiện, reset, thông báo kết quả và ẩn nhóm trống.
5. Thêm /contact/ tập trung thầy Khang và thầy Khánh; khangnttm@uit.edu.vn đã có trong repo, email/định danh đầy đủ của thầy Khánh chờ người dùng xác nhận. Không bịa email hoặc gán học hàm.
6. Build, kiểm tra link và metadata; kiểm tra logic lọc kết hợp. Giữ hiệu ứng reveal và vùng cuộn. Chưa có nghiệm thu trực quan do hạn chế trình duyệt của môi trường.

Cập nhật: Contact dùng tên đầy đủ Nguyen Tan Tran Minh Khang và Khanh Duy Nguyen; đã xác nhận danh tính Khánh, email còn thiếu. Trang chủ `/homes/` đã gộp vào `/`, giữ route chuyển tiếp.
