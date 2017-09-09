import math
import numpy as np


# **Important things in this file:**
# - np.exp(x) works for any np.array x and applies the exponential function to every coordinate
# - the sigmoid function and its gradient
# - image2vector is commonly used in deep learning
# - np.reshape is widely used. In the future, you'll see that keeping your matrix/vector dimensions
#       straight will go toward eliminating a lot of bugs.
# - numpy has efficient built-in functions
# - broadcasting is extremely useful


def basic_sigmoid(x):
    """
    Compute sigmoid of x.

    Arguments:
    x -- A scalar

    Return:
    s -- sigmoid(x)
    """
    s = 1.0 / (1.0 + math.exp(-x))
    return s


def sigmoid(x):
    """
    Compute the sigmoid of x

    Arguments:
    x -- A scalar or numpy array of any size

    Return:
    s -- sigmoid(x)
    """

    s = 1.0 / (1.0 + np.exp(-x))

    return s

"""
The function sigmoid_derivative() computes the gradient of the sigmoid function with respect to its input x.
The formula is: $$sigmoid\_derivative(x) = \sigma'(x) = \sigma(x) (1 - \sigma(x))\tag{2}$$
>>> sigmoid_derivative([1,2,3])
[0.19661193  0.10499359  0.04517666]
"""


def sigmoid_derivative(x):
    """
    Compute the gradient (also called the slope or derivative) of the sigmoid function with respect to its input x.
    You can store the output of the sigmoid function into variables and then use it to calculate the gradient.

    Arguments:
    x -- A scalar or numpy array

    Return:
    ds -- Your computed gradient.
    """
    s = sigmoid(x)
    ds = s * (1 - s)
    return ds


def image2vector(image):
    """
    Takes an input of shape (length, height, depth) and returns a vector of shape (length * height * depth, 1).
    Argument:
    image -- a numpy array of shape (length, height, depth)

    Returns:
    v -- a vector of shape (length*height*depth, 1)
    """
    v = image.reshape((image.shape[0] * image.shape[1] * image.shape[2], 1))
    return v


def normalizeRows(x):
    """
    Function that normalizes each row of the matrix x (to have unit length, meaning length 1).

    Argument:
    x -- A numpy matrix of shape (n, m)

    Returns:
    x -- The normalized (by row) numpy matrix. You are allowed to modify x.
    """

    # Compute x_norm as the norm 2 of x. Use np.linalg.norm(..., ord = 2, axis = ..., keepdims = True)
    x_norm = np.linalg.norm(x, ord = 2, axis = 1, keepdims = True)

    # Divide x by its norm.
    x = x / x_norm
    return x


def softmax(x):
    """Calculates the softmax for each row of the input x.

    Your code should work for a row vector and also for matrices of shape (n, m).

    Argument:
    x -- A numpy matrix of shape (n,m)

    Returns:
    s -- A numpy matrix equal to the softmax of x, of shape (n,m)
    """
    # Apply exp() element-wise to x. Use np.exp(...).
    x_exp = np.exp(x)

    # Create a vector x_sum that sums each row of x_exp. Use np.sum(..., axis = 1, keepdims = True).
    x_sum = np.sum(x_exp, axis = 1, keepdims = True)

    # Compute softmax(x) by dividing x_exp by x_sum. It should automatically use numpy broadcasting.
    s = x_exp / x_sum

    return s


"""
The L1 loss function.
>>> yhat = np.array([.9, 0.2, 0.1, .4, .9])
>>> y = np.array([1, 0, 0, 1, 1])
>>> str(L1(yhat,y))
1.1
"""


def L1(yhat, y):
    """
    Arguments:
    yhat -- vector of size m (predicted labels)
    y -- vector of size m (true labels)

    Returns:
    loss -- the value of the L1 loss function defined above
    """
    loss = np.sum(np.abs(y - yhat), axis = 0)
    return loss

"""
The L2 loss function.
>>> yhat = np.array([.9, 0.2, 0.1, .4, .9])
>>> y = np.array([1, 0, 0, 1, 1])
>>> str(L2(yhat,y))
0.43
"""


def L2(yhat, y):
    """
    Arguments:
    yhat -- vector of size m (predicted labels)
    y -- vector of size m (true labels)

    Returns:
    loss -- the value of the L2 loss function defined above
    """
    e = y - yhat
    loss = np.dot(e,e)

    return loss
