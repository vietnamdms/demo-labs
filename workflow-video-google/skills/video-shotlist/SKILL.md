---
name: video-shotlist
description: "Phân kịch bản video thành scene và shot có ID, thời lượng, camera, hành động, start/end state và kiểu nối để tạo ảnh/video trên Flow. Dùng khi có kịch bản cần storyboard hoặc cần sửa shot theo timing lời dẫn. Không tạo ảnh hoặc render clip."
---

# Video Shotlist
Updated: 2026-10-17 11:03 +07

Nhận script và brief; đọc [hợp đồng shotlist](../video-workflow/references/contracts.md#shotlistjson). Dùng [continuity.md](references/continuity.md) khi có nối hành động/đổi góc.

## Thực hiện

1. Phân biệt chương (nội dung), scene (không gian/thời điểm), shot (một lựa chọn máy quay) và take (một lượt tạo). Không coi mỗi câu thoại là một clip.
2. Tạo shot_id/scene_id và beat_ids. Mọi ý bắt buộc, nhất là hook/payoff, phải có hình ảnh hoặc đoạn phủ lời tương ứng. Một beat có thể đi qua nhiều shot.
3. Cho mỗi shot: mô tả purpose, camera, chủ thể, start_state, end_state, motion, reference_ids, audio_mode, lời/âm thanh liên quan và transition sang shot sau.
4. Tập trung một hành động chính phù hợp thời lượng. Tách các thay đổi không gian/hành động quá lớn thành shot mới. Camera tĩnh không có nghĩa clip không chuyển động.
5. Ghi duration_s là thời gian dùng trong bản dựng; generation_duration_s là thời gian xin tạo, để null khi chưa biết model. Chừa trim handles khi cần, đừng đưa tất cả thời lượng tạo vào bản cuối.
6. Nháp dùng timing_basis=estimated. Khi có audio-plan đã đo, phân bổ shot theo cue và cập nhật timing_basis=measured. Video không lời có thể dùng action; không tự tạo lời dẫn để đủ biểu mẫu.
7. Với cảnh liên tục, kiểm tra hướng chuyển động, hướng nhìn, vị trí tay/đạo cụ, ánh sáng; chỉ dùng lại end frame cho shot sau khi góc máy và hành động thực sự phù hợp.

## Đầu ra và kiểm tra

Xuất shotlist.json và bảng shotlist.md cùng version. Bảng gồm shot/scene, beat, thời gian, camera, start/end, motion, âm thanh và kiểu nối. Kiểm tra tổng thời lượng so với brief, ghi lý do nếu cần thay đổi.

Không chọn một model chỉ dựa trên trí nhớ về giới hạn. Khi Flow preflight trả giới hạn mới, điều chỉnh shot hoặc thời gian tạo trong phạm vi đã thống nhất; giữ cặp start/end. Nếu thay đổi ảnh hưởng câu chuyện, quay lại beat liên quan thay vì âm thầm bỏ nội dung.
