clear all
close all
rmat=load("matlab.mat");
ann=rmat.results.net;
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
height=load("height.mat");
Wid=load("Width1.mat");
num=0;
for it=3000:size(height.result_mat1,2)
    num=num+1;
    rel=[sim(ann1,height.result_mat1(:,it)) sim(ann2,height.result_mat1(:,it)) sim(ann3,height.result_mat1(:,it)) sim(ann4,height.result_mat1(:,it)) sim(ann5,height.result_mat1(:,it))];
    simre1=sum(rel)/5;
    simre2=(sum(rel)-max(rel)-min(rel))/3;
    simre3=median(rel);
    simre4=sim(ann,height.result_mat1(:,it));
    err1(num)=(Wid.result_mat(it)-simre1);
    err2(num)=Wid.result_mat(it)-simre2;
    err3(num)=Wid.result_mat(it)-simre3;
    err4(num)=Wid.result_mat(it)-simre4;
end
figure;
histogram(err1);
grid on;
figure;
histogram(err2);
grid on;
figure;
histogram(err3);
grid on;
figure;
histogram(err4);