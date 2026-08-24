# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from fpdf import FPDF

FONT_DIR = r'C:\Windows\Fonts'
IMG_DIR = r'C:\HK3-25-26\THTKVM\Tuan4\report_build'

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
            self.cell(0, 5, 'Bao cao thuc hanh Tuan 4', align='L')
            self.set_text_color(*DARK_GRAY)
            self.cell(0, 5, '23207124 - Le Ngoc Tuong', align='R', new_x='LMARGIN', new_y='NEXT')
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
        self.cell(0, 12, 'BÁO CÁO THỰC HÀNH TUẦN 4:', align='C', new_x='LMARGIN', new_y='NEXT')
        self.cell(0, 12, 'MÔ PHỎNG LOGIC BẰNG TRÌNH BIÊN DỊCH VCS', align='C', new_x='LMARGIN', new_y='NEXT')
        self.cell(0, 12, '& GIAO DIỆN DVE', align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(18)

        info = [
            ('Họ và tên Sinh viên:', 'Lê Ngọc Tường'),
            ('Mã số Sinh viên:', '23207124'),
            ('Lớp học:', '23DTV_CLC3'),
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
        self.ln(2)
        self.cell(0, 6, '%s. %s' % (num, title), new_x='LMARGIN', new_y='NEXT')
        self.ln(1)

    def subsection_title(self, letter, title):
        self.set_font('ArialN', 'B', 11)
        self.set_text_color(*DARK_GRAY)
        self.ln(1)
        self.cell(0, 6, '%s) %s' % (letter, title), new_x='LMARGIN', new_y='NEXT')
        self.ln(0.5)

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

        # Single pass: draw fill+text per line, border at page transitions
        seg_start = self.get_y() + pad
        self.set_y(seg_start)
        y_line = seg_start
        for i, line in enumerate(raw_lines):
            # Check if we need to page break
            if y_line + line_h > page_bot - 5:
                # Draw border for the segment ending on this page
                self.set_draw_color(*BLUE)
                self.set_fill_color(*CODE_BG)
                self.rect(x_left, seg_start, box_w, y_line - seg_start + pad, style='D')
                # New page
                self.set_y(y_line + pad)
                self.set_auto_page_break(auto=True, margin=15)
                self.add_page()
                self.set_auto_page_break(auto=False)
                seg_start = self.get_y() + pad
                y_line = seg_start

            # Background fill per line
            self.set_fill_color(*CODE_BG)
            self.set_xy(x_left, y_line)
            self.cell(box_w, line_h, '', fill=True)

            # Line number
            self.set_xy(x_code, y_line)
            self.set_font('CourierN', '', 6.5)
            self.set_text_color(*LIGHT_GRAY)
            self.cell(7, line_h, str(i + 1).rjust(3), align='R')

            # Code text
            self.set_font('CourierN', '', 7.5)
            self.set_text_color(*DARK_GRAY)
            self.cell(0, line_h, ' ' + line)
            y_line += line_h

        # Draw border for the final segment
        self.set_draw_color(*BLUE)
        self.set_fill_color(*CODE_BG)
        self.rect(x_left, seg_start, box_w, y_line - seg_start + pad, style='D')

        self.set_y(y_line + pad + 1)
        self.set_auto_page_break(auto=True, margin=15)
    def add_image_full(self, img_path, caption=None):
        if not os.path.exists(img_path):
            self.body_text('[Khong tim thay anh: %s]' % img_path)
            return

        self.set_auto_page_break(auto=False)
        remaining = 280 - self.get_y()

        if remaining < 30:
            self.set_auto_page_break(auto=True, margin=15)
            self.add_page()
            self.set_auto_page_break(auto=False)

        self.image(img_path, x=10, w=190)
        self.ln(1)

        if caption:
            self.set_font('ArialN', 'I', 9)
            self.set_text_color(*LIGHT_GRAY)
            self.cell(0, 4, caption, align='C', new_x='LMARGIN', new_y='NEXT')
            self.ln(1)

        self.set_auto_page_break(auto=True, margin=15)

    def bullet_list(self, items):
        self.set_font('ArialN', '', 11)
        self.set_text_color(*DARK_GRAY)
        for item in items:
            self.set_x(15)
            self.cell(5, 6, '-')
            self.set_x(20)
            self.multi_cell(170, 6, item)
        self.ln(1)


pdf = ReportPDF()
pdf.set_title('Bao cao thuc hanh Tuan 4')
pdf.set_author('Le Ngoc Tuong 23207124')

pdf.cover_page()

# ==================== BAI 1 ====================
pdf.add_page()
pdf.section_title('1', 'Thiết kế và kiểm chứng mạch tổ hợp')
pdf.subsection_title('a', 'Phân tích lý thuyết')
pdf.body_text('Mạch tổ hợp thực hiện hàm logic:')
pdf.set_font('CourierN', 'B', 11)
pdf.set_text_color(*DARK_GRAY)
pdf.cell(0, 7, 'Y = ~A.~B.~C + A.~B.~C + A.~B.C', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.ln(2)
pdf.body_text('Rút gọn biểu thức logic: Y = ~B.(~C + A)')
pdf.body_text('Bảng chân trị ngõ ra đối chứng:')

pdf.set_font('ArialN', 'B', 10)
cols = ['A', 'B', 'C', 'Y']
col_w = [25, 25, 25, 25]
x_start = 55
pdf.set_x(x_start)
for col in cols:
    pdf.cell(col_w[0], 7, col, border=1, align='C')
pdf.ln()
rows = [
    ('0','0','0','1'), ('0','0','1','0'), ('0','1','0','0'), ('0','1','1','0'),
    ('1','0','0','1'), ('1','0','1','1'), ('1','1','0','0'), ('1','1','1','0'),
]
pdf.set_font('ArialN', '', 10)
for row in rows:
    pdf.set_x(x_start)
    for val in row:
        pdf.cell(col_w[0], 6, val, border=1, align='C')
    pdf.ln()
pdf.ln(2)

pdf.subsection_title('b', 'Mã nguồn Verilog')
pdf.body_text('Mạch tổ hợp được thiết kế bằng ngôn ngữ Verilog với hàm logic gán liên tục (assign).')
pdf.code_block('''module combinational (
    input A,
    input B,
    input C,
    output Y
);
    assign Y = (~A & ~B & ~C) | (A & ~B & ~C) | (A & ~B & C);
endmodule''', 'Mã nguồn thiết kế mạch tổ hợp:')

pdf.body_text('Testbench chạy mô phỏng với tất cả 8 tổ hợp ngõ vào:')
pdf.code_block('''`timescale 1ns/1ns

module combinational_tb;
    reg A, B, C;
    wire Y;

    combinational uut (
        .A(A), .B(B), .C(C), .Y(Y)
    );

    initial begin
        $monitor($time, " ns | A=%b B=%b C=%b -> Y=%b", A, B, C, Y);
        A = 0; B = 0; C = 0; #10;
        A = 0; B = 0; C = 1; #10;
        A = 0; B = 1; C = 0; #10;
        A = 0; B = 1; C = 1; #10;
        A = 1; B = 0; C = 0; #10;
        A = 1; B = 0; C = 1; #10;
        A = 1; B = 1; C = 0; #10;
        A = 1; B = 1; C = 1; #10;
        $finish;
    end
endmodule''', 'Mã nguồn chạy mô phỏng:')

pdf.subsection_title('c', 'Kết quả mô phỏng')
pdf.body_text('Giản đồ xung và thông tin xuất ra màn hình mô phỏng:')
pdf.add_image_full(os.path.join(IMG_DIR, 'bai1_waveform.png'), 'Giản đồ xung mạch tổ hợp')
pdf.add_image_full(os.path.join(IMG_DIR, 'bai1_console.png'), 'Kết quả Console Monitor')

# ==================== BAI 2 ====================
pdf.add_page()
pdf.section_title('2', 'Thiết kế và kiểm chứng mạch đếm 8-bit Counter')
pdf.subsection_title('a', 'Phân tích lý thuyết')
pdf.body_text('Mạch đếm tăng dần sau mỗi chu kỳ xung nhịp clock khi chân reset clear ở mức 0. Khi clear lên mức 1, ngõ ra lập tức đưa giá trị về 0 bất chấp trạng thái của clock.')
pdf.body_text('Bộ đếm 8-bit có thể đếm từ 0 đến 255. Mỗi cạnh lên của clock sẽ tăng giá trị hiện tại lên 1 đơn vị. Khi đạt giá trị 255 (11111111), giá trị sẽ quay về 0 (00000000) ở cạnh clock tiếp theo.')

pdf.subsection_title('b', 'Mã nguồn Verilog')
pdf.body_text('Bộ đếm được thiết kế với biến reg lưu trạng thái, cập nhật tại cạnh lên của clock:')
pdf.code_block('''module counter (
    input clear,
    input clock,
    output reg [7:0] state
);
    always @(posedge clock or posedge clear) begin
        if (clear)
            state <= 8'b0000_0000;
        else
            state <= state + 1'b1;
    end
endmodule''', 'Mã nguồn thiết kế bộ đếm:')

pdf.body_text('Testbench kiểm tra hoạt động reset và đếm:')
pdf.code_block('''`timescale 1ns/1ns

module counter_tb;
    reg clear;
    reg clock;
    wire [7:0] state;

    counter uut (
        .clear(clear),
        .clock(clock),
        .state(state)
    );

    always #5 clock = ~clock;

    initial begin
        clock = 0;
        clear = 1;
        #15;
        clear = 0;
        #200;
        clear = 1;
        #20;
        $finish;
    end

    initial begin
        $monitor($time, " ns | clear=%b | state = %d (bin: %b)", clear, state, state);
    end
endmodule''', 'Mã nguồn chạy mô phỏng:')

pdf.subsection_title('c', 'Kết quả mô phỏng')
pdf.body_text('Giản đồ xung và thông tin xuất ra màn hình mô phỏng:')
pdf.add_image_full(os.path.join(IMG_DIR, 'bai2_waveform.png'), 'Giản đồ xung mạch đếm Counter')
pdf.add_image_full(os.path.join(IMG_DIR, 'bai2_console.png'), 'Kết quả Console Monitor')

# ==================== BAI 3 ====================
pdf.add_page()
pdf.section_title('3', 'Decoder 3-to-8 và MUX 8-to-1')
pdf.subsection_title('a', 'Decoder 3-to-8 có chân Enable')
pdf.body_text('Decoder 3-to-8 nhận đầu vào 3-bit và kích hoạt 1 trong 8 ngõ ra tương ứng. Khi Enable ở mức 0, toàn bộ ngõ ra được đặt về 0. Khi Enable ở mức 1, một trong 8 ngõ ra sẽ được kích hoạt tùy theo giá trị đầu vào.')
pdf.body_text('Bảng chân trị Decoder 3-to-8:')

pdf.set_font('ArialN', 'B', 9)
cols = ['in[2]', 'in[1]', 'in[0]', 'en', 'out[7:0]']
col_w = [22, 22, 22, 18, 40]
x_start = 40
pdf.set_x(x_start)
for col in cols:
    pdf.cell(col_w[0], 7, col, border=1, align='C')
pdf.ln()
rows = [
    ('0','0','0','1','0000_0001'), ('0','0','1','1','0000_0010'),
    ('0','1','0','1','0000_0100'), ('0','1','1','1','0000_1000'),
    ('1','0','0','1','0001_0000'), ('1','0','1','1','0010_0000'),
    ('1','1','0','1','0100_0000'), ('1','1','1','1','1000_0000'),
]
pdf.set_font('ArialN', '', 9)
for row in rows:
    pdf.set_x(x_start)
    for val in row:
        pdf.cell(col_w[0], 6, val, border=1, align='C')
    pdf.ln()
pdf.ln(2)

pdf.subsection_title('b', 'Mã nguồn Verilog - Decoder 3-to-8')
pdf.body_text('Decoder được thiết kế bằng cấu trúc case để giải mã 3-bit đầu vào:')
pdf.code_block('''module decoder3to8 (
    input [2:0] in,
    input en,
    output reg [7:0] out
);
    always @(*) begin
        if (!en)
            out = 8'b0000_0000;
        else begin
            case (in)
                3'b000: out = 8'b0000_0001;
                3'b001: out = 8'b0000_0010;
                3'b010: out = 8'b0000_0100;
                3'b011: out = 8'b0000_1000;
                3'b100: out = 8'b0001_0000;
                3'b101: out = 8'b0010_0000;
                3'b110: out = 8'b0100_0000;
                3'b111: out = 8'b1000_0000;
                default: out = 8'b0000_0000;
            endcase
        end
    end
endmodule''', 'Mã nguồn Decoder 3-to-8:')

pdf.subsection_title('c', 'MUX 8-to-1 cấu trúc từ MUX 2-to-1')
pdf.body_text('MUX 8-to-1 được xây dựng từ 3 tầng MUX 2-to-1. Mỗi tầng giảm số lượng tín hiệu đi một nửa cho đến khi còn 1 ngõ ra duy nhất. Đầu vào select 3-bit chọn 1 trong 8 tín hiệu đầu vào.')
pdf.code_block('''module mux2to1 (
    input a, b, sel,
    output out
);
    assign out = sel ? b : a;
endmodule''', 'Mạch thành phần MUX 2-to-1:')

pdf.code_block('''module mux8to1 (
    input [7:0] in,
    input [2:0] sel,
    output out
);
    wire [3:0] w1;
    wire [2:0] w2;

    mux2to1 m10 (in[0], in[1], sel[0], w1[0]);
    mux2to1 m11 (in[2], in[3], sel[0], w1[1]);
    mux2to1 m12 (in[4], in[5], sel[0], w1[2]);
    mux2to1 m13 (in[6], in[7], sel[0], w1[3]);

    mux2to1 m20 (w1[0], w1[1], sel[1], w2[0]);
    mux2to1 m21 (w1[2], w1[3], sel[1], w2[1]);

    mux2to1 m30 (w2[0], w2[1], sel[2], out);
endmodule''', 'Mạch chính MUX 8-to-1:')

pdf.subsection_title('d', 'Kết quả mô phỏng')
pdf.body_text('Testbench kiểm tra Decoder 3-to-8 với Enable và MUX 8-to-1:')
pdf.code_block('''`timescale 1ns/1ps

module tb_bai3;
    reg [2:0] th_in;
    reg en;
    wire [7:0] dec_out;
    reg [7:0] mux_in;
    reg [2:0] mux_sel;
    wire mux_out;

    decoder3to8 uut_dec (.in(th_in), .en(en), .out(dec_out));
    mux8to1 uut_mux (.in(mux_in), .sel(mux_sel), .out(mux_out));

    initial begin
        en = 0; th_in = 3'b011; #10;
        en = 1; th_in = 3'b000; #10;
        th_in = 3'b011; #10;
        th_in = 3'b111; #10;
        mux_in = 8'b1010_0101; mux_sel = 3'b000; #10;
        mux_sel = 3'b001; #10;
        mux_sel = 3'b111; #10;
        $finish;
    end
endmodule''', 'Mã source testbench:')

pdf.body_text('Kết quả mô phỏng:')
pdf.add_image_full(os.path.join(IMG_DIR, 'bai3_sim.png'), 'Kết quả mô phỏng Decoder 3-to-8 và MUX 8-to-1')

# ==================== BAI 4 ====================
pdf.add_page()
pdf.section_title('4', 'Counter 4-bit Up/Down với Parallel Load')
pdf.subsection_title('a', 'Phân tích lý thuyết')
pdf.body_text('Bộ đếm 4-bit có khả năng đếm lên hoặc xuống tùy theo tín hiệu mode. Khi load được kích hoạt, giá trị data_in sẽ được nạp vào bộ đếm. Reset bất đồng bộ khi rst_n ở mức 0.')
pdf.body_text('Chức năng các chân:')
pdf.bullet_list([
    'rst_n: Reset bất đồng bộ, khi ở mức 0 sẽ đưa bộ đếm về 0',
    'clk: Xung nhịp clock, bộ đếm cập nhật tại cạnh lên',
    'load: Chức năng nạp song song, khi load=1 sẽ nạp giá trị từ data_in',
    'mode: Chọn chế độ đếm, mode=1 đếm lên, mode=0 đếm xuống',
    'data_in[3:0]: Dữ kiện 4-bit đầu vào khi nạp song song',
    'count[3:0]: Ngõ ra 4-bit hiển thị giá trị đếm hiện tại',
])

pdf.subsection_title('b', 'Mã nguồn Verilog')
pdf.body_text('Bộ đếm được thiết kế với biến reg lưu trạng thái, cập nhật tại cạnh lên của clock:')
pdf.code_block('''module counter_updown (
    input clk,
    input rst_n,
    input load,
    input [3:0] data_in,
    input mode,
    output reg [3:0] count
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 4'b0000;
        else if (load)
            count <= data_in;
        else begin
            if (mode)
                count <= count + 1'b1;
            else
                count <= count - 1'b1;
        end
    end
endmodule''', 'Mã nguồn thiết kế bộ đếm Up/Down:')

pdf.subsection_title('c', 'Kết quả mô phỏng')
pdf.body_text('Testbench kiểm tra các chức năng reset, nạp song song, đếm lên và đếm xuống:')
pdf.code_block('''`timescale 1ns/1ps

module tb_counter;
    reg clk;
    reg rst_n;
    reg load;
    reg mode;
    reg [3:0] data_in;
    wire [3:0] count;

    counter_updown uut (
        .clk(clk),
        .rst_n(rst_n),
        .load(load),
        .data_in(data_in),
        .mode(mode),
        .count(count)
    );

    always #5 clk = ~clk;

    initial begin
        clk = 0; rst_n = 0; load = 0;
        mode = 1; data_in = 4'b1010;
        #12 rst_n = 1;
        #20 mode = 1;
        #20 load = 1;
        #10 load = 0;
        #20 mode = 0;
        #50 $finish;
    end
endmodule''', 'Mã source testbench:')

pdf.body_text('Kết quả mô phỏng:')
pdf.add_image_full(os.path.join(IMG_DIR, 'bai4_sim.png'), 'Kết quả mô phỏng Counter 4-bit Up/Down')

# ==================== BAI 5 ====================
pdf.add_page()
pdf.section_title('5', 'Accumulator - Bộ cộng tích lũy 8-bit')
pdf.subsection_title('a', 'Phân tích lý thuyết')
pdf.body_text('Bộ cộng tích lũy thực hiện phép cộng liên tục giữa giá trị hiện tại acc_out và đầu vào data_in. Khi clear ở mức 1, ngõ ra được reset về 0. Kết quả tích lũy được cập nhật tại mỗi cạnh lên của xung clock.')
pdf.body_text('Công thức tích lũy: acc_out[n] = acc_out[n-1] + data_in')
pdf.body_text('Bộ đếm tích lũy được sử dụng phổ biến trong các mạch xử lý tín hiệu số, đặc biệt là trong bộ lọc FIR và phép tính tích chập.')

pdf.subsection_title('b', 'Mã nguồn Verilog')
pdf.body_text('Bộ cộng tích lũy được thiết kế với biến reg lưu trạng thái:')
pdf.code_block('''module accumulator (
    input clk,
    input clear,
    input [8:0] data_in,
    output reg [8:0] acc_out
);
    always @(posedge clk) begin
        if (clear)
            acc_out <= 8'b0000_0000;
        else
            acc_out <= acc_out + data_in;
    end
endmodule''', 'Mã nguồn thiết kế Accumulator:')

pdf.subsection_title('c', 'Kết quả mô phỏng')
pdf.body_text('Testbench kiểm tra chức năng reset và tích lũy:')
pdf.code_block('''`timescale 1ns/1ps

module tb_accumulator;
    reg clk;
    reg clear;
    reg [8:0] data_in;
    wire [8:0] acc_out;

    accumulator uut (
        .clk(clk),
        .clear(clear),
        .data_in(data_in),
        .acc_out(acc_out)
    );

    always #5 clk = ~clk;

    initial begin
        clk = 0; clear = 1; data_in = 8'd0;
        #15 clear = 0;
        data_in = 8'd5; #10;
        data_in = 8'd10; #10;
        data_in = 8'd20; #10;
        clear = 1; #10;
        clear = 0; data_in = 8'd7; #10;
        $finish;
    end
endmodule''', 'Mã source testbench:')

pdf.body_text('Kết quả mô phỏng:')
pdf.add_image_full(os.path.join(IMG_DIR, 'bai5_sim.png'), 'Kết quả mô phỏng Accumulator')

output_path = os.path.join(IMG_DIR, '..', '23207124_LeNgocTuong_CLC3_Tuan4.pdf')
try:
    pdf.output(output_path)
    print('PDF saved to: ' + output_path)
except PermissionError:
    alt = os.path.join(IMG_DIR, '..', 'report_tuan4.pdf')
    pdf.output(alt)
    print('File dang mo, da luu vao: ' + alt)
