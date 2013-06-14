%% Kaggle titanic solution

clear ; close all; clc

data = csvread('clean_data.csv');
data_m = size(data,1);
%data = data(randperm(data_m),:);




%data = data(:,2);

X_data = data(:,2:end);

%pclass(1),sex(2),age(3),sibsp(4),parch(5),fare(6),embarked(7)

%features = [1 2 3 4 5 6];
features = [1 2 3 4 5 6 7];
X_data = X_data(:,features);

%survived(1),
Y_data = data(:,1);

[X_norm, mu, sigma0] = featureNormalize(X_data);

train_m = int32(0.8 * data_m);


X_train = X_norm(1:train_m,:);
Y_train = Y_data(1:train_m,:);


X_val = X_norm(train_m+1:end,:);
Y_val = Y_data(train_m+1:end,:);


% Try different SVM Parameters here
[C, sigma] = dataset3ParamsLibSVM(X_train, Y_train, X_val, Y_val);



% Train the SVM
%model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));

options = sprintf('-c %1.3f -g %1.3f',C,sigma);
model = svmtrain(Y_train, X_train, options);
[predict_label, accuracy, dec_values] = svmpredict(Y_val, X_val, model);

fprintf('final accuracy=%f\n',accuracy(1));
fprintf('final C=%f sigma=%f\n',C,sigma);

%visualizeBoundaryLibSVM(X_train, Y_train, model);



test_data = csvread('clean_test_data.csv');
X_test = test_data(:,features);
[X_test, mu, sigma0] = featureNormalize(X_test);
Y_test = zeros(size(X_test,1),1);
[Y_test_predict, accuracy, dec_values] = svmpredict(Y_test, X_test, model);

fid = fopen('exp.txt','w');
fprintf(fid,'%d\n',Y_test_predict);
