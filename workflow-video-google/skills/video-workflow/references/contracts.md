# Hợp đồng dữ liệu v1.0
Updated: 2026-10-17 13:48 +07

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

### Content strategy

Mở rộng biên tập tương thích schema_version="1.0": dùng cho project mới hoặc khi sửa nội dung có ý nghĩa; không bắt project cũ điền lại chỉ để tiếp tục render. Helper hiện chưa kiểm tra các trường mở rộng này; skill phải rà soát ngữ nghĩa và liên kết vai/thoại. Không xem `validate` pass là đã duyệt nội dung.

Nguồn chuẩn quyết định biên tập là `script.content_strategy`; bản Markdown trình bày tóm tắt quyết định này cùng hook/payoff. Ví dụ sau chỉ là object mở rộng, không phải một script đầy đủ:

```json
{
  "audience_situation": "Người chơi thấy game giật và định đổi router trước khi kiểm tra",
  "audience_need": "Biết cần kiểm tra gì trước khi chọn cách xử lý",
  "audience_basis": "Giả định sáng tạo từ brief, chưa khảo sát người xem",
  "journey_stage": "awareness",
  "core_takeaway": "Nhìn cả FPS và ping trước khi chọn hướng xử lý",
  "narrative_mode": "story",
  "story": {
    "protagonist_id": "tiny.gray",
    "goal": "Chơi ổn định và tránh mua nhầm thiết bị",
    "conflict": "Quy mọi biểu hiện giật cho Wi-Fi",
    "discovery": "Nhận thấy FPS tụt dù ping đang ổn trong ví dụ",
    "resolution": "Hoãn mua để kiểm tra trước"
  },
  "primary_cta": {
    "action": "Đọc hướng dẫn kiểm tra",
    "benefit": "Biết các bước khoanh vùng vấn đề",
    "destination": "Bài hướng dẫn đã xác minh trong research của project"
  },
  "measurement_plan": null
}
```

journey_stage: awareness/consideration/decision/not-applicable/unknown. narrative_mode: story/explanation/tutorial; chọn theo nhiệm vụ, không áp đặt mục tiêu marketing. Với explanation/tutorial, `story` có thể null; lời hứa và câu trả lời vẫn nằm ở hook/payoff. `primary_cta` có thể null nếu kết thúc không cần CTA. `measurement_plan`, khi nhiệm vụ cần, chứa hypothesis, signals[], baseline (null nếu chưa biết), observed_results (null trước đo). Không bịa mục tiêu, nghiên cứu khán giả hoặc kết quả.

Beat có thể thêm `story_function` (chức năng của beat) và `viewer_change` (điều người xem hiểu/cảm/làm khác sau beat). Các trường này giải thích role hiện có, không thêm giá trị vào enum role. Chapter dài có thể thêm `viewer_question`, `takeaway`, `evidence_plan`, `transition_reason`; thông tin đang cần quay/đo phải được phân biệt với nguồn đã có trong source_urls.

### Thoại và vai kể

Với nhiều người nói, khai báo `script.characters[]`: character_id, name, proposed_role, confirmed_features[], voice_direction, asset_id (nullable khi chưa có asset). Character ID là định danh vai; asset_id nối đến bộ tham chiếu, không tự coi đã có ảnh. Narrator có thể là một vai riêng không có asset. Phân biệt mô tả nhân vật do người dùng xác nhận với đề xuất diễn xuất.

Beat/cue có lời dùng `speaker_id` trỏ character_id tương ứng; beat im lặng có thể null. Với nhiều lượt nói, tách beat/cue có ID riêng để không nhét nhiều người vào một speaker_id. Độc thoại cũ không có characters vẫn hợp lệ; khi cần đối chiếu nhiều vai, chuẩn hóa mapping trước khi sản xuất thoại.

Shot có một lượt thoại có thể ghi speaker_id/dialogue để đối chiếu; nhiều lượt trong shot dùng audio_cue_ids theo thứ tự, ghi người nói ngoài hình nếu cần. Script sở hữu lời chuẩn; audio-plan sở hữu cue/track và thời gian thực; shot không tự sửa lời. Skill rà speaker tồn tại, text khớp và cue thuộc beat của shot trước bàn giao.

## shotlist.json

Required: timing_basis (estimated/measured/action), shots[].

shots[]: shot_id, scene_id, beat_ids[], purpose, duration_s (>0, thời gian bản dựng), generation_duration_s (null hoặc >0), camera, start_state, end_state, motion, reference_ids[], audio_mode, audio_cue_ids[], continuity, transition, handles.

continuity: screen_direction, eyeline, subject_positions, props_state, lighting. Ghi mô tả ngắn, không bịa số đo chính xác.

transition: type (cut/match-cut/continuous/dissolve/end), target_shot_id (null ở cuối). handles: head_s/tail_s >=0. Nếu generation_duration_s đã biết thì phải >= duration_s + handles; nếu dissolve chồng thời gian, edit-plan là nguồn timing cuối và phải ghi rõ chênh lệch với tổng shot thô.

Có thể thêm `story_action` cho hành động nhìn thấy thực hiện purpose; đây không phải trường thay thế start_state/end_state/motion.

Mọi beat phải có shot phủ nội dung, kể cả ending chữ/âm thanh. narration có thể đi qua nhiều shot, cue không phải đơn vị render. Đổi ý tưởng nội dung thì sửa script trước; đổi camera thì sửa shotlist.

## assets.json

Required: assets[]. Entry: asset_id, type (character/product/prop/location/style), scope (series/episode/scene), description, fixed_features[], allowed_variations[], image_paths[], source_url (nullable), review. Ảnh ở references/ của project, không trùng references/ của skill. JSON/MD mô tả không thay thế ảnh tham chiếu.

Character asset có thể thêm `performance_profile`: role, motivation, relationships, speech_style, reaction_style, allowed_emotional_changes, evidence_status. `evidence_status` phân biệt chi tiết được cung cấp với đề xuất. Nguồn chuẩn profile diễn xuất nằm ở assets.json; script chỉ giữ thông tin vai/giọng cần viết, nếu thay đổi phải đối chiếu và cập nhật profile. Trạng thái theo thời gian của đạo cụ thuộc shotlist, không thuộc fixed_features.

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

## Dependency cho nội dung tổng hợp

Khi đăng ký beat scoped, `script` tổng hợp phải phụ thuộc mọi `beat.Bxx` hiện có và tài liệu vai diễn thực sự dùng. `script.readable` và `audio.plan` phụ thuộc script; `shot.Sxx` phụ thuộc beat/cue/asset thực sự dùng. Không đăng ký beat song song với script rồi bỏ mất cạnh phụ thuộc tổng hợp: sửa beat phải làm bản đọc và audio cần rà soát.

Có thể đăng ký `strategy` là scope `/content_strategy` trong script.json, phụ thuộc brief/research tương ứng. Khi dùng cách này, các beat phụ thuộc strategy; strategy không phụ thuộc script tổng hợp, tránh chu trình. Nếu không đăng ký scope riêng, coi thay đổi strategy là thay đổi input nội dung và đánh dấu các beat chịu ảnh hưởng trước downstream.

Chèn/xóa beat: giữ ID còn đúng chức năng, thêm ID mới, cập nhật selector, danh sách dependency và coverage; loại entry active đã bỏ chỉ sau khi xử lý các dependency còn trỏ tới nó, lưu bản cũ để tra cứu. Bản đề xuất để riêng thư mục không tự thay bản đang sản xuất. Khi nhận bản đề xuất, đồng bộ JSON/Markdown, shot, cue và manifest theo thay đổi thực, không tăng version hàng loạt rồi coi media đã được làm lại.
