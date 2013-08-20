%% Machine Learning Online Class
%  Exercise 5 | Regularized Linear Regression and Bias-Variance
%
%  Instructions
%  ------------
% 
%  This file contains code that helps you get started on the
%  exercise. You will need to complete the following functions:
%
%     linearRegCostFunction.m
%     learningCurve.m
%     validationCurve.m
%
%  For this exercise, you will not need to change any code in this file,
%  or any other files other than those mentioned above.
%

%% Initialization
clear ; close all; clc

%% =========== Part 1: Loading and Visualizing Data =============
%  We start the exercise by first loading and visualizing the dataset. 
%  The following code will load the dataset into your environment and plot
%  the data.
%

% Load Training Data
fprintf('Loading and Visualizing Data ...\n')

% Load from ex5data1: 
% You will have X, y, Xval, yval, Xtest, ytest in your environment

%load ('ex5data1.mat');
X = csvread('x_features.txt');
y = csvread('y_time.txt');
Xval = csvread('xval_features.txt');
yval = csvread('yval_time.txt');
Xtest = csvread('xtest_features.txt');
ytest = csvread('ytest_time.txt');

% m = Number of examples
m = size(X, 1);

% Plot training data
%plot(X, y, 'rx', 'MarkerSize', 10, 'LineWidth', 1.5);
%xlabel('Change in water level (x)');
%ylabel('Water flowing out of the dam (y)');

fprintf('Program paused. Press enter to continue.\n');
pause;

%% =========== normalize features ================
%normalize
[X_nor, X_mu, X_sigma] = featureNormalizeZeroMean(X);  
[Xval_nor, Xval_mu, Xval_sigma] = featureNormalizeZeroMean(Xval);  
[Xtest_nor, Xtest_mu, Xtest_sigma] = featureNormalizeZeroMean(Xtest);

%% =========== Part 8: Validation for Selecting Lambda =============
%  You will now implement validationCurve to test various values of 
%  lambda on a validation set. You will then use this to select the
%  "best" lambda value.
%

[lambda_vec, error_train, error_val] = ...
    validationCurve(X_nor, y, Xval_nor, yval);

figure(1);
plot(lambda_vec, error_train, lambda_vec, error_val);
legend('Train', 'Cross Validation');
xlabel('lambda');
ylabel('Error');
%axis([0 10 0 0.05])
fprintf('lambda\t\tTrain Error\tValidation Error\n');
min_error_val = Inf;
min_lambda = 0;
for i = 1:length(lambda_vec)
	fprintf(' %f\t%f\t%f\n', ...
            lambda_vec(i), error_train(i), error_val(i));
    if min_error_val > error_val(i)
        min_lambda = lambda_vec(i);
    end
end

fprintf('Validation for Selecting Lambda finished.\n');
fprintf('Program paused. Press enter to continue.\n');
pause;

%% =========== Part 5: Learning Curve for Linear Regression =============
%  Next, you should implement the learningCurve function. 
%
%  Write Up Note: Since the model is underfitting the data, we expect to
%                 see a graph with "high bias" -- slide 8 in ML-advice.pdf 
%
lambda = min_lambda;



[theta] = trainLinearReg(X_nor, y, lambda);

%[theta] = trainLinearReg(X_poly, y, lambda);
[error_train, error_val] = ...
    learningCurve([ones(m, 1) X_nor], y, ...
                  [ones(size(Xval_nor, 1), 1) Xval_nor], yval, ...
                  lambda);
figure(2);
plot(1:m, error_train, 1:m, error_val);
title('Learning curve for linear regression')
legend('Train', 'Cross Validation')
xlabel('Number of training examples')
ylabel('Error')
%axis([0 m 0 150])

fprintf('# Training Examples\tTrain Error\tCross Validation Error\n');
for i = 1:m
    fprintf('  \t%d\t\t%f\t%f\n', i, error_train(i), error_val(i));
end
fprintf('Learning Curve finished.\n');
%fprintf('Program paused. Press enter to continue.\n');
%pause;
