---
title: "BÁO CÁO THỰC HÀNH TUẦN 4"
subtitle: "MÔ PHỎNG LOGIC BẰNG TRÌNH BIÊN DỊCH VCS & GIAO DIỆN DVE"
author: |
  Họ và tên: Lê Ngọc Tường \\
  Mã số SV: 23207124 \\
  Lớp: 23DTV-CLC3 \\
  Môn học: Thực hành thiết kế vi mạch điện tử
date: "Tuần 4"
geometry: margin=2cm
fontsize: 12pt
header-includes:
  - \usepackage{listings}
  - \usepackage{xcolor}
  - \usepackage{graphicx}
  - \usepackage{float}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhead[L]{Báo cáo thực hành Tuần 4}
  - \fancyhead[R]{23207124 - Lê Ngọc Tường}
  - \fancyfoot[C]{\thepage}
  - \lstset{
      language=Verilog,
      basicstyle=\ttfamily\small,
      keywordstyle=\color{blue}\bfseries,
      commentstyle=\color{gray},
      stringstyle=\color{red},
      numbers=left,
      numberstyle=\tiny\color{gray},
      numbersep=8pt,
      frame=single,
      breaklines=true,
      backgroundcolor=\color{gray!10},
      showstringspaces=false,
      tabsize=2,
      captionpos=b
    }
---

\thispagestyle{empty}
\begin{center}
\vspace*{2cm}

{\Large\textbf{TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐHQG TP.HCM}}

\vspace{0.3cm}

{\large\textbf{KHOA ĐIỆN TỬ VIỄN THÔNG}}

\vspace{2cm}

{\LARGE\textbf{BÁO CÁO THỰC HÀNH TUẦN 4}}

\vspace{0.5cm}

{\Large MÔ PHỎNG LOGIC BẰNG TRÌNH BIÊN DỊCH VCS \& GIAO DIỆN DVE}

\vspace{3cm}

\begin{minipage}{0.6\textwidth}
\begin{flushleft}
\textbf{Họ và tên Sinh viên:} Lê Ngọc Tường \\
\textbf{Mã số Sinh viên:} 23207124 \\
\textbf{Lớp học:} 23DTV-CLC3 \\
\textbf{Môn học:} Thực hành thiết kế vi mạch điện tử
\end{flushleft}
\end{minipage}

\vspace{4cm}

{\large\today}
\end{center}

\newpage
\setcounter{page}{1}

# 1. Thiết kế và kiểm chứng mạch tổ hợp

## 1.1 Phân tích lý thuyết

Mạch tổ hợp thực hiện hàm logic:

$$Y = \overline{A}.\overline{B}.\overline{C} + A.\overline{B}.\overline{C} + A.\overline{B}.C$$

Rút gọn biểu thức logic:

$$Y = \overline{B}.\overline{C}.(\overline{A} + A) + A.\overline{B}.C = \overline{B}.\overline{C} + A.\overline{B}.C = \overline{B}.(\overline{C} + A)$$

Bảng chân trị ngõ ra đối chứng:

| A | B | C | Y |
|---|---|---|---|
| 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 |
| 1 | 1 | 1 | 0 |

## 1.2 Mã nguồn Verilog

Mã nguồn thiết kế mạch tổ hợp:

```verilog
module combinational (
    input A,
    input B,
    input C,
    output Y
);
    assign Y = (~A & ~B & ~C) | (A & ~B & ~C) | (A & ~B & C);
endmodule
```

Mã nguồn chạy mô phỏng:

```verilog
`timescale 1ns/1ns

module combinational_tb;
    reg A, B, C;
    wire Y;

    combinational uut (
        .A(A),
        .B(B),
        .C(C),
        .Y(Y)
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
endmodule
```

## 1.3 Kết quả mô phỏng

Giản đồ xung và thông tin xuất ra màn hình mô phỏng:

![Giản đồ xung mạch tổ hợp](bai1_waveform.png){ width=100% }

![Kết quả Console Monitor](bai1_console.png){ width=100% }

# 2. Thiết kế và kiểm chứng mạch đếm 8-bit Counter

## 2.1 Nguyên lý hoạt động

Mạch đếm tăng dần sau mỗi chu kỳ xung nhịp clock khi chân reset clear ở mức 0. Khi clear lên mức 1, ngõ ra lập tức đưa giá trị về 0 bất chấp trạng thái của clock.

## 2.2 Mã nguồn Verilog

Mã nguồn thiết kế bộ đếm:

```verilog
module counter (
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
endmodule
```

Mã nguồn chạy mô phỏng:

```verilog
`timescale 1ns/1ns

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
endmodule
```

## 2.3 Kết quả mô phỏng

Giản đồ xung và thông tin xuất ra màn hình mô phỏng:

![Giản đồ xung mạch đếm Counter](bai2_waveform.png){ width=100% }

![Kết quả Console Monitor](bai2_console.png){ width=100% }

# 3. Decoder 3-to-8 và MUX 8-to-1

## 3.1 Decoder 3-to-8 có chân Enable

Decoder 3-to-8 nhận đầu vào 3-bit và kích hoạt 1 trong 8 ngõ ra tương ứng. Khi Enable ở mức 0, toàn bộ ngõ ra được đặt về 0.

```verilog
module decoder3to8 (
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
endmodule
```

## 3.2 MUX 8-to-1 cấu trúc từ MUX 2-to-1

MUX 8-to-1 được xây dựng từ 3 tầng MUX 2-to-1. Mỗi tầng giảm số lượng tín hiệu đi một nửa cho đến khi còn 1 ngõ ra duy nhất.

Mạch thành phần MUX 2-to-1:

```verilog
module mux2to1 (
    input a, b, sel,
    output out
);
    assign out = sel ? b : a;
endmodule
```

Mạch chính MUX 8-to-1:

```verilog
module mux8to1 (
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
endmodule
```

## 3.3 Testbench và kết quả mô phỏng

```verilog
`timescale 1ns/1ps

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
endmodule
```

![Kết quả mô phỏng Decoder 3-to-8 và MUX 8-to-1](bai3_sim.png){ width=100% }

# 4. Counter 4-bit Up/Down với Parallel Load

## 4.1 Nguyên lý hoạt động

Bộ đếm 4-bit có khả năng đếm lên hoặc xuống tùy theo tín hiệu mode. Khi load được kích hoạt, giá trị data_in sẽ được nạp vào bộ đếm. Reset bất đồng bộ khi rst_n ở mức 0.

- mode = 1: Đếm lên
- mode = 0: Đếm xuống
- load = 1: Nạp giá trị từ data_in
- rst_n = 0: Reset bộ đếm về 0

## 4.2 Mã nguồn Verilog

```verilog
module counter_updown (
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
endmodule
```

## 4.3 Testbench và kết quả mô phỏng

```verilog
`timescale 1ns/1ps

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
        clk = 0; rst_n = 0; load = 0; mode = 1; data_in = 4'b1010;
        #12 rst_n = 1;
        #20 mode = 1;
        #20 load = 1;
        #10 load = 0;
        #20 mode = 0;
        #50 $finish;
    end
endmodule
```

![Kết quả mô phỏng Counter 4-bit Up/Down](bai4_sim.png){ width=100% }

# 5. Accumulator - Bộ cộng tích lũy 8-bit

## 5.1 Nguyên lý hoạt động

Bộ cộng tích lũy thực hiện phép cộng liên tục giữa giá trị hiện tại acc_out và đầu vào data_in. Khi clear ở mức 1, ngõ ra được reset về 0. Kết quả tích lũy được cập nhật tại mỗi cạnh lên của xung clock.

## 5.2 Mã nguồn Verilog

```verilog
module accumulator (
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
endmodule
```

## 5.3 Testbench và kết quả mô phỏng

```verilog
`timescale 1ns/1ps

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
endmodule
```

![Kết quả mô phỏng Accumulator](bai5_sim.png){ width=100% }
