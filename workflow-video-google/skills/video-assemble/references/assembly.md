# Dựng theo ba chế độ
Updated: 2026-10-17 14:49 +07

## Chuẩn bị âm thanh

Nhận file hoặc công cụ TTS thật. ffprobe có thể đo duration; thời gian speech/cue vẫn cần nghe/căn chỉnh. Ghi phát âm tên người, sản phẩm và từ viết tắt. Nếu chỉ có lời đọc thử, stage=scratch; không đổi tên file thành final để vượt điều kiện hoàn thành.

## Bản nháp từ ảnh

edit-plan.json phải ở root project và các đường dẫn nằm trong project. Ví dụ một shot:

```json
{
  "schema_version": "1.0", "project_id": "coffee-morning", "version": 1,
  "mode": "animatic", "width": 720, "height": 1280, "fps": 24,
  "audio_path": null,
  "segments": [
    {"shot_id": "S01", "start_frame": "frames/S01/start.png", "end_frame": "frames/S01/end.png", "duration_s": 4}
  ]
}
```

Helper render_animatic.py dùng ffmpeg/ffprobe từ PATH hoặc tham số --ffmpeg/--ffprobe, không tự cài dependency. Nó dựng frame tĩnh, encode H.264/yuv420p, padding giữ tỉ lệ, optional một track AAC. Số frame mỗi shot làm tròn theo fps, ít nhất hai frame; thông báo duration thực. Nếu audio dài hơn timeline ngoài sai số một frame thì lỗi; audio ngắn được pad silence, không tự kéo nhanh/chậm lời.

Đầu ra không được tồn tại; chọn tên phiên bản mới nếu đã có. Không tự ghi review=pass hoặc đổi manifest. Xem/nghe rồi mới đăng ký ready. Với âm thanh nhiều track/caption/transition dùng editor phù hợp, đừng truyền trường không hỗ trợ và nghĩ helper đã làm.

## Dựng cuối

Thay ảnh bằng clip đã chọn, lấy trim tại trạng thái nối thật. Không tự tăng tốc clip chỉ để khớp lời nếu ảnh hưởng hành động/âm thanh. Căn lời dẫn, giữ tiếng môi trường phù hợp, không để tiếng từ clip xung đột narration. Nếu cần chữ/logo chính xác, thêm và kiểm tra ở hậu kỳ.

Chọn export theo brief; kiểm tra duration, ratio, fps, codec và streams bằng ffprobe. Sau đó xem/nghe nội dung thực, đặc biệt hook, điểm nối và payoff. Metadata không phát hiện sai khuôn mặt, sai phát âm hoặc câu bị cắt giữa chừng.

Scenebuilder có thể sắp xếp, trim, preview và download scene theo [tài liệu Google](https://support.google.com/flow/answer/16935718?hl=en). Không coi đó là xác nhận mọi tính năng mix/subtitle đều có.

Animatic dựa trên thực hành storyboard có thời gian, xem [Adobe](https://www.adobe.com/creativecloud/animation/discover/animation.html). Không thể đo chất lượng video AI hoặc retention thực tế từ animatic.

## Nhịp câu chuyện và CTA

Dành thời gian cho phát hiện và phản ứng, nhất là ở payoff. Đối chiếu âm thanh/hình ảnh: hiệu ứng chiến thắng, nhạc giải tỏa hoặc gameplay mượt đặt ngay sau sản phẩm có thể tạo kết luận hiệu quả mà script không có. Điều chỉnh dựng để giữ đúng mức chắc chắn của nội dung.

Với nhiều vai, giữ speaker_id qua script → cue → shot. Nghe lượt chuyển vai và phát âm; hình phản ứng có thể đi với lời ngoài khung nếu chủ ý rõ. Cue mới hoặc câu rút gọn cần cập nhật nguồn chuẩn, không chỉ sửa phụ đề.

CTA nếu có phải đọc được ở bản xuất theo tỉ lệ đích, nói rõ lợi ích và chỉ tới tài nguyên thật. Mời đọc một bài cụ thể có thể rõ hơn chỉ nói “xem blog”; không giả định link bấm được hay link trong bio chưa xác minh.

Khi bàn giao kế hoạch đo theo yêu cầu, phân biệt điều người biên tập đã quan sát với phản hồi người xem chưa có. Lấy khung đo tại [content-strategy.md](../../video-workflow/references/content-strategy.md); không tự triển khai phân phối.

## Dựng nhanh mà giữ giọng

Đọc [pacing-short.md](../../video-workflow/references/pacing-short.md) cho short và [voice-continuity.md](../../video-workflow/references/voice-continuity.md) cho vai cần giọng nhất quán. Mẫu chuẩn có version trong assets, cue trong audio-plan, take trong renders; kiểm tra mapping trước dựng. Nghe nối cùng vai sau mix, không chỉ nghe các cảnh riêng lẻ.

1. Đo nguồn và đánh dấu câu, hành động, khoảng chờ có thể cắt. Thử rút head/tail và khoảng im không có chức năng từ take có sẵn trước. Không cắt ngang từ, phụ âm hoặc thao tác tạo payoff.
2. Với câu dài, giữ audio liên tục và phủ reaction/insert đúng ý. J-cut cho tiếng cảnh sau đến trước hình; L-cut giữ tiếng cảnh trước trên hình sau. Ghi audio_segments/audio_bridges theo [contracts](../../video-workflow/references/contracts.md#giọng-và-nhịp-dựng), giữ cue/speaker và kiểm tra khẩu hình khi người nói hiện lại.
3. Giữ speech playback_rate=1.0 mặc định. Không đổi pitch/formant để giả giọng giống mẫu; không tăng tốc toàn video chỉ để đạt mục tiêu. Nếu cần viết gọn câu, cập nhật script/cue và đánh dấu audio/clip liên quan cần sửa trước khi coi timeline đồng bộ.
4. Cân gain/EQ vừa đủ để rõ lời, nhạc/SFX không che thoại hoặc tạo suy luận sai. Nghe lại để không làm biến dạng căn tính giọng. Chỉ đổi mix không tự buộc render lại ảnh/clip còn đúng input.
5. Caption chia theo ý và audio thực, xem trên khung xuất nhỏ; giảm nhãn lặp nguyên lời. Safe zone, nhãn giả định, CTA và dấu nền tảng phải còn rõ; không crop/xóa dấu để có thêm chỗ chữ.
6. Ghi version timeline, duration đo thực, nguồn audio/rate, voice_review theo vai và lỗi còn lại. Nếu chưa nghe, bản xuất là review-copy với review unchecked; file H.264/AAC hợp lệ không tự là final đạt.

Editor/FFmpeg cho final phải được kiểm tra khả năng với công việc thực tế. Không gửi audio_segments, J/L-cut, playback_rate hoặc caption cho helper animatic rồi tuyên bố đã render các hiệu ứng đó. Với long, dùng thay đổi hình theo câu hỏi/chương và giữ khoảng giải thích cần thiết.
