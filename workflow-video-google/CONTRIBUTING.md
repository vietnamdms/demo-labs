# Workflow Video Google — hướng dẫn sử dụng và đóng góp
Updated: 2026-10-17 13:48 +07

Áp dụng [quy trình đóng góp của repo](../CONTRIBUTING.md). Tài liệu này là nơi chứa hướng dẫn sử dụng, yêu cầu môi trường và lệnh của lab.

## Requirements

- Python 3.9 trở lên cho hai helper; chỉ dùng thư viện chuẩn Python.
- FFmpeg và ffprobe có trong PATH để dựng animatic và chạy kiểm tra media. FFmpeg cần encoder libx264 và AAC.
- Khi thực thi sản xuất: công cụ ảnh/âm thanh phù hợp và quyền truy cập Google Flow. Bộ skill không cung cấp tài khoản, credential hoặc API Flow.

## Installation

Copy cả 8 thư mục con trong `skills/` vào thư mục skill của Codex: `$CODEX_HOME/skills` nếu đã cấu hình CODEX_HOME, hoặc `~/.codex/skills` mặc định. Giữ chúng cùng cấp để các liên kết dữ liệu dùng chung hoạt động. Đối chiếu trước nếu đã có skill cùng tên và đã tùy biến; không ghi đè các thay đổi đó một cách tự động.

Đây là nội dung skill và helper, không có package dependency ứng dụng phải cài. Hướng dẫn cài đặt không tự khởi động tạo media có phí.

## Usage

Gọi toàn workflow sau khi cài:

```text
$video-workflow
Tạo kịch bản và bảng phân cảnh cho video TikTok 30 giây về một buổi sáng chậm lại cùng cà phê.
Lời dẫn tiếng Việt, phong cách tự nhiên, ánh sáng buổi sáng.
Lưu trong project mới và làm đến bước phân cảnh trước.
```

Tiếp tục project:

```text
$video-workflow
Tiếp tục project đã có. Chuẩn bị bộ tham chiếu, cặp start/end frame và dựng animatic.
```

Có thể gọi từng skill theo tên trong [danh sách](README.md#skills). `video-assemble` có ba mode: `prepare-audio`, `animatic`, `final`. Các mốc kiểm tra chất lượng không mặc định là yêu cầu duyệt thủ công; thực hiện trong phạm vi và ngân sách người dùng đã cho phép.

## Local helper commands

Chạy các lệnh từ root repo. Thư mục project ví dụ bên dưới được ignore, không đưa media vào Git.

```sh
python3 workflow-video-google/skills/video-workflow/scripts/project.py init workflow-video-google/projects/coffee-morning --id coffee-morning --format short --platform tiktok --idea 'Một buổi sáng chậm lại cùng cà phê' --duration 30
python3 workflow-video-google/skills/video-workflow/scripts/project.py validate workflow-video-google/projects/coffee-morning
```

Khi đã có frame đăng ký trong manifest và vừa sửa nội dung file, đánh dấu phần cần rà soát:

```sh
python3 workflow-video-google/skills/video-workflow/scripts/project.py revise workflow-video-google/projects/coffee-morning --artifact frame.S03.end --reason 'Đổi vị trí tách ở cuối shot'
```

Khi đã có `edit-plan.json` và ảnh thật theo [hợp đồng edit-plan](skills/video-workflow/references/contracts.md#edit-planjson), dựng nháp:

```sh
python3 workflow-video-google/skills/video-assemble/scripts/render_animatic.py workflow-video-google/projects/coffee-morning/edit-plan.json --output workflow-video-google/projects/coffee-morning/animatic-v1.mp4
```

Helper animatic ghép ảnh tĩnh theo thời gian, hỗ trợ một track audio và từ chối mode final. Nó không tạo chuyển động AI, không mix nhiều track và không tự thêm phụ đề. Xem/nghe bản xuất trước khi ghi review pass. `validate` kiểm tra dữ liệu hiện có, không chứng minh toàn bộ production đã hoàn tất.

## Verification

```sh
python3 -m unittest discover -s workflow-video-google/tests -p 'test_*.py' -v
git diff --check
```

Test lấy skill từ checkout hiện tại bằng đường dẫn tương đối, không phụ thuộc bộ skill đã cài trong máy. Nếu thiếu FFmpeg/ffprobe, các test media được skip; phải báo rõ khi đó chưa xác minh renderer.

Khi sửa code: viết test lỗi có ý nghĩa trước, sửa rồi chạy nhóm hồi quy liên quan. Khi sửa skill: kiểm tra YAML frontmatter, link relative, mẫu dữ liệu và quyết định của skill. Mọi Markdown tạo/sửa có Updated ngay dưới H1 theo hướng dẫn root.

## Verification evidence

Ngày: 2026-10-17 +07. Phạm vi: bản đóng gói cục bộ trước khi push; trạng thái Git báo riêng sau thao tác thực tế.

| Kiểm tra | Expected | Actual |
| --- | --- | --- |
| Test trước khi import helper | Bộ test portable phát hiện chưa có source trong lab | Fail với FileNotFoundError tại scripts/project.py |
| Test sau khi import | Kiểm tra dùng source trong checkout, gồm media thật | 17/17 pass; 0 skipped |
| Skill structure | 8 skill có frontmatter, UI metadata và link hợp lệ | 8/8 pass |
| Portability | Không có đường dẫn máy cá nhân trong bundle | Không tìm thấy đường dẫn home tuyệt đối |
| Documentation | Updated ngay sau H1, link local đúng, fence cân bằng | Pass |
| Media production | Chỉ xác minh helper với ảnh/âm thanh mẫu cục bộ | Chưa chạy Flow, TTS hoặc tạo ảnh dịch vụ |

## Data ownership

[contracts.md](skills/video-workflow/references/contracts.md) là nguồn chuẩn của dữ liệu; mỗi SKILL.md sở hữu hướng dẫn bước tương ứng. Tránh sao chép hợp đồng vào nhiều skill. Khi thay đổi schema, cập nhật helper, test và tài liệu liên quan cùng nhau.

## Cập nhật hướng dẫn nội dung — 17/10/2026

Phạm vi: tám SKILL.md, reference theo bước, tài liệu thiết kế nội dung dùng chung và hợp đồng mở rộng. Hai helper và bộ test giữ nguyên. Các kết quả 17/17 phía trên thuộc lần đóng gói ban đầu, không phải kết quả chạy lại cho bản nâng cấp này.

Khi cài nâng cấp, đối chiếu và sao lưu bản đã tùy biến trước khi copy. Giữ tám thư mục cùng cấp. Các project đang chạy không bị tự chuyển script hay tái tạo media; áp dụng hướng dẫn khi viết/sửa phần nội dung liên quan. Các trường content_strategy, profile diễn xuất và mapping nhiều vai cần review bằng skill; helper hiện không chứng minh chúng hợp lệ về ngữ nghĩa.

Nguồn bài học là bản EPUB Inbound Content người dùng cung cấp; bộ phân phối chỉ chứa hướng dẫn diễn giải và ví dụ sáng tạo, không chứa sách hoặc đường dẫn máy cá nhân. Ghi chú nguồn nằm tại [content-strategy.md](skills/video-workflow/references/content-strategy.md).

Evidence cho lần cập nhật hướng dẫn: đã đọc diff và chạy `git diff --check` không có lỗi whitespace. Không chạy lại unit test hoặc render dịch vụ trong lần cập nhật này; không thay đổi mã helper. Bản cài cục bộ được sao lưu trước khi đồng bộ từ checkout.
