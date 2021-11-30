import numpy as np
class NN():
    self __init__(self):
        pass

    def sigmoid(z):
        return 1/(1+np.exp(-z))

    def forward_propagation(Ws, Bs, X):
        a = X
        activations = [a]
        for i in range(len(Ws)):
            z = np.dot(Ws[i].T, a) + Bs[i].T
            a = np.array([sigmoid(zi) for zi in z])
            activations += [a]
        return activations
