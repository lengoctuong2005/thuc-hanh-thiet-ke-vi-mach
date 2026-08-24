# Cơ sở dữ liệu và Nhật ký hệ thống

Thư mục này chứa các file cơ sở dữ liệu SQLite và metadata được hệ thống ghi nhận trong quá trình thực hiện các bài lab từ tuần 2 đến tuần 5.

## 1. Cơ sở dữ liệu SQLite (sqlite_db/)
- antigravity.db: Lưu trữ thông tin phiên làm việc, lịch sử trích xuất dữ liệu PDK 90nm và quá trình compile báo cáo.
- chroma.sqlite3: Cơ sở dữ liệu vector lưu chỉ mục dữ liệu bài làm.
- compliance.db: Dữ liệu kiểm tra quy chuẩn thiết kế.
- failure_memory.db: Dữ liệu ghi nhận các lỗi DRC, LVS và thao tác sửa lỗi trong quá trình thực hành.

## 2. File Metadata (memory_metadata/)
- causal-graph.yaml: Ràng buộc công nghệ và quan hệ thiết kế.
- experience-engine.yaml: Ghi nhận bài học kinh nghiệm và kết quả thực tế qua từng bài lab.
- failure-database.yaml: Danh sách các lỗi gặp phải trong quá trình mô phỏng.
- session-state.md: Trạng thái tiến độ thực hiện bài làm.
- layer1_user_profile.md đến layer4_lessons_learned.md: Các ghi chép kỹ thuật theo từng lớp thông tin.
