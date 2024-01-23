# Semantic Search in the LSF ontology
## Generate Embeddings for the Data


#In this tutorial, we use the [Neural Network Language Model (NNLM)](https://tfhub.dev/google/nnlm-en-dim128/2) to generate embeddings for the headline data. The sentence embeddings can then be easily used to compute sentence level meaning similarity. We run the embedding generation process using Apache Beam.
### Embedding extraction method
import pandas as pd
import tensorflow_hub as hub
import annoy
from sentence_transformers import SentenceTransformer

# import retrieveLSFOntology

# LSF_exisiting_names, LSF_Labels,LFIDs,categories=retrieveLSFOntology.generate_lfid_categories_labels('../../../GitHub/LSF-Ontology/ontology/LSF-Ontology-V2.obo')


def generate_embeddings2(text, model_url='https://tfhub.dev/google/nnlm-en-dim128/2'):
    """
     Receives list of words or phrases and generates embeddings for them
     Input:
         text: list of words or phrases
         model_url (optional): url for neural network hub model
     Output:
         text, embedding
    """
    # Beam will run this function in different processes that need to
    # import hub and load embed_fn (if not previously loaded)
    embed_fn = None
    #model_url = 'https://tfhub.dev/google/nnlm-en-dim128/2' #@param {type:"string"}
    #global embed_fn
    if embed_fn is None:
        embed_fn = hub.load(model_url)
        embeddings = embed_fn(text).numpy()
    return embeddings



# embed_fn=None
# model_url='https://tfhub.dev/google/nnlm-en-dim128/2'
# annoy_index=None


annoy_index=None
embed_fn=None
sentence_transformer='all-mpnet-base-v2'
embedding_model = SentenceTransformer(sentence_transformer)


# if embed_fn is None:
#     print('loaded')
    
def generate_embeddings(text):
    """
     Receives list of words or phrases and generates embeddings for them
     Input:
         text: list of words or phrases
         model_url (optional): url for neural network hub model
     Output:
         text, embedding
    """
    # Beam will run this function in different processes that need to
    # import hub and load embed_fn (if not previously loaded)
    global embed_fn
    if embed_fn is None:
        embed_fn = hub.load(model_url)
        print('loaded')
    
    embeddings = embed_fn(text).numpy()
    return embeddings

# embeddings=generate_embeddings(LSF_exisiting_names,model_url)

# embeddings[1].shape

# len(embeddings[1][0])
## Build the ANN Index for the Embeddings




   
def generate_embeddingsـcustom(text,sentence_transformer='all-mpnet-base-v2'):
    """
     Receives list of words or phrases and generates embeddings for them
     Input:
         text: list of words or phrases
         sentence_transformer (optional): name of the sentence transformer
     Output:
         embedding
    """
    global embedding_model
    # model = SentenceTransformer(sentence_transformer)
    # embeddings=model.encode(text)
    embeddings=embedding_model.encode(text)


    return embeddings


#model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')





def build_annoy_index(LSF_names, vector_length=128,metric='angular', num_trees=100):
    """Receives LSF_names which are extracted from existing LSF ontology and creates an Annoy index using the embeddings generated from these names

        [ANNOY](https://github.com/spotify/annoy) (Approximate Nearest Neighbors Oh Yeah) is a C++ library with Python bindings to search for points in space that are close to a given query point.
        It also creates large read-only file-based data structures that are mapped into memory. 
        It is built and used by [Spotify](https://www.spotify.com) for music recommendations. 

        * angular distance or the Euclidean distance,
        * In case of angular distance, results will be smaller than 2

        * annoy's "angular" distance is really just the euclidean distance of normalized vectors i.e. (u / |u| - v / |v|)^2
        * If we divide by the norm of the vector, the euclidean and angular distance will be identical

    Args:
        LSF_names (list): exisiting LSF names
        vector_length (int, optional): embedding size. Defaults to 128.
        metric (str, optional): _description_. Defaults to 'angular'.
        num_trees (int, optional): _description_. Defaults to 100.

    Returns:
        Annoy Index: _description_
    """
    # global annoy_index
    # if annoy_index is not None:  # already exist
    #     return annoy_index
    
    # otherwise build it
    #embeddings=generate_embeddings(LSF_names) 
    embeddings=generate_embeddingsـcustom(LSF_names)
    vector_length=embeddings.shape[1] # get embedding dimension
    annoy_index = annoy.AnnoyIndex(vector_length, metric=metric)
  

    



    for item_counter,embedding in enumerate(embeddings):
        annoy_index.add_item(item_counter, embedding)

    print('Building the index with {} trees...'.format(num_trees))
    annoy_index.build(n_trees=num_trees)
    print('Index is successfully built.')
    

    # print('Saving index to disk...')
    # annoy_index.save(index_filename)
    # print('Index is saved to disk.')
    # print("Index file size: {} GB".format(
    # round(os.path.getsize(index_filename) / float(1024 ** 3), 2)))
    #annoy_index.unload()
    return annoy_index




def find_neighbor_ids(index,query_name, num_matches=1,distance_treshold=1.0):
    """similar to others but returns only indices of neighburs

    Args:
        index (_type_): _description_
        LSF_exisiting_names (_type_): _description_
        query_name (_type_): _description_
        num_matches (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """
    embeddings=generate_embeddingsـcustom([query_name])   

    ids = index.get_nns_by_vector(embeddings[0], num_matches, search_k=-1, include_distances=True)
    #print(ids)
    #items = [LSF_exisiting_names[i] for i in ids[0]]
    # return similar LSF names and distances  
    distance_treshold
    ids = [ids[0][i] for i,distance in enumerate(ids[1]) if distance< distance_treshold]

    return ids




def find_neighbors(index,LSF_exisiting_names,query_name, num_matches=1):
    """Using the Annoy index to find LSF names that are semantically close to an input query.
    Args:
        index (_type_): _description_
        LSF_exisiting_names (list): to convert the indices of matches to actual names
        num_matches (int, optional): number of nearest neighburs to be returned. Defaults to 5.
        query_name(str): canidate LSF name to be searched for similar names within the index
    Returns:
        _type_: _description_
    """
    embeddings=generate_embeddingsـcustom([query_name])   

    ids = index.get_nns_by_vector(embeddings[0], num_matches, search_k=-1, include_distances=True)
    #print(ids)
    items = [LSF_exisiting_names[i] for i in ids[0]]
    # return similar LSF names and distances  
    return items,ids[1]



def find_neighbors_by_embedding(index,LSF_exisiting_names,embedding, num_matches=1):
    """Using the Annoy index to find LSF names that are semantically close to an embedding
    Args:
        index (_type_): _description_
        LSF_exisiting_names (list): to convert the indices of matches to actual names
        num_matches (int, optional): number of nearest neighburs to be returned. Defaults to 5.
        query_name(str): canidate LSF name to be searched for similar names within the index
    Returns:
        _type_: _description_
    """
    #embeddings=generate_embeddings([query_name])   

    ids = index.get_nns_by_vector(embedding, num_matches, search_k=-1, include_distances=True)
    #print(ids)
    items = [LSF_exisiting_names[i] for i in ids[0]]
    # return similar LSF names and distances  
    return items,ids[1]




def find_neighbors_independent(LSF_exisiting_names,query_name, num_matches=1,rebuild_index=False):
    """Using the Annoy index to find LSF names that are semantically close to an input query.
        Note: This version build the index and there is no need to send the index
    Args:
        index (_type_): _description_
        LSF_exisiting_names (list): to convert the indices of matches to actual names
        num_matches (int, optional): number of nearest neighburs to be returned. Defaults to 5.
        query_name(str): canidate LSF name to be searched for similar names within the index
    Returns:
        _type_: _description_
    """
    global annoy_index
    if annoy_index is None  or rebuild_index==True:    
        annoy_index=build_annoy_index(LSF_exisiting_names)
    
    embeddings=generate_embeddings([query_name])   

    ids = annoy_index.get_nns_by_vector(embeddings[0], num_matches, search_k=-1, include_distances=True)
    #print(ids)
    items = [LSF_exisiting_names[i] for i in ids[0]]
    # return similar LSF names and distances  
    return items,ids[1]




def find_neighbors_by_name_only(query_name, num_matches=1,rebuild_index=False):
    
    """Using the Annoy index to find LSF names that are semantically close to an input query.
        Note: This version build the index and there is no need to send the index
    Args:
        index (_type_): _description_
        LSF_exisiting_names (list): to convert the indices of matches to actual names
        num_matches (int, optional): number of nearest neighburs to be returned. Defaults to 5.
        query_name(str): canidate LSF name to be searched for similar names within the index
    Returns:
        _type_: _description_
    """
    global annoy_index
    if annoy_index is None  or rebuild_index==True:  
        annoy_index=build_annoy_index(LSF_exisiting_names)
        print('Index Built')  
    
    embeddings=generate_embeddings([query_name])   

    ids = annoy_index.get_nns_by_vector(embeddings[0], num_matches, search_k=-1, include_distances=True)
    #print(ids)
    items = [LSF_exisiting_names[i] for i in ids[0]]
    # return similar LSF names and distances  
    return items,ids[1]


def suggest_label(index,query,LSF_exisiting_names,dict_name2Label):
    """Receives the query name and the previously built Annoy Index to find neareste neighbur and the label of the neighbur 

    Args:
        query (str): a candidate name to be searched for
        index (Annoy Index): Previously created annoy index using only training samples
        trainlist (list): list of training names used to create the index, this is required since the index doesn't store the names but onnlt the idicies of them
        dict_name2label (dict): A dict which maps LSF names to the corresponig sub-category index

    Returns:
        tuple: nearest neighbur,distance to the query name, label of the nearest neighbur
    """
    similar_names,distances=find_neighbors(index,LSF_exisiting_names,query)
    neighbur_label=dict_name2Label[similar_names[0]]
    return similar_names[0],distances[0],neighbur_label

 