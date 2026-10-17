# Thực thi Google Flow
Updated: 2026-10-17 14:49 +07

## Preflight theo lần chạy

1. Xác nhận đúng project và tài khoản qua giao diện/công cụ cho phép; không lấy thông tin bí mật từ profile trình duyệt.
2. Chọn thao tác Video/Frames tương ứng UI thực tế. Quan sát hỗ trợ first+last, tỉ lệ, duration, resolution, audio và số outputs. Tên nút có thể đổi; đừng click theo tọa độ cũ không quan sát.
3. Lưu checked_at timezone, model/mode và thông tin credit hiện thấy. Tài liệu hỗ trợ đọc lại khi có điểm chưa rõ, không cần nghiên cứu lại mọi lượt nếu snapshot còn đúng và UI không đổi.
4. Đối chiếu đầu vào đã xem, version và giới hạn credit. Nếu giao diện tự đổi model, kiểm tra lại trước submit.

Nguồn chính thức (kiểm tra lần đầu khi xây skill: 2026-10-17; không phải cam kết tính năng tài khoản):
- [Create videos](https://support.google.com/flow/answer/16353334?hl=en)
- [Models/features](https://support.google.com/flow/answer/16352836?hl=en)
- [Edit/Scenebuilder](https://support.google.com/flow/answer/16935718?hl=en)

Với yêu cầu giữ giọng, đọc [voice-continuity.md](../../video-workflow/references/voice-continuity.md). Tài liệu Create videos đối chiếu ngày 17/10/2026 hướng dẫn Omni Flash → Video → Ingredients → Voices, chọn preset/custom voice rồi tham chiếu `@Voice`; hiện ghi voice reference chỉ dùng với Ingredients, mode khác sẽ báo lỗi. Models/features liệt kê các tính năng riêng không chứng minh voice reference đi cùng first+last frames.

Kiểm tra model, mode, vùng/tài khoản và tổ hợp thật trước khi submit. Ghi supports_voice_reference, voice_reference_modes và supports_first_last_with_voice_reference theo [contracts](../../video-workflow/references/contracts.md#giọng-và-nhịp-dựng), chưa biết để null. Nếu UI/tài liệu hiện tại không hỗ trợ tổ hợp bắt buộc, không chạy batch thoại hoặc tự đổi Frames sang Ingredients. Tiếp tục chuẩn bị phần độc lập; nêu phương án cùng tác động tới brief. Route khác chỉ dùng khi vẫn đáp ứng yêu cầu hoặc thay đổi đã được cho phép. Nếu cần track narration riêng, phối hợp assemble; sync-dialogue cần kiểm tra khẩu hình thực tế.

Khi tổ hợp hỗ trợ và giọng chưa có bằng chứng xuyên take, pilot trong ngân sách với câu khác nhau của từng vai, nghe với mẫu trước khi nhân rộng. Không mặc định mọi model Google dùng chung một voice ID; khi đổi model phải kiểm tra mapping/căn tính lại. Bản sao prompt chỉ là voice direction, không coi là reference đã được gắn.

## Prompt chuyển động

Mô tả hành động nối start/end, thời điểm hoặc nhịp khi hữu ích, camera, môi trường giữ nguyên và sound design yêu cầu. Khi ảnh đã quyết định bố cục, đừng mô tả lại theo cách mâu thuẫn. Ví dụ: “Tay trái nâng tách lên chậm, hơi nước bốc nhẹ; camera tiến rất nhẹ; ánh sáng sáng sớm ổn định; tiếng căn phòng yên, không lời thoại.”

## Job và chi phí

Fingerprint dựa trên shot/version, frame/version, prompt, model, duration, mode, output count và voice_inputs/version mẫu-profile nếu có. Có thể băm JSON canonical bằng SHA-256; hash chỉ nhận diện request, không là cơ chế chống gửi trùng phía dịch vụ. Một yêu cầu trùng có thể vẫn bị tính phí nếu gửi lại.

Trước submit ghi planned. Sau submit ghi submitted cùng dấu vết take. Nếu UI biến mất/lỗi mạng, unknown; khi tiếp tục kiểm tra lịch sử/project trước khi quyết định failed hay gửi mới. Không có job ID thì lưu URL, mô tả vị trí/timestamp và prompt đủ đối chiếu.

Ngân sách gồm generation cost × outputs và số lượt sửa; upscale hoặc thao tác khác có thể có chi phí riêng. Không dùng giá API Veo để tính credit Flow. Chưa biết chi phí thì không gắn 0.

## Review và sửa

Lỗi nhận diện/bố cục: xem lại frame và asset. Chuyển động quá gấp: xem duration/action. Frame tốt nhưng động tác sai: sửa prompt có mục tiêu. Sai câu thoại: kiểm tra script/audio và model; không gắn pass từ việc chỉ có âm thanh.

Sửa tối thiểu có ích, giữ take cũ và lý do loại. Dừng khi đạt hoặc hết giới hạn; báo phần còn thiếu bằng dữ liệu thực.

Với thoại cần giữ giọng, nghe từng vai với mẫu và nghe nối các take; ghi voice_review theo vai với version và thời điểm kiểm tra. Lệch giọng hoặc đổi vai thì needs-revision; chưa nghe thì unchecked. ASR chỉ hỗ trợ so lời, không đánh giá căn tính giọng. Đừng sửa lỗi giọng bằng thay pitch/tốc độ toàn clip; sửa input/profile/model route phù hợp trong retry được phép. Giọng pass không thay overall review hình/thoại/hành động.

## Ý đồ kể chuyện trong prompt và take

Ghi thứ tự hành động và phản ứng quan trọng từ shot: nhận ra chi tiết → dừng lại → quyết định, cùng ai nói và ai nghe. Chỉ yêu cầu phần diễn tiến nằm trong shot và vừa thời lượng. Không nhồi toàn bộ đường dây câu chuyện vào một lượt render.

Review lấy từ clip thật: hành động mục tiêu có xảy ra, đúng vai có phát hiện/quyết định, câu nói có đúng và điểm trim có giữ được payoff? Trạng thái review chỉ pass sau khi quan sát phần liên quan. Không chọn một clip đẹp nhưng đổi ý nghĩa, đổi người nói hoặc thêm cam kết sản phẩm.

Nếu cần sửa lời, quay lại script/audio; nếu cần sửa trạng thái đầu–cuối, quay lại shot/frame. Giữ take cũ và lý do loại để không lặp lại lỗi; chi phí sửa vẫn thuộc budget và retry đã chốt.
