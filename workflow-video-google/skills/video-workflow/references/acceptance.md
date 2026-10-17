# Nghiệm thu khi triển khai hoặc sửa bộ skill
Updated: 2026-10-17 11:03 +07

Không cần render dịch vụ trả phí để kiểm tra cấu trúc. Đánh giá riêng hành vi viết nội dung, kiểm tra dữ liệu và chất lượng media thực tế.

1. Short: script có một hook rõ, payoff tồn tại phía sau; mọi beat được shotlist phủ. Gán payoff tới beat không tồn tại phải bị validator chặn.
2. Long: có concept title/thumbnail và chapter mục đích rõ; mọi beat thuộc chương hợp lệ; không dừng ở dàn ý khi người dùng yêu cầu script đầy đủ.
3. Frames: mỗi shot có đủ hai ảnh; ảnh thiếu ở artifact ready phải lỗi. Mô tả ảnh không được xem là ảnh thực.
4. Continuity: có cảnh nối liên tục và cảnh đổi góc; kiểm tra không ép end S01 thành start S02 nếu khác bố cục.
5. Sửa S03: dependency downstream cần revision, S01 không liên quan giữ nguyên; version cũ không được coi mới.
6. Flow: model thiếu tổ hợp frame/voice phải báo đúng; không tự bỏ end frame. Timeout không tự retry nếu chưa kiểm tra kết quả cũ.
7. Clip: downloaded nhưng review unchecked không đủ để selected. File tồn tại nhưng sai chuyển động cần review needs-revision.
8. Audio: audio dài hơn animatic phải báo, không tự cắt lời. Final không âm thanh nếu brief bắt buộc lời dẫn phải ghi chưa hoàn tất.
9. Export: helper animatic chỉ chấp nhận mode animatic; không ghi đè file có sẵn; path không thoát project.
10. Bộ skill: frontmatter hợp lệ, link nội bộ có thật, UI prompt gọi đúng tên skill, không còn scaffold TODO.
