---
name: video-flow-generate
description: "Tạo hoặc tiếp tục clip trên Google Flow từ cặp start/end frame và shotlist đã chuẩn bị. Soạn prompt chuyển động, kiểm tra model/mode/credit, theo dõi take và chọn clip. Dùng cho thực thi Flow hoặc chuẩn bị gói render; không coi API Veo là thao tác trên Flow."
---

# Video Flow Generate
Updated: 2026-10-17 13:48 +07

Đọc [hợp đồng renders](../video-workflow/references/contracts.md#rendersjson) và [quy trình Flow](references/flow-runbook.md) trước khi thực thi. Nhận shotlist, cặp frame, animatic/timing và phạm vi chi phí đã cho phép.

## Chuẩn bị

- Kiểm tra file ảnh, version và review. Với yêu cầu chỉ soạn prompt, xuất render package và dừng đúng phạm vi.
- Dùng connector hoặc giao diện trình duyệt được hỗ trợ trong môi trường. Không tự dựng endpoint Flow, đọc cookie hoặc coi có skill là đã có đăng nhập. Tài liệu Veo API chỉ là tham khảo model.
- Quan sát model/mode, tỉ lệ, độ dài, phân giải, âm thanh và credit thật; ghi capability snapshot có thời điểm và nguồn. Giữ chế độ first-and-last-frame cho yêu cầu cặp frame của bộ này.
- Không mặc định Frames, Ingredients và voice references dùng đồng thời được. Nếu tổ hợp không hỗ trợ, giữ yêu cầu cặp ảnh, nêu xung đột và phương án phù hợp; không tự chuyển sang một tool trả phí khác.

## Chạy từng take

1. Kiểm tra render job/take cũ của shot; chưa rõ kết quả thì để unknown và đối chiếu trước khi tạo lại.
2. Viết prompt mô tả chuyển động nối hai trạng thái, camera, nhịp và âm thanh. Không mâu thuẫn ảnh hoặc nhồi thêm hành động ngoài shot.
3. Kiểm tra chi phí/lượt, số output, giới hạn project và shot đã thống nhất. Nếu thiếu thông tin bắt buộc, hoàn thiện gói render và chỉ hỏi phần chặn chi phí; không hỏi lại khi đã có quyền/ngân sách.
4. Lưu take_id, snapshot input/version và request fingerprint trước submit. Sau submit lưu job_id nếu có; nếu không, lưu Flow project URL và dấu vết nhận diện take. Không bịa ID hay chi phí.
5. Theo dõi submitted/running/succeeded/failed/unknown/downloaded. Không coi timeout là thất bại chắc chắn. Khi lấy file, xác nhận clip đúng take và mở được.
6. Xem toàn clip, nghe âm thanh; kiểm tra nhận diện, hành động, chi tiết xuyên thời gian, frame thực tế tại điểm cắt và thoại nếu có. Không chỉ kiểm tra thumbnail.
7. Chọn take nếu đạt yêu cầu. Nếu lỗi, phân loại frame/prompt/model để sửa có mục đích; dừng khi chạm giới hạn. Ghi selected và review riêng với trạng thái job.

## Review clip theo nội dung

Dùng chức năng beat, `purpose`/`story_action` của shot và profile vai diễn để soạn prompt. Nêu ai hành động/nói, phản ứng nào cần thấy và trạng thái kết thúc; giữ thoại đã chốt. Không yêu cầu model tự thêm câu bán hàng hoặc kết quả ngoài script.

Khi xem take, xác nhận đúng người nói, câu thoại, phản ứng và trình tự phát hiện → quyết định. Kiểm tra trạng thái thật tại điểm trim: clip không được cắt mất hành động tạo payoff hoặc biến minh họa thành bằng chứng hiệu quả. Ghi tại `review.notes` điều đã quan sát và lỗi còn lại; thành công của job, hình đẹp hoặc audio có tiếng chưa đủ để chọn take.

Lỗi ý nghĩa bắt đầu từ script/shot thì sửa ở nguồn và cập nhật dependency trước render lại. Lỗi thực hiện của model thì sửa prompt/timing trong ngân sách đã có. Giữ mọi giới hạn về retry, trạng thái unknown và credit ở quy trình trên.

## Bàn giao

Renders.json phải nêu take được chọn, file/link thật, nguồn frame/version, chi phí quan sát được và lỗi còn lại. File tồn tại không đủ để ready. Chỉ render một phần nếu đó là phạm vi được giao; không tự render cả project từ yêu cầu sửa một shot. Chuyển clip đạt yêu cầu sang video-assemble final.
