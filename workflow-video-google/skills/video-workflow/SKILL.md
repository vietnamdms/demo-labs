---
name: video-workflow
description: "Điều phối project sản xuất video bằng Google Flow từ ý tưởng, kịch bản TikTok/YouTube Shorts hoặc YouTube dài đến storyboard start/end frame và bản dựng. Dùng khi cần chạy toàn workflow, tiếp tục project, hoặc sửa các đầu ra phụ thuộc. Các yêu cầu chỉ viết kịch bản hay chỉ tạo frame dùng skill chuyên trách."
---

# Video Workflow
Updated: 2026-10-17 11:03 +07

Điều phối bộ 8 skill cho video dựa trên storyboard. Trả lời và viết kịch bản theo ngôn ngữ người dùng; mặc định tiếng Việt nếu brief chưa chỉ định. Đọc [hợp đồng dữ liệu](references/contracts.md) trước khi tạo hoặc cập nhật project; chỉ đọc tài liệu của bước đang làm.

## Bắt đầu hoặc tiếp tục

1. Tìm project.json trong thư mục người dùng chọn. Nếu chưa có, chuẩn hóa ý tưởng, format, platform, khán giả, mục tiêu, thời lượng, tỉ lệ, phong cách và chế độ âm thanh. Ghi giả định có thể sửa; chỉ hỏi điều còn thiếu thực sự chặn bước tiếp theo.
2. Giữ đúng phạm vi yêu cầu: planning tạo tài liệu; production tạo media trong phạm vi đã được cho phép. Yêu cầu tạo một skill không phải yêu cầu chạy sản xuất video.
3. Kiểm tra công cụ ảnh, truy cập Flow, âm thanh và dựng có sẵn; không tuyên bố đã kết nối từ việc chỉ tìm thấy tài liệu. Thiếu một công cụ không chặn các phần độc lập còn làm được.
4. Với nội dung thực tế cần kiểm chứng, dùng nguồn phù hợp và chuyển source URLs cho script. Không bịa số liệu để tăng sức hút hook. Truyện hư cấu không mặc định cần nghiên cứu web.

Có thể khởi tạo manifest bằng helper không dùng dịch vụ trả phí:

```bash
python3 scripts/project.py init /absolute/project-dir --id coffee-morning --format short --platform youtube-shorts --idea 'Một buổi sáng chậm lại cùng cà phê' --duration 30
```

Đường dẫn `scripts/` trong lệnh là tương đối với thư mục skill này; chạy bằng đường dẫn tuyệt đối khi cwd khác. Nếu đã có project, đọc nó; không ghi đè để khởi tạo lại.

## Điều phối theo đầu ra

| Bước | Skill cùng bộ | Khi nào xong |
|---|---|---|
| Kịch bản short | [video-script-short](../video-script-short/SKILL.md) | Hook, lời hứa, nội dung và payoff liên kết được |
| Kịch bản dài | [video-script-youtube](../video-script-youtube/SKILL.md) | Concept tiêu đề/thumbnail, chương và bản lời đọc đầy đủ |
| Phân shot nháp | [video-shotlist](../video-shotlist/SKILL.md) | Mỗi shot có trạng thái đầu/cuối và hành động |
| Lời dẫn thử | [video-assemble](../video-assemble/SKILL.md), prepare-audio | Timing được đo nếu có lời; phân biệt nháp/final |
| Chốt timing | video-shotlist | Cập nhật theo lời dẫn hoặc nhịp hành động |
| Tham chiếu | [video-visual-bible](../video-visual-bible/SKILL.md) | Nhận diện và biến thể có chủ ý được định nghĩa |
| Cặp frame | [video-storyboard-frames](../video-storyboard-frames/SKILL.md) | Ảnh thật tồn tại, được xem và đánh giá |
| Dựng nháp | video-assemble, animatic | Nhịp/hook/payoff đã kiểm tra qua bản ảnh có thời gian |
| Tạo clip | [video-flow-generate](../video-flow-generate/SKILL.md) | Có clip được chọn, đã kiểm tra cả chuyển động và âm thanh |
| Dựng cuối | video-assemble, final | File xuất đúng yêu cầu và đã được xem/nghe |

Skill điều phối thực hiện các bước trong cùng phiên; không đồng nghĩa tạo chat hay subagent. Mốc kiểm tra chất lượng không tự sinh bước xin duyệt. Tôn trọng mốc duyệt người dùng đã đặt và quyền thao tác hiện có.

## Trạng thái, sửa đổi, chi phí

- Ghi project.json sau mỗi đầu ra quan trọng. Dùng ID ổn định; đánh dấu version nguồn của từng artifact. Xem [contracts.md](references/contracts.md) về nguồn chuẩn.
- Khi sửa một shot/frame/lời dẫn, chỉ đánh dấu các artifact thật sự phụ thuộc. Dùng dependency theo shot/beat, tránh gắn mọi clip vào toàn bộ tài liệu nếu không cần.
- Trước khi tiếp tục render, đối chiếu job/take đang chạy. `unknown` nghĩa chưa biết kết quả, không nghĩa thất bại; kiểm tra trước khi gửi lại.
- Budget credit chưa biết là null, không là 0 hoặc vô hạn. Lấy chi phí từ UI khi chạy. Đã có ngân sách thì tiếp tục trong giới hạn đó; chưa có thì hoàn thiện gói đầu vào và xác định giới hạn cần thiết trước hành động phát sinh chi phí.
- Không tăng retry vô hạn. Helper chỉ kiểm tra trạng thái, không quản lý giao dịch credit hoặc tự hủy job.

```bash
python3 scripts/project.py validate /absolute/project-dir
python3 scripts/project.py revise /absolute/project-dir --artifact frame.S03.end --reason 'Đổi vị trí tách ở cuối shot'
```

`revise` tăng version artifact đã sửa và đánh dấu nó cùng các phụ thuộc cần rà soát; không sửa file media hay gọi dịch vụ. Chỉ dùng sau khi lưu nội dung thay đổi. Đọc kết quả trước khi làm lại phần liên quan.

## Bàn giao

Nêu phần hoàn thành, đường dẫn, phần còn chặn và bước tiếp theo. Phân biệt kịch bản/prompt, animatic và video final. Không tự đăng bài. Ví dụ cấu trúc thực tế: [examples.md](references/examples.md); tiêu chí nghiệm thu bộ skill: [acceptance.md](references/acceptance.md).
