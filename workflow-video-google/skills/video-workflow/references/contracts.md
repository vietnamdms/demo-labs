# Hợp đồng dữ liệu v1.0
Updated: 2026-10-17 11:03 +07

Đây là nguồn chuẩn dùng chung của bộ 8 skill. Đọc phần đang xử lý; không cần nạp mọi ví dụ. Lưu project riêng với thư mục skill. JSON UTF-8, schema_version="1.0", số thời gian tính bằng giây. Không dùng 0 để biểu thị giá trị chưa biết: dùng null.

## Quy ước chung

- Mỗi tài liệu JSON có schema_version, project_id, version (số nguyên dương). project.json là registry và cũng có version.
- ID ổn định: B01 (beat), C01 (chapter), SC01 (scene), S01 (shot), H01 (hook), character.mai (asset), T-S01-01 (take). Không tái đánh số khi xóa/chèn; ID mới không tái sử dụng ID cũ.
- Path tương đối tính từ thư mục chứa project.json, không từ skill. Helper từ chối path ra ngoài project để tránh ghi nhầm. Copy/import tài nguyên cần dùng vào project; giữ nguồn gốc trong source_url nếu cần.
- `review`: `{ "status": "unchecked|pass|needs-revision", "notes": "..." }`. Pass phải dựa trên việc đã kiểm tra thật, không chỉ file tồn tại.
- Artifact `status`: planned, ready, needs-revision, blocked. Job có trạng thái riêng. Ready cần file thật, review pass, các dependency đúng version và ready. Một artifact planning (script/prompt) ready không có nghĩa media ready.
- Trường chưa mô tả có thể thêm có mục đích; không đổi ý nghĩa trường hiện có. Helper kiểm tra liên kết và bất biến quan trọng, không phải JSON Schema validator đầy đủ hoặc hệ thống đánh giá nghệ thuật.

## project.json

```json
{
  "schema_version": "1.0",
  "project_id": "coffee-morning",
  "version": 1,
  "brief": {
    "idea": "Một buổi sáng chậm lại cùng cà phê",
    "format": "short",
    "platform": "youtube-shorts",
    "language": "vi",
    "audience": "Người thích những câu chuyện đời thường",
    "goal": "Kể một khoảnh khắc thư giãn",
    "target_duration_s": 30,
    "aspect_ratio": "9:16",
    "style": "Tự nhiên, ánh sáng buổi sáng",
    "audio_mode": "narration",
    "assumptions": []
  },
  "budget": { "max_credits": null, "max_attempts_per_shot": 2 },
  "artifacts": []
}
```

format: short/youtube-long. platform: tiktok/youtube-shorts cho short, youtube cho long. aspect_ratio: 9:16/16:9/1:1 (không hàm ý Flow hỗ trợ mọi tỉ lệ). audio_mode: narration/sync-dialogue/ambient/none. Retry=2 là giới hạn mặc định có thể đổi, không là cho phép chi tiêu; max_credits=null nghĩa chưa chốt.

Artifact record:

```json
{
  "id": "frame.S03.end", "kind": "image", "scope": "S03", "version": 1,
  "path": "frames/S03/end.png", "status": "planned",
  "depends_on": [{ "id": "frame.S03.start", "version": 1 }],
  "review": { "status": "unchecked", "notes": "Chưa tạo ảnh" }
}
```

Registry chứa cả document và media: kind=document/image/audio/video. Chỉ đăng ký file sẽ tạo hoặc đã có, không chèn placeholder media. File planned có thể chưa tồn tại. Ready bắt buộc tồn tại, không rỗng; helper không kiểm tra codec. Tài nguyên remote phải tải về bằng công cụ cho phép trước khi dùng helper local; source_url có thể ghi kèm. Khi môi trường không cho tải, giữ bàn giao remote và ghi giới hạn helper.

Có thể đăng ký phần riêng trong cùng JSON bằng `scope` và `selector` JSON Pointer, ví dụ id=shot.S03, path=shotlist.json, selector=/shots/2. Index là vị trí hiện tại, ID là định danh ổn định: cập nhật selector nếu sắp xếp lại. Scope giúp tránh invalidation cả project. Version artifact scoped chỉ tăng khi phần đó thay đổi, không tự tăng theo file container. Helper xác minh selector tồn tại; người dùng skill đối chiếu ID/nội dung.

Dependency luôn trỏ ID và version cụ thể. Ví dụ clip.S03.T01 → frame.S03.start/end, shot.S03 và audio cue nếu clip sinh thoại; không gắn vào mọi frame trong tập. Chỉ nội dung thực sự dùng làm input mới là dependency. Registry là đồ thị không chu trình.

## script.json

Required: format, platform, hook, chapters, beats ngoài envelope chung.

hook: hook_id, beat_id, promise, visual, spoken, on_screen_text, payoff_beat_id. promise/visual không rỗng; spoken/on_screen_text được rỗng cho hook hình ảnh. Hook là một beat role=hook, payoff trỏ beat role=payoff ở sau. Độ dài hook không cố định.

beats[]: beat_id, chapter_id (null cho short), role (hook/content/payoff/ending), spoken, visual, estimated_duration_s (>0), source_urls[]. Lời đọc nằm trọn trong spoken; chỉ dẫn quay không trộn vào lời đọc.

chapters[]: chapter_id, title, purpose. Short thường là []; long có ít nhất một chương và mọi beat liên kết chapter hợp lệ. Long còn có packaging: title_concept, thumbnail_concept, promise; đây là kế hoạch chưa phải asset thumbnail.

Nguồn chuẩn nội dung là script.json; script.md là bản trình bày sinh từ JSON. Nếu người dùng sửa Markdown, nhập lại thay đổi vào JSON và tăng version trước downstream. Không sửa hai bản độc lập rồi coi chúng đồng bộ. Script đầy đủ không được thay bằng tóm tắt.

## shotlist.json

Required: timing_basis (estimated/measured/action), shots[].

shots[]: shot_id, scene_id, beat_ids[], purpose, duration_s (>0, thời gian bản dựng), generation_duration_s (null hoặc >0), camera, start_state, end_state, motion, reference_ids[], audio_mode, audio_cue_ids[], continuity, transition, handles.

continuity: screen_direction, eyeline, subject_positions, props_state, lighting. Ghi mô tả ngắn, không bịa số đo chính xác.

transition: type (cut/match-cut/continuous/dissolve/end), target_shot_id (null ở cuối). handles: head_s/tail_s >=0. Nếu generation_duration_s đã biết thì phải >= duration_s + handles; nếu dissolve chồng thời gian, edit-plan là nguồn timing cuối và phải ghi rõ chênh lệch với tổng shot thô.

Mọi beat phải có shot phủ nội dung, kể cả ending chữ/âm thanh. narration có thể đi qua nhiều shot, cue không phải đơn vị render. Đổi ý tưởng nội dung thì sửa script trước; đổi camera thì sửa shotlist.

## assets.json

Required: assets[]. Entry: asset_id, type (character/product/prop/location/style), scope (series/episode/scene), description, fixed_features[], allowed_variations[], image_paths[], source_url (nullable), review. Ảnh ở references/ của project, không trùng references/ của skill. JSON/MD mô tả không thay thế ảnh tham chiếu.

## frames.json

Required: pairs[]. Entry: shot_id, start_path, end_path, start_artifact_id, end_artifact_id, start_prompt, end_prompt, reference_ids[], review. Mọi shot phải có đúng một cặp. Có thể cùng file khi chủ ý giữ trạng thái, vẫn phải đủ hai trường. Paths phải trùng registry tương ứng. Lưu ảnh thật ở frames/S01/start.png, end.png hoặc định dạng thực.

## audio-plan.json

Required: audio_mode, stage (scratch/final/none), path (nullable), duration_s (nullable), timing_basis (estimated/measured/action), cues[]. cue: cue_id, beat_ids[], start_s, end_s, text, pronunciation_notes. Thời gian bắt đầu >=0, kết thúc > bắt đầu, không vượt duration đo được. Một track narration không chồng cue; nếu đa thoại/track cần thêm track_id và editor phù hợp.

Với none: stage=none, path=null, cues=[]; video có tiếng môi trường chưa có track riêng có thể path=null. Không khai timing measured cho một lời dẫn chưa có file. Cues không tự chứng minh lời nói được phát âm đúng.

## renders.json

Required: capability, takes[], selected (map shot_id → take_id).

capability: checked_at (ISO 8601 có timezone), evidence_url hoặc evidence_notes, model, mode, aspect_ratio, allowed_durations_s[], resolution, supports_audio, credits_per_output (nullable), supports_first_last_frame. Chỉ ghi những gì đã quan sát; unknown không được chuyển thành true.

take: take_id, shot_id, input_versions[] ({id,version}), request_fingerprint (chuỗi băm ổn định do script/tool tạo hoặc mô tả nhận diện, không bịa hash), prompt, model, mode, generation_duration_s, outputs_requested, job_id (nullable), project_url (nullable), status, path (nullable), observed_credits (nullable), review.

status: planned/submitted/running/succeeded/failed/unknown/downloaded. Submitted trước có thể chưa có job_id; unknown sau timeout cần đối chiếu UI. Downloaded đòi file; selected đòi downloaded, review pass và input_versions còn hợp lệ/ready. Không chọn take đang chạy. observed_credits là giá trị quan sát, không dùng estimate thay cho actual. Một lượt nhiều output phải ghi rõ để tính ngân sách.

## edit-plan.json

Required: mode (animatic/final), width, height (số nguyên dương chẵn), fps (>0), segments[], audio_path (nullable). Paths tính từ thư mục project; helper yêu cầu edit-plan.json đặt ngay thư mục project.

Animatic segment: shot_id, start_frame, end_frame, duration_s (>0). Renderer ghép hai ảnh mỗi ảnh nửa duration, có thể lệch tối đa một frame do làm tròn; muốn timing chi tiết hơn dùng editor riêng. Không tự thêm transition hoặc tạo chuyển động AI.

Final segment: shot_id, take_id, video_path, trim_in_s (>=0), duration_s. Chọn clip từ renders.selected. Ghi thêm audio tracks, subtitles, overlays và transition nếu editor hỗ trợ; helper animatic từ chối mode final.

Timeline phải đủ toàn bộ nội dung; trim không vượt độ dài clip đo được. Audio dài hơn timeline không được tự cắt mất câu. audio_path là một track guide cho helper animatic; final có thể dùng nhiều track qua editor.

## Kiểm tra và thay đổi

Helper project.py validate đọc các tài liệu chuẩn hiện có, kiểm tra IDs, dependency/version, ready file/review, hook→payoff, liên kết shot/frame/take và media path. Chưa có document của bước sau không là lỗi project nháp; bản final cần đủ đầu ra theo brief, do skill điều phối đánh giá.

Sau sửa, revise tăng version artifact mục tiêu, đánh dấu mục tiêu và downstream needs-revision, review=unchecked. Không tự ghi dependency sang version mới: chỉ cập nhật sau khi thật sự kiểm tra/làm lại artifact đó. Backup manifest trước mọi mutation helper. Không xóa các take cũ.
