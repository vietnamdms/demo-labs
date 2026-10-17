# Workflow Video Google
Updated: 2026-10-17 13:48 +07

Bộ 8 skill Codex để sản xuất video bằng Google Flow: ý tưởng → kịch bản có hook → phân shot → bộ tham chiếu → start/end frame → animatic → clip → bản dựng cuối.

Hỗ trợ hai nhánh kịch bản: TikTok/YouTube Shorts và YouTube dài. Mỗi shot giữ cặp ảnh đầu/cuối; lời dẫn và timing được chuẩn bị trước khi render.

## Where to look

| Nhu cầu | Tài liệu |
| --- | --- |
| Cài đặt, cách gọi và lệnh kiểm tra | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Chạy workflow đầy đủ hoặc tiếp tục project | [video-workflow](skills/video-workflow/SKILL.md) |
| Thiết kế nội dung, câu chuyện và CTA | [content-strategy.md](skills/video-workflow/references/content-strategy.md) |
| Hợp đồng dữ liệu và phiên bản | [contracts.md](skills/video-workflow/references/contracts.md) |
| Ví dụ short, long và sửa project | [examples.md](skills/video-workflow/references/examples.md) |
| Tình huống nghiệm thu | [acceptance.md](skills/video-workflow/references/acceptance.md) |

## Skills

| Skill | Trách nhiệm |
| --- | --- |
| [video-workflow](skills/video-workflow/SKILL.md) | Điều phối, trạng thái, phụ thuộc và ngân sách |
| [video-script-short](skills/video-script-short/SKILL.md) | Kịch bản TikTok/Shorts có hook và payoff |
| [video-script-youtube](skills/video-script-youtube/SKILL.md) | Kịch bản YouTube dài, chương và concept title/thumbnail |
| [video-shotlist](skills/video-shotlist/SKILL.md) | Shot, camera, hành động, trạng thái đầu/cuối và timing |
| [video-visual-bible](skills/video-visual-bible/SKILL.md) | Nhân vật, sản phẩm, đạo cụ, bối cảnh và phong cách |
| [video-storyboard-frames](skills/video-storyboard-frames/SKILL.md) | Tạo và kiểm tra cặp frame từng shot |
| [video-flow-generate](skills/video-flow-generate/SKILL.md) | Kiểm tra khả năng Flow, tạo take và chọn clip |
| [video-assemble](skills/video-assemble/SKILL.md) | Chuẩn bị âm thanh, dựng animatic và bản cuối |

## Nâng cấp nội dung theo Inbound Content

Cả tám skill đã bổ sung tiêu chí nội dung từ brief đến bản dựng: hoàn cảnh khán giả, một ý chính, nhân vật và thay đổi, hook/payoff, thoại nhiều vai, CTA phù hợp và đo lường theo mục tiêu. Nhánh short tập trung một tình huống; nhánh YouTube dài phát triển câu hỏi qua từng chương. Hướng dẫn đầy đủ nằm tại [thiết kế nội dung](skills/video-workflow/references/content-strategy.md).

Các trường biên tập là phần mở rộng tương thích dữ liệu v1.0; helper hiện giữ nguyên và chưa tự kiểm tra các trường mới. Project cũ có thể tiếp tục, bổ sung thông tin khi sửa nội dung. Đây là nâng cấp hướng dẫn, chưa có kết quả đo hiệu quả video với người xem.

## Status

Đã triển khai bộ skill và hai helper cục bộ. Cấu trúc, liên kết và các kiểm tra helper đã được xác minh; xem [evidence](CONTRIBUTING.md#verification-evidence). Chưa chạy sản xuất trên tài khoản Flow hoặc đo chất lượng sáng tạo trên video thực.

## Repository layout

```text
workflow-video-google/
├── README.md
├── CONTRIBUTING.md
├── skills/
│   ├── video-workflow/
│   ├── video-script-short/
│   ├── video-script-youtube/
│   ├── video-shotlist/
│   ├── video-visual-bible/
│   ├── video-storyboard-frames/
│   ├── video-flow-generate/
│   └── video-assemble/
└── tests/
    └── test_video_skills.py
```

Không kèm video, ảnh người dùng, dữ liệu tài khoản hoặc credential. Các project tạo sau này nên lưu ở thư mục riêng; `projects/` trong lab đã được ignore.
