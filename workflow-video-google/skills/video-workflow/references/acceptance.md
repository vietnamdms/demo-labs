# Nghiệm thu khi triển khai hoặc sửa bộ skill
Updated: 2026-10-17 14:49 +07

Không cần render dịch vụ trả phí để kiểm tra cấu trúc. Đánh giá riêng hành vi viết nội dung, kiểm tra dữ liệu và chất lượng media thực tế.

1. Short: script có một hook rõ, payoff tồn tại phía sau; mọi beat được shotlist phủ. Gán payoff tới beat không tồn tại phải bị validator chặn.
2. Long: có concept title/thumbnail và chapter mục đích rõ; mọi beat thuộc chương hợp lệ; không dừng ở dàn ý khi người dùng yêu cầu script đầy đủ.
3. Frames: mỗi shot có đủ hai ảnh; ảnh thiếu ở artifact ready phải lỗi. Mô tả ảnh không được xem là ảnh thực.
4. Continuity: có cảnh nối liên tục và cảnh đổi góc; kiểm tra không ép end S01 thành start S02 nếu khác bố cục.
5. Sửa S03: dependency downstream cần revision, S01 không liên quan giữ nguyên; version cũ không được coi mới.
6. Flow: model thiếu tổ hợp frame/voice phải báo đúng; không tự bỏ end frame. Timeout không tự retry nếu chưa kiểm tra kết quả cũ.
7. Clip: downloaded nhưng review unchecked không đủ để selected. File tồn tại nhưng sai chuyển động cần review needs-revision.
8. Audio: audio dài hơn animatic phải báo, không tự cắt lời. Final không âm thanh nếu brief bắt buộc lời dẫn phải ghi chưa hoàn tất.
9. Export: helper animatic chỉ chấp nhận mode animatic; không ghi đè file có sẵn; path không thoát project.
10. Bộ skill: frontmatter hợp lệ, link nội bộ có thật, UI prompt gọi đúng tên skill, không còn scaffold TODO.

## Tình huống giữ giọng và tăng nhịp

Các ca sau kiểm tra quyết định và đầu ra khi triển khai, không phải kết quả media đã chạy. Helper chưa tự duyệt các extension voice/pacing của [contracts](contracts.md#giọng-và-nhịp-dựng).

| Tình huống | Kết quả cần quan sát |
| --- | --- |
| Hai câu khác nhau của cùng vai ở hai take; cảm xúc đổi nhưng căn tính giữ | Hồ sơ/mẫu/version được tái dùng; nghe đối chiếu và ghi review từng take, không đòi waveform trùng |
| Take đúng lời qua ASR nhưng giọng bị đổi | voice_review needs-revision, không selected; không gắn pass từ ASR |
| Hai vai đổi lượt nhanh hoặc thoại ngoài khung | Cue/speaker/reference không bị hoán đổi; người nghe không nói nhép câu của vai còn lại |
| Mẫu chuẩn chưa có audio hoặc người làm chưa nghe được | Profile/take unchecked, không công bố đã khóa giọng; bàn giao phần độc lập |
| Frames và Voice không dùng chung được trong model/mode hiện tại | Snapshot ghi đúng giới hạn; không batch thoại, bỏ end frame hoặc đổi nhà cung cấp trái brief |
| Đổi profile giọng của một vai | Cue/take/bản dựng dùng profile cũ cần rà; frame và vai không liên quan giữ nguyên; dependency không chu trình |
| Rút short bằng trim/audio bridge từ take hiện có | Không mất câu/động tác tạo payoff; speaker đúng, audio/caption khớp; speech rate giữ tự nhiên |
| Tập Tiny 30–33 giây đề xuất không chứa đủ câu theo đo thực | Điều chỉnh lời có version hoặc mục tiêu thời gian; không ép tốc độ và không gọi mục tiêu là timing measured |
| YouTube dài nhiều chương | Cùng narrator/profile xuyên chương; không ép cắt 1–2 giây theo short |
| Project schema 1.0 cũ thiếu voice/pacing | Vẫn đọc và dùng phần hợp lệ; bổ sung khi áp dụng rule mới, không tự gắn review đạt |

Nếu viết test helper trong tương lai, kiểm tra mapping/version/invalidation và các từ chối observable bằng fixture thật; không test bằng đếm từ khóa hay so khớp câu hướng dẫn. Chất lượng căn tính giọng, nhịp và khẩu hình cần nghe/xem media thực riêng.
