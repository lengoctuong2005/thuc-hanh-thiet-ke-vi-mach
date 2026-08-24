# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from fpdf import FPDF

FONT_DIR = r'C:\Windows\Fonts'
IMG_DIR = r'c:\HK3-25-26\THTKVM\Tuan5\images'

BLUE = (31, 78, 121)
DARK_GRAY = (51, 51, 51)
LIGHT_GRAY = (120, 120, 120)
CODE_BG = (235, 242, 250)

class ReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('ArialN', '', os.path.join(FONT_DIR, 'arial.ttf'))
        self.add_font('ArialN', 'B', os.path.join(FONT_DIR, 'arialbd.ttf'))
        self.add_font('ArialN', 'I', os.path.join(FONT_DIR, 'ariali.ttf'))
        self.add_font('CourierN', '', os.path.join(FONT_DIR, 'cour.ttf'))
        self.add_font('CourierN', 'B', os.path.join(FONT_DIR, 'courbd.ttf'))
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        if self.page_no() > 1:
            self.set_font('ArialN', '', 8)
            self.set_text_color(*BLUE)
            self.cell(0, 5, 'Báo cáo thực hành Tuần 5', align='L')
            self.set_text_color(*DARK_GRAY)
            self.cell(0, 5, '23207124 - Lê Ngọc Tường', align='R', new_x='LMARGIN', new_y='NEXT')
            self.set_draw_color(*BLUE)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('ArialN', '', 8)
        self.set_text_color(*LIGHT_GRAY)
        self.cell(0, 10, str(self.page_no()), align='C')

    def cover_page(self):
        self.add_page()
        self.ln(35)
        self.set_font('ArialN', 'B', 11)
        self.set_text_color(*BLUE)
        self.cell(0, 7, 'TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TP.HCM', align='C', new_x='LMARGIN', new_y='NEXT')
        self.cell(0, 7, 'KHOA ĐIỆN TỬ VIỄN THÔNG', align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(12)
        self.set_font('ArialN', 'B', 20)
        self.set_text_color(*BLUE)
        self.cell(0, 12, 'BÁO CÁO THỰC HÀNH TUẦN 5:', align='C', new_x='LMARGIN', new_y='NEXT')
        self.cell(0, 12, 'TỔNG HỢP MẠCH VÀ XÁC MINH THIẾT KẾ', align='C', new_x='LMARGIN', new_y='NEXT')
        self.cell(0, 12, '(ASIC FLOW)', align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(18)

        info = [
            ('Họ và tên Sinh viên:', 'Lê Ngọc Tường'),
            ('Mã số Sinh viên:', '23207124'),
            ('Lớp học:', 'CLC3'),
            ('Môn học:', 'Thực hành thiết kế vi mạch điện tử'),
        ]
        col_w_label = 45
        col_w_value = 100
        x_start = (210 - col_w_label - col_w_value) / 2

        self.set_draw_color(*DARK_GRAY)
        for label, value in info:
            y = self.get_y()
            self.set_font('ArialN', 'B', 11)
            self.set_text_color(*DARK_GRAY)
            self.set_xy(x_start, y)
            self.cell(col_w_label, 8, label, border=1)
            self.set_font('ArialN', '', 11)
            self.cell(col_w_value, 8, '  ' + value, border=1, new_x='LMARGIN', new_y='NEXT')

    def section_title(self, num, title):
        self.set_font('ArialN', 'B', 11)
        self.set_text_color(*DARK_GRAY)
        self.ln(3)
        self.cell(0, 6, '%s. %s' % (num, title), new_x='LMARGIN', new_y='NEXT')
        self.ln(1.5)

    def subsection_title(self, letter, title):
        self.set_font('ArialN', 'B', 11)
        self.set_text_color(*DARK_GRAY)
        self.ln(2)
        self.cell(0, 6, '%s) %s' % (letter, title), new_x='LMARGIN', new_y='NEXT')
        self.ln(1)

    def body_text(self, text):
        self.set_font('ArialN', '', 11)
        self.set_text_color(*DARK_GRAY)
        self.multi_cell(0, 5.5, text)
        self.ln(0.5)

    def code_block(self, code, title=None):
        if title:
            self.set_font('ArialN', 'B', 10)
            self.set_text_color(*DARK_GRAY)
            self.cell(0, 5, title, new_x='LMARGIN', new_y='NEXT')
            self.ln(1)

        raw_lines = code.strip().split('\n')
        line_h = 4
        pad = 2
        x_left = 10
        x_code = 19
        box_w = 190
        page_bot = 280

        self.set_auto_page_break(auto=False)

        if self.get_y() + line_h * 2 + pad * 2 > page_bot:
            self.add_page()

        seg_start = self.get_y() + pad
        self.set_y(seg_start)
        y_line = seg_start
        for i, line in enumerate(raw_lines):
            if y_line + line_h > page_bot - 5:
                self.set_draw_color(*BLUE)
                self.set_fill_color(*CODE_BG)
                self.rect(x_left, seg_start, box_w, y_line - seg_start + pad, style='D')
                self.set_y(y_line + pad)
                self.set_auto_page_break(auto=True, margin=15)
                self.add_page()
                self.set_auto_page_break(auto=False)
                seg_start = self.get_y() + pad
                y_line = seg_start

            self.set_fill_color(*CODE_BG)
            self.set_xy(x_left, y_line)
            self.cell(box_w, line_h, '', fill=True)

            self.set_xy(x_code, y_line)
            self.set_font('CourierN', '', 6.5)
            self.set_text_color(*LIGHT_GRAY)
            self.cell(7, line_h, str(i + 1).rjust(3), align='R')

            self.set_font('CourierN', '', 7.5)
            self.set_text_color(*DARK_GRAY)
            self.cell(0, line_h, ' ' + line)
            y_line += line_h

        self.set_draw_color(*BLUE)
        self.set_fill_color(*CODE_BG)
        self.rect(x_left, seg_start, box_w, y_line - seg_start + pad, style='D')

        self.set_y(y_line + pad + 1)
        self.set_auto_page_break(auto=True, margin=15)

    def add_image_full(self, img_path, caption=None):
        if not os.path.exists(img_path):
            self.body_text('[Không tìm thấy ảnh: %s]' % img_path)
            return

        self.set_auto_page_break(auto=False)
        remaining = 280 - self.get_y()

        # Allocate space based on size estimation
        if remaining < 90:
            self.set_auto_page_break(auto=True, margin=15)
            self.add_page()
            self.set_auto_page_break(auto=False)

        # Draw image fitting width
        self.image(img_path, x=10, w=190)
        self.ln(1)

        if caption:
            self.set_font('ArialN', 'I', 9)
            self.set_text_color(*LIGHT_GRAY)
            self.cell(0, 4, caption, align='C', new_x='LMARGIN', new_y='NEXT')
            self.ln(1.5)

        self.set_auto_page_break(auto=True, margin=15)

pdf = ReportPDF()
pdf.set_title('Báo cáo thực hành Tuần 5')
pdf.set_author('Lê Ngọc Tường 23207124')

pdf.cover_page()

# ==================== PHẦN 1 ====================
pdf.add_page()
pdf.section_title('I', 'PHẦN 1: BÀI TẬP KHỞI ĐỘNG - CỔNG AND')
pdf.subsection_title('1.1', 'Mục tiêu và các bước Setup trên Design Vision')
pdf.body_text('Bài tập khởi động nhằm giúp sinh viên làm quen với công cụ tổng hợp Synopsys Design Vision và công cụ xác minh Synopsys Formality thông qua một thiết kế đơn giản là cổng AND 2 ngõ vào.')
pdf.body_text('Quy trình thiết lập được thực hiện thông qua dòng lệnh dc_shell kết hợp giao diện đồ họa:')
pdf.body_text('Trong lần biên dịch đầu tiên, hệ thống báo lỗi cú pháp do khai báo cổng không đúng chuẩn Verilog. Sau khi sửa lại file mã nguồn RTL, quá trình phân tích và hiện thực đã thành công.')

pdf.add_image_full(os.path.join(IMG_DIR, '2.png'), 'Hình 1.1: Thông báo lỗi biên dịch ban đầu của cổng AND trong Design Vision.')
pdf.add_image_full(os.path.join(IMG_DIR, '4.png'), 'Hình 1.2: Cấu trúc cổng AND hiển thị trên giao diện schematic của Design Vision.')

pdf.subsection_title('1.2', 'Kết quả tổng hợp mạch AND_GATE')
pdf.body_text('Sau khi chạy lệnh compile_ultra -no_autoungroup, ta thu được kết quả tổng hợp của cổng AND.')
pdf.add_image_full(os.path.join(IMG_DIR, '5.png'), 'Hình 1.3: Sơ đồ mạch cổng AND được ánh xạ sang thư viện công nghệ SAED32nm.')

pdf.body_text('Phân tích Báo cáo Diện tích:')
pdf.body_text('- Combinational Area: 2.033152 um2')
pdf.body_text('- Noncombinational Area: 0.000000 um2 do cổng AND là mạch tổ hợp và không chứa Flip-Flop.')
pdf.body_text('- Total Cell Area: 2.033152 um2')
pdf.add_image_full(os.path.join(IMG_DIR, '9.png'), 'Hình 1.4: Báo cáo diện tích chi tiết của cổng AND.')

pdf.body_text('Phân tích Báo cáo Timing & QoR:')
pdf.body_text('- Worst Negative Slack (WNS): 0.00')
pdf.body_text('- Cell Count: 1 Cell duy nhất.')
pdf.add_image_full(os.path.join(IMG_DIR, '8.png'), 'Hình 1.5: Báo cáo QoR cổng AND.')

pdf.subsection_title('1.3', 'Xác minh thiết kế cổng AND trên Formality')
pdf.body_text('Sử dụng công cụ Synopsys Formality để đối chiếu chức năng giữa file thiết kế RTL và Netlist mức cổng sau tổng hợp.')
pdf.body_text('- Kết quả matching: Ghép nối thành công các điểm so sánh.')
pdf.body_text('- Kết quả verification: Verification Succeeded.')
pdf.add_image_full(os.path.join(IMG_DIR, '11.png'), 'Hình 1.6: Kết quả đối chiếu điểm so khớp trên Formality cho cổng AND.')
pdf.add_image_full(os.path.join(IMG_DIR, '17.png'), 'Hình 1.7: Giao diện Formality thông báo xác minh cổng AND thành công.')

pdf.subsection_title('1.4', 'Mô phỏng Testbench cổng AND trên VCS')
pdf.body_text('Thực hiện mô phỏng sau tổng hợp bằng trình mô phỏng Synopsys VCS để kiểm tra hoạt động chức năng tổ hợp của cổng AND.')
pdf.body_text('Mã nguồn Testbench cổng AND (and_gate_tb.v):')
pdf.code_block('''`timescale 1ns/1ns
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
endmodule''')

pdf.body_text('Câu lệnh thực thi biên dịch trên VCS:')
pdf.code_block('''vcs -debug_all and_gate_tb.v design_mapped.v saed32nm.v
./simv -gui''')

pdf.body_text('Kết quả mô phỏng thu được trên Terminal:')
pdf.code_block('''At time 0: a = 0, b = 0 => y = 0
At time 10: a = 0, b = 1 => y = 0
At time 20: a = 1, b = 0 => y = 0
At time 30: a = 1, b = 1 => y = 1''')
pdf.body_text('Kết quả trên chứng minh chức năng hoạt động của mạch sau tổng hợp hoàn toàn chính xác theo đúng bảng chân trị của cổng AND.')

# ==================== PHẦN 2 ====================
pdf.add_page()
pdf.section_title('II', 'PHẦN 2: TỔNG HỢP VÀ ĐÁNH GIÁ MẠCH BỘ ĐẾM 8-BIT')
pdf.subsection_title('2.1', 'Các bước Setup tổng hợp')
pdf.body_text('Mạch đếm 8-bit (counter) được tiến hành tổng hợp trên Design Vision với mục tiêu tối ưu hóa diện tích và timing.')
pdf.code_block('''set top_module counter
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
compile_ultra -no_autoungroup''', 'Tcl Script thiết lập tổng hợp:')

pdf.add_image_full(os.path.join(IMG_DIR, 'counter.png'), 'Hình 2.1: Quá trình Link thư viện công nghệ SAED32nm cho thiết kế counter.')
pdf.add_image_full(os.path.join(IMG_DIR, 'counter1.png'), 'Hình 2.2: Lệnh compile_ultra bắt đầu ánh xạ thiết kế counter.')
pdf.add_image_full(os.path.join(IMG_DIR, 'mach.png'), 'Hình 2.3: Sơ đồ mạch Schematic bộ đếm 8-bit sau tổng hợp trên Design Vision.')

pdf.subsection_title('2.2', 'Phân tích báo cáo diện tích ban đầu và giải pháp khắc phục lỗi Hold Time')
pdf.body_text('Sau lần biên dịch đầu tiên bằng lệnh compile_ultra, hệ thống đã xuất ra báo cáo diện tích ban đầu:')
pdf.body_text('- Combinational Area: 35.3263 um2')
pdf.body_text('- Noncombinational Area: 56.9283 um2')
pdf.body_text('- Total Cell Area: 92.2546 um2')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.15.png'), 'Hình 2.4: Báo cáo diện tích ban đầu của bộ đếm 8-bit.')

pdf.body_text('Phát hiện vi phạm Hold Time:')
pdf.body_text('Khi chạy báo cáo kiểm tra lỗi ràng buộc và timing, công cụ phát hiện lỗi vi phạm về Hold Time tại ngõ vào D của thanh ghi state_reg[0], thời gian giữ thực tế chỉ đạt 0.09 ns trong khi yêu cầu tối thiểu là 0.10 ns.')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.23.2.png'), 'Hình 2.5: Báo cáo vi phạm Hold Time tại chân state_reg[0]/D.')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.36.png'), 'Hình 2.6: Lệnh report_constraint chỉ ra điểm vi phạm Hold Time.')

pdf.body_text('Giải pháp khắc phục:')
pdf.body_text('Cấu hình sửa lỗi tự động trong Design Compiler bằng các lệnh sau:')
pdf.code_block('''set_fix_hold [all_clocks]
compile_ultra -incremental''')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.37.png'), 'Hình 2.7: Thực thi các lệnh chèn buffer để sửa lỗi Hold Time.')

pdf.subsection_title('2.3', 'Báo cáo QoR và diện tích sau khi sửa lỗi Hold Time')
pdf.body_text('Sau khi chạy biên dịch incremental, lỗi vi phạm Hold Time đã được khắc phục triệt để. Tổng diện tích Cell tăng từ 92.25 um2 lên 95.30 um2 do trình tổng hợp tự động chèn thêm các tế bào đệm trên đường truyền dữ liệu phản hồi để kéo dài thời gian trễ của tín hiệu.')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.41.png'), 'Hình 2.8: Báo cáo QoR sau sửa lỗi chỉ ra 0 vi phạm Hold.')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.42.png'), 'Hình 2.9: Báo cáo diện tích sau sửa lỗi.')

pdf.subsection_title('2.4', 'Báo cáo QoR và diện tích phân chia chi tiết (Dữ liệu tổng hợp)')
pdf.body_text('Dưới đây là các báo cáo QoR và phân tách diện tích tổng thể thu được sau quá trình tối ưu hóa:')
pdf.add_image_full(os.path.join(IMG_DIR, 'counter11.png'), 'Hình 2.10: Báo cáo QoR tổng hợp của mạch Counter 8-bit.')
pdf.add_image_full(os.path.join(IMG_DIR, 'counter12.png'), 'Hình 2.11: Phân chia chi tiết diện tích Cell và diện tích thiết kế.')
pdf.body_text('Sau khi thiết kế đạt chuẩn, các file netlist mapped, ràng buộc và cơ sở dữ liệu được xuất ra thư mục đầu ra bằng các lệnh:')
pdf.code_block('''write_file -format verilog -hierarchy -output ./output/design_mapped.v
write_file -format ddc -hierarchy -output ./output/design_mapped.ddc
write_sdc -nosplit ../cons/icc2.sdc
write_sdf ./output/design_mapped.sdf''')
pdf.body_text('Các tệp tin đầu ra bao gồm netlist mức cổng (design_mapped.v), file ràng buộc thiết kế SDC (icc2.sdc) và file thông tin trễ SDF (design_mapped.sdf).')

# ==================== PHẦN 3 ====================
pdf.add_page()
pdf.section_title('III', 'PHẦN 3: XÁC MINH HÌNH THỨC TRÊN TOOL FORMALITY')
pdf.body_text('Thực hiện xác minh tương đương chức năng cho bộ đếm 8-bit để đảm bảo quá trình sửa lỗi Hold Time không làm thay đổi logic hoạt động của mạch.')
pdf.body_text('- Thiết kế tham chiếu: File nguồn counter.v viết ở mức hành vi.')
pdf.body_text('- Thiết kế hiện thực: Netlist mức cổng sau tổng hợp design_mapped.v.')
pdf.body_text('- Thiết lập hằng số: Khai báo chân reset clear cố định ở mức 0 để so khớp.')

pdf.add_image_full(os.path.join(IMG_DIR, '2b_2.png'), 'Hình 3.1: Các điểm so sánh được ánh xạ thành công.')
pdf.add_image_full(os.path.join(IMG_DIR, '2b_matched.png'), 'Hình 3.2: Chi tiết các điểm so khớp logic.')
pdf.add_image_full(os.path.join(IMG_DIR, '2b_verifysuccess.png'), 'Hình 3.3: Giao diện Formality thông báo xác minh mạch đếm thành công.')

# ==================== PHẦN 4 ====================
pdf.add_page()
pdf.section_title('IV', 'PHẦN 4: MÔ PHỎNG SAU TỔNG HỢP VỚI VCS')
pdf.subsection_title('4.1', 'Thiết lập lệnh biên dịch mô phỏng')
pdf.code_block('''vcs -gui -debug_all \\
    counter_tb.v \\
    design_mapped.v \\
    saed32nm.v''', 'Lệnh biên dịch mô phỏng VCS:')

pdf.subsection_title('4.2', 'Phân tích giản đồ xung mô phỏng')
pdf.body_text('Giản đồ xung thu được từ giao diện mô phỏng VCS thể hiện chính xác chu kỳ đếm của bộ đếm 8-bit.')
pdf.add_image_full(os.path.join(IMG_DIR, '2b-cqau1.png'), 'Hình 4.1: Dạng sóng mô phỏng trạng thái hoạt động của bộ đếm 8-bit.')
pdf.add_image_full(os.path.join(IMG_DIR, '2b-cau1.1.png'), 'Hình 4.2: Terminal in giá trị output của bộ đếm thay đổi tuần tự.')

output_path = r'c:\HK3-25-26\THTKVM\Tuan5\23207124_LeNgocTuong_CLC3_Tuan5.pdf'
pdf.output(output_path)
print('PDF saved successfully to: ' + output_path)

