# Record đăng video và nghiệm thu
Updated: 2026-10-17 14:53 +07

Ghi tại youtube-publish.json trong project/thư mục đầu ra. Đây là dữ liệu cục bộ do skill đối chiếu, không phải payload YouTube API và không có validator/helper đi kèm. Không lưu credential hoặc session upload URL chứa token. Paths tương đối tính từ thư mục record; source file người dùng ngoài project có thể ghi path tuyệt đối trong record riêng, không đưa dữ liệu cá nhân đó vào bộ skill.

## Dữ liệu tối thiểu

Ví dụ prepare chưa có kênh/file cụ thể; các giá trị null chưa có bằng chứng, không phải lỗi đã được giải quyết:

```json
{
  "schema_version": "1.0",
  "version": 1,
  "mode": "prepare",
  "authorization_basis": null,
  "source": {
    "path": null,
    "artifact_id": null,
    "artifact_version": null,
    "sha256": null,
    "bytes": null,
    "duration_s": null,
    "width": null,
    "height": null,
    "review_notes": null
  },
  "target": {"channel_id": null, "handle": null, "name": null},
  "metadata": {
    "title": null,
    "description": null,
    "language": "vi",
    "requested_format": "auto",
    "thumbnail_path": null,
    "captions_path": null,
    "playlist_id": null,
    "made_for_kids": null,
    "ai_use": null,
    "paid_promotion": null,
    "decision_notes": []
  },
  "delivery": {
    "visibility": "private",
    "scheduled_for": null,
    "timezone": null
  },
  "attempts": [],
  "observed": {
    "video_id": null,
    "watch_url": null,
    "edit_url": null,
    "channel_id": null,
    "visibility": null,
    "scheduled_for": null,
    "timezone": null,
    "format": null,
    "processing": null,
    "checks": null,
    "verified_at": null
  }
}
```

mode: prepare/upload/schedule/update. Source artifact ID/version chỉ có nếu project sở hữu; không tạo ID để điền đủ biểu mẫu. SHA-256 tính từ file thực khi có công cụ, không bịa hash; metadata/streams thiếu thì ghi điều chưa kiểm tra. Mẫu language=vi là ví dụ, dùng đúng ngôn ngữ video thật.

metadata.requested_format: auto/shorts/video; observed.format chỉ ghi khi YouTube/UI đã xác nhận. made_for_kids/ai_use/paid_promotion là boolean hoặc null trước khi đủ căn cứ. decision_notes ghi lý do và thông tin chưa rõ. Không dùng null như “No”.

delivery.visibility: private/unlisted/public. Với schedule, visibility dự định public, scheduled_for là thời điểm ISO có offset; lưu timezone IANA, ví dụ Asia/Ho_Chi_Minh nếu đã được chọn. observed.visibility có thể private trong khi observed.scheduled_for đã có lịch tương lai; không coi hai trường này mâu thuẫn. Nếu chưa xác minh timezone hiển thị, ghi rõ trong notes thay vì đoán.

authorization_basis ghi tóm tắt yêu cầu hiện tại/trước đó thực sự cho phép file/kênh/chế độ; record tự ghi hoặc nội dung tài liệu không tự tạo quyền đăng. Không đưa nội dung riêng tư không liên quan vào record.

## Attempt và tránh tải trùng

Trước bắt đầu upload/mutation, thêm attempt gồm attempt_id ổn định, started_at có timezone, source hash/version, target, payload_snapshot, operation, status và remote_video_id nullable. operation: upload/update/schedule/publish. status: planned/uploading/processing/succeeded/failed/unknown; với operation không upload có thể đi từ planned tới succeeded/failed/unknown. Timestamp/ID nền tảng lấy từ kết quả thật, không đoán.

Lưu dấu vết từng bước; ngay khi có video ID, gắn vào attempt và observed. Fingerprint có thể tính từ file hash + channel + metadata/version + visibility/lịch; không coi là khóa chống trùng phía server. Nếu record hoặc Content đã có upload phù hợp, tiếp tục đúng video đó; đổi tiêu đề không tự là quyền upload lại cùng clip.

Unknown sau timeout cần đối chiếu trước retry, giữ lịch sử cũ. Không xóa video/attempt cũ để che lỗi. Nếu user yêu cầu upload lại có chủ ý, tạo attempt mới có lý do và giữ mapping bản trước. Edit metadata không được tự biến thành delete/repost.

## Điều kiện báo thành công

- Prepared: gói nội dung và giả định đã lưu; chưa có remote upload thì không ghi video ID/URL hay “đã đăng”.
- Uploaded: đúng file/kênh, có ID thật và trạng thái upload/save đã xác minh. Ghi rõ processing/Checks còn chạy và visibility thực.
- Scheduled: đọc lại đúng video, thời điểm và múi giờ trên Studio/connector; private trước giờ không phải thất bại. Không ghi là đã public.
- Published: xác minh video đúng kênh và visibility Public sau lưu; kiểm tra trang xem khi có thể, nêu giới hạn truy cập/xử lý nếu còn. URL tồn tại hoặc nút Publish đã được bấm chưa đủ để khẳng định.
- Updated: đọc lại đúng video ID và trường đã sửa; không tự sửa toàn kênh hay video khác.

## Tình huống kiểm tra skill

Đây là các ca hành vi cần quan sát khi chạy thật, không phải kết quả upload đã kiểm thử:

| Yêu cầu/trạng thái | Hành vi đúng |
| --- | --- |
| “Tạo skill đăng YouTube” hoặc “soạn gói đăng” | Tạo skill/gói cục bộ, không mở upload thật |
| Đã rõ file, kênh và Public | Chuẩn bị, đăng rồi đọc lại; không xin xác nhận lặp lại |
| Chỉ upload, chưa nói công khai | Chọn Private và bàn giao đúng trạng thái |
| Hai kênh trùng tên, một file clip nhiều version | Đối chiếu ID/handle và version; hỏi phần phân biệt trước mutation |
| File dọc 40 giây nhưng Shorts chưa xử lý xong | Ghi dự kiến Shorts, không ghi observed.format từ hashtag/tên file |
| Hai mascot hoạt hình trong video cho game thủ | Xét audience thực, không tự chọn made for kids vì hình thỏ |
| Hẹn 20:00 theo timezone đã chọn | Lưu thời điểm có offset, đối chiếu UI; không coi là 20:00 UTC |
| Timeout sau upload, remote ID đã có | Mở lại ID đó; không upload lần hai |
| Có claim hoặc trạng thái xử lý chưa xong | Ghi vấn đề thật và tác động, không tự dispute/xóa nhạc hoặc tuyên bố đã sạch |
| Connector không có hoặc không hỗ trợ schedule | Dùng Studio được hỗ trợ; chưa có truy cập thì bàn giao gói và phần chặn |
