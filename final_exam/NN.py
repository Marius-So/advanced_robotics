import numpy as np

class NN():
    def __init__(self, genes, input_neurons, hidden_neurons, output_neurons):
        # TODO: split the genotype to the weights that we need for the NN
        hidden_layers = [hidden_neurons]
        layers = np.array([input_neurons] + hidden_layers + [output_neurons])
        num_layers = len(layers)
        self.Bs = []
        cur_gene = 0

        for i in range(num_layers-1):
            self.Bs.append(genes[cur_gene: cur_gene + layers[i+1]])
            cur_gene =  cur_gene + layers[i+1]

        self.Ws = []
        for i in range(num_layers-1):
            rel_genes = genes[cur_gene: cur_gene + layers[i]*layers[i+1]]
            self.Ws.append(np.reshape(rel_genes, (layers[i], layers[i+1])))
            cur_gene =  cur_gene +  layers[i]*layers[i+1]

    def sigmoid(self, z):
        return 1/(1+np.exp(-z))

    def forward_propagation(self, X):
        a = X
        for i in range(len(self.Ws)):
            z = np.dot(self.Ws[i].T, a) + self.Bs[i].T
            a = np.array([self.sigmoid(zi) for zi in z])
        a[0] = a[0] * 40 - 20
        a[1] = a[1] * 40 - 20
        return a

def get_number_of_genes(input_neurons, hidden_neurons, output_neurons):
    return (input_neurons + 1) * (hidden_neurons) + (hidden_neurons +1) * output_neurons

if __name__ == '__main__':
    inp = np.random.random(100)
    genes = np.random.random(1032)
    my_nn = NN(genes= genes, input_neurons = 100, hidden_neurons = 10, output_neurons = 2)
    # maybe we need to be a bit carefull because of the activation function
    print(my_nn.forward_propagation(inp))

