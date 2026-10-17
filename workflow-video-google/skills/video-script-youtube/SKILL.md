---
name: video-script-youtube
description: "Viết hoặc sửa kịch bản YouTube dài cho workflow storyboard/Google Flow: concept tiêu đề và thumbnail, hook, chương, lời dẫn đầy đủ và payoff. Dùng cho video YouTube nhiều phần cần phân cảnh; video Shorts dùng video-script-short."
---

# Video Script YouTube
Updated: 2026-10-17 14:49 +07

Đọc [hợp đồng script](../video-workflow/references/contracts.md#scriptjson) khi xuất dữ liệu. Dùng [hướng dẫn chương](references/writing.md) khi cấu trúc video dài.

## Thực hiện

1. Từ brief, xác định câu hỏi trung tâm, người xem, mục tiêu, thời lượng và thông tin cần kiểm chứng.
2. Viết concept tiêu đề, thumbnail và lời hứa nội dung trước bản đầy đủ. Đây là concept phục vụ kịch bản; không tự tạo thumbnail, SEO package hoặc đăng bài.
3. Viết hook bằng tình huống, kết quả mẫu, câu hỏi hoặc mâu thuẫn phù hợp. Gắn vào payoff cụ thể. Hook không cần cùng độ dài ở mọi video; tránh mở đầu kéo dài không phục vụ câu chuyện.
4. Lập chương theo tiến trình hiểu hoặc diễn biến. Mỗi chương có purpose và câu hỏi được giải đáp; chapter_id ổn định. Không thêm chương chỉ để đạt số lượng cố định.
5. Viết đầy đủ spoken/visual cho từng beat: hook, content, payoff và ending. Ví dụ, dẫn chứng và chuyển ý phải được viết thật. Chia công việc thành từng chương nếu dài nhưng hoàn thành toàn bộ phạm vi đã yêu cầu.
6. Ghi thời lượng estimated; tách lời dẫn liên tục khỏi hình minh họa. Một câu có thể phủ qua nhiều shot. Sau bản đọc thử, sửa nhịp chứ không tăng tốc giọng để ép khớp máy móc.
7. Xuất script.json và script.md cùng version, có concept title/thumbnail, chapter map, hook liên kết payoff, nguồn cho tuyên bố thực tế.

## Tiến trình nội dung dài

Dùng [thiết kế nội dung](../video-workflow/references/content-strategy.md) để chốt `content_strategy`, câu hỏi trung tâm, lợi ích và cách kể. Giai đoạn hành trình chỉ dùng cho nội dung marketing. Tiêu đề, thumbnail concept và hook cùng hứa một kết quả mà video thực sự có thể cung cấp.

Mỗi chương xác định `viewer_question`, `takeaway`, `evidence_plan` và `transition_reason` theo hợp đồng. Viết ví dụ, giải thích và kết luận nhỏ thành các beat thật; nếu còn thiếu bằng chứng, nêu điều chưa xác định hoặc diễn đạt thành kế hoạch, không trình bày như kết quả đã có. Chương sau phát triển điều người xem vừa hiểu.

Với nhiều nhân vật, dùng `characters` và `speaker_id` theo [hợp đồng thoại](../video-workflow/references/contracts.md). Cho từng vai đóng góp phát hiện/thử nghiệm/quyết định theo câu chuyện; giữ giọng và quan hệ nhất quán. CTA giúp thực hiện bước tiếp theo; không tự thêm lời mời mua hoặc đăng ký vào mọi chương.

## Kiểm tra

Với narrator hoặc nhân vật tái diễn, đọc [giữ giọng](../video-workflow/references/voice-continuity.md) và tái dùng cùng hồ sơ qua chương/tập. Lời và speaker_id phải nối được tới mẫu/phiên bản giọng trong assets/audio-plan; mô tả giọng bằng chữ không tự chứng minh đã khóa giọng.

Nếu yêu cầu nhanh hơn, rút mở đầu, luận điểm lặp và khoảng chờ; dùng ví dụ, hình phủ và chuyển câu hỏi để giữ tiến triển. Có thể ghi `content_strategy.pacing.mode=brisk`, nhưng giữ thời gian hiểu, kiểm tra bằng chứng và phản ứng. Không nhập lịch cắt 1–2 giây hoặc mục tiêu thời lượng short vào video dài.

- Phần mở đầu đáp ứng kỳ vọng concept title/thumbnail; không chỉ gây tò mò mà không giải đáp.
- Các chương phát triển nội dung, không lặp luận điểm để kéo dài video.
- Hook phụ hoặc chuyển nhịp xuất hiện khi có lý do nội dung; không ép lịch gây tò mò/cắt cảnh theo phút.
- Script có lời đọc đầy đủ và hình ảnh khả thi, đủ dữ liệu để video-shotlist làm việc.
- Chưa có dữ liệu khán giả thì chỉ đề xuất phương án, không hứa CTR/retention cụ thể.

Rà soát nội dung trước khi chuyển sang [video-shotlist](../video-shotlist/SKILL.md). Chỉ nghiên cứu thêm khi cần chứng cứ; không mở rộng thành chiến dịch phân phối ngoài yêu cầu.
