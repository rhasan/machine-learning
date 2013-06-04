%% ========== Part 1: Training libSVM ==========


% Load from ex6data3: 
% You will have X, y in your environment
load('ex6data3.mat');

% Try different SVM Parameters here
[C, sigma] = dataset3ParamsLibSVM(X, y, Xval, yval);


% Train the SVM
%model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));

options = sprintf('-c %1.3f -g %1.3f',C,sigma);
model = svmtrain(y, X, options);
[predict_label, accuracy, dec_values] = svmpredict(yval, Xval, model);
%fprintf('final accuracy=%f\n',accuracy(1));
visualizeBoundaryLibSVM(X, y, model);
