# TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TP.HCM
## KHOA ĐIỆN TỬ VIỄN THÔNG
### BỘ MÔN ĐIỆN TỬ - VIỄN THÔNG

---

# BÁO CÁO THỰC HÀNH THIẾT KẾ VI MẠCH ĐIỆN TỬ
## BÁO CÁO TUẦN 3: THIẾT KẾ LAYOUT VÀ KIỂM TRA DRC, LVS, STARRC CHO CÁC CỔNG INVERTER, NAND, NOR

* **Họ và tên Sinh viên:** Lê Ngọc Tường
* **Mã số Sinh viên:** 23207124
* **Lớp học:** 23DTV_CLC3 (Ca 2)
* **Môn học:** Thực hành thiết kế vi mạch điện tử
* **Giáo viên hướng dẫn:** TS. Nguyễn Duy Thảo
* **Công nghệ thiết kế:** Synopsys Custom Compiler & SAED 90nm PDK (Vdd = 1.2V)

---

## Báo cáo

### 1. Thiết kế layout và kiểm tra DRC, LVS cho mạch Inverter.

#### a) Thiết kế Layout và kiểm tra luật thiết kế DRC
Mạch Inverter được thiết kế layout vật lý dựa trên sơ đồ nguyên lý schematic. Transistor PMOS được đặt trong vùng giếng N (Nwell) có kích thước thiết kế $W = 0.5\,\mu	ext{m}, L = 0.1\,\mu	ext{m}$. Transistor NMOS được đặt trong đế P (P-substrate) với $W = 0.25\,\mu	ext{m}, L = 0.1\,\mu	ext{m}$.
Sau khi vẽ layout, tiến hành chạy kiểm tra DRC. Kết quả DRC báo 0 errors, chứng tỏ không có vi phạm luật công nghệ.

| Layout cổng Inverter | Kiểm tra DRC (0 errors) |
| :---: | :---: |
| ![Layout Inverter](images/layout_inv.png) | ![DRC Inverter](images/drc_inv.png) |

#### b) Kiểm tra LVS và trích xuất ký sinh StarRC
Tiến hành chạy LVS (Layout Versus Schematic), kết quả hiển thị "Matched", nghĩa là layout đã vẽ khớp hoàn toàn với sơ đồ nguyên lý schematic gốc. Cuối cùng, thực hiện trích xuất thông số ký sinh (StarRC) thành công để thu được netlist post-layout chứa các tham số tụ ký sinh.

| Kết quả LVS (Matched) | Kết quả StarRC Inverter |
| :---: | :---: |
| ![LVS Inverter](images/lvs_inv.png) | ![StarRC Inverter](images/starrc_inv.png) |


### 2. Thiết kế layout và kiểm tra DRC, LVS cho mạch Nand.

#### a) Thiết kế Layout và kiểm tra DRC
Mạch NAND 2 ngõ vào được vẽ layout với 2 transistor PMOS mắc song song và 2 transistor NMOS mắc nối tiếp. Để tối ưu diện tích, kỹ thuật dùng chung vùng khuếch tán (share diffusion) được áp dụng. Kết quả kiểm tra DRC cho mạch báo lỗi bằng 0.

| Layout cổng NAND | Kiểm tra DRC NAND |
| :---: | :---: |
| ![Layout NAND](images/layout_nand.png) | ![DRC NAND](images/drc_nand.png) |

#### b) Trích xuất ký sinh StarRC
Bước trích xuất ký sinh StarRC cho cổng NAND cũng hoàn thành tốt đẹp, thu được netlist chứa đầy đủ các tụ ký sinh.

| Kết quả StarRC NAND |
| :---: |
| ![StarRC NAND](images/starrc_nand.png) |


### 3. Thiết kế layout và kiểm tra DRC, LVS cho mạch Nor.

#### a) Thiết kế Layout và trích xuất StarRC
Mạch NOR 2 ngõ vào có 2 PMOS mắc nối tiếp và 2 NMOS mắc song song. Việc đi dây (routing) VDD và VSS được tối ưu để khoảng cách ngắn nhất mà không gây vi phạm DRC.
Tiến hành trích xuất StarRC thành công, thu được thông số ký sinh chuẩn.

| Layout cổng NOR | Kết quả StarRC NOR |
| :---: | :---: |
| ![Layout NOR](images/layout_nor.png) | ![StarRC NOR](images/starrc_nor.png) |


### 4. Thiết kế nguyên lý và mô phỏng bổ sung các cổng OR, XOR, XNOR (Điểm cộng)

Bên cạnh các yêu cầu cơ bản, em đã thiết kế bổ sung sơ đồ nguyên lý và tiến hành chạy mô phỏng kiểm chứng logic cho các cổng logic OR, XOR và XNOR trên Synopsys Custom Compiler:

#### a) Cổng OR 2 ngõ vào
Thực hiện thiết kế nguyên lý ghép cổng NOR với cổng đảo Inverter.

| Sơ đồ nguyên lý cổng OR | Dạng sóng mô phỏng Transient |
| :---: | :---: |
| ![OR Schematic](images/OR_sche.png) | ![OR Waveform](images/OR_waveform.png) |

#### b) Cổng XOR 2 ngõ vào
Thực hiện thiết kế nguyên lý cổng XOR sử dụng các cặp transistor truyền dẫn bổ sung.

| Sơ đồ nguyên lý cổng XOR | Dạng sóng mô phỏng Transient |
| :---: | :---: |
| ![XOR Schematic](images/XOR_sche.png) | ![XOR Waveform](images/XOR_sim_fn.png) |

#### c) Cổng XNOR 2 ngõ vào
Thực hiện thiết kế nguyên lý cổng XNOR bằng cách đảo ngõ ra của cổng XOR.

| Sơ đồ nguyên lý cổng XNOR | Dạng sóng mô phỏng Transient |
| :---: | :---: |
| ![XNOR Schematic](images/XNOR_sche.png) | ![XNOR Waveform](images/XNOR_wave.png) |
