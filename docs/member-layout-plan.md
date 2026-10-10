# Bố cục Member

## Mục tiêu và dữ liệu

Trang `/team/` và `/vi/team/` giữ nguyên URL. Bỏ phân trang riêng trang này; giữ tìm tên/khóa. Ba nhóm: Supervisor, Current Members từ K2023, Former Members đến K2022.

Supervisor có 10 thẻ, thứ tự từng hàng trên desktop:

| Bên trái | Bên phải |
|---|---|
| Khang Nguyen — Leader | Tam Nguyen — Collaborator |
| Khanh Duy Nguyen | Doanh C. Bui |
| Tung Minh Tran | Nguyen Duy Vo |
| Hiep Nguyen | Dung Truong |
| My Hoan Nguyen | Long Duong |

Yêu cầu ban đầu ghi cả Leader và Collaborator bên phải; áp dụng Leader trái / Collaborator phải theo thứ tự đã liệt kê. Nhãn vai trò nằm trong thẻ. ID cũ được giữ; thêm ID mới cho Doanh C. Bui và các thành viên hiện tại. Không tự bổ sung học vị, affiliation hoặc biography chưa được cung cấp. Mỗi Current Member có phần About/Giới thiệu, hiển thị thông báo sẽ cập nhật khi `bio_en`/`bio_vi` còn trống.

Bốn ảnh K2023: Lê Đức Thành, Nguyễn Ngọc Thanh Phương, Trần Minh Vũ, Huỳnh Diên Thục. Ba tên Phạm Trần Xuân Tiến, Huỳnh Nhật Thanh, Đỗ Minh Dũng được thêm Current Members; khóa để trống đến khi được xác nhận, không tạo ảnh giả. K2024/K2025 có thể bổ sung hồ sơ sau. Danh sách các khóa cũ giữ nguyên, kể cả lịch sử K2019 của Doanh C. Bui.

## Trải nghiệm cuộn

Cuộn toàn trang, không tạo scrollbar lồng nhau và không dùng scroll snap. Thanh chuyển nhanh dùng anchor, theo dõi phần đang xem bằng IntersectionObserver. Tham khảo các thẻ `speaker-card reveal-up` trong `core-source/healthinfo_uit_edu_vn.html`: từng thẻ Member, heading và tên cựu thành viên fade/translate riêng khi đi vào viewport, thời lượng 1 giây và độ trễ xen kẽ tối đa 80ms. Không ẩn/chuyển động nguyên khối Supervisor hoặc Current Members. Chỉ cuộn xuống lặp hiệu ứng; cuộn lên hiển thị ngay, không chuyển động; reduced motion, keyboard focus, không JavaScript và print vẫn đọc được nội dung. Bio của Nguyễn Ngọc Thanh Phương giữ đúng câu người dùng cung cấp ở cả EN/VI.

## Triển khai và kiểm tra

Dữ liệu ở `members.json`/`cohorts.json`; template Team và partial member; CSS/JS riêng chỉ tải trên trang Member. Bỏ thuộc tính kích hoạt pager trên Team ở base layout, không đổi pager Publications. Kiểm tra đủ 10 Supervisor đúng hàng, 7 Current Members, danh sách khóa cũ không mất/đổi thứ tự, không có pager Team, hai ngôn ngữ, ảnh tồn tại, repeated reveal/reduced motion và điều hướng phần. Chạy build/check_site, các tests liên quan.

Nguồn kỹ thuật: [MDN Scroll Snap](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll_snap/Basic_concepts), [MDN IntersectionObserver](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API).
