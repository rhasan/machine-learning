function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%


% C_vec = [0.01 0.03 0.1 0.3 1 3 10 30]';
% sigma_vec = [0.01 0.03 0.1 0.3 1 3 10 30]';
% 
% min_error = Inf;
% for i = 1:length(C_vec)
%     C_try = C_vec(i);
%     for j = 1:length(sigma_vec)
%         sigma_try = sigma_vec(j);
%         % Train the SVM
%         %model= svmTrain(X, y, C_try, @(x1, x2) gaussianKernel(x1, x2, sigma_try));
%         
%         options = sprintf('-c %1.3f -g %1.3f',C_try,sigma_try);
%         
%         model = svmtrain(y, X, options);
%         
%         %predictions = svmPredict(model, Xval);
%         [predictions] = svmpredict(yval, Xval, model);
%         error = mean(double(predictions ~= yval));
%         if min_error>error
%             min_error = error;
%             C = C_try;
%             sigma = sigma_try;
%         end
%         fprintf('C=%f sigma=%f error=%f\n',C_try,sigma_try,error);
%     end
% end
% fprintf('C=%f sigma=%f\n',C,sigma);
C = 3;
sigma = 30;

% =========================================================================

end
