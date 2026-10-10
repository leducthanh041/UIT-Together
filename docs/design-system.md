# UIT-Together design system

Academic modern, light theme, navy/blue accent, native CSS + Bootstrap hiện có. DESIGN_VARIANCE 4, MOTION_INTENSITY 2, VISUAL_DENSITY 4. Áp dụng taste-skill và ui-ux-pro-max theo nhu cầu website nghiên cứu, không chuyển framework vì ví dụ của skill.

Tokens ba lớp primitive/semantic/component nằm ở src/assets/css/site.css. Font sans hệ thống hỗ trợ tiếng Việt, tránh yêu cầu tải font ngoài. Giữ logo thật, grid rõ, không gradient hoặc hiệu ứng trang trí nặng. Header dùng link text, menu mobile có ARIA/Escape; footer không cố định che nội dung.

Paper/member và danh sách dùng spacing thống nhất; tìm kiếm bỏ dấu tiếng Việt, trạng thái không kết quả và clear filters. Nội dung vẫn có khi tắt JS. Bảng và code tutorial cuộn trong phạm vi riêng; ảnh responsive. Gallery Team hiển thị tĩnh thay carousel phụ thuộc jQuery.

Focus rõ, reduced-motion, mobile styles có trong CSS. Chưa có nghiệm thu visual tự động: Firefox headless crash do môi trường; cần kiểm tra local ở 375/768/1024/1440 px và keyboard trước public. Icon decoration FontAwesome cũ chưa được tải; navigation không phụ thuộc icon.

## Tham chiếu CORE Lab — cập nhật 2026-10-10

Đã đọc các HTML local trong core-lab-source, đặc biệt trang chủ. Đây là HTML xuất từ Next.js; CSS chunks được tham chiếu nhưng không có trong thư mục, nên không tuyên bố đã sao chép stylesheet hoặc xem đầy đủ bản render. Thiết kế UIT-Together tham khảo header compact, hero hai cột, typography phân cấp và các nhóm nội dung rõ.

Palette mới: navy #10386b, blue #145ac4, nền #f6f9ff, chữ #233e61. Font system sans hỗ trợ tiếng Việt. Hero dùng ảnh nhóm team0 có sẵn, không dùng artwork/asset của CORE. Footer navy, thẻ nội dung trắng, vùng cuộn giữ nguyên và có keyboard focus. Mobile hero thành một cột. Không thêm dependency hoặc chuyển Next.js.
