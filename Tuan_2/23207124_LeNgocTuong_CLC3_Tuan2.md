# TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TP.HCM
## KHOA ĐIỆN TỬ VIỄN THÔNG
### BỘ MÔN ĐIỆN TỬ - VIỄN THÔNG

---

# BÁO CÁO THỰC HÀNH THIẾT KẾ VI MẠCH ĐIỆN TỬ
## BÁO CÁO TUẦN 2: THIẾT KẾ VÀ MÔ PHỎNG MẠCH MỨC SCHEMATIC - INVERTER, NAND, AND, NOR

* **Họ và tên Sinh viên:** Lê Ngọc Tường
* **Mã số Sinh viên:** 23207124
* **Lớp học:** 23DTV_CLC3 (Ca 2)
* **Môn học:** Thực hành thiết kế vi mạch điện tử
* **Giáo viên hướng dẫn:** TS. Nguyễn Duy Thảo
* **Công nghệ thiết kế:** Synopsys Custom Compiler & SAED 90nm PDK (Vdd = 1.2V)

---

## Báo cáo

### 1. Thiết kế nguyên lý và mô phỏng cổng đảo Inverter

#### a) Sơ đồ nguyên lý và ký hiệu đóng gói
Mạch Inverter được thiết kế sử dụng cặp transistor bù PMOS và NMOS. Đối với PMOS, độ rộng kênh W được thiết lập bằng $0.24\,\mu\text{m}$ và chiều dài kênh L là $0.1\,\mu\text{m}$ nhằm tuân thủ quy định tối thiểu của công nghệ 90nm. Đối với NMOS, độ rộng kênh W là $0.12\,\mu\text{m}$ và chiều dài L là $0.1\,\mu\text{m}$. PMOS được thiết kế với độ rộng kênh gấp đôi NMOS nhằm cân bằng dòng điện dẫn giữa hai khối kéo lên và kéo xuống, bù đắp cho việc độ di động của lỗ trống trong PMOS thấp hơn của electron trong NMOS.

| Sơ đồ nguyên lý | Ký hiệu đóng gói |
| :---: | :---: |
| ![Sơ đồ nguyên lý Inverter](images/interver%20(8).png) | ![Ký hiệu đóng gói Inverter](images/interver%20(9).png) |

#### b) Sơ đồ mô phỏng kiểm tra
Sơ đồ mô phỏng Inverter_TB sử dụng nguồn cấp một chiều $V_{DC} = 1.2\text{V}$ cấp cho chân VDD và nguồn xung vpulse cấp cho ngõ vào VIN. Nguồn xung có chu kỳ $20\,\text{ns}$, độ rộng xung $10\,\text{ns}$, thời gian sườn lên và sườn xuống đều bằng $0.1\,\text{ns}$. Ngõ ra VOUT nối với một tụ tải dung ký sinh $C_L = 10\,\text{fF}$ để mô phỏng điều kiện tải thực tế.

![Sơ đồ mô phỏng Inverter](images/interver%20(7).png)

#### c) Kết quả mô phỏng transient kiểm chứng logic
Dạng sóng ngõ ra VOUT thể hiện hoạt động logic đảo pha hoàn toàn so với ngõ vào VIN. Khi điện áp ngõ vào ở mức cao 1.2V, transistor NMOS dẫn kéo ngõ ra về mức đất 0V. Khi ngõ vào ở mức thấp 0V, transistor PMOS dẫn kéo ngõ ra lên mức nguồn 1.2V.

| Dạng sóng đáp ứng ngõ ra | Chi tiết dạng sóng |
| :---: | :---: |
| ![Transient ngõ ra Inverter](images/interver%20(4).png) | ![Chi tiết Transient Inverter](images/interver%20(10).png) |

#### d) Đặc tuyến truyền đạt tĩnh
Đặc tuyến truyền tĩnh thể hiện ngưỡng chuyển mạch của cổng đảo. Khi thực hiện quét điện áp ngõ vào từ 0V đến 1.2V, điểm chuyển trạng thái nằm gần trung điểm $0.6\text{V}$ nhờ tỉ lệ định cỡ độ rộng kênh PMOS/NMOS bằng 2. Đặc tuyến có độ dốc lớn tại vùng chuyển trạng thái thể hiện hệ số khuếch đại cao, giúp mạch có khả năng chống nhiễu tốt.

![Đặc tuyến truyền đạt tĩnh Inverter](images/interver%20(1).png)

#### e) Các thông số thời gian trễ và sườn xung
Thời gian trễ truyền lan được đo bằng chênh lệch thời gian giữa ngõ vào và ngõ ra tại mốc điện áp 0.6V. Giá trị trễ cạnh xuống $t_{pHL}$ được xác định tại sườn lên của ngõ vào, và trễ cạnh lên $t_{pLH}$ tại sườn xuống của ngõ vào. Thời gian sườn lên $t_r$ và sườn xuống $t_f$ được tính trong khoảng biên độ từ 10% đến 90%, tương đương điện áp từ 0.12V đến 1.08V.

| Đo đạc thời gian trễ | Đo đạc thời gian sườn xung |
| :---: | :---: |
| ![Đo thời gian trễ Inverter](images/interver%20(11).png) | ![Đo thời gian sườn Inverter](images/interver%20(12).png) |

### 2. Thiết kế nguyên lý và mô phỏng cổng NAND

#### a) Sơ đồ nguyên lý và ký hiệu đóng gói
Cổng NAND hai ngõ vào gồm khối kéo lên cấu thành từ hai transistor PMOS mắc song song nối với nguồn $V_{DD}$, và khối kéo xuống gồm hai transistor NMOS mắc nối tiếp nối với đất $V_{SS}$. Mạch hoạt động theo nguyên lý chỉ cần một ngõ vào ở mức thấp thì ít nhất một PMOS dẫn để kéo ngõ ra lên cao. Để ngõ ra về mức thấp, cả hai NMOS phải đồng thời dẫn khi cả hai ngõ vào đều ở mức cao.

| Sơ đồ nguyên lý | Ký hiệu đóng gói |
| :---: | :---: |
| ![Sơ đồ nguyên lý NAND](images/nand%20(3).png) | ![Ký hiệu đóng gói NAND](images/nand%20(4).png) |

#### b) Sơ đồ mô phỏng kiểm tra
Để kiểm tra hoạt động của mạch NAND, sơ đồ mô phỏng NAND_TB sử dụng hai nguồn xung vpulse cho hai đầu vào A và B. Các chu kỳ nguồn xung được thiết lập lệch pha nhau, cụ thể chu kỳ tín hiệu A là $20\,\text{ns}$ và tín hiệu B là $10\,\text{ns}$. Thiết lập này giúp tạo ra đầy đủ bốn tổ hợp ngõ vào phân biệt nhằm quét hết các trạng thái logic.

![Sơ đồ mô phỏng NAND](images/nand%20(2).png)

#### c) Kết quả mô phỏng transient kiểm chứng logic
Dạng sóng ngõ ra VOUT đáp ứng đúng theo bảng chân trị logic NAND. Khi các tổ hợp ngõ vào là 00, 01 hoặc 10, ít nhất một PMOS dẫn nên ngõ ra được giữ ở mức cao 1.2V. Chỉ khi ngõ vào đạt tổ hợp 11 thì cả hai NMOS mới dẫn, kéo điện áp ngõ ra về mức thấp 0V.

| Dạng sóng logic | Chi tiết phân trạng thái |
| :---: | :---: |
| ![Dạng sóng logic NAND](images/nand%20(1).png) | ![Chi tiết sườn sóng NAND](images/nand%20(9).png) |

#### d) Các thông số thời gian trễ và sườn xung
Thời gian trễ và sườn xung được đo đạc trực tiếp bằng các thước đo trong công cụ hiển thị dạng sóng. Cấu trúc nối tiếp của NMOS và song song của PMOS làm xuất hiện sự lệch nhẹ về thời gian đáp ứng so với cổng đảo. Khi chuyển trạng thái từ cao xuống thấp, dòng điện đi qua hai transistor NMOS nối tiếp khiến điện trở kênh dẫn tăng gấp đôi, làm thời gian trễ kéo xuống lớn hơn.

| Đo đạc thời gian trễ | Đo đạc thời gian sườn xung |
| :---: | :---: |
| ![Đo thời gian trễ NAND](images/nand%20(10).png) | ![Đo thời gian sườn NAND](images/nand%20(11).png) |

### 3. Thiết kế nguyên lý và mô phỏng cổng AND

#### a) Sơ đồ nguyên lý và ký hiệu đóng gói
Trong công nghệ CMOS tĩnh, cổng AND được thiết kế bằng cách ghép nối tiếp một cổng đảo Inverter phía sau cổng NAND hai ngõ vào do cấu trúc CMOS cơ bản luôn có đặc tính đảo pha. Cổng NAND thực hiện chức năng đảo trước khi Inverter đảo ngược kết quả để tạo ra hàm logic AND mong muốn.

| Sơ đồ nguyên lý | Ký hiệu đóng gói |
| :---: | :---: |
| ![Sơ đồ nguyên lý AND](images/and%20(2).png) | ![Ký hiệu đóng gói AND](images/and%20(3).png) |

#### b) Sơ đồ mô phỏng kiểm tra
Sơ đồ mô phỏng cổng AND sử dụng cấu hình nguồn xung lệch pha tương tự như cổng NAND nhằm kiểm chứng hoạt động trên toàn bộ các tổ hợp ngõ vào.

![Sơ đồ mô phỏng AND](images/and%20(1).png)

#### c) Kết quả mô phỏng transient kiểm chứng logic
Dạng sóng mô phỏng transient xác nhận hoạt động của cổng AND. Ngõ ra chỉ lên mức cao 1.2V khi cả hai ngõ vào A và B đều ở mức cao 1.2V. Đối với tất cả các trường hợp ngõ vào còn lại, điện áp ngõ ra luôn giữ ở mức thấp 0V.

| Dạng sóng logic | Chi tiết đo đạc |
| :---: | :---: |
| ![Dạng sóng logic AND](images/and%20(4).png) | ![Đo chi tiết cổng AND](images/and%20(9).png) |

#### d) Các thông số thời gian trễ và sườn xung
Vì cổng AND gồm hai tầng logic ghép nối tiếp, tín hiệu ngõ ra phải chịu thêm thời gian trễ của bộ đảo Inverter phía sau cổng NAND. Do đó, tổng thời gian trễ truyền lan của cổng AND lớn hơn cổng NAND đơn lẻ.

| Đo đạc thời gian trễ | Đo đạc thời gian sườn xung |
| :---: | :---: |
| ![Đo thời gian trễ AND](images/and%20(5).png) | ![Đo thời gian sườn AND](images/and%20(6).png) |

### 4. Thiết kế nguyên lý và mô phỏng cổng NOR

#### a) Sơ đồ nguyên lý và ký hiệu đóng gói
Cổng NOR hai ngõ vào gồm khối kéo lên làm từ hai transistor PMOS mắc nối tiếp nối từ nguồn $V_{DD}$ xuống ngõ ra, và khối kéo xuống gồm hai transistor NMOS mắc song song nối từ ngõ ra xuống đất $V_{SS}$. Việc nối tiếp hai PMOS làm tăng điện trở sạc cho tụ tải, làm tăng thời gian trễ sườn lên. Ngược lại, khi có bất kỳ ngõ vào nào ở mức cao, transistor NMOS tương ứng sẽ dẫn và xả nhanh điện áp ngõ ra về đất.

| Sơ đồ nguyên lý | Ký hiệu đóng gói |
| :---: | :---: |
| ![Sơ đồ nguyên lý NOR](images/nor%20(6).png) | ![Ký hiệu đóng gói NOR](images/nor%20(5).png) |

#### b) Sơ đồ mô phỏng kiểm tra
Sơ đồ mô phỏng cổng NOR sử dụng hai nguồn xung độc lập kích vào hai đầu vào để quét qua toàn bộ tổ hợp trạng thái ngõ vào.

![Sơ đồ mô phỏng NOR](images/nor%20(4).png)

#### c) Kết quả mô phỏng transient và đo đạc thông số
Kết quả mô phỏng transient xác định hoạt động logic của cổng NOR. Khi cả hai ngõ vào cùng ở mức thấp, hai PMOS nối tiếp dẫn để sạc ngõ ra lên mức cao 1.2V. Ở các tổ hợp ngõ vào còn lại, tối thiểu một NMOS dẫn giúp xả điện áp ngõ ra về mức thấp 0V. Các thông số trễ truyền lan và sườn xung được đo trực tiếp tại các thời điểm chuyển mạch tương ứng.

| Dạng sóng Transient kiểm chứng | Đo đạc thông số động học |
| :---: | :---: |
| ![Transient cổng NOR](images/nor%20(2).png) | ![Đo thông số cổng NOR](images/nor%20(3).png) |
