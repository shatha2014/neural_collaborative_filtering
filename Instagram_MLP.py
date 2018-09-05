'''
Implementation taken from
He Xiangnan et al. Neural Collaborative Filtering. In WWW 2017.
@author: Xiangnan He (xiangnanhe@gmail.com)

Adapted to our Instagram dataset
by Shatha Jaradat
KTH - Royal Institute of Technology
'''

import numpy as np

import theano
import theano.tensor as T
import keras
from keras import backend as K
from keras import initializations
from keras.regularizers import l2, activity_l2
from keras.models import Sequential, Graph, Model
from keras.layers.core import Dense, Lambda, Activation
from keras.layers import Embedding, Input, Dense, merge, Reshape, Merge, Flatten, Dropout
from keras.constraints import maxnorm
from keras.optimizers import Adagrad, Adam, SGD, RMSprop
from evaluate import evaluate_model
from InstagramDataset import InstagramDataset
from time import time
import sys
import argparse
import multiprocessing as mp

#################### Arguments ####################
def parse_args():
    parser = argparse.ArgumentParser(description="Run MLP.")
    parser.add_argument('--path', nargs='?', default='InstagramData/',
                        help='Input data path.')
    parser.add_argument('--dataset', nargs='?', default='outfits',
                        help='Choose a dataset.')
    parser.add_argument('--epochs', type=int, default=100,
                        help='Number of epochs.')
    parser.add_argument('--batch_size', type=int, default=256,
                        help='Batch size.')
    parser.add_argument('--layers', nargs='?', default='[243,81,27,9]',
                        help="Size of each layer. Note that the first layer is the concatenation of subcategory and and material pattern embeddings. So layers[0]/3 is the embedding size.")
    parser.add_argument('--reg_layers', nargs='?', default='[0,0,0,0]',
                        help="Regularization for each layer")
    parser.add_argument('--num_neg', type=int, default=4,
                        help='Number of negative instances to pair with a positive instance.')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='Learning rate.')
    parser.add_argument('--learner', nargs='?', default='adam',
                        help='Specify an optimizer: adagrad, adam, rmsprop, sgd')
    parser.add_argument('--verbose', type=int, default=1,
                        help='Show performance per X iterations')
    parser.add_argument('--out', type=int, default=1,
                        help='Whether to save the trained model.')
    return parser.parse_args()

def init_normal(shape, name=None):
    return initializations.normal(shape, scale=0.01, name=name)

def get_model(num_users, num_subcategories, num_patterns, num_materials, layers = [20,10], reg_layers=[0,0]):
    assert len(layers) == len(reg_layers)
    num_layer = len(layers) #Number of layers in the MLP
    # Input variables
    subcategory_input = Input(shape=(1,), dtype='int32', name = 'subcategory_input')
    material_input = Input(shape=(1,), dtype='int32', name = 'material_input')
    pattern_input = Input(shape=(1,), dtype='int32', name = 'pattern_input')

    MLP_Embedding_Subcategory = Embedding(input_dim = num_subcategories, output_dim = layers[0]/3, name = 'subcategory_embedding',
                                  init = init_normal, W_regularizer = l2(reg_layers[0]), input_length=1)
    MLP_Embedding_Material = Embedding(input_dim = num_patterns, output_dim = layers[0]/3, name = 'material_embedding',
                                  init = init_normal, W_regularizer = l2(reg_layers[0]), input_length=1)
    MLP_Embedding_Pattern = Embedding(input_dim = num_materials, output_dim = layers[0]/3, name = 'pattern_embedding',
                                  init = init_normal, W_regularizer = l2(reg_layers[0]), input_length=1)


    # Crucial to flatten an embedding vector!
    subcategory_latent = Flatten()(MLP_Embedding_Subcategory(subcategory_input))
    material_latent = Flatten()(MLP_Embedding_Material(material_input))
    pattern_latent = Flatten()(MLP_Embedding_Pattern(pattern_input))


    # The 0-th layer is the concatenation of embedding layers
    vector = merge([subcategory_latent, material_latent, pattern_latent], mode = 'concat')

    # MLP layers
    for idx in xrange(1, num_layer):
        layer = Dense(layers[idx], W_regularizer= l2(reg_layers[idx]), activation='relu', name = 'layer%d' %idx)
        vector = layer(vector)

    # Final prediction layer
    prediction = Dense(1, activation='sigmoid', init='lecun_uniform', name = 'prediction')(vector)

    model = Model(input=[subcategory_input, material_input, pattern_input],
                  output=prediction)

    return model

def get_train_instances(train, num_negatives):
    subcategory_input, material_input, pattern_input, style_labels = [],[],[],[]
    num_users = train.shape[0]
    for (subcat, mat, pat) in train.keys():
        # positive instance
        subcategory_input.append(subcat)
        material_input.append(mat)
        pattern_input.append(pat)
        style_labels.append(1)
        # negative instances
        #for t in xrange(num_negatives):
        #    j = np.random.randint(num_items)
        #    while train.has_key((u, j)):
        #        j = np.random.randint(num_items)
        #    user_input.append(u)
        #    item_input.append(j)
        #    labels.append(0)
    return user_input, subcategory_input, material_input,pattern_input, style_labels

if __name__ == '__main__':
    args = parse_args()
    path = args.path
    dataset = args.dataset
    layers = eval(args.layers)
    reg_layers = eval(args.reg_layers)
    num_negatives = args.num_neg
    learner = args.learner
    learning_rate = args.lr
    batch_size = args.batch_size
    epochs = args.epochs
    verbose = args.verbose

    topK = 10
    evaluation_threads = 1 #mp.cpu_count()
    print("MLP arguments: %s " %(args))
    model_out_file = 'Pretrain/%s_MLP_%s_%d.h5' %(args.dataset, args.layers, time())

    # Loading data
    t1 = time()
    dataset = InstagramDataset(args.path + args.dataset)
    train, test = dataset.trainData, dataset.testData
    #testNegatives = dataset.testNegatives
    num_subcategories, num_materials, num_patterns = 20,50,50
    print("Load data done [%.1f s]. #user=%d, #subcategory=%d, #material=%d,#oattern=%d, #train=%d, #test=%d"
          %(time()-t1, num_users, num_subcategories, num_materials, num_patterns, len(train), len(test)))

    # Build model
    model = get_model(num_users, num_subcategories, num_materials, num_patterns, layers, reg_layers)
    if learner.lower() == "adagrad":
        model.compile(optimizer=Adagrad(lr=learning_rate), loss='binary_crossentropy')
    elif learner.lower() == "rmsprop":
        model.compile(optimizer=RMSprop(lr=learning_rate), loss='binary_crossentropy')
    elif learner.lower() == "adam":
        model.compile(optimizer=Adam(lr=learning_rate), loss='binary_crossentropy')
    else:
        model.compile(optimizer=SGD(lr=learning_rate), loss='binary_crossentropy')

    # Check Init performance
    t1 = time()
    (hits, ndcgs) = evaluate_model(model, test, test, topK, evaluation_threads)
    hr, ndcg = np.array(hits).mean(), np.array(ndcgs).mean()
    print('Init: HR = %.4f, NDCG = %.4f [%.1f]' %(hr, ndcg, time()-t1))

    # Train model
    best_hr, best_ndcg, best_iter = hr, ndcg, -1
    for epoch in xrange(epochs):
        t1 = time()
        # Generate training instances
        user_input, subcategory_input, material_input, pattern_input, labels = get_train_instances(train, num_negatives)

        # Training
        hist = model.fit([np.array(user_input), np.array(subcategory_input), np.array(material_input), np.array(pattern_input)], #input
                         np.array(labels), # labels
                         batch_size=batch_size, nb_epoch=1, verbose=0, shuffle=True)
        t2 = time()

        # Evaluation
        if epoch %verbose == 0:
            (hits, ndcgs) = evaluate_model(model, testRatings, testNegatives, topK, evaluation_threads)
            hr, ndcg, loss = np.array(hits).mean(), np.array(ndcgs).mean(), hist.history['loss'][0]
            print('Iteration %d [%.1f s]: HR = %.4f, NDCG = %.4f, loss = %.4f [%.1f s]'
                  % (epoch,  t2-t1, hr, ndcg, loss, time()-t2))
            if hr > best_hr:
                best_hr, best_ndcg, best_iter = hr, ndcg, epoch
                if args.out > 0:
                    model.save_weights(model_out_file, overwrite=True)

    print("End. Best Iteration %d:  HR = %.4f, NDCG = %.4f. " %(best_iter, best_hr, best_ndcg))
    if args.out > 0:
        print("The best MLP model is saved to %s" %(model_out_file))
