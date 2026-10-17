---
name: video-visual-bible
description: "Chuẩn bị bộ tham chiếu nhân vật, sản phẩm, bối cảnh và phong cách, cùng hồ sơ/mẫu giọng cho video storyboard/Flow. Dùng khi cần giữ nhận diện và giọng nhân vật xuyên shot/tập hoặc tái sử dụng asset theo series; không phải skill tạo brand kit tổng quát."
---

# Video Visual Bible
Updated: 2026-10-17 14:49 +07

Nhận brief, script, shotlist và ảnh đã có. Đọc [hợp đồng assets](../video-workflow/references/contracts.md#assetsjson), dùng [asset-spec.md](references/asset-spec.md) khi lập bộ nhận diện.

1. Kiểm kê ảnh người dùng cung cấp và tài nguyên project; xem ảnh trước khi đánh giá. Không suy đoán nội dung từ tên file.
2. Định danh character/product/prop/location/style; ghi đặc điểm cố định, biến thể hợp lệ và phạm vi series/episode/scene. Cần ảnh rõ để kiểm soát nhận diện, không cần sinh mọi góc nếu shotlist không dùng.
3. Tái sử dụng asset phù hợp trước khi tạo mới. Với đối tượng cần đúng chi tiết, ưu tiên hình tham chiếu thực; ghi điều chưa thấy rõ thay vì bịa.
4. Nếu cần tạo hoặc chỉnh ảnh, dùng công cụ ảnh khả dụng và tuân theo skill/tool của công cụ đó. Flow image tools hoặc imagegen chỉ được coi là khả dụng khi thật sự có trong môi trường. Đừng viết script xử lý ảnh thay cho công cụ image editing khi công cụ quy định dùng imagegen.
5. Dùng ảnh nhân vật/sản phẩm nền sạch khi thích hợp; ảnh phong cách/bối cảnh không chứa chủ thể dư gây nhầm. Giữ hướng dẫn văn bản tương thích với ảnh.
6. Lưu assets.json và visual-bible.md: asset_id, image_paths, đặc điểm, scope, version và tình trạng kiểm tra. Ghi nguồn hoặc người cung cấp khi biết; không tự suy luận quyền sử dụng.

## Nhất quán về vai diễn

Với nhân vật có thoại hoặc hành động kể chuyện, ghi `performance_profile` bên cạnh nhận diện: vai trò, mong muốn, quan hệ, giọng nói, cách phản ứng và giới hạn diễn xuất cần giữ. Lấy ý đồ từ script; phân biệt đặc điểm được cung cấp/xác nhận với lựa chọn sáng tạo. Giữ nguyên `character_id` và liên kết asset qua `asset_id` khi có ảnh.

Nhân vật có thể thay đổi cảm xúc hoặc quyết định qua câu chuyện; giữ tính nhất quán không có nghĩa giữ một biểu cảm suốt video. Người giúp nên có thái độ phù hợp brief; với hướng dẫn thân thiện, tránh biến lời giải thích thành chế nhạo người chưa biết.

Đạo cụ phục vụ mở đầu/payoff cần nhận diện cố định và danh sách trạng thái hợp lệ. Shotlist sở hữu thời điểm đổi trạng thái. Ghi hướng dẫn phát âm/giọng làm đề xuất cho audio, không khẳng định model đã giữ được giọng từ một mô tả chữ.

## Hoàn thành

Với vai có yêu cầu giữ giọng, đọc [voice-continuity.md](../video-workflow/references/voice-continuity.md). Lưu `voice_profile` trực tiếp trong character asset theo [contracts](../video-workflow/references/contracts.md#giọng-và-nhịp-dựng): ID/version, căn tính giọng, mẫu thật, reference nền tảng, từ điển phát âm và review. Nghe mẫu trước khi ghi pass; hồ sơ đề xuất chưa có âm thanh để planned/unchecked. Tái dùng chuẩn series trước khi chọn giọng mới; narrator không lên hình có thể dùng character asset chỉ có mẫu audio.

Biến thể cảm xúc không được làm đổi căn tính giọng. Đổi giọng có chủ ý phải tăng version profile và đánh dấu cue/take dùng nó cần rà soát; ảnh chỉ bị ảnh hưởng khi nhận diện hình thực sự thay đổi. Không sao chép cả hồ sơ vào từng shot hoặc tạo một voice-bible song song với assets.json.

Xem các ảnh cần dùng trong shotlist, đánh giá nhận diện/phong cách và ghi lỗi cụ thể. Đã có prompt nhưng chưa có ảnh thì trạng thái planned/blocked, không ready. Nếu đổi nhận diện, đánh dấu các frame/clip dùng asset đó cần xem lại. [video-storyboard-frames](../video-storyboard-frames/SKILL.md) sở hữu bố cục từng shot; skill này sở hữu tài nguyên tham chiếu chung.
