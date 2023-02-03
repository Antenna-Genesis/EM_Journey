clear;
clc
options = gaoptimset('PopulationSize',1000, 'Generations', 600,'plotFcn',@gaplotbestf); % 遗传算法相关配置
fun = @fitnessfun; % 设置适应度函数句柄
% nonlcon = @nonlconfun; % 设置非线性约束函数句柄
nvars = 4; % 自变量个数
A = [];  b = [];
Aeq = [];  beq = [];
lb = [1;1;1;1];  ub = [30;30;30;30];
[x_best, fval] = ga(fun, nvars, A,b,Aeq,beq,lb,ub,@nonlcon,options);
function f = fitnessfun(x)
rmat2=load("net2.mat");
ann2=rmat2.results.net;
rmat3=load("net3.mat");
ann3=rmat3.results.net;
rmat4=load("net4.mat");
ann4=rmat4.results.net;
rmat5=load("net5.mat");
ann5=rmat5.results.net1;
rmat1=load("net1.mat");
ann1=rmat1.results.net;
rel=[sim(ann1,[x(1),x(2),x(3),x(4)]'),sim(ann2,[x(1),x(2),x(3),x(4)]'),sim(ann3,[x(1),x(2),x(3),x(4)]'),sim(ann4,[x(1),x(2),x(3),x(4)]'),sim(ann5,[x(1),x(2),x(3),x(4)]')];
 f = -(sum(rel)-max(rel)-min(rel))/3;
end
function [c,ceq]=nonlcon(x)
rmat2=load("net2.mat");
ann2=rmat2.results.net;
rmat3=load("net3.mat");
ann3=rmat3.results.net;
rmat4=load("net4.mat");
ann4=rmat4.results.net;
rmat5=load("net5.mat");
ann5=rmat5.results.net1;
rmat1=load("net1.mat");
ann1=rmat1.results.net;
rel=[sim(ann1,[x(1),x(2),x(3),x(4)]'),sim(ann2,[x(1),x(2),x(3),x(4)]'),sim(ann3,[x(1),x(2),x(3),x(4)]'),sim(ann4,[x(1),x(2),x(3),x(4)]'),sim(ann5,[x(1),x(2),x(3),x(4)]')];
c=max(rel)-min(rel)-5;
% c=[];
ceq=[];
end
