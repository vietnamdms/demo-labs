---
name: youtube-publish
description: "Tải và đăng clip lên YouTube/YouTube Shorts, lưu riêng tư/không công khai, hẹn giờ hoặc cập nhật video đã xác định. Dùng khi người dùng yêu cầu đăng video, upload YouTube, lên lịch YouTube hoặc tiếp tục lượt tải bị gián đoạn. Chuẩn bị metadata, xác minh đúng kênh, tránh tải trùng và kiểm tra trạng thái sau lưu; không tự tạo video hoặc tự mở rộng sang các nền tảng khác."
---

# Đăng clip lên YouTube
Updated: 2026-10-17 14:53 +07

Đăng một hoặc nhiều file video trong phạm vi người dùng giao. Hỗ trợ Shorts và video dài; không phụ thuộc bộ skill sản xuất để chạy độc lập. Khi nhận project video, dùng đúng file/version đã chọn và metadata từ nguồn chuẩn.

## Phạm vi và đầu vào

1. Xác định mode `prepare`, `upload`, `schedule` hoặc `update`, file/video ID, kênh đích, metadata, visibility và lịch nếu có. Yêu cầu tạo skill, lên kế hoạch hoặc chỉ soạn tiêu đề dùng prepare; không tự đăng.
2. Tìm thông tin trong yêu cầu, project và lựa chọn đã chốt trước khi hỏi. Nếu thiếu kênh hoặc có nhiều file/kênh hợp lý, hỏi đúng phần còn thiếu và tiếp tục chuẩn bị độc lập. Không dùng kênh đang mở làm bằng chứng người dùng đã chọn kênh đó.
3. Với upload/schedule, kiểm tra file thật, version, duration/ratio/streams bằng công cụ media nếu có; không tự lấy animatic hoặc review-copy thay bản cuối. Nếu người dùng chỉ định chính bản xem duyệt, dùng đúng bản đó và giữ ghi chú chất lượng còn lại.
4. Lời yêu cầu đăng/hẹn giờ là quyền thực hiện trong phạm vi tương ứng. Nếu đã có đủ file/kênh/chế độ và quyền, hoàn thiện metadata rồi thực hiện, không thêm vòng xác nhận mỗi nút. Nếu chỉ yêu cầu tải lên và chưa rõ ý định công khai, chọn Private và báo rõ; không dựa vào mặc định Public của tài khoản. Yêu cầu Public/Unlisted hoặc lịch đã rõ phải giữ đúng lựa chọn đó.

## Chuẩn bị gói đăng

Đọc [record và kiểm tra](references/publishing-record.md). Lưu `youtube-publish.json` trong thư mục project/người dùng chọn, tách dữ liệu dự định với kết quả quan sát. Mode prepare không cần đăng nhập hoặc tạo bản nháp trên YouTube.

- Viết một tiêu đề chính, mô tả đúng nội dung, CTA/URL có thật và hashtag liên quan vừa đủ. Giữ lời chốt của người dùng; không bịa thành tích, giá hoặc hứa hiệu quả. Không biến đăng một clip thành chiến dịch SEO.
- Xác định ngôn ngữ, audience, khai báo AI use/Altered content và paid promotion theo nội dung/brief; ghi căn cứ. Không tự suy “hoạt hình = dành cho trẻ em”, “AI = phải chọn Yes” hoặc “logo thương hiệu = tài trợ”. Nếu thiếu thông tin không thể suy ra cho trường bắt buộc, hỏi đúng thông tin đó trước khi lưu lựa chọn sai.
- Tái dùng thumbnail/SRT/playlist đã có khi phù hợp và được yêu cầu. Kiểm tra hỗ trợ trên tài khoản/UI hiện tại; không hứa đã gắn thumbnail/phụ đề khi chỉ có file. Không tự tạo playlist, thay hình hoặc chỉnh nội dung video ngoài phạm vi.
- Phân loại Shorts từ file và điều kiện YouTube hiện hành; tên file, hashtag #Shorts hoặc video dọc không tự chứng minh YouTube đã phân loại. Giữ requested_format khác observed_format nếu chưa xác minh.
- Khi hẹn giờ, ghi ngày giờ cụ thể, múi giờ IANA và ISO có offset/UTC; đối chiếu giờ trên UI. Dùng múi giờ phiên/người dùng khi đã biết, không diễn giải giờ địa phương thành UTC. Lịch đã qua hoặc mơ hồ cần giải quyết trước khi đặt lịch.

## Thực thi

Đọc [YouTube Studio runbook](references/youtube-studio.md) trước thao tác. Ưu tiên connector YouTube thật sự có và hỗ trợ đủ trường; nếu không có, dùng YouTube Studio qua công cụ trình duyệt được hỗ trợ. Không bịa connector, endpoint, quota hoặc khả năng upload. Không cần cài tool/API mới chỉ để viết gói đăng.

1. Xác minh kênh hiện tại bằng tên/handle/channel ID quan sát được và đối chiếu đích người dùng. Với login/2FA, để người dùng hoàn tất qua UI; không đọc mật khẩu, cookie hay token từ profile.
2. Trước mutation, đọc record/lượt tải cũ và Content để tránh trùng. Lưu attempt với file fingerprint, kênh, payload và trạng thái planned trước chọn file/submit. Hash chỉ hỗ trợ đối chiếu cục bộ, không là idempotency key của YouTube.
3. Tải đúng file, lưu video ID/edit URL ngay khi có. Điền metadata/audience/AI use và các asset phù hợp, xem Checks và trạng thái xử lý. Lỗi/cảnh báo thật phải được ghi, không gọi một lần Checks sạch là chứng nhận bản quyền lâu dài.
4. Đối chiếu toàn bộ dữ liệu và visibility/lịch ngay trước Save/Publish/Schedule rồi bấm theo quyền hiện có. Không tự đổi chế độ công khai, Premiere, thông báo người đăng ký, monetization hoặc cài đặt toàn kênh.
5. Sau lưu, đọc lại video trong Content/Details: đúng kênh, video ID, tiêu đề, visibility, lịch/múi giờ và asset quan trọng. Kiểm tra playback/processing khi có thể; tách “đã tải”, “đã hẹn giờ” và “đã công khai”. Scheduled thường còn Private trước giờ đăng.
6. Nếu timeout hoặc mất UI sau submit, ghi unknown và đối chiếu video ID/Content trước retry; không tạo upload thứ hai khi chưa biết kết quả lượt trước. Lỗi đã xác định chỉ sửa/retry có mục tiêu; dừng khi không có tiến triển, gặp giới hạn tài khoản hoặc thiếu quyền/công cụ.

## Bàn giao

Lưu record với giá trị quan sát thật, timestamp, URL dùng được, kết quả xử lý và phần chưa xác minh. Không bịa video ID/URL từ tên file. File/metadata thay đổi làm lần đăng mới có version mới, không âm thầm thay bản trên kênh hoặc xóa upload cũ.

Trả lời ngắn: video nào, kênh nào, link, trạng thái thực và lịch giờ địa phương nếu có. Hẹn giờ thành công không có nghĩa đã public hoặc đã có automation theo dõi; không tự tạo lịch nhắc, bình luận, gửi tin, xóa/repost hoặc phân phối nền tảng khác. Nếu chỉ prepare, bàn giao file kế hoạch và phần còn thiếu, không tuyên bố đã tải.
