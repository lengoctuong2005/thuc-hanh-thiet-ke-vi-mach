# Minh chứng Thực hành Thiết kế Vi mạch

Sinh viên: Lê Ngọc Tường  
MSSV: 23207124  
Lớp: 23DTV_CLC3 (Ca 2)  
Môn học: Thực hành Thiết kế Vi mạch  

Thư mục này lưu trữ tài liệu, hình ảnh chụp màn hình phần mềm EDA, mã nguồn script và cơ sở dữ liệu nhật ký cho các bài thực hành từ tuần 2 đến tuần 5.

## Cấu trúc thư mục

| Thư mục | Nội dung | Tài liệu chính |
| :--- | :--- | :--- |
| [Database_Logs/](./Database_Logs/) | Cơ sở dữ liệu SQLite và metadata ghi nhận quá trình làm bài | antigravity.db, compliance.db, failure_memory.db, file yaml |
| [Tuan_2/](./Tuan_2/) | Khởi tạo PDK 90nm, mô phỏng và layout cổng Inverter, NAND, NOR, AND | Báo cáo .md, .pdf, 36 ảnh chụp trong Images_Goc |
| [Tuan_3/](./Tuan_3/) | Vẽ schematic và mô phỏng mạch logic (XOR, XNOR, OR, INV) | Báo cáo .md, .pdf, ảnh schematic và waveform trong Images_Goc |
| [Tuan_4/](./Tuan_4/) | Vẽ layout vật lý, kiểm tra DRC và LVS | Báo cáo .md, .pdf, ảnh kết quả DRC/LVS trong Images_Goc |
| [Tuan_5/](./Tuan_5/) | Bóc tách ký sinh RLC, mô phỏng sau layout (Post-layout) | Script Python gen_pdf.py, báo cáo .md, .pdf, ảnh trích xuất trong Images_Goc |

## Mô tả dữ liệu lưu trữ
- Báo cáo chi tiết từng tuần được lưu dưới dạng file Markdown (.md) và PDF (.pdf) trong thư mục của tuần tương ứng.
- Toàn bộ hình ảnh chụp màn hình trong quá trình làm bài được đặt tại thư mục Images_Goc của mỗi tuần.
- Nhật ký thao tác hệ thống và cơ sở dữ liệu theo dõi tiến trình được lưu tại thư mục Database_Logs.
