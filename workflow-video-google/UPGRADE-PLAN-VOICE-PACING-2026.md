# Kế hoạch nâng cấp: giữ giọng nhân vật và tăng nhịp video
Updated: 2026-10-17 14:49 +07

Trạng thái: đã triển khai phần hướng dẫn và hợp đồng cho cả tám skill theo yêu cầu tiếp theo của người dùng. Kết quả kiểm tra và đồng bộ bản cài ghi tại [CONTRIBUTING.md](CONTRIBUTING.md#cập-nhật-giữ-giọng-và-nhịp-dựng--17102026). Pilot Flow, nghe duyệt giọng và bản Tiny dựng nhanh là công việc sản xuất riêng, chưa được thực hiện trong lần cập nhật skill.

## Mục tiêu và phạm vi

Giữ bộ tám skill hiện có. Bổ sung một chuẩn giọng cho từng nhân vật xuyên cảnh và xuyên tập, đồng thời làm nhịp short nhanh hơn bằng nội dung, hành động và dựng. Giữ nhánh YouTube dài với nhịp theo chương; không áp dụng máy móc thông số short.

Với project Tiny: ảnh, nhân vật, video và giọng sinh bằng model Google trong Google Flow; giữ dấu Google. Start/end frame vẫn là yêu cầu sản xuất. Mốc 300 credit thuộc lần sản xuất đã được cho phép, đã dùng 200 theo bản bàn giao; kế hoạch này không phát sinh chi phí hoặc tự mở rộng ngân sách.

## Cơ sở nghiên cứu

Đối chiếu nguồn chính thức ngày 17/10/2026. Phân biệt báo cáo xu hướng, hướng dẫn sáng tạo và tính năng được tài khoản thực sự hỗ trợ.

| Nguồn | Điều có thể áp dụng | Giới hạn |
| --- | --- | --- |
| [TikTok Next 2026](https://ads.tiktok.com/business/library/TikTok_Next_2026_Trend_Report.pdf) | Tình huống gần gũi, sự tò mò và lợi ích có lý do; Tiny có thể kể sai lầm quen thuộc của game thủ và phát hiện giúp tránh mua nhầm | Báo cáo dự báo văn hóa; không quy định mỗi cảnh phải dài bao nhiêu giây và không xác nhận một meme đang thịnh hành tại Việt Nam |
| [TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices) — cập nhật 06/2025 | Đưa giá trị nội dung vào ba giây đầu, dùng hook sớm, chữ hỗ trợ và CTA rõ | Hướng dẫn cho quảng cáo; dùng làm điểm khởi đầu cho organic, không coi là quy tắc thuật toán 2026 |
| [YouTube Shorts deep dive](https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/) — 28/01/2025 | Cuộc trao đổi với creator nhấn mạnh hook ngay giây đầu và câu chuyện ngắn có điểm thỏa mãn | Lời khuyên từ cuộc trao đổi, không phải ngưỡng xếp hạng bắt buộc |
| [Google Flow: Create videos](https://support.google.com/flow/answer/16353334?hl=en) | Hướng dẫn voice reference một người nói qua Omni Flash, Ingredients và Voices; có custom voice từ preset | Tài liệu hiện ghi voice reference chỉ dùng với Ingredients; các kiểu generation khác sẽ báo lỗi |
| [Google Flow models/features](https://support.google.com/flow/answer/16352836?hl=en) | Gemini Omni Flash hỗ trợ custom voices và các mode hình ảnh khác nhau | Các tính năng riêng lẻ không chứng minh voice reference dùng đồng thời với first+last frames; vẫn cần kiểm tra UI, vùng và tài khoản |

Không gọi một nhịp cắt đề xuất là “chuẩn trend 2026”. Khi sản xuất một tập theo trend cụ thể, ghi ví dụ đang hoạt động trong ngách, thị trường, URL và ngày quan sát; kiểm tra lại trước sản xuất nếu ví dụ đã cũ. Không tự tải nhạc hoặc đưa meme không liên quan vào video Tiny.

## Rule giữ nguyên giọng nhân vật

Nội dung dự kiến đưa vào nguồn hướng dẫn dùng chung, rồi liên kết từ các skill liên quan:

> Mỗi nhân vật có thoại phải ánh xạ đến một hồ sơ giọng có version và một mẫu âm thanh chuẩn đã được nghe kiểm tra. Mọi lượt thoại và take dùng đúng hồ sơ đó. Giữ căn tính giọng, âm sắc, âm vực nền, giọng vùng và cách phát âm tên riêng; cảm xúc, nhấn nhá và độ mạnh được thay đổi theo diễn xuất. Không chọn take khi giọng bị đổi hoặc hoán đổi người nói. Chưa nghe đối chiếu với mẫu thì để review=unchecked. Chỉ đổi hồ sơ giọng khi yêu cầu sáng tạo cho phép và phải cập nhật các đầu ra phụ thuộc.

“Giữ nguyên” nghĩa là giữ căn tính có thể nhận ra; không hứa hai waveform giống hệt nhau khi lời thoại khác nhau. Tăng nhịp dựng không được làm đổi pitch hoặc biến nhân vật thành người nói khác.

Các điều kiện thực thi:

1. Mẫu phải có một người nói rõ, không lẫn vai còn lại hoặc nhạc che lời. Chọn từ clip đã có nếu phù hợp; chỉ sinh mẫu mới khi cần và trong quyền chi tiêu hiện có. Với Tiny, giọng Xám và Nâu hiện chưa được nghe duyệt đầy đủ nên chưa được coi là đã khóa.
2. Lưu mô tả giọng và mẫu thực tế. Mô tả bằng chữ, prompt lặp lại, cùng model hoặc cùng character image không chứng minh đã giữ giọng.
3. Chuẩn phát âm tối thiểu cho Tiny: Tiny, Wi-Fi, ping, FPS, LAN. Chốt bằng nghe mẫu; ASR hỗ trợ rà lời thiếu/lặp, không duyệt căn tính giọng.
4. Tái dùng cùng voice reference/ID khi mode và model hỗ trợ. Ghi chính xác model, mode, reference và version vào từng take trước submit.
5. Nghe đối chiếu từng nhân vật với mẫu và nghe nối các cảnh của cùng vai. Kiểm tra cả đổi vai, giọng vùng, âm sắc, phát âm và khẩu hình tại điểm cắt.
6. Take lệch giọng là needs-revision, không đưa vào selected. Hết retry/budget thì bàn giao phần đạt và lỗi còn lại; không tự thay bằng giọng ngoài Google Flow.

### Xử lý xung đột Frames và voice reference

Điểm cần giải quyết trước batch render có thoại: tài liệu Google hiện yêu cầu Ingredients cho voice reference, trong khi project Tiny yêu cầu render có first+last frames. Không suy ra hai cơ chế kết hợp được vì cùng xuất hiện trong một model.

Trong bước triển khai, kiểm tra UI/capability thực tế trước. Nếu có tổ hợp hợp lệ, lưu evidence rồi làm pilot có hai câu khác nhau của mỗi vai trước khi nhân rộng. Nếu chỉ có Ingredients+Voice, ghi đây là nhánh thay đổi cách điều khiển frame, chưa đáp ứng yêu cầu render hiện tại. Tiếp tục chuẩn bị script, storyboard và timing; chỉ lập batch thoại sau khi có phương án thỏa các ràng buộc. Không dùng prompt-only để gắn nhãn voice-locked, không ghép voiceover lên khẩu hình khác rồi gọi là sync-dialogue đạt.

## Nhịp short đề xuất cho Tiny

Các số dưới đây là cấu hình thử nghiệm sáng tạo, cần đo bằng audio và xem animatic; không phải thông số chính thức của TikTok hoặc YouTube.

| Thành phần | Điểm khởi đầu đề xuất | Cách kiểm tra |
| --- | --- | --- |
| Tổng thời lượng | 30–33 giây từ bản xem duyệt 40 giây | Giữ đủ hai nhánh FPS/ping, câu điều kiện, thao tác kiểm tra và payoff |
| Mở đầu | Tình huống/hành động có vấn đề xuất hiện ngay; người xem hiểu giá trị trong ba giây | Bỏ khoảng đứng chờ và intro logo riêng |
| Tiến triển trong hình | Thử một thay đổi có ích mỗi 1–2 giây: phản ứng, insert, chữ khóa hoặc đổi góc | Không bắt buộc tạo clip AI mới hoặc thêm hiệu ứng ở mọi mốc |
| Shot | Phản ứng/insert có thể 0,7–1,5 giây; thoại thường cần 2–4 giây hoặc hơn | Chọn theo câu nói và hành động thực; không cắt mất phát hiện hoặc nối trạng thái sai |
| Nhịp thoại | Giữ tốc độ giọng tự nhiên; giảm câu lặp, chờ đầu/cuối và khoảng im không có chức năng | Mặc định playback_rate=1.0 cho thoại; nghe lại toàn câu và nối vai |
| Câu giải thích dài | Cho audio liên tục đi qua insert/phản ứng bằng J-cut/L-cut khi phù hợp | Giữ rõ ai nói; không cho thấy miệng vai khác đang nói câu đó |
| Phụ đề | Cụm ngắn theo ý, thường 3–6 từ mỗi cụm, tối đa hai dòng | Đây là kích thước cụm, không phải tốc độ đọc; xem trên màn hình nhỏ và giữ safe zone |
| Chữ trong hình | Một ý trọng tâm mỗi thời điểm | Giảm lặp nguyên câu ở cả nhãn giải thích lẫn phụ đề; giữ nhãn giả định và dấu Google rõ |
| Âm thanh | Nhạc nền nhỏ và SFX ở thao tác quan trọng nếu phù hợp | Không che phụ âm hoặc biến ví dụ thành hiệu quả đã được chứng minh |
| CTA | Thử 2–3 giây nếu đích đến và lợi ích vẫn đọc được; kéo dài khi cần | Giữ một hành động chính, không ép đọc URL và câu dài quá nhanh |

Không thêm “pattern interrupt” chỉ vì đồng hồ đến mốc. Giữ khoảng dừng giúp người xem nhận ra thông tin mới; dùng cắt trên hành động, phản ứng và khám phá để tạo nhịp.

### Áp dụng cho bản Tiny hiện có

- S01/S02: đi thẳng vào hiểu nhầm Wi-Fi và lời ngăn lại; cắt thời gian chờ sau câu, giữ thao tác dán giấy.
- S09/S04: gọn phản ứng và câu hỏi; giữ chữ NẾU cho tình huống giả định.
- S03/S05: câu hướng dẫn vẫn đủ ý, thêm insert FPS/ping hoặc dây LAN để hình tiến triển trong khi một giọng nói liên tục. Chỉ dùng nguồn/asset phù hợp, không bịa số đo.
- S07: giữ cả “suýt mua nhầm” và quyết định đo trước, rút khoảng trống giữa hai câu bằng điểm nối có hình phủ phù hợp. Không cắt mất thao tác bóc giấy tạo payoff.
- S08: rút CTA bằng biên tập lời nếu cần; lời thay đổi phải cập nhật script/audio và có thể cần render lại, không hứa hoàn thành chỉ từ trim.

Thứ tự tối ưu: thử dựng từ take hiện có trước; chỉ lập danh sách render bổ sung cho vấn đề không sửa được bằng dựng. Mốc 30–33 giây có thể điều chỉnh nếu bản nghe đo thực tế không đủ chỗ; không tăng tốc toàn video để đạt con số.

## Kế hoạch cập nhật tám skill

| Skill | Thay đổi cần triển khai | Đầu ra/điều kiện hoàn thành |
| --- | --- | --- |
| video-workflow | Nhận yêu cầu voice consistency và pacing trong brief; điều phối kiểm tra khả năng kết hợp frame/voice; theo dõi version giọng và lỗi chặn batch | Có yêu cầu, nguồn giọng, ngân sách và route sản xuất rõ; không tự tuyên bố voice-locked |
| video-script-short | Hook có hành động ngay; câu thoại ngắn có phản hồi; mỗi beat có tiến triển; giữ phong cách nói của từng vai | Script đọc được, giữ hook/payoff và nghĩa kỹ thuật; có pacing profile short và phương án CTA gọn |
| video-script-youtube | Dùng cùng hồ sơ giọng cho narrator/nhân vật; nhịp theo câu hỏi/chương, thay đổi hình theo nội dung | Không ép video dài vào mốc 1–2 giây hoặc thời lượng 30–33 giây của Tiny |
| video-shotlist | Tách generation duration khỏi thời gian dựng; thêm kế hoạch insert/phản ứng, audio bridge và mốc hành động phải giữ | Trim/J-cut/L-cut có cue tham chiếu; đủ coverage và không đổi người nói |
| video-visual-bible | Mở rộng profile diễn xuất bằng hồ sơ giọng có mẫu, phát âm, version và biến thể cảm xúc được phép | Mỗi vai có mẫu thật đã nghe và mapping ổn định; không tạo skill thứ chín |
| video-storyboard-frames | Chuẩn bị cặp frame cho góc phản ứng/insert thực sự cần; giữ nhận diện và điểm nối khi cắt nhanh | Đủ start/end cho shot sản xuất; bố cục hỗ trợ crop nếu dùng mà không mất chi tiết hoặc dấu Google |
| video-flow-generate | Bổ sung preflight voice reference theo model/mode; prompt đúng speaker và hồ sơ giọng; pilot và review nối cảnh; fingerprint chứa input giọng | Take ghi nguồn/version giọng; lệch giọng bị loại; không render batch trong tổ hợp chưa được xác minh |
| video-assemble | Đối chiếu mẫu giọng, tối ưu khoảng chờ, audio bridge, caption, cân âm lượng và kiểm tra toàn timeline | Có bản nhanh hơn đo được, thoại tự nhiên, không đổi pitch, đủ nghĩa và âm thanh đã nghe |

## Dữ liệu và nguồn sở hữu dự kiến

Mở rộng có chủ đích trong contracts.md, giữ tên trường và ý nghĩa hiện có. Chỉ đổi schema_version nếu thay đổi không tương thích; không tạo voice-bible.json trùng với assets.json.

- assets.json: character asset sở hữu voice_profile, gồm voice_id, version, engine/model, language, accent, identity_description, locked_features, allowed_performance_changes, reference_path, reference_span_s, sample_text, pronunciation_dictionary và review. Mẫu chưa có thì path=null và review=unchecked.
- script.json: character_id/speaker_id tiếp tục sở hữu vai và lời; content_strategy.pacing ghi mode, target_duration_s, hook_goal_s, các khoảng tham khảo và lý do. Từ điển phát âm không được chép thành nhiều bản riêng theo shot.
- audio-plan.json: cue ghi speaker_id, voice_id và voice_version; track/timing thực thuộc audio-plan. Phần kiểm tra giọng dùng cùng enum review hiện có và ghi mẫu nào đã được nghe đối chiếu.
- renders.json: capability ghi hỗ trợ voice reference theo model/mode và khả năng kết hợp first+last, giá trị chưa biết để null; take lưu voice_inputs và kết quả review giọng. Request fingerprint bao gồm profile/reference version thực sự gửi.
- edit-plan.json: ghi audio source, các đoạn trim/audio bridge và speed thực của segment. Helper animatic hiện không hỗ trợ dựng đa track hoặc J/L-cut; không mô tả tính năng này như đã có sẵn.
- project.json: thêm dependency scoped của profile/mẫu giọng vào đúng cue/take dùng nó. Đổi căn tính giọng làm clip phụ thuộc cần review lại; chỉ đổi gain/mix không tự làm hỏng frame hoặc script không liên quan.

Hướng dẫn chung dự kiến đặt tại video-workflow/references/voice-continuity.md và pacing-short.md; SKILL.md liên kết đúng phần cần đọc. Flow runbook sở hữu thao tác/capability, assembly.md sở hữu kỹ thuật dựng; không sao chép toàn bộ rule vào tám nơi.

## Thứ tự triển khai và nghiệm thu

| Đợt | Công việc | Điều kiện chuyển tiếp |
| --- | --- | --- |
| 1 — chuẩn dữ liệu và giọng | Cập nhật contracts, reference chung, visual-bible, workflow và Flow preflight; rà mapping vai của Tiny | Phân biệt được profile đề xuất với mẫu đã khóa; xử lý rõ xung đột Frames/Voice; chưa cần render batch |
| 2 — viết và phân cảnh nhanh | Cập nhật hai skill script, shotlist, storyboard; tạo bản timing Tiny đề xuất | Có animatic đúng nghĩa và kế hoạch dùng lại take; thời lượng dựa trên đo khi có audio |
| 3 — tạo và dựng | Triển khai voice input/review trong flow-generate và audio bridge/caption/review trong assemble | Pilot hợp lệ trước batch; trong ngân sách; bản cuối được xem và nghe đầy đủ |
| 4 — xác minh và phân phối | Kiểm tra cấu trúc skill, liên kết, dependency và helper nếu có sửa; sao lưu trước đồng bộ bản cài | Phân biệt bản nguồn, bản cài và artifact sản xuất; ghi evidence thực; thao tác Git theo yêu cầu khi triển khai |

Các tình huống cần kiểm tra khi triển khai:

1. Cùng nhân vật hai câu khác nhau: nhận ra cùng giọng, dù cảm xúc khác.
2. Hai nhân vật đổi lượt nhanh: speaker, voice reference và khuôn mặt không bị hoán đổi.
3. Một take đúng lời nhưng lệch giọng: không được selected; ASR đúng không thay đổi kết luận này.
4. Voice reference không hỗ trợ mode Frames: phát hiện trước batch, không tự chuyển tool/model ngoài ràng buộc.
5. Sửa voice profile chỉ đánh dấu cue/clip/bản dựng liên quan; không làm lại ảnh không bị ảnh hưởng.
6. Cắt nhanh giữ nguyên nội dung hai nhánh FPS/ping, chữ giả định và payoff; phụ đề không vượt timeline hay che dấu Google.
7. Project cũ thiếu voice_profile vẫn đọc được; khi áp dụng yêu cầu khóa giọng mới, bổ sung mẫu và review trước khi công bố đạt.
8. Nhánh YouTube dài giữ khoảng giải thích cần thiết và cùng giọng xuyên chương.

Nếu thay đổi hành vi helper, viết kiểm tra hành vi cho mapping/version/invalidation trước khi sửa theo CONTRIBUTING. Không tạo test chỉ so khớp câu chữ trong skill. Đo hiệu quả người xem bằng retention, thời gian xem, tỷ lệ xem hết và phản hồi nếu được cung cấp; chưa có dữ liệu thì không kết luận bản nhanh hơn sẽ hiệu quả hơn.

## Evidence của lần lập kế hoạch

Expected: kế hoạch bao phủ tám skill, rule giọng có cách xác minh, nhịp short có cơ sở và giới hạn Flow được nêu rõ.

Actual: đã đọc tám skill, contracts, Flow runbook và assembly; đối chiếu timeline Tiny 40 giây và ghi chú audio chưa nghe duyệt; tra nguồn chính thức qua Tavily và mở trực tiếp các tài liệu được dẫn. Chỉ tạo tài liệu kế hoạch này. Chưa triển khai skill, nghe duyệt giọng, chạy pilot, sửa video, chạy unit test hoặc push.
