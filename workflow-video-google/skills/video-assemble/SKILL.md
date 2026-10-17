---
name: video-assemble
description: "Chuẩn bị lời dẫn và timing, dựng animatic từ cặp frame hoặc dựng video cuối từ clip của project storyboard/Google Flow. Dùng khi cần đọc thử, kiểm tra nhịp trước render, ghép clip, âm thanh và phụ đề; không tự đăng video."
---

# Video Assemble
Updated: 2026-10-17 13:48 +07

Chọn đúng mode `prepare-audio`, `animatic`, `final` theo yêu cầu và đầu ra hiện có. Đọc [hợp đồng audio/edit](../video-workflow/references/contracts.md#audio-planjson), rồi [assembly.md](references/assembly.md) cho mode đang làm.

## prepare-audio

Nhận lời dẫn/thoại từ script. Nhận file thu hoặc dùng công cụ giọng nói khả dụng trong phạm vi được phép; không giả lập đã có audio khi chỉ có text. Đo thời lượng file bằng công cụ media, nghe cách phát âm tiếng Việt/tên riêng, ghi cues và chỗ nghỉ. Phân biệt narration, sync-dialogue, ambient, none. Đồng bộ khẩu hình không thể giải quyết chỉ bằng ghép voiceover lên miệng đang nói khác.

Xuất audio-plan.json với path, duration_s đo được, cue timings, script version và stage scratch/final. Nếu video không lời, ghi mode none/ambient và mốc nhịp hành động. Nếu thay script, timing cũ cần rà soát. Chuyển timing cho video-shotlist.

## animatic

Nhận cặp frame đã xem, shotlist và audio thử nếu có. Tạo edit-plan.json mode animatic, thứ tự shot, thời gian và đường dẫn ảnh. Ghép start/end theo nhịp để đánh giá câu chuyện; bản dựng bằng ảnh không thể xác nhận chất lượng chuyển động AI.

Helper có sẵn chỉ dựng nháp bằng ảnh, không gọi dịch vụ:

```bash
python3 scripts/render_animatic.py /absolute/project-dir/edit-plan.json --output /absolute/project-dir/animatic.mp4
```

Lệnh dùng đường dẫn script tuyệt đối nếu cwd không phải thư mục skill. Helper cần ffmpeg/ffprobe, giữ tỉ lệ bằng padding, cắt giữa start/end ở nửa thời lượng shot, tùy chọn một track audio. Không hỗ trợ mix nhiều track, captions hoặc motion interpolation. Đọc [assembly.md](references/assembly.md) trước khi chạy.

Xem bản nháp, kiểm tra hook, khả năng hiểu, tổng thời gian và payoff. Sửa đúng shot/beat nếu lệch nhịp. Ghi review; mốc này không tự yêu cầu phê duyệt người dùng.

## final

Nhận selected takes và audio final nếu brief cần. Chọn công cụ dựng khả dụng, giữ trim điểm vào/ra đã định và lời dẫn liên tục qua shot nếu phù hợp. Cân âm thanh, thêm chữ/phụ đề từ nội dung đúng; không lấy chữ AI lỗi trong cảnh làm phụ đề.

Kiểm tra khả năng công cụ trước khi hứa hiệu ứng/mix/subtitles. Flow Scenebuilder có thể dùng cho thao tác được hỗ trợ; các yêu cầu còn lại thực hiện bằng editor/FFmpeg phù hợp. Helper animatic không phải renderer final.

Xuất edit-plan.json mode final và file video thực. Kiểm tra metadata, phát/xem toàn bộ, nghe âm thanh, soát chữ tiếng Việt, nhịp nối và hook/payoff. Nếu thiếu khả năng xem/nghe, ghi phần chưa kiểm tra; không tuyên bố đã đạt kiểm tra cảm quan từ ffprobe.

## Biên tập nội dung và bàn giao học hỏi

Đối chiếu `script.content_strategy`, hook/payoff và vai trò shot khi dựng. Giữ khoảng ngừng để người xem nhận ra phát hiện, phản ứng hoặc kết quả. Có thể rút lời lặp hoặc cảnh thừa, nhưng thay đổi lời/ý phải cập nhật script và các cue liên quan trước khi coi bản dựng đồng bộ.

Với nhiều vai, đo/nghe từng lượt nói, kiểm tra speaker/track/cue và khoảng chuyển lượt. Bản dựng không được đổi người nói bằng cách đặt tiếng lên khuôn mặt đang nói lời khác. Nhịp cắt, nhạc và hình sau thao tác không được tạo cảm giác đã chứng minh hiệu quả khi chỉ có ví dụ giả định.

Kiểm tra CTA nếu có: người xem biết hành động, lợi ích và đích đến; chữ đủ đọc và đúng tài nguyên thực. Ghi nhận xét biên tập cụ thể thay cho điểm số tùy ý hoặc hứa viral. Animatic chỉ giúp đánh giá nhịp và khả năng hiểu, không chứng minh retention.

Nếu được giao đánh giá hiệu quả, dùng mục đo lường trong [thiết kế nội dung](../video-workflow/references/content-strategy.md): ghi giả thuyết, tín hiệu theo mục tiêu, baseline/kết quả còn thiếu. Không tự đăng, tạo automation hoặc gửi thông điệp để thu thập dữ liệu.

## Trạng thái

Animatic và final là artifact riêng. Bản cuối dùng audio nháp chỉ khi brief cho phép; nếu chưa có audio bắt buộc, giữ trạng thái chưa hoàn tất. Mọi thay đổi timing/trim phải có version để phát hiện clip hoặc phụ đề cần cập nhật.
