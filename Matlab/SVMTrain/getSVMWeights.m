clear;
clc;

data_file = '/Users/keyanchen/Files/Dataset/704/AIR-SARShip-1.0/data.txt';
data = load(data_file);

save("data.mat")


%训练分类模型
%svmModel = svmtrain(train,group,'kernel_function','linear','showplot',true);
%分类测试
%classification=svmclassify(svmModel,test,'Showplot',true);
