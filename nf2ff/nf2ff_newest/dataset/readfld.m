function readfld(filename,savename)
E1=importdata(filename);
E=E1.data;
% 导出的fld文件的第一列到第三列为xyz坐标
% 第四列Ex实部，第五列Ex实部，第六列第七列Ey实部和虚部
Ex=E(:,4)+1i*E(:,5);
Ey=E(:,6)+1i*E(:,7);
Ez=E(:,8)+1i*E(:,9);
csvwrite([savename 'x' '.csv'],Ex);
csvwrite([savename 'y' '.csv'],Ey);
csvwrite([savename 'z' '.csv'],Ez);

