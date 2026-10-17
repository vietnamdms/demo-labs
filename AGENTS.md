# Agent standing orders
Updated: 2026-10-17 11:21 +07

Scope: checkout này và mọi subtree chưa có AGENTS.md riêng.

## Read before acting

- **Điểm vào.** Đọc README.md để chọn tài liệu phù hợp trước khi làm việc. ([định tuyến](README.md#where-to-look))
- **Quy trình đóng góp.** Đọc CONTRIBUTING.md và phần áp dụng trước khi thay đổi file. ([hướng dẫn](CONTRIBUTING.md))
- **Phạm vi.** Hoàn thành công việc đã được cho phép; chỉ hỏi khi thông tin thiếu ảnh hưởng đáng kể đến tính đúng, phạm vi hoặc quyền thực hiện. ([phạm vi](CONTRIBUTING.md#scope-and-changes))

## Repository layout

- **Nhà của thông tin.** Giữ standing orders tại AGENTS.md, điểm vào tại README.md và quy trình cùng reference tại CONTRIBUTING.md; mỗi fact chỉ có một nhà. ([phân tầng](CONTRIBUTING.md#documentation-ownership))
- **Hướng dẫn theo subtree.** Kiểm tra AGENTS.md gần file đích và áp dụng phạm vi của nó trước khi sửa. ([phân tầng](CONTRIBUTING.md#documentation-ownership))
- **Alias của agent.** Giữ CLAUDE.md là symlink tương đối tới AGENTS.md tại root và mọi subtree có AGENTS.md. ([phân tầng](CONTRIBUTING.md#documentation-ownership))

## Commands

- **Lệnh thực tế.** Lấy lệnh từ hướng dẫn đóng góp đã được kiểm chứng; không suy đoán công cụ hoặc báo một lệnh đã chạy khi chưa chạy. ([lệnh](CONTRIBUTING.md#command-catalog))
- **Kiểm tra.** Chạy probe hoặc test phù hợp với thay đổi và thu đủ output của tiến trình nền trước khi kết luận. ([xác minh](CONTRIBUTING.md#verification))
- **Giới hạn công cụ.** Báo công cụ bắt buộc bị thiếu và phép kiểm tra bị ảnh hưởng; không thay thế bằng tuyên bố thành công. ([xác minh](CONTRIBUTING.md#verification))

## Hard rules

- **Bảo toàn nội dung.** Giữ instruction hợp lệ, import còn hiệu lực và thay đổi của người khác; chỉ loại memory cũ theo phạm vi đã được cho phép. ([phạm vi](CONTRIBUTING.md#scope-and-changes))
- **Sửa nguyên nhân.** Sửa nguyên nhân của lỗi; không tắt chức năng hoặc kiểm tra để làm kết quả trông đạt. ([chất lượng](CONTRIBUTING.md#lint-and-doctor-policy))
- **Quyền thực hiện.** Chỉ commit, push, phát hành hoặc gửi thông điệp ra ngoài khi yêu cầu hiện tại cho phép thao tác tương ứng. ([phạm vi](CONTRIBUTING.md#scope-and-changes))

## Conventions

- **Thiết kế.** Áp dụng SOLID, separation of concerns, DRY, KISS và YAGNI khi có thay đổi phần mềm. ([đóng góp phần mềm](CONTRIBUTING.md#software-changes))
- **Test trước.** Dùng TDD cho thay đổi hành vi phần mềm và chạy kiểm tra hồi quy liên quan. ([đóng góp phần mềm](CONTRIBUTING.md#software-changes))
- **Văn phong.** Dùng ngôn ngữ chuyên nghiệp, không emoji và giữ mỗi rule trong file này trên một dòng. ([tài liệu](CONTRIBUTING.md#documentation-ownership))
- **Ngày cập nhật.** Đặt dòng Updated ngay dưới H1 của tài liệu được tạo hoặc sửa, theo định dạng YYYY-MM-DD HH:mm +07. ([tài liệu](CONTRIBUTING.md#documentation-ownership))

## Governance

- **Nguồn quản trị.** Đọc tài liệu governance hiện có và giữ một nguồn sự thật; không tự tạo chính sách từ đường dẫn chưa tồn tại. ([quản trị](CONTRIBUTING.md#governance-and-wiki))
- **KStack.** Chỉ dùng lifecycle KStack khi checkout thuộc dự án đã đăng ký và context hợp lệ; dừng registered operations nếu context dự kiến không giải được. ([quản trị](CONTRIBUTING.md#governance-and-wiki))
- **Giới hạn sửa.** Giữ thay đổi trong artifact được yêu cầu và báo xung đột instruction ảnh hưởng kết quả. ([phạm vi](CONTRIBUTING.md#scope-and-changes))

## Context persistence

- **Handoff.** Khi phạm vi cho phép, đọc RESTART_NOTE.md hiện tại trước khi cập nhật NOW, NEXT, BLOCK cùng liên kết quyết định và evidence; giữ tối đa 200 dòng. ([bàn giao](CONTRIBUTING.md#handoff-and-evidence))
- **Evidence.** Ghi Expected và Actual sau bước có ý nghĩa; nêu rõ blocker và kiểm tra chưa thực hiện. ([bàn giao](CONTRIBUTING.md#handoff-and-evidence))
- **Phạm vi chỉ đọc.** Khi yêu cầu giới hạn handoff ở chế độ chỉ đọc, ghi evidence trong artifact được phép hoặc báo cáo cuối thay vì sửa ngoài phạm vi. ([bàn giao](CONTRIBUTING.md#handoff-and-evidence))
