import faiss
import numpy
import numpy as np

if __name__ == '__main__':
    nlist = 16
    k = 5
    dimension = 512
    quantizer = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
    features_folder = "features/features.npy"
    image_features = np.load(features_folder).astype('float32')
    index.train(image_features)
    index.add(image_features)
    faiss.write_index(index, "image_index")