# BÁO CÁO THỰC HÀNH TUẦN 5: TỔNG HỢP MẠCH VÀ XÁC MINH THIẾT KẾ

* **Môn học:** Thực hành Thiết kế vi mạch điện tử
* **Họ và tên sinh viên:** Lê Ngọc Tường
* **Mã số sinh viên:** 23207124
* **Lớp:** CLC3
* **Bài báo cáo:** Tổng hợp logic, xác minh hình thức và mô phỏng sau tổng hợp cho các mạch cổng logic và bộ đếm 8-bit (Counter).

---

## PHẦN 1: BÀI TẬP KHỞI ĐỘNG - CỔNG AND

### 1.1 Mục tiêu và các bước Setup trên Design Vision
Bài tập khởi động nhằm giúp sinh viên làm quen với công cụ tổng hợp Synopsys Design Vision và công cụ xác minh Synopsys Formality thông qua một thiết kế đơn giản là cổng AND 2 ngõ vào.

Quy trình thiết lập được thực hiện thông qua dòng lệnh dc_shell kết hợp giao diện đồ họa:
1. Khởi động GUI: `start_gui`
2. Đặt module đỉnh: `set top_module and_gate`
3. Ghi nhận file biến đổi: `set_svf $top_module.svf`
4. Khai báo thư viện và đọc thiết kế RTL.

Trong lần biên dịch đầu tiên, hệ thống báo lỗi cú pháp do khai báo cổng không đúng chuẩn Verilog:
```
Error: ./and_gate.v:1: Syntax error at or near token 'input'. (VER-294)
```
Sau khi sửa lại file mã nguồn RTL, quá trình phân tích và hiện thực đã thành công.

![Lỗi biên dịch cổng AND ban đầu](images/2.png)
*Hình 1.1: Thông báo lỗi biên dịch ban đầu của cổng AND trong Design Vision.*

![Giao diện Design Vision tải cổng AND](images/4.png)
*Hình 1.2: Cấu trúc cổng AND hiển thị trên giao diện schematic của Design Vision.*

---

### 1.2 Kết quả tổng hợp mạch AND_GATE
Sau khi chạy lệnh `compile_ultra -no_autoungroup`, ta thu được kết quả tổng hợp của cổng AND. 

![Sơ đồ nguyên lý cổng AND sau tổng hợp](images/5.png)
*Hình 1.3: Sơ đồ mạch cổng AND được ánh xạ sang thư viện công nghệ SAED32nm.*

#### Phân tích Báo cáo Diện tích:
* **Combinational Area:** $2.033152\ \mu\text{m}^2$
* **Noncombinational Area:** $0.000000\ \mu\text{m}^2$ do cổng AND là mạch tổ hợp và không chứa Flip-Flop.
* **Total Cell Area:** $2.033152\ \mu\text{m}^2$

![Báo cáo diện tích cổng AND](images/9.png)
*Hình 1.4: Báo cáo diện tích chi tiết của cổng AND.*

#### Phân tích Báo cáo Timing & QoR:
* **Worst Negative Slack:** $0.00$
* **Cell Count:** 1 Cell duy nhất.

![Báo cáo QoR cổng AND](images/8.png)
*Hình 1.5: Báo cáo QoR cổng AND.*

---

### 1.3 Xác minh thiết kế cổng AND trên Formality
Sử dụng công cụ Synopsys Formality để đối chiếu chức năng giữa file thiết kế RTL và Netlist mức cổng sau tổng hợp.

* Kết quả matching: Ghép nối thành công các điểm so sánh.
* Kết quả verification: **Verification Succeeded**.

![Formality cổng AND](images/11.png)
*Hình 1.6: Kết quả đối chiếu điểm so khớp trên Formality cho cổng AND.*

![Xác minh Formality thành công cho cổng AND](images/17.png)
*Hình 1.7: Giao diện Formality thông báo xác minh cổng AND thành công.*

---

### 1.4 Mô phỏng Testbench cổng AND trên VCS
Thực hiện mô phỏng sau tổng hợp bằng trình mô phỏng Synopsys VCS để kiểm tra hoạt động chức năng tổ hợp của cổng AND.

#### Mã nguồn Testbench cổng AND (`and_gate_tb.v`):
```verilog
`timescale 1ns/1ns
module and_gate_tb;
  reg a;
  reg b;
  wire y;

  and_gate uut (
    .a(a),
    .b(b),
    .y(y)
  );

  initial begin
    $monitor("At time %t: a = %b, b = %b => y = %b", $time, a, b, y);
    a = 0; b = 0; #10;
    a = 0; b = 1; #10;
    a = 1; b = 0; #10;
    a = 1; b = 1; #10;
    $finish;
  end
endmodule
```

#### Câu lệnh thực thi biên dịch trên VCS:
```bash
# Biên dịch testbench cùng netlist sau tổng hợp và thư viện saed32nm.v
vcs -debug_all and_gate_tb.v design_mapped.v saed32nm.v
# Chạy mô phỏng để xuất kết quả dạng văn bản hoặc mở giao diện GUI
./simv -gui
```

#### Kết quả mô phỏng thu được trên Terminal:
```text
At time 0: a = 0, b = 0 => y = 0
At time 10: a = 0, b = 1 => y = 0
At time 20: a = 1, b = 0 => y = 0
At time 30: a = 1, b = 1 => y = 1
```
Kết quả trên chứng minh chức năng hoạt động của mạch sau tổng hợp hoàn toàn chính xác theo đúng bảng chân trị của cổng AND.

---

## PHẦN 2: TỔNG HỢP VÀ ĐÁNH GIÁ MẠCH BỘ ĐẾM 8-BIT (COUNTER 8-BIT)

Mạch thiết kế chính là Bộ đếm 8-bit (ở mức thiết kế RTL được đặt tên module là `counter` tương ứng với Bài 2 trong bài thực hành Tuần 4). Mạch thực hiện chức năng tăng giá trị đếm sau mỗi chu kỳ xung nhịp. Thiết kế được tổng hợp bằng Synopsys Design Vision nhằm tối ưu hóa diện tích và timing.

### 2.1 Các bước Setup tổng hợp
Các câu lệnh thiết lập môi trường và chạy tổng hợp được thực hiện tuần tự như sau:
```tcl
set top_module counter
set_svf $top_module.svf
define_design_lib work -path ./work
lappend search_path ../Lib/db ../cons ../RTL
set LIB "saed32rvt_tt1p05v25c.db"
set target_library [list $LIB]
set link_library [list * $LIB]
analyze -format verilog {counter.v}
elaborate -lib work counter
link
check_design
source -echo dc.sdc
compile_ultra -no_autoungroup
```

![Liên kết thư viện cổng counter](images/counter.png)
*Hình 2.1: Quá trình Link thư viện công nghệ SAED32nm cho thiết kế counter.*

![Bắt đầu chạy compile_ultra cho counter](images/counter1.png)
*Hình 2.2: Lệnh compile_ultra bắt đầu ánh xạ thiết kế counter.*

![Sơ đồ mạch Schematic bộ đếm 8-bit sau tổng hợp](images/mach.png)
*Hình 2.3: Sơ đồ mạch Schematic bộ đếm 8-bit sau tổng hợp trên Design Vision.*

---

### 2.2 Phân tích báo cáo diện tích ban đầu và giải pháp khắc phục lỗi Hold Time
Sau lần biên dịch đầu tiên bằng lệnh `compile_ultra`, hệ thống đã xuất ra báo cáo diện tích ban đầu:

![Báo cáo diện tích ban đầu của counter](images/2a.15.png)
*Hình 2.4: Báo cáo diện tích ban đầu của bộ đếm.*

* **Combinational Area:** $35.3263\ \mu\text{m}^2$
* **Noncombinational Area:** $56.9283\ \mu\text{m}^2$
* **Total Cell Area:** $92.2546\ \mu\text{m}^2$

#### Phát hiện vi phạm Hold Time:
Khi chạy báo cáo kiểm tra lỗi ràng buộc và timing, công cụ phát hiện lỗi vi phạm về Hold Time tại ngõ vào D của thanh ghi `state_reg[0]`, thời gian giữ thực tế chỉ đạt $0.09\ \text{ns}$ trong khi yêu cầu tối thiểu của thư viện là $0.10\ \text{ns}$. Lượng vi phạm âm dẫn đến lỗi Slack (Hold).

![Lỗi vi phạm Hold Time](images/2a.23.2.png)
*Hình 2.5: Báo cáo vi phạm Hold Time tại chân state_reg[0]/D.*

![Ràng buộc vi phạm chi tiết](images/2a.36.png)
*Hình 2.6: Lệnh report_constraint chỉ ra điểm vi phạm Hold Time.*

#### Giải pháp khắc phục:
Để sửa lỗi vi phạm thời gian giữ, ta thực hiện cấu hình sửa lỗi tự động để Design Compiler tự động chèn thêm các cell đệm (delay buffers) vào đường dẫn tín hiệu:
1. Kích hoạt tự động sửa thời gian giữ:
   ```tcl
   dc_shell> set_fix_hold [all_clocks]
   ```
2. Thực hiện tối ưu hóa tăng cường:
   ```tcl
   dc_shell> compile_ultra -incremental
   ```

![Lệnh set_fix_hold và chạy incremental compile](images/2a.37.png)
*Hình 2.7: Thực thi các lệnh chèn buffer để sửa lỗi Hold Time.*

---

### 2.3 Báo cáo diện tích và QoR sau khi sửa lỗi Hold Time
Sau khi thực hiện chạy incremental compile, lỗi vi phạm Hold Time đã được khắc phục triệt để.

![Báo cáo QoR sau sửa lỗi](images/2a.41.png)
*Hình 2.8: Báo cáo QoR sau sửa lỗi chỉ ra 0 vi phạm Hold.*

#### So sánh diện tích trước và sau khi sửa lỗi:
* **Trước khi sửa:** Diện tích Cell là $92.2546\ \mu m^2$.
* **Sau khi sửa:** Diện tích Cell tăng lên $95.3040\ \mu m^2$.
* **Nhận xét:** Việc tăng diện tích là do trình tổng hợp tự động chèn thêm các tế bào đệm (buffer) để kéo dài thời gian trễ của tín hiệu, từ đó đáp ứng yêu cầu về thời gian giữ.

![Báo cáo diện tích sau sửa lỗi](images/2a.42.png)
*Hình 2.9: Báo cáo diện tích chi tiết của mạch đếm sau khi chèn buffer.*

---

### 2.4 Báo cáo QoR và diện tích phân chia chi tiết (Dữ liệu tổng hợp)
Dưới đây là các báo cáo QoR và phân tách diện tích tổng thể thu được sau quá trình tối ưu hóa:

![Báo cáo QoR của counter](images/counter11.png)
*Hình 2.10: Báo cáo QoR tổng hợp của mạch Counter 8-bit.*

![Báo cáo diện tích tổng hợp của counter](images/counter12.png)
*Hình 2.11: Phân chia chi tiết diện tích Cell và diện tích thiết kế.*

Sau khi thiết kế đạt chuẩn, các file netlist mapped, ràng buộc và cơ sở dữ liệu được xuất ra thư mục `./output` bằng các lệnh:

```tcl
dc_shell> write_file -format verilog -hierarchy -output ./output/design_mapped.v
dc_shell> write_file -format ddc -hierarchy -output ./output/design_mapped.ddc
dc_shell> write_sdc -nosplit ../cons/icc2.sdc
dc_shell> write_sdf ./output/design_mapped.sdf
```
Các tệp tin đầu ra bao gồm netlist mức cổng (`design_mapped.v`), tệp cơ sở dữ liệu ddc (`design_mapped.ddc`), file ràng buộc SDC (`icc2.sdc`) và file thông tin trễ SDF (`design_mapped.sdf`) phục vụ trực tiếp cho quá trình xác minh tương đương chức năng (Formality) và mô phỏng sau tổng hợp (VCS).

---

## PHẦN 3: XÁC MINH HÌNH THỨC TRÊN TOOL FORMALITY

Thực hiện xác minh tương đương chức năng cho bộ đếm 8-bit nhằm đảm bảo quá trình tổng hợp và chèn buffer sửa lỗi Hold Time không làm sai lệch logic thiết kế.

1. **Thiết kế tham chiếu (Reference):** File mã nguồn RTL `counter.v`.
2. **Thiết kế hiện thực (Implementation):** Netlist mức cổng sau tổng hợp `design_mapped.v`.
3. **Thiết lập hằng số:** Khai báo chân reset cố định để so khớp trạng thái đếm:
   ```tcl
   Formality (setup)> set_constant -type port r:/WORK/counter/clear 0
   ```

Giao diện Formality ghi nhận quá trình so khớp và đối chiếu:

![Thực hiện Match điểm so khớp](images/2b_2.png)
*Hình 3.1: Các điểm so sánh được ánh xạ thành công.*

![Kết quả Match chi tiết](images/2b_matched.png)
*Hình 3.2: Chi tiết các điểm so khớp logic thành công.*

Khi chạy kiểm tra với lệnh **Verify**, Formality thực hiện chứng minh toán học và trả về thông báo tương đương chức năng hoàn toàn giữa thiết kế RTL và Netlist mức cổng sau tổng hợp:
```
Verification SUCCEEDED
```

![Xác minh Formality thành công cho counter](images/2b_verifysuccess.png)
*Hình 3.3: Giao diện Formality thông báo xác minh mạch đếm thành công.*

---

## PHẦN 4: MÔ PHỎNG SAU TỔNG HỢP VỚI VCS

Ta tiến hành mô phỏng động mức cổng sau tổng hợp bằng Synopsys VCS để kiểm tra hoạt động thời gian thực của bộ đếm 8-bit trong điều kiện trễ vật lý.

### 4.1 Thiết lập lệnh biên dịch mô phỏng
```bash
# Biên dịch testbench cùng netlist sau tổng hợp và thư viện verilog công nghệ saed32nm.v
vcs -gui -debug_all \
    counter_tb.v \
    design_mapped.v \
    saed32nm.v
```

### 4.2 Phân tích giản đồ dạng sóng mô phỏng
Giản đồ dạng sóng thu được từ giao diện mô phỏng VCS thể hiện chu kỳ đếm nhị phân chính xác của bộ đếm 8-bit.

![Giản đồ dạng sóng mô phỏng bộ đếm 8-bit](images/2b-cqau1.png)
*Hình 4.1: Dạng sóng mô phỏng trạng thái dịch chuyển đếm của bộ đếm 8-bit.*

![Kết quả in trạng thái trên terminal](images/2b-cau1.1.png)
*Hình 4.2: Terminal in giá trị output thay đổi tuần tự của bộ đếm.*

#### Giải thích hoạt động logic:
* **Trạng thái khởi đầu:** Khi chân `clear` được kích hoạt, ngõ ra `state` lập tức được đưa về `8'b0000_0000` bất đồng bộ.
* **Hoạt động đếm nhị phân:** Khi chân `clear` xuống mức 0, tại mỗi cạnh lên của clock, giá trị của `state` tăng lên 1 đơn vị tuần tự (`state = state + 1`).
* **Nhận xét trễ vật lý:** Sườn thay đổi trạng thái của ngõ ra trễ một khoảng thời gian nhỏ so với sườn dương của xung clock do trễ lan truyền thực tế của tế bào Flip-Flop trong thư viện SAED32nm. Điều này chứng minh mô phỏng mức cổng phản ánh đúng bản chất vật lý của thiết kế phần cứng sau tổng hợp.
