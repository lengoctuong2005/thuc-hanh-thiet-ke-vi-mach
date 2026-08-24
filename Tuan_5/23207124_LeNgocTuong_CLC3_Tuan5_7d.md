# BÁO CÁO THỰC HÀNH TUẦN 5: TỔNG HỢP MẠCH VÀ XÁC MINH THIẾT KẾ (MỨC 7 ĐIỂM)

* **Môn học:** Thực hành Thiết kế vi mạch điện tử
* **Họ và tên sinh viên:** Lê Ngọc Tường
* **Mã số sinh viên:** 23207124
* **Lớp:** CLC3

---

## PHẦN 1: TỔNG HỢP MẠCH CỔNG AND

### 1.1 Khởi tạo và thiết lập thư viện công nghệ
Sử dụng công cụ Synopsys Design Compiler (DC) ở chế độ giao diện đồ họa (Design Vision) để tổng hợp mạch cổng AND với thư viện công nghệ SAED32nm.

* Khởi động công cụ Design Vision:
  ```bash
  design_vision &
  ```
* Thiết lập thư viện công nghệ trong file cấu hình `.synopsys_dc.setup`:
  ```tcl
  set target_library "saed32rvt_tt1p0sv25c.db"
  set link_library "* saed32rvt_tt1p0sv25c.db dw_foundation.sldb"
  ```

### 1.2 Đọc file thiết kế và phân tích kết quả tổng hợp
* Đọc mã nguồn RTL của cổng AND (`and_gate.v`):
  ```tcl
  analyze -format verilog and_gate.v
  elaborate and_gate
  ```
* Liên kết thiết kế và kiểm tra ràng buộc:
  ```tcl
  link
  check_design
  ```
* Tiến hành tổng hợp mạch logic mức cổng (Gate-level):
  ```tcl
  compile_ultra
  ```

#### Kết quả Sơ đồ mạch Schematic:
Sơ đồ mạch logic sau khi tổng hợp được ánh xạ sang các tế bào cổng chuẩn trong thư viện công nghệ SAED32nm:

![Sơ đồ nguyên lý cổng AND sau tổng hợp](images/5.png)
*Hình 1.1: Sơ đồ mạch cổng AND.*

#### Phân tích Báo cáo Diện tích:
* **Combinational Area:** $2.033152\ \mu\text{m}^2$
* **Noncombinational Area:** $0.000000\ \mu\text{m}^2$ (không có flip-flop).
* **Total Cell Area:** $2.033152\ \mu\text{m}^2$

![Báo cáo diện tích cổng AND](images/9.png)
*Hình 1.2: Báo cáo diện tích cổng AND.*

#### Phân tích Báo cáo QoR:
Báo cáo Quality of Results (QoR) chỉ ra thời gian trễ đường truyền cực kỳ nhỏ và không xuất hiện vi phạm timing:

![Báo cáo QoR cổng AND](images/8.png)
*Hình 1.3: Báo cáo QoR của cổng AND.*

### 1.3 Xác minh hình thức bằng Formality
Tiến hành so sánh thiết kế RTL (`and_gate.v` - Reference) với Netlist sau tổng hợp (`and_gate_mapped.v` - Implementation) để xác minh tính tương đương chức năng:

* Kết quả đối sánh điểm chốt (Compare Points):

![Formality cổng AND](images/11.png)
*Hình 1.4: So khớp các điểm logic.*

* Kết quả xác minh hoàn tất thành công:

![Xác minh Formality thành công cho cổng AND](images/17.png)
*Hình 1.5: Formality báo cáo xác minh thành công.*

---

## PHẦN 2: TỔNG HỢP VÀ ĐÁNH GIÁ MẠCH BỘ ĐẾM 8-BIT

### 2.1 Các bước Setup tổng hợp
Thiết kế chính của bài thực hành là Bộ đếm 8-bit (`counter`). Các bước tổng hợp tương tự như phần trên nhưng áp dụng thêm các ràng buộc về chu kỳ xung clock ($T_{clk} = 250\ \text{ns}$):

```tcl
create_clock -name clk -period 250 [get_ports clk]
set_input_delay -max 75 -clock clk [remove_from_collection [all_inputs] [get_ports clk]]
set_output_delay -max 75 -clock clk [all_outputs]
```

Sau khi đọc thiết kế, tiến hành phân tích sơ đồ Schematic:

![Sơ đồ mạch Schematic bộ đếm 8-bit sau tổng hợp](images/mach.png)
*Hình 2.1: Sơ đồ mạch bộ đếm 8-bit.*

### 2.2 Đánh giá kết quả tổng hợp ban đầu và phát hiện lỗi timing

#### Kết quả diện tích ban đầu:
* **Combinational Area:** $35.3263\ \mu\text{m}^2$
* **Noncombinational Area:** $56.9283\ \mu\text{m}^2$
* **Total Cell Area:** $92.2546\ \mu\text{m}^2$

![Báo cáo diện tích ban đầu của counter](images/2a.15.png)
*Hình 2.2: Diện tích bộ đếm ban đầu.*

#### Phát hiện lỗi vi phạm Hold Time:
Báo cáo timing chỉ ra lỗi vi phạm thời gian giữ (Hold Time) ở flip-flop đầu tiên `state_reg[0]`. Lượng trễ thực tế chỉ đạt $0.09\ \text{ns}$ so với yêu cầu tối thiểu của thư viện là $0.10\ \text{ns}$.

![Lỗi vi phạm Hold Time](images/2a.23.2.png)
*Hình 2.3: Báo cáo vi phạm thời gian giữ Hold Time.*

### 2.3 Khắc phục lỗi Hold Time và tối ưu hóa thiết kế
Để khắc phục lỗi Hold Time, ta sử dụng lệnh tự động sửa lỗi giữ trong Design Compiler và chạy biên dịch tối ưu hóa gia tăng (incremental):

```tcl
set_fix_hold [all_clocks]
compile_ultra -incremental
```

![Lệnh set_fix_hold và chạy incremental compile](images/2a.37.png)
*Hình 2.4: Chạy biên dịch incremental để sửa lỗi.*

#### Kết quả sau sửa lỗi:
* Lỗi Hold Time được loại bỏ hoàn toàn (Slack bằng $0.00\ \text{ns}$).
* Tổng diện tích tăng nhẹ từ $92.25\ \mu\text{m}^2$ lên $95.30\ \mu\text{m}^2$ do công cụ chèn thêm tế bào đệm (Buffer) nhằm tăng thời gian trễ đường truyền.

![Báo cáo QoR sau sửa lỗi](images/2a.41.png)
*Hình 2.5: Báo cáo QoR sau khi tối ưu hóa.*

### 2.4 Báo cáo diện tích phân chia chi tiết và xuất dữ liệu
Các báo cáo diện tích và QoR chi tiết được ghi nhận:

![Báo cáo diện tích tổng hợp của counter](images/counter12.png)
*Hình 2.6: Phân chia chi tiết diện tích Cell.*

Sau khi thiết kế đạt chuẩn, ta xuất netlist mức cổng và file ràng buộc SDC để làm đầu vào cho các bước tiếp theo:
```tcl
write_file -format verilog -hierarchy -output ./output/design_mapped.v
write_sdc -nosplit ../cons/icc2.sdc
```

---

## PHẦN 3: XÁC MINH HÌNH THỨC TRÊN TOOL FORMALITY

Tiến hành xác minh tương đương chức năng cho bộ đếm 8-bit giữa file thiết kế RTL (`counter.v`) và netlist mức cổng sau tối ưu hóa (`design_mapped.v`):

* Thực hiện so khớp điểm chốt logic:

![Kết quả Match chi tiết](images/2b_matched.png)
*Hình 3.1: Các điểm so khớp trong Formality.*

* Kết quả xác minh thành công (Verification Succeeded):

![Xác minh Formality thành công cho counter](images/2b_verifysuccess.png)
*Hình 3.2: Xác minh tương đương bộ đếm thành công.*

---

## PHẦN 4: MÔ PHỎNG SAU TỔNG HỢP VỚI VCS

Sử dụng VCS để mô phỏng kiểm tra chức năng động của bộ đếm 8-bit mức netlist sau tổng hợp:

### 4.1 Biên dịch mô phỏng
Lệnh biên dịch sử dụng thư viện mô phỏng công nghệ `saed32nm.v`:
```bash
vcs -gui -debug_all counter_tb.v design_mapped.v saed32nm.v
```

### 4.2 Giản đồ dạng sóng mô phỏng
Giản đồ dạng sóng thu được từ giao diện DVE của VCS thể hiện chính xác chu kỳ đếm nhị phân của bộ đếm 8-bit:

![Giản đồ dạng sóng mô phỏng bộ đếm 8-bit](images/2b-cqau1.png)
*Hình 4.1: Dạng sóng mô phỏng của bộ đếm 8-bit.*

![Kết quả in trạng thái trên terminal](images/2b-cau1.1.png)
*Hình 4.2: Terminal hiển thị kết quả giá trị đếm.*
