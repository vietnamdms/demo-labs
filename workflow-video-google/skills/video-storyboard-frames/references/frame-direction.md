# Đạo diễn cặp frame
Updated: 2026-10-17 11:03 +07

Prompt start: tên shot, reference IDs kèm ảnh thật cho tool, chủ thể/trạng thái đầu, bố cục/camera, không gian/ánh sáng, style, tỉ lệ. Prompt end: tham chiếu start và asset nhận diện, thay đổi hành động cụ thể, trạng thái cuối, các yếu tố cần giữ. Không yêu cầu start chứa cả diễn biến theo thời gian.

Nếu prompt yêu cầu đưa tách lên môi, end phải thể hiện vị trí tương thích; nếu end thay cả căn phòng, không kỳ vọng một chuyển động nhỏ giải thích được thay đổi. Chia shot hoặc thay hướng kể khi cần.

Kiểm tra pair theo thứ tự: subject identity → pose/prop state → spatial layout → camera/light → feasible motion → aspect ratio. Ghi lỗi cụ thể, không chấm điểm tùy ý không có tiêu chí.

Contact sheet có thể là file HTML với hàng shot_id, ảnh start, ảnh end, mô tả motion và review; dùng đường dẫn tương đối từ file HTML tới ảnh thật. Không cần nhúng media từ web hoặc tạo file ảnh ghép nếu một gallery đủ để xem.

Các nguyên tắc có căn cứ: [Flow creation](https://support.google.com/flow/answer/16353334?hl=en) khuyên ảnh tham chiếu sạch và prompt không mâu thuẫn hình; [Google Veo guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1) minh họa tạo cặp frame rồi mô tả chuyển động. Hướng dẫn model/API không thay thế kiểm tra giao diện Flow hiện tại.
