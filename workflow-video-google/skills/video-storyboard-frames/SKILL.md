---
name: video-storyboard-frames
description: "Tạo và sửa cặp start frame/end frame cho từng shot trong workflow video Google Flow, dùng bộ tham chiếu để giữ nhân vật và bối cảnh nhất quán. Xuất storyboard và bảng tổng hợp ảnh; không render chuyển động."
---

# Video Storyboard Frames
Updated: 2026-10-17 13:48 +07

Đọc [hợp đồng frames](../video-workflow/references/contracts.md#framesjson) và [frame-direction.md](references/frame-direction.md). Đầu vào là shotlist, assets và các ảnh hiện có; không tự dựng một câu chuyện mới từ prompt ảnh rời.

## Tạo từng cặp

1. Kiểm tra shot đã có start_state, end_state, motion, camera và reference_ids. Thiếu thông tin thì hoàn thiện mô tả từ script hoặc trả đúng phần cần bổ sung.
2. Xem ảnh tham chiếu. Tạo start frame với bố cục, ánh sáng, chủ thể và vùng trống cho chữ nếu brief cần.
3. Xem kết quả start trước khi tạo end. Dùng start cùng tham chiếu nhận diện để chỉnh/tạo end; giữ các yếu tố không được yêu cầu đổi. Cung cấp reference thực tế cho công cụ, không chỉ ghi trong prompt rằng đã dùng ảnh.
4. Dùng công cụ ảnh được hỗ trợ. Với imagegen, đọc skill và hướng dẫn tool imagegen khi áp dụng; không dựng giả ảnh bằng file placeholder. Nếu không có công cụ, bàn giao gói prompt và trạng thái còn thiếu.
5. So sánh cặp ảnh: khuôn mặt/trang phục/đạo cụ, số lượng chủ thể, hướng nhìn, vị trí, ánh sáng, tỉ lệ và khả năng chuyển động trong thời gian shot.
6. Cảnh đổi góc dùng bố cục mới với cùng trạng thái câu chuyện; cảnh nối liên tục mới cân nhắc chia sẻ frame. Giữ hai đường dẫn trong record dù cùng tham chiếu một file hợp lệ.
7. Lưu ảnh, prompt, phiên bản tham chiếu, frames.json và bảng tổng hợp storyboard có shot ID. Có thể dùng HTML gallery tham chiếu ảnh gốc để xem cạnh nhau; không cần sửa pixel để tạo bảng.

## Ý nghĩa của cặp frame

Đối chiếu `purpose`/`story_action` với script: frame đầu cho thấy trạng thái trước hành động, frame cuối cho thấy trạng thái sau đủ để hiểu chức năng shot. Giữ điểm nhìn, biểu cảm và đạo cụ hỗ trợ phát hiện hoặc lựa chọn của nhân vật. Shot tĩnh/giải thích có thể giữ cùng trạng thái; không thêm biến cố chỉ để hai frame khác nhau.

Với chi tiết được nhắc lại ở payoff, kiểm tra trạng thái xuyên các shot liên quan; không tự thêm/bỏ đạo cụ giữa chừng. Chừa khoảng cho chữ hậu kỳ, giữ hình mô phỏng khác với kết quả thật. Ảnh nhân vật vui hoặc màn hình mượt không được ngầm chứng minh sản phẩm đã chữa lỗi nếu script chỉ gợi ý kiểm tra.

Ghi review về ý nghĩa bên cạnh nhận diện/kỹ thuật. Nếu hình đẹp nhưng không thể hiện đúng hành động, sửa đúng frame; nếu mục tiêu shot mâu thuẫn, trả về shotlist/script thay vì tự viết lại câu chuyện qua prompt.

## Tiêu chí

- Mọi shot có start và end thật, xem được, đúng tỉ lệ đích. Nếu cần crop/reframe, thực hiện có chủ ý qua công cụ phù hợp, không âm thầm cắt chủ thể.
- Không bảo đảm nhận diện/chuyển động của clip chỉ từ ảnh. Ghi rõ đây là storyboard mục tiêu, phải kiểm tra lại sau render.
- Nếu cặp ảnh mâu thuẫn, sửa ảnh hoặc đề xuất chia shot trước khi gửi Flow.
- Ghi review từng frame/pair. Sửa S03 không tự tạo lại các shot không phụ thuộc S03.

Khi có cặp ảnh dùng được, chuyển sang [video-assemble](../video-assemble/SKILL.md) ở chế độ animatic trước render.
