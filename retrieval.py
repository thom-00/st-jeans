from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from posts import get_posts_with_id_and_title, get_posts_contents

scoreDict = {}
embedder = SentenceTransformer('Huffon/sentence-klue-roberta-base')
top_k = 10

index_postsTitle = None
index_postsContents = None

def encodeToINDEX(corpusList):
    embeddings_withID = []
    embeddings_ID = []
    contents_embbedings = []
    for idx, corpus in enumerate(corpusList):
        embeddings_ID.append(posts_withID_ID[idx])
        contents_embbedings.append(embedder.encode(corpus, convert_to_tensor=False))

    encoded_data = np.array(contents_embbedings)
    lecIDArray = np.array(embeddings_ID).astype('int64')
    index = faiss.IndexIDMap(faiss.IndexFlatIP(encoded_data.shape[1]))
    index.add_with_ids(encoded_data, lecIDArray)
    return index

def initialize_indexes():
    global index_postsTitle, index_postsContents
    posts_withID_ID, posts_title = get_posts_with_id_and_title()
    posts_contents = get_posts_contents()
    index_postsTitle = encodeToINDEX(posts_title)
    index_postsContents = encodeToINDEX(posts_contents)

def findFaiss(query, way, reward):
    if way == 'title':
        index = index_postsTitle
    else:
        index = index_postsContents
    query_vector = embedder.encode([query])
    ds, ids = index.search(query_vector, top_k)
    ids = [x for x in ids.tolist()[0]]
    for i, posts_id in enumerate(ids):
        if posts_id in scoreDict:
            scoreDict[posts_id] += reward / ds[0][i]
        else:
            scoreDict[posts_id] = reward / ds[0][i]

def findExactly(query, targetList, reward):
    for idx, target in enumerate(targetList):
        if query in target:
            if idx != target.index(query):
                raise Exception('타겟 인덱스 != idx')
            if idx in scoreDict:
                scoreDict[idx] += reward
            else:
                scoreDict[idx] = reward
