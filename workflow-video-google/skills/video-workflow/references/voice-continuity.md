# Giữ giọng nhân vật xuyên cảnh và xuyên tập
Updated: 2026-10-17 14:51 +07

Đọc khi project có thoại/giọng kể và cần nhất quán. Dữ liệu do [contracts.md](contracts.md#giọng-và-nhịp-dựng) sở hữu; thao tác model/mode do [Flow runbook](../../video-flow-generate/references/flow-runbook.md) sở hữu. Với video none/ambient, không tạo hồ sơ giọng không cần thiết.

## Rule

Mỗi nhân vật có thoại được ánh xạ tới một hồ sơ giọng có version và một mẫu âm thanh chuẩn đã được nghe kiểm tra. Dùng cùng hồ sơ xuyên cảnh và xuyên tập của series. Giữ căn tính giọng, âm sắc, âm vực nền, giọng vùng và cách phát âm tên riêng; cảm xúc, nhấn nhá và độ mạnh được thay đổi theo diễn xuất. Take đổi giọng hoặc hoán đổi người nói phải sửa; chưa nghe đối chiếu thì để review=unchecked, không selected.

Giữ căn tính có thể nhận ra, không đòi waveform giống nhau cho câu khác nhau. Mô tả chữ, character image, prompt lặp lại hoặc cùng model không chứng minh giọng đã nhất quán. Không gọi hồ sơ planned là đã khóa.

## Lập mẫu và hồ sơ

1. Tìm giọng đã được người dùng chọn hoặc mẫu đã duyệt của series trước. Không tự chọn một giọng mới nếu đã có chuẩn phù hợp. Với project cũ chưa nghe duyệt, ghi ứng viên và phần còn thiếu.
2. Tái dùng đoạn một người nói rõ từ media được phép dùng; chọn đoạn đủ nghe căn tính giọng, không lẫn vai khác hoặc bị nhạc che. Ghi file, đoạn thời gian, lời mẫu, nguồn và kết quả nghe. Không dùng file im lặng/placeholder làm mẫu.
3. Nếu cần sinh mẫu, dùng model/công cụ trong phạm vi brief và ngân sách. Lưu voice reference ID thực nếu nền tảng có; ID chưa biết để null. Không bịa voice ID hoặc coi tên nhân vật là ID giọng.
4. visual-bible lưu voice_profile trong character asset; script dùng character_id/speaker_id và hướng dẫn diễn xuất, audio-plan nối cue với voice_id/version. Narrator cần giữ giọng cũng có character asset cho âm thanh, image_paths có thể rỗng nếu không lên hình.
5. Nghe mẫu và chốt locked_features, allowed_performance_changes, phát âm tên riêng/từ viết tắt. Ví dụ dự án Tiny cần thống nhất Tiny, Wi-Fi, ping, FPS, LAN; đây là ví dụ theo brief, không là từ điển bắt buộc của mọi project.

Lượt sinh mẫu ban đầu được dùng hồ sơ planned và stage scratch để tạo đầu vào còn thiếu trong ngân sách; không coi đó là clip final hoặc bắt phải có mẫu đã duyệt trước khi có thể sinh mẫu. Chốt mẫu/version sau khi nghe rồi mới dùng cho production và pilot kiểm tra xuyên take.

Với series, chỉ ra project/tài nguyên chuẩn có thể truy cập; import bản dùng trong tập cùng provenance/version. Thay đổi mẫu chuẩn không được âm thầm thay căn tính giọng của các tập đang làm.

## Chuẩn bị và sinh thoại

Đối chiếu speaker → character → asset → voice_profile trước render. Một cue chỉ có một người nói. Ghi rõ vai ngoài khung; người nghe không nói hoặc mấp máy theo câu của người nói. Prompt giữ nguyên lời chuẩn, voice direction và reference thực sự gắn vào request; cảm xúc thuộc cue, không phải giọng mới.

Khi route/model chưa có bằng chứng giữ được giọng qua nhiều take, kiểm tra bằng pilot có ít nhất hai câu khác nhau ở các lượt khác nhau cho từng vai cần giữ giọng. Tái dùng take đã có nếu đủ bằng chứng; không mặc định sinh thêm pilot cho mỗi shot. Pilot tính vào ngân sách và retry; pilot đạt không thay thế review các take sau.

Nếu model/mode không hỗ trợ tổ hợp frame/voice bắt buộc, hoàn thiện các đầu vào độc lập và ghi rõ xung đột trước batch thoại. Không tự bỏ end frame, chuyển nhà cung cấp, hoặc gắn nhãn voice-locked từ prompt-only. Chỉ thay route khi route mới vẫn đáp ứng brief hoặc thay đổi yêu cầu đã được người dùng cho phép.

## Nghe duyệt và sửa

Nghe toàn bộ phần thoại cần chọn và nghe nối các cảnh của cùng vai với mẫu chuẩn. Đối chiếu đúng speaker, âm sắc/âm vực nền/giọng vùng, phát âm, nội dung, độ tự nhiên và khẩu hình ở phần dùng trong bản dựng. Tách cảm xúc hợp lệ khỏi đổi căn tính giọng.

- pass: đã nghe đối chiếu, ghi mẫu/version, đoạn đã kiểm tra và nhận xét cụ thể.
- needs-revision: đã nghe thấy lệch giọng/đổi vai/sai phát âm hoặc khẩu hình; ghi lỗi, đoạn và bước sửa.
- unchecked: chưa nghe được, mẫu chưa duyệt hoặc bằng chứng chưa đủ. ASR/ffprobe không thay phần nghe này.

`voice_review` chỉ đánh giá giọng; overall review vẫn phải đạt hình, lời, hành động và dependency. Không chọn clip chỉ vì voice_review pass. Khi chưa thể nghe, bàn giao bản xem duyệt và ghi giới hạn; không tạo vòng hỏi duyệt người dùng nếu agent có khả năng kiểm tra trong phạm vi hiện tại.

Tăng nhịp bằng biên tập nội dung/hình trước. Giữ speech playback_rate=1.0 mặc định; không đổi pitch, formant hoặc căn tính để ép thời lượng. Nếu yêu cầu sáng tạo cho phép đổi giọng, tăng version hồ sơ, cập nhật mẫu rồi đánh dấu đúng cue/take/bản dựng phụ thuộc. Đổi gain/EQ để cân mix không tự là thay căn tính giọng; vẫn nghe lại để tránh méo tiếng.
