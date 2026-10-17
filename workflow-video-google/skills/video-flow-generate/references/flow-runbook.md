# Thực thi Google Flow
Updated: 2026-10-17 13:48 +07

## Preflight theo lần chạy

1. Xác nhận đúng project và tài khoản qua giao diện/công cụ cho phép; không lấy thông tin bí mật từ profile trình duyệt.
2. Chọn thao tác Video/Frames tương ứng UI thực tế. Quan sát hỗ trợ first+last, tỉ lệ, duration, resolution, audio và số outputs. Tên nút có thể đổi; đừng click theo tọa độ cũ không quan sát.
3. Lưu checked_at timezone, model/mode và thông tin credit hiện thấy. Tài liệu hỗ trợ đọc lại khi có điểm chưa rõ, không cần nghiên cứu lại mọi lượt nếu snapshot còn đúng và UI không đổi.
4. Đối chiếu đầu vào đã xem, version và giới hạn credit. Nếu giao diện tự đổi model, kiểm tra lại trước submit.

Nguồn chính thức (kiểm tra lần đầu khi xây skill: 2026-10-17; không phải cam kết tính năng tài khoản):
- [Create videos](https://support.google.com/flow/answer/16353334?hl=en)
- [Models/features](https://support.google.com/flow/answer/16352836?hl=en)
- [Edit/Scenebuilder](https://support.google.com/flow/answer/16935718?hl=en)

Voice reference và Frames có thể không tương thích trong cùng lượt. Tra cứu/current UI trước khi hứa giọng nhất quán. Nếu cần track narration riêng, phối hợp assemble; nếu cần sync-dialogue phải kiểm tra khẩu hình thực tế.

## Prompt chuyển động

Mô tả hành động nối start/end, thời điểm hoặc nhịp khi hữu ích, camera, môi trường giữ nguyên và sound design yêu cầu. Khi ảnh đã quyết định bố cục, đừng mô tả lại theo cách mâu thuẫn. Ví dụ: “Tay trái nâng tách lên chậm, hơi nước bốc nhẹ; camera tiến rất nhẹ; ánh sáng sáng sớm ổn định; tiếng căn phòng yên, không lời thoại.”

## Job và chi phí

Fingerprint dựa trên shot/version, frame/version, prompt, model, duration, mode, output count. Có thể băm JSON canonical bằng SHA-256; hash chỉ nhận diện request, không là cơ chế chống gửi trùng phía dịch vụ. Một yêu cầu trùng có thể vẫn bị tính phí nếu gửi lại.

Trước submit ghi planned. Sau submit ghi submitted cùng dấu vết take. Nếu UI biến mất/lỗi mạng, unknown; khi tiếp tục kiểm tra lịch sử/project trước khi quyết định failed hay gửi mới. Không có job ID thì lưu URL, mô tả vị trí/timestamp và prompt đủ đối chiếu.

Ngân sách gồm generation cost × outputs và số lượt sửa; upscale hoặc thao tác khác có thể có chi phí riêng. Không dùng giá API Veo để tính credit Flow. Chưa biết chi phí thì không gắn 0.

## Review và sửa

Lỗi nhận diện/bố cục: xem lại frame và asset. Chuyển động quá gấp: xem duration/action. Frame tốt nhưng động tác sai: sửa prompt có mục tiêu. Sai câu thoại: kiểm tra script/audio và model; không gắn pass từ việc chỉ có âm thanh.

Sửa tối thiểu có ích, giữ take cũ và lý do loại. Dừng khi đạt hoặc hết giới hạn; báo phần còn thiếu bằng dữ liệu thực.

## Ý đồ kể chuyện trong prompt và take

Ghi thứ tự hành động và phản ứng quan trọng từ shot: nhận ra chi tiết → dừng lại → quyết định, cùng ai nói và ai nghe. Chỉ yêu cầu phần diễn tiến nằm trong shot và vừa thời lượng. Không nhồi toàn bộ đường dây câu chuyện vào một lượt render.

Review lấy từ clip thật: hành động mục tiêu có xảy ra, đúng vai có phát hiện/quyết định, câu nói có đúng và điểm trim có giữ được payoff? Trạng thái review chỉ pass sau khi quan sát phần liên quan. Không chọn một clip đẹp nhưng đổi ý nghĩa, đổi người nói hoặc thêm cam kết sản phẩm.

Nếu cần sửa lời, quay lại script/audio; nếu cần sửa trạng thái đầu–cuối, quay lại shot/frame. Giữ take cũ và lý do loại để không lặp lại lỗi; chi phí sửa vẫn thuộc budget và retry đã chốt.
