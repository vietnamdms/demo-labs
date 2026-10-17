---
name: video-script-short
description: "Viết hoặc sửa kịch bản TikTok/YouTube Shorts cho workflow storyboard và Google Flow. Tạo hook hình ảnh/lời nói, nội dung, payoff, lời dẫn và beat có ID để phân shot. Dùng khi cần kịch bản video ngắn có thể chuyển sang sản xuất; không phụ trách render hoặc đăng video."
---

# Video Script Short
Updated: 2026-10-17 13:48 +07

Viết kịch bản đầy đủ phục vụ sản xuất. Đọc [hợp đồng script](../video-workflow/references/contracts.md#scriptjson) khi xuất dữ liệu; dùng [mẫu short](references/writing.md) để chọn cấu trúc phù hợp, không ép mọi ý tưởng theo một công thức.

## Thực hiện

1. Nhận brief và tài nguyên/nguồn sẵn có. Ghi platform `tiktok` hoặc `youtube-shorts`; nếu dùng cả hai, giữ core script và ghi biến thể có lý do. Không tự thêm nền tảng hoặc CTA bán hàng.
2. Xác định một ý chính và điều khán giả được nhận. Với thông tin thực tế chưa có bằng chứng, kiểm chứng hoặc diễn đạt đúng mức chắc chắn trước khi viết hook.
3. Viết hook xuất hiện ngay khi video mở: hình ảnh, lời nói và chữ nếu cần. Hook có lời hứa cụ thể; gắn hook.beat_id và payoff_beat_id. Có thể đề xuất vài phương án khi hữu ích, nhưng chọn một bản chính để downstream không tự chọn nhầm.
4. Viết các beat content đưa tới payoff, rồi ending/CTA nếu phù hợp. Câu nói phải là lời có thể đọc, chỉ dẫn hình ảnh phải là hành động nhìn thấy được. Không dùng đoạn tóm tắt thay cho bản lời đọc đầy đủ.
5. Ước lượng thời gian theo cách kể và nhịp hành động; đánh dấu estimated. Với video có lời, chuyển bản đọc sang prepare-audio trước khi chốt timing. Không coi số từ là thời lượng đã đo.
6. Xuất script.json, bản đọc script.md cùng version; mỗi beat có ID ổn định. Giữ ID của beat được sửa, dùng ID mới cho nội dung mới.

## Thiết kế câu chuyện

Đọc [thiết kế nội dung](../video-workflow/references/content-strategy.md) để ghi `content_strategy`: hoàn cảnh, lợi ích, một ý chính và kiểu kể. Với tiểu phẩm, xác định mong muốn → trở ngại/hiểu nhầm → phát hiện → lựa chọn/hành động mới. Với giải thích/hướng dẫn, tổ chức câu hỏi → thông tin/bước làm → câu trả lời/cách kiểm tra, không ép thêm nhân vật.

Mỗi beat phải đóng góp vào tiến trình. Để nhân vật đại diện khán giả có quyền phát hiện hoặc quyết định; người giúp không chỉ đọc một đoạn quảng cáo. Payoff nên thể hiện bằng hành động hoặc câu trả lời cụ thể. Chọn vai trò sản phẩm và CTA theo nhu cầu người xem, giữ nguyên mục tiêu người dùng đã giao.

Khi có nhiều người nói, khai báo `characters` và `speaker_id` theo [hợp đồng thoại](../video-workflow/references/contracts.md). Đọc lại lời theo từng vai, kiểm tra phản hồi có tự nhiên và giữ đúng tính cách; không chia đều thoại máy móc. Ghi `story_function` và `viewer_change` cho beat khi cần chuyển ý đồ sang shot.

## Kiểm tra và bàn giao

- Hook có tạo đúng kỳ vọng; payoff có thực sự trả lời? Tránh hứa điều kịch bản không thể chứng minh.
- Hình ảnh có thể hiểu được và có vai trò trong câu chuyện? Nếu cần xem không bật âm thanh, mô tả chữ thiết yếu để hậu kỳ thêm.
- Có đủ thời gian cho câu nói và hành động? Chưa đo thì ghi rõ chưa chốt timing.
- Không gọi một hook là thắng A/B hoặc chắc chắn viral khi chưa có dữ liệu.
- Chỉ sở hữu nội dung và nhịp kể. Shotlist sở hữu camera/trạng thái từng shot; assemble sở hữu file lời dẫn, phụ đề và timeline.

Nếu người dùng chỉ yêu cầu kịch bản, hoàn thành kịch bản và dừng đúng phạm vi. Nếu đang chạy project, ghi manifest và chuyển đầu ra cho video-shotlist.
