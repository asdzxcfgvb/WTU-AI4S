clear all; clc; close all ; %清除变量空间的所有变量、函数、MEX文件
%这是PINN文章里的薛定谔方程用分步傅里叶法
n = 1024; %x上打4096（2的幂次）个点
nx = 0.01; %网格的间距
x = (-n / 2:n / 2 - 1) * nx; %打好x的点，令其每一列有4096个点且间隔为0.01 （把减1去掉变成歪的？）
q = 2 * sech(x); %给q赋初始时刻的值 的的
u(:, 1) = abs(q); %把q的值赋给矩阵u的第一列
hw = 2 * pi / (n * nx); %傅里叶变换把真实空间的间隔变为傅里叶空间的间隔
w = fftshift((-n / 2:n / 2 - 1) * hw); %将零频点移到频谱的中间，具体来说，fftshift函数将输入的频谱数据进行循环平移，使得原始数据的中心点（即零频点）位于新频谱的中间位置。通过这个操作，可以方便地在频谱中观察到信号的低频和高频成分，并进行相应的频谱分析和处理。
L = pi / 2; %演化的长度
nm = round(L * 2000); %循环次数
h = L / nm; %步长

for j = 1:nm %开始循环，循环次数为nm
    j
    D1 = exp(-1i * w .^ 2 * h / 4); %分步傅里叶法，先算h/2步线性的
    step1 = ifft(D1 .* fft(q)); %step1就是线性部分单独作用的h/2时的值
    D2 = exp(1i * abs(step1) .^ 2 * h); %算非线性的h步
    step2 = D2 .* step1; %以上一步的结果为初解，step2就是线性的一半加非线性的整个h时的值
    q = ifft(D1 .* fft(step2)); %再算h/2步线性的，q就是整个的线性加整个的非线性时h时的值，并更新了q
    r = 1 + floor((j - 1) / 10); %每循环100次存储数据
    u(:, r) = abs(q); %将q的值赋给u的第r列
end

z = 0:h * 10:L; %每隔100个步长打点来作图
mesh(x, z, u') %画图，u转置来匹配维度
