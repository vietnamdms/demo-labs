# Contributor guide
Updated: 2026-10-17 11:21 +07

Hướng dẫn thực hiện và xác minh thay đổi trong checkout.

## Documentation ownership

| Loại nội dung | Nhà duy nhất |
| --- | --- |
| Mệnh lệnh thường trực cho agent | AGENTS.md |
| Giới thiệu, trạng thái và định tuyến | README.md |
| Quy trình, lệnh, chính sách và reference chi tiết | CONTRIBUTING.md |

Khi dời nội dung, thay đoạn ở nhà cũ bằng liên kết đến nhà mới. Giữ import còn hiệu lực nguyên văn; không thay import bằng một bản sao nội dung. Khi bổ sung hướng dẫn cho subtree, dùng cùng cách phân tầng này.

## Scope and changes

Khảo sát trạng thái checkout và diff trước khi sửa; giữ nguyên các thay đổi không thuộc công việc. Với yêu cầu chỉ sửa tài liệu, chỉ stage đúng các artifact đã được cho phép. Nếu instruction mâu thuẫn, áp dụng thứ tự ưu tiên của yêu cầu hiện tại và giải thích quyết định có ảnh hưởng đến kết quả.

## Command catalog

Các mục dưới đây là nhà của yêu cầu môi trường và lệnh vận hành. Chỉ bổ sung lệnh sau khi có cấu hình thực tế và đã kiểm chứng.

### System requirements

Công cụ dùng cho bộ tài liệu: Git, shell POSIX, grep, wc và readlink; Python 3 hỗ trợ probe bổ sung. Yêu cầu Python và FFmpeg cho lab video nằm tại [Workflow Video Google requirements](workflow-video-google/CONTRIBUTING.md#requirements).

### Installation

Repo chưa có package manifest chung. Cách cài bộ skill video nằm tại [Workflow Video Google installation](workflow-video-google/CONTRIBUTING.md#installation).

### Database initialization and migrations

Chưa chọn database, công cụ migration hoặc lệnh khởi tạo dữ liệu.

### Database seeding

Chưa có dataset hay lệnh seed được định nghĩa.

### Development server

Chưa có lệnh hoặc cổng development server được cấu hình.

### MCP surface

Chưa khai báo MCP server, transport hay tool surface của repo.

## Software changes

Trước khi thêm phần mềm, mô tả hành vi mong đợi và viết test thất bại có ý nghĩa; triển khai tối thiểu rồi refactor, giữ test xanh. Đối với thay đổi thuần tài liệu, dùng các probe cấu trúc, liên kết và diff ở mục Verification. Chỉ công bố lệnh build/test sau khi có cấu hình tương ứng.

## Lint and doctor policy

Chỉ sử dụng tsgolint khi dự án thực sự có cấu hình và dependency tương ứng; hiện chưa thiết lập công cụ này. Không tự tạo kết quả lint hoặc bỏ qua kiểm tra đang có hiệu lực.

Chọn doctor theo framework thực tế và ghi rõ phiên bản, lệnh cùng kết quả khi sử dụng. Không cài thêm doctor cho bộ tài liệu này. Các reference lint/doctor chi tiết được giữ tại mục này hoặc liên kết từ đây tới docs_root đã xác minh.

## Governance and wiki

Hiện checkout không có governance/, docs_root hoặc wiki được khai báo. Các tài liệu RULES.md, MECE.md và FEYNMAN.md được nhắc trong brief chưa tồn tại tại governance/; chúng không phải import đang có hiệu lực.

Khi repo bổ sung wiki, tìm theo chủ đề, đọc nguồn evidence trước khi kết luận và liên kết đến trang chuẩn thay vì sao chép reference. Với dự án KStack đã đăng ký, giải context bằng lệnh dưới đây; yêu cầu ok: true và data.schema: kstack.workspace-context.v1, lấy roots từ kết quả rồi đọc governance/PRINCIPLES.md dưới docs_root. Không đoán docs root và không đăng ký dự án chỉ để chỉnh tài liệu.

```sh
kstack --json workspace context --path "$PWD"
```

## Technology and architecture decisions

Quyết định kỹ thuật của lab video nằm tại [Workflow Video Google](workflow-video-google/CONTRIBUTING.md). Repo chưa chọn stack ứng dụng chung hoặc nơi lưu ADR. Khi có quyết định, ghi bối cảnh, phương án được chọn, trade-off và evidence tại nguồn được repo quy định; chỉ để liên kết định tuyến trong README.md.

## Verification

Kiểm tra diff bằng git diff --check và xác nhận chỉ có artifact dự kiến. Chạy từng probe trong brief và kiểm tra thêm target của symlink ở mọi subtree, thứ tự Updated, rule trên một dòng, liên kết nội bộ, code fence và số import trước/sau.

Các probe cấu trúc không thay thế test phần mềm. Bộ kiểm tra helper video và lệnh chạy nằm tại [Workflow Video Google verification](workflow-video-google/CONTRIBUTING.md#verification). Repo chưa có production build chung.

## Handoff and evidence

Handoff phải tham chiếu evidence có thể kiểm chứng. Tách việc đã xác minh khỏi việc chưa thực hiện; không ghi trước kết quả commit hoặc push. Trong lần khởi tạo này, RESTART_NOTE.md không được tạo hoặc sửa vì yêu cầu giới hạn artifact; quyết định và evidence được giữ tại mục dưới.

## Initialization evidence

Ngày kiểm tra: 2026-10-17 11:21 +07; baseline sau pull: f0fd47a.

Git pull --ff-only: PASS, dae7ca1 → f0fd47a; working tree sạch trước và sau pull. Thay đổi mới từ origin được giữ nguyên.

Baseline theo wc -w: AGENTS=634, README=206, CONTRIBUTING=1027; memory=0; import=0; một CLAUDE.md hợp lệ tại root, không có AGENTS.md ở subtree.

Quyết định: giữ standing orders và định tuyến lab sau pull; cập nhật evidence, tập trung reference tại contributor guide. RESTART_NOTE.md chỉ đọc theo giới hạn artifact. Không tạo import hay docs root từ governance chưa tồn tại. Chỉ sửa ba tài liệu, giữ symlink; không commit/push.

| Tiêu chí | Expected | Actual |
| --- | --- | --- |
| AC-1 | Memory=0; đủ 7 H2; chỉ standing orders | PASS;memory=0;H2=7/7;rules=standing-orders |
| AC-2 | Mọi alias là symlink tới AGENTS.md | PASS;symlinks=1/1;target=AGENTS.md |
| AC-3 | Đủ 4 H2 bắt buộc trong README | PASS;H2=4/4 |
| AC-4 | Keyword công cụ lint: README=0; CONTRIBUTING>=1 | PASS;README=0;CONTRIBUTING=1 |
| AC-5 | Một H2 Lint and doctor policy | PASS;H2=1 |
| AC-6 | AGENTS<=1950 từ; tổng không tăng | PASS;AGENTS=634;README=191;CONTRIBUTING=1034;total=1859<=1867 |
| AC-7 | Fence cân bằng; giữ import hiệu lực | PASS;fences=0,0,2;imports=0/0 |

Actual được kiểm tra lại trên tài liệu cuối.

Bổ sung: PASS; git diff --check, liên kết nội bộ, định dạng rule và vị trí Updated.
