# Thao tác YouTube Studio
Updated: 2026-10-17 14:53 +07

Đọc khi upload, hẹn giờ hoặc cập nhật video thật. UI/tính năng có thể khác theo tài khoản; quan sát trạng thái hiện tại trước thao tác, không dùng tọa độ hoặc tên nút cũ làm bằng chứng.

## Công cụ và kênh

Tìm connector nếu môi trường có, đọc schema thật và xác minh khả năng upload file/visibility/schedule. Nếu không có route đó, mở https://studio.youtube.com bằng công cụ trình duyệt được hỗ trợ. Chỉ dùng API trình duyệt đã được công cụ công bố; khởi tạo và đọc documentation theo quy định của nó. Upload file qua API upload/file chooser hoặc UI được hỗ trợ, không tự chèn endpoint, script trang, cookie hoặc giả một đường dẫn local thành URL công khai.

Kiểm tra tên/handle/channel ID từ Studio và tài khoản kênh đã chọn. Nếu cần đổi kênh, dùng account/channel switcher thật rồi kiểm tra lại. Kênh cùng tên phải đối chiếu ID/handle, không chọn theo avatar. Chưa đăng nhập không chứng minh kênh không tồn tại; hỏi người dùng hoàn tất login khi cần, vẫn chuẩn bị metadata/file được.

## Upload và metadata

Luồng thông thường: Create → Upload videos → chọn file → Details → Video elements → Checks → Visibility. Theo UI hiện có nếu thứ tự hoặc nhãn khác. Sau khi có video ID/edit URL, lưu ngay vào [record](publishing-record.md), không đợi đến lúc công khai mới ghi dấu vết.

Nguồn [upload YouTube](https://support.google.com/youtube/answer/57407?hl=en) đối chiếu ngày 17/10/2026 ghi giới hạn title 100 ký tự, description 5.000 ký tự; kiểm tra lỗi thực của form khi nhập. Tôn trọng thông tin người dùng đã chốt. Không nhồi tags/hashtag, không thêm nội dung không có trong clip. Language/category/playlist chỉ chọn đúng mục có thật và phù hợp yêu cầu.

Thumbnail: dùng ảnh được chọn, xác minh tính năng và điều kiện tài khoản. Theo [hướng dẫn thumbnail](https://support.google.com/youtube/answer/72431?hl=en) cùng ngày, Studio desktop có custom thumbnail cho Shorts trên tài khoản đã xác minh; không dùng quy tắc cũ “Shorts không thể upload thumbnail” làm mặc định. Đọc giới hạn file/tỉ lệ trên UI hiện tại. Nếu không hỗ trợ, ghi chưa gắn thay vì gọi thao tác thành công.

Phụ đề: kiểm tra SRT khớp version/timeline clip, đặt ngôn ngữ đúng rồi đọc lại trạng thái track. Chữ đã burn-in không phải track captions tải riêng. Không tự sửa video nguồn hoặc thay asset để vượt lỗi upload.

## Shorts và các khai báo theo nội dung

- [Điều kiện Shorts](https://support.google.com/youtube/answer/15424877?hl=en): tài liệu hiện hành cho video upload mới trên kênh tiêu chuẩn, vuông/dọc, tối đa ba phút. Với kênh nghệ sĩ hoặc trường hợp đặc biệt đọc phần áp dụng; xác minh nhãn/tab thực sau xử lý. Không thêm viền/cắt hình để ép format ngoài yêu cầu.
- [Audience](https://support.google.com/youtube/answer/9528076?hl=en): xác định khán giả đích từ nội dung và brief. Video hoạt hình hoặc family-friendly không tự là made for kids. Không chọn mặc định theo hình mascot; còn mơ hồ thì hỏi khán giả dự định.
- [AI use/Altered content](https://support.google.com/youtube/answer/14328491?hl=en): dựa trên bản chất nội dung, đặc biệt hình/tiếng tổng hợp có vẻ thật hoặc sửa sự kiện/người thật. Hoạt hình phi hiện thực không tự bắt buộc khai báo chỉ vì được AI tạo. Với nhạc AI là trọng tâm, xem yêu cầu âm nhạc hiện hành. Ghi quyết định/căn cứ, không xóa nhãn tự động hoặc dấu nguồn để né khai báo.
- Paid promotion/branded content: dùng thông tin về tài trợ/quan hệ thương mại được cung cấp, không đoán từ logo. Không đổi chính sách toàn kênh cho một video.

## Checks, visibility và lịch

Ghi trạng thái Checks/processing như quan sát. Nếu có claim/block/error, ghi loại và tác động cụ thể; không tự dispute, xóa âm thanh, thay nhạc hoặc xóa video. Nếu vấn đề thực sự cản mục tiêu, giữ phần chuẩn bị và xử lý đúng lỗi trước bước cuối. Không thêm bước xin duyệt mặc định khi mọi dữ liệu và quyền đã rõ.

Private, Unlisted và Public là ba lựa chọn khác nhau. Đối chiếu trước bấm, không tin mặc định tài khoản hoặc coi đã upload là đã public. Nếu chỉ yêu cầu tải lên mà chưa chọn công khai, dùng Private theo SKILL.md và báo rõ kết quả.

Với [hẹn giờ](https://support.google.com/youtube/answer/1270709?hl=en), đặt ngày, giờ và timezone của lịch; record lưu cả ISO/offset và múi giờ IANA. Sau Save/Schedule, đọc lại lịch trong Studio. Watch page có thể hiển thị ngày theo múi giờ khác; không so chuỗi ngày rời rạc để kết luận đặt sai. Nếu lịch đã qua, không tự đổi thành Publish now hoặc tự dời ngày.

Sau thao tác, vào Content tìm bằng video ID ưu tiên; đối chiếu tiêu đề, thumbnail, visibility/lịch và trạng thái xử lý. Private video có watch URL vẫn không có nghĩa công chúng xem được. Scheduled cần có lịch quan sát, không chỉ một video Private. Nếu HD chưa xong, báo mức xử lý hiện tại; không mặc định upload lỗi hoặc tải lại toàn bộ.

## Tiếp tục lượt gián đoạn

Nếu có video ID, mở lại đúng video để kiểm tra/cập nhật. Nếu chưa có, dùng đúng kênh, thời gian, tiêu đề/file và dấu vết upload để tìm trong Content; so record trước/sau. Unknown chưa được chuyển thành failed chỉ vì timeout. Khi vẫn không phân biệt được hai ứng viên, giữ unknown và hỏi thông tin phân biệt; không xóa hoặc tạo thêm bản sao để làm trạng thái trông sạch.

Các nguồn trên được kiểm tra ngày 17/10/2026; đọc lại mục áp dụng khi UI hoặc policy thay đổi. Đây là hướng dẫn thao tác, không xác nhận khả năng tài khoản hay kết quả đăng thật.
