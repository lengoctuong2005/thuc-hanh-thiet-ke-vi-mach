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
            self.cell(0, 5, 'Báo cáo thực hành Tuần 5 (Bản Khá)', align='L')
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
        self.cell(0, 12, '(PHIÊN BẢN 7 ĐIỂM - KHÁ)', align='C', new_x='LMARGIN', new_y='NEXT')
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

        if remaining < 90:
            self.set_auto_page_break(auto=True, margin=15)
            self.add_page()
            self.set_auto_page_break(auto=False)

        self.image(img_path, x=10, w=190)
        self.ln(1)

        if caption:
            self.set_font('ArialN', 'I', 9)
            self.set_text_color(*LIGHT_GRAY)
            self.cell(0, 4, caption, align='C', new_x='LMARGIN', new_y='NEXT')
            self.ln(1.5)

        self.set_auto_page_break(auto=True, margin=15)

pdf = ReportPDF()
pdf.set_title('Báo cáo thực hành Tuần 5 - Bản 7đ')
pdf.set_author('Lê Ngọc Tường 23207124')

pdf.cover_page()

# ==================== PHẦN 1 ====================
pdf.add_page()
pdf.section_title('I', 'PHẦN 1: BÀI TẬP KHỞI ĐỘNG - CỔNG AND')
pdf.subsection_title('1.1', 'Khởi tạo và thiết lập thư viện công nghệ')
pdf.body_text('Sử dụng công cụ Synopsys Design Compiler (chế độ Design Vision) để tổng hợp mạch cổng AND với thư viện SAED32nm.')
pdf.body_text('Khai báo thư viện công nghệ được lưu trong file cấu hình .synopsys_dc.setup:')
pdf.code_block('''set target_library "saed32rvt_tt1p0sv25c.db"
set link_library "* saed32rvt_tt1p0sv25c.db dw_foundation.sldb"''')

pdf.subsection_title('1.2', 'Đọc file thiết kế và phân tích kết quả tổng hợp')
pdf.body_text('Sau khi chạy lệnh compile_ultra, ta xem sơ đồ Schematic và các báo cáo:')
pdf.add_image_full(os.path.join(IMG_DIR, '5.png'), 'Hình 1.1: Sơ đồ mạch cổng AND sau tổng hợp.')

pdf.body_text('Thông tin diện tích cổng AND:')
pdf.body_text('- Combinational Area: 2.033152 um2')
pdf.body_text('- Noncombinational Area: 0.000000 um2')
pdf.body_text('- Total Cell Area: 2.033152 um2')
pdf.add_image_full(os.path.join(IMG_DIR, '9.png'), 'Hình 1.2: Báo cáo diện tích của cổng AND.')
pdf.add_image_full(os.path.join(IMG_DIR, '8.png'), 'Hình 1.3: Báo cáo QoR của cổng AND.')

pdf.subsection_title('1.3', 'Xác minh hình thức bằng Formality')
pdf.body_text('Sử dụng Formality để so khớp cổng AND giữa RTL và Netlist sau tổng hợp:')
pdf.add_image_full(os.path.join(IMG_DIR, '11.png'), 'Hình 1.4: So khớp các điểm so sánh.')
pdf.add_image_full(os.path.join(IMG_DIR, '17.png'), 'Hình 1.5: Xác minh Formality thành công.')

# ==================== PHẦN 2 ====================
pdf.add_page()
pdf.section_title('II', 'PHẦN 2: TỔNG HỢP VÀ ĐÁNH GIÁ MẠCH BỘ ĐẾM 8-BIT')
pdf.subsection_title('2.1', 'Các bước Setup tổng hợp')
pdf.body_text('Tiến hành thiết lập các tham số thời gian và chạy tổng hợp cho mạch counter:')
pdf.code_block('''create_clock -name clk -period 250 [get_ports clk]
set_input_delay -max 75 -clock clk [remove_from_collection [all_inputs] [get_ports clk]]
set_output_delay -max 75 -clock clk [all_outputs]''')
pdf.add_image_full(os.path.join(IMG_DIR, 'mach.png'), 'Hình 2.1: Sơ đồ Schematic bộ đếm 8-bit sau tổng hợp.')

pdf.subsection_title('2.2', 'Đánh giá diện tích và phát hiện lỗi timing')
pdf.body_text('Thông tin diện tích ban đầu của bộ đếm:')
pdf.body_text('- Combinational Area: 35.3263 um2\n- Noncombinational Area: 56.9283 um2\n- Total Cell Area: 92.2546 um2')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.15.png'), 'Hình 2.2: Diện tích bộ đếm ban đầu.')

pdf.body_text('Công cụ phát hiện lỗi Hold Time tại ngõ vào D của state_reg[0], giá trị Slack âm:')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.23.2.png'), 'Hình 2.3: Vi phạm thời gian giữ Hold Time.')

pdf.subsection_title('2.3', 'Khắc phục lỗi Hold Time và tối ưu hóa thiết kế')
pdf.body_text('Chạy lệnh set_fix_hold và compile_ultra -incremental để sửa lỗi Hold Time:')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.37.png'), 'Hình 2.4: Thực hiện biên dịch incremental để tự động sửa lỗi Hold.')

pdf.body_text('Sau khi tối ưu hóa, lỗi Hold Time đã được sửa hoàn toàn, diện tích tăng nhẹ lên 95.30 um2 do chèn thêm buffer:')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.41.png'), 'Hình 2.5: Báo cáo QoR sau khi khắc phục lỗi Hold.')

pdf.subsection_title('2.4', 'Báo cáo diện tích phân chia chi tiết và xuất dữ liệu')
pdf.add_image_full(os.path.join(IMG_DIR, 'counter12.png'), 'Hình 2.6: Phân chia chi tiết diện tích Cell.')

pdf.body_text('Xuất file Netlist mapped mức cổng và file ràng buộc SDC:')
pdf.code_block('''write_file -format verilog -hierarchy -output ./output/design_mapped.v
write_sdc -nosplit ../cons/icc2.sdc''')

# ==================== PHẦN 3 ====================
pdf.add_page()
pdf.section_title('III', 'PHẦN 3: XÁC MINH HÌNH THỨC TRÊN TOOL FORMALITY')
pdf.body_text('Xác minh tương đương chức năng cho bộ đếm 8-bit bằng Formality:')
pdf.add_image_full(os.path.join(IMG_DIR, '2b_matched.png'), 'Hình 3.1: So khớp chi tiết các điểm so sánh.')
pdf.add_image_full(os.path.join(IMG_DIR, '2b_verifysuccess.png'), 'Hình 3.2: Formality báo cáo xác minh thành công.')

# ==================== PHẦN 4 ====================
pdf.add_page()
pdf.section_title('IV', 'PHẦN 4: MÔ PHỎNG SAU TỔNG HỢP VỚI VCS')
pdf.subsection_title('4.1', 'Thiết lập lệnh biên dịch mô phỏng')
pdf.code_block('vcs -gui -debug_all counter_tb.v design_mapped.v saed32nm.v')

pdf.subsection_title('4.2', 'Giản đồ dạng sóng mô phỏng')
pdf.body_text('Dạng sóng mô phỏng thu được hiển thị chu kỳ đếm nhị phân chính xác:')
pdf.add_image_full(os.path.join(IMG_DIR, '2b-cqau1.png'), 'Hình 4.1: Giản đồ dạng sóng mô phỏng bộ đếm 8-bit.')
pdf.add_image_full(os.path.join(IMG_DIR, '2b-cau1.1.png'), 'Hình 4.2: Terminal in giá trị output thay đổi tuần tự.')

output_path = r'c:\HK3-25-26\THTKVM\Tuan5\23207124_LeNgocTuong_CLC3_Tuan5_7d.pdf'
pdf.output(output_path)
print('PDF saved successfully to: ' + output_path)
