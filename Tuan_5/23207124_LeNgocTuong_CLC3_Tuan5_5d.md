# BÁO CÁO THỰC HÀNH TUẦN 5: TỔNG HỢP MẠCH VÀ XÁC MINH THIẾT KẾ (MỨC 5 ĐIỂM)

* **Môn học:** Thực hành Thiết kế vi mạch điện tử
* **Họ và tên sinh viên:** Lê Ngọc Tường
* **Mã số sinh viên:** 23207124
* **Lớp:** CLC3

---

## PHẦN 1: TỔNG HỢP MẠCH CỔNG AND

Tổng hợp thiết kế cổng AND đơn giản bằng Design Compiler:

* Sơ đồ Schematic sau tổng hợp:

![Sơ đồ nguyên lý cổng AND sau tổng hợp](images/5.png)
*Hình 1.1: Sơ đồ Schematic cổng AND.*

* Kết quả diện tích cổng AND:
  * **Total Cell Area:** $2.033152\ \mu\text{m}^2$

* Xác minh cổng AND bằng Formality thành công:

![Xác minh Formality thành công cho cổng AND](images/17.png)
*Hình 1.2: Kết quả xác minh cổng AND.*

---

## PHẦN 2: TỔNG HỢP MẠCH BỘ ĐẾM 8-BIT

Tổng hợp mạch bộ đếm 8-bit và tối ưu hóa timing.

* Sơ đồ Schematic bộ đếm:

![Sơ đồ mạch Schematic bộ đếm 8-bit sau tổng hợp](images/mach.png)
*Hình 2.1: Sơ đồ Schematic bộ đếm 8-bit.*

* Báo cáo phát hiện lỗi Hold Time:
  * Lỗi Slack âm xảy ra tại chân `state_reg[0]/D`.

![Lỗi vi phạm Hold Time](images/2a.23.2.png)
*Hình 2.2: Báo cáo timing lỗi Hold.*

* Khắc phục lỗi:
  * Chạy lệnh `set_fix_hold` và chạy `compile_ultra -incremental` để tự động sửa lỗi giữ. Kết quả diện tích tăng lên $95.30\ \mu\text{m}^2$.

---

## PHẦN 3: XÁC MINH BẰNG FORMALITY

Đối sánh thiết kế RTL và Netlist sau tổng hợp của bộ đếm 8-bit bằng Formality:

![Xác minh Formality thành công cho counter](images/2b_verifysuccess.png)
*Hình 3.1: Formality báo cáo tương đương chức năng.*

---

## PHẦN 4: MÔ PHỎNG VỚI VCS

Mô phỏng kiểm tra hoạt động chức năng động của bộ đếm sau tổng hợp:

![Giản đồ dạng sóng mô phỏng bộ đếm 8-bit](images/2b-cqau1.png)
*Hình 4.1: Giản đồ dạng sóng xung đếm.*
