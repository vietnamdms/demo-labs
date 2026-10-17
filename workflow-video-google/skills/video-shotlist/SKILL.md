---
name: video-shotlist
description: "Phân kịch bản video thành scene và shot có ID, thời lượng, camera, hành động, start/end state và kiểu nối để tạo ảnh/video trên Flow. Dùng khi có kịch bản cần storyboard hoặc cần sửa shot theo timing lời dẫn. Không tạo ảnh hoặc render clip."
---

# Video Shotlist
Updated: 2026-10-17 14:49 +07

Nhận script và brief; đọc [hợp đồng shotlist](../video-workflow/references/contracts.md#shotlistjson). Dùng [continuity.md](references/continuity.md) khi có nối hành động/đổi góc.

## Thực hiện

1. Phân biệt chương (nội dung), scene (không gian/thời điểm), shot (một lựa chọn máy quay) và take (một lượt tạo). Không coi mỗi câu thoại là một clip.
2. Tạo shot_id/scene_id và beat_ids. Mọi ý bắt buộc, nhất là hook/payoff, phải có hình ảnh hoặc đoạn phủ lời tương ứng. Một beat có thể đi qua nhiều shot.
3. Cho mỗi shot: mô tả purpose, camera, chủ thể, start_state, end_state, motion, reference_ids, audio_mode, lời/âm thanh liên quan và transition sang shot sau.
4. Tập trung một hành động chính phù hợp thời lượng. Tách các thay đổi không gian/hành động quá lớn thành shot mới. Camera tĩnh không có nghĩa clip không chuyển động.
5. Ghi duration_s là thời gian dùng trong bản dựng; generation_duration_s là thời gian xin tạo, để null khi chưa biết model. Chừa trim handles khi cần, đừng đưa tất cả thời lượng tạo vào bản cuối.
6. Nháp dùng timing_basis=estimated. Khi có audio-plan đã đo, phân bổ shot theo cue và cập nhật timing_basis=measured. Video không lời có thể dùng action; không tự tạo lời dẫn để đủ biểu mẫu.
7. Với cảnh liên tục, kiểm tra hướng chuyển động, hướng nhìn, vị trí tay/đạo cụ, ánh sáng; chỉ dùng lại end frame cho shot sau khi góc máy và hành động thực sự phù hợp.

## Chuyển ý nghĩa thành hình ảnh

Đọc `script.content_strategy` và chức năng các beat trước khi chọn góc. Viết `purpose` bằng điều shot giúp người xem nhận ra; `story_action` là hành động nhìn thấy thực hiện mục đích đó. Với shot giải thích, sơ đồ hoặc chi tiết được chỉ ra cũng có thể thực hiện chức năng này, không cần thêm diễn xuất.

Mô tả phản ứng sau thông tin quan trọng và thời gian cho payoff. Khi một đạo cụ liên kết đầu–cuối, ghi trạng thái qua các shot tại `continuity.props_state`; giữ nguyên nếu chưa có hành động đổi. Đánh dấu ví dụ giả định, hình mô phỏng và bằng chứng thực khác nhau trong visual/notes.

Đối chiếu `speaker_id`, lời thoại và cue với script/audio-plan. Giữ nguyên người nói khi đổi góc; shot phản ứng có thể để người nói ngoài khung, phải ghi rõ. Nếu một shot chứa nhiều lượt thoại, dùng danh sách cue theo thứ tự thay vì gán toàn bộ lời cho một vai. Không gộp phản ứng hoặc cắt phần giải thích làm thay đổi ý nghĩa.

## Đầu ra và kiểm tra

Đọc [pacing short](../video-workflow/references/pacing-short.md) khi brief cần nhịp nhanh. Ghi `cut_constraints` cho hành động/câu phải giữ, `coverage_role` cho main/reaction/insert và `audio_bridge` khi lời đi qua điểm cắt theo [contracts](../video-workflow/references/contracts.md#giọng-và-nhịp-dựng). Thử dựng từ take đã có trước khi đề xuất job mới; thời gian sinh clip không quyết định thời gian dùng cuối.

Khi đổi góc hoặc cho lời chạy qua cảnh phản ứng, giữ speaker/cue và mapping giọng theo [voice-continuity.md](../video-workflow/references/voice-continuity.md). Ghi vai ngoài khung, không đặt lời lên miệng vai khác. Chừa thời gian thật để giữ payoff; chỉ thay góc/cắt nhanh nếu trạng thái đạo cụ và tiến trình còn đúng.

Xuất shotlist.json và bảng shotlist.md cùng version. Bảng gồm shot/scene, beat, thời gian, camera, start/end, motion, âm thanh và kiểu nối. Kiểm tra tổng thời lượng so với brief, ghi lý do nếu cần thay đổi.

Không chọn một model chỉ dựa trên trí nhớ về giới hạn. Khi Flow preflight trả giới hạn mới, điều chỉnh shot hoặc thời gian tạo trong phạm vi đã thống nhất; giữ cặp start/end. Nếu thay đổi ảnh hưởng câu chuyện, quay lại beat liên quan thay vì âm thầm bỏ nội dung.
