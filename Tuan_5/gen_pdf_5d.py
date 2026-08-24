# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from fpdf import FPDF

FONT_DIR = r'C:\Windows\Fonts'
IMG_DIR = r'c:\HK3-25-26\THTKVM\Tuan5\images'

BLUE = (31, 78, 121)
DARK_GRAY = (51, 51, 51)
LIGHT_GRAY = (120, 120, 120)
CODE_BG = (245, 245, 245)

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
            self.cell(0, 5, 'Báo cáo thực hành Tuần 5 (Bản Trung Bình)', align='L')
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
        self.cell(0, 12, '(PHIÊN BẢN 5 ĐIỂM - TRUNG BÌNH)', align='C', new_x='LMARGIN', new_y='NEXT')
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
pdf.set_title('Báo cáo thực hành Tuần 5 - Bản 5đ')
pdf.set_author('Lê Ngọc Tường 23207124')

pdf.cover_page()

# ==================== PHẦN 1 ====================
pdf.add_page()
pdf.section_title('I', 'PHẦN 1: BÀI TẬP KHỞI ĐỘNG - CỔNG AND')
pdf.body_text('Thực hiện tổng hợp cổng AND sử dụng Design Compiler với thư viện saed32rvt_tt1p0sv25c.db.')
pdf.add_image_full(os.path.join(IMG_DIR, '5.png'), 'Hình 1.1: Sơ đồ Schematic cổng AND.')
pdf.body_text('Kết quả Formality cho cổng AND:')
pdf.add_image_full(os.path.join(IMG_DIR, '17.png'), 'Hình 1.2: Formality báo Verify Succeeded.')

# ==================== PHẦN 2 ====================
pdf.add_page()
pdf.section_title('II', 'PHẦN 2: TỔNG HỢP VÀ SỬA TIMING BỘ ĐẾM 8-BIT')
pdf.body_text('Chạy lệnh compile_ultra để tổng hợp thiết kế bộ đếm 8-bit. Kết quả sơ đồ mạch:')
pdf.add_image_full(os.path.join(IMG_DIR, 'mach.png'), 'Hình 2.1: Sơ đồ Schematic bộ đếm 8-bit.')

pdf.body_text('Báo cáo diện tích ban đầu của bộ đếm:')
pdf.body_text('- Total Cell Area: 92.2546 um2')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.15.png'), 'Hình 2.2: Diện tích bộ đếm ban đầu.')

pdf.body_text('Chạy lệnh set_fix_hold và compile_ultra -incremental để sửa lỗi vi phạm Hold Time:')
pdf.add_image_full(os.path.join(IMG_DIR, '2a.41.png'), 'Hình 2.3: Báo cáo QoR sau khi sửa lỗi Hold.')

# ==================== PHẦN 3 ====================
pdf.add_page()
pdf.section_title('III', 'PHẦN 3: XÁC MINH FORMALITY BỘ ĐẾM')
pdf.body_text('So sánh đối chiếu thiết kế RTL và Netlist sau tổng hợp sử dụng Formality:')
pdf.add_image_full(os.path.join(IMG_DIR, '2b_verifysuccess.png'), 'Hình 3.1: Kết quả Formality xác minh thành công.')

# ==================== PHẦN 4 ====================
pdf.add_page()
pdf.section_title('IV', 'PHẦN 4: MÔ PHỎNG SAU TỔNG HỢP VỚI VCS')
pdf.body_text('Sử dụng VCS để mô phỏng giản đồ sóng ngõ ra của thiết kế Netlist:')
pdf.add_image_full(os.path.join(IMG_DIR, '2b-cqau1.png'), 'Hình 4.1: Giản đồ dạng sóng mô phỏng bộ đếm.')

output_path = r'c:\HK3-25-26\THTKVM\Tuan5\23207124_LeNgocTuong_CLC3_Tuan5_5d.pdf'
pdf.output(output_path)
print('PDF saved successfully to: ' + output_path)
