---
name: video-visual-bible
description: "Chuẩn bị bộ tham chiếu nhân vật, sản phẩm, đạo cụ, bối cảnh và phong cách cho project video storyboard/Flow. Dùng khi cần giữ nhận diện xuyên shot hoặc tái sử dụng asset theo series; không phải skill tạo brand kit tổng quát."
---

# Video Visual Bible
Updated: 2026-10-17 11:03 +07

Nhận brief, script, shotlist và ảnh đã có. Đọc [hợp đồng assets](../video-workflow/references/contracts.md#assetsjson), dùng [asset-spec.md](references/asset-spec.md) khi lập bộ nhận diện.

1. Kiểm kê ảnh người dùng cung cấp và tài nguyên project; xem ảnh trước khi đánh giá. Không suy đoán nội dung từ tên file.
2. Định danh character/product/prop/location/style; ghi đặc điểm cố định, biến thể hợp lệ và phạm vi series/episode/scene. Cần ảnh rõ để kiểm soát nhận diện, không cần sinh mọi góc nếu shotlist không dùng.
3. Tái sử dụng asset phù hợp trước khi tạo mới. Với đối tượng cần đúng chi tiết, ưu tiên hình tham chiếu thực; ghi điều chưa thấy rõ thay vì bịa.
4. Nếu cần tạo hoặc chỉnh ảnh, dùng công cụ ảnh khả dụng và tuân theo skill/tool của công cụ đó. Flow image tools hoặc imagegen chỉ được coi là khả dụng khi thật sự có trong môi trường. Đừng viết script xử lý ảnh thay cho công cụ image editing khi công cụ quy định dùng imagegen.
5. Dùng ảnh nhân vật/sản phẩm nền sạch khi thích hợp; ảnh phong cách/bối cảnh không chứa chủ thể dư gây nhầm. Giữ hướng dẫn văn bản tương thích với ảnh.
6. Lưu assets.json và visual-bible.md: asset_id, image_paths, đặc điểm, scope, version và tình trạng kiểm tra. Ghi nguồn hoặc người cung cấp khi biết; không tự suy luận quyền sử dụng.

## Hoàn thành

Xem các ảnh cần dùng trong shotlist, đánh giá nhận diện/phong cách và ghi lỗi cụ thể. Đã có prompt nhưng chưa có ảnh thì trạng thái planned/blocked, không ready. Nếu đổi nhận diện, đánh dấu các frame/clip dùng asset đó cần xem lại. [video-storyboard-frames](../video-storyboard-frames/SKILL.md) sở hữu bố cục từng shot; skill này sở hữu tài nguyên tham chiếu chung.
