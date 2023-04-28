clear all
lb=4801;
ub=6027;
pth="E:\attest\OneDrive_SiqiBai\ML in EM";
result_mat1=[];
for it=lb:ub
eff_list(it+1)=it;
data=readmatrix(pth+"\sim"+num2str(it)+"\height"+num2str(it)+".csv",'OutputType', 'string');
data=data([2:3],[2:3]);
data=strrep(data,"mm","");
data=str2double(data);
data=data(:);
if it==0
    result_mat1=data;
else
result_mat1=[result_mat1,data];
end
end
disp(result_mat1)
pth="E:\attest\OneDrive_SiqiBai\ML in EM";
result_mat=[]
no_eff_num=0;
for it=lb:ub
data=readmatrix(pth+"\sim"+num2str(it)+"\para"+num2str(it)+".csv",'OutputType', 'string');
data(1,:)=[];
data(:,1)=[];
data=strrep(data,"[","");
data=strrep(data,"]","");
if str2double(data(1))~=0
data=strsplit(data(2+2*str2double(data(1)),1),",");
data=str2double(data(2));
 if it==0
     result_mat=[data];
 else
     result_mat=[result_mat,data];
 end
else
    no_eff_num=1+no_eff_num;
    no_eff(no_eff_num)=it+1;
end
end
for it=1:no_eff_num
    result_mat1(:,no_eff(no_eff_num-it+1)-lb)=[];
    disp(no_eff(no_eff_num-it+1))
    eff_list(no_eff(no_eff_num-it+1))=[];
end

save("h2.mat","result_mat1")
save("Widthdiv2.mat","result_mat")
% save("valid_data","eff_list")