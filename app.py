%%writefile app.py
import streamlit as st
import posts
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# 게시물 데이터를 저장하는 리스트
scoreDict = {}
embedder = SentenceTransformer('Huffon/sentence-klue-roberta-base')
top_k = 10

posts_withID = []

posts = posts.posts

def encodeToINDEX(corpusList):
  global embedder
  embeddings_ID = []
  corpus_embbedings = []
  for idx, corpus in enumerate(corpusList):
    embeddings_ID.append(posts[idx]['postID'])
    corpus_embbedings.append(embedder.encode(corpus, convert_to_tensor=False))

  encoded_data = np.array(corpus_embbedings)
  lecIDArray = np.array(embeddings_ID).astype('int64')
  index = faiss.IndexIDMap(faiss.IndexFlatIP(encoded_data.shape[1]))
  index.add_with_ids(encoded_data, lecIDArray)
  return index

def findFaiss(query, way, reward):
  global scoreDict
  if way =='title': index = index_postsTitle
  else: index = index_postsContents
  query_vector = embedder.encode([query])
  ds, ids = index.search(query_vector, top_k)
  ids = [x for x in ids.tolist()[0]]
  for i, posts_id in enumerate(ids):
    if posts_id in scoreDict: scoreDict[posts_id] += reward/ds[0][i]
    else: scoreDict[posts_id] = reward/ds[0][i]

def findExactly(query, targetList, reward):
  for idx, target in enumerate(targetList):
    if query in target:
      if idx != target.index(query): 
        raise Exception('타겟 인덱스 != idx')
      if idx in scoreDict: scoreDict[idx] += reward
      else: scoreDict[idx] = reward


index_postsTitle = encodeToINDEX([_['title'] for _ in posts])
index_postsContents = encodeToINDEX([_['contents'] for _ in posts])

#st 시작
st.title("JEANS 커뮤니티")
post_title = st.text_input("게시물 제목")
post_content = st.text_area("게시물 내용")


if st.button("게시물 추가"):
    if post_title and post_content:
        post = {"제목": post_title, "내용": post_content}
        posts.append({'postID':len(post), 'title':post_title, 'contents':post_content})
        index_postsTitle = encodeToINDEX([_['title'] for _ in posts])
        index_postsContents = encodeToINDEX([_['contents'] for _ in posts])
        st.success("게시물이 추가되었습니다.")
        
    else:
        st.warning("게시물 제목과 내용을 모두 입력하세요.")

search_query = st.text_input("게시물 검색")

if search_query: 
  scoreDict = {}
  findFaiss(query=search_query, reward=100, way='title')
  for i in range(3):
      with st.expander(f"{posts[list(scoreDict)[i]]['title']}"):
          st.write(posts[list(scoreDict)[i]]['contents'])

else:
    # 페이지 당 게시물 수
    posts_per_page = 10

    # 페이지 수 계산
    num_pages = len(posts) // posts_per_page + (len(posts) % posts_per_page > 0)


    # 현재 페이지 번호
    selected_page = st.session_state.get("selected_page", 1)

    # '다음' 버튼 클릭 시 페이지 이동


    col1, col2, col3 = st.columns(3)

    with col1:
      if st.button("이전"):
          if selected_page > 1:
              selected_page -= 1
        
    with col2:
      pass
        
    with col3:
      if st.button("다음"):
          if selected_page < num_pages:
              selected_page += 1

    # '이전' 버튼 클릭 시 페이지 이동


    # 현재 페이지 번호 저장
    st.session_state.selected_page = selected_page

    # 현재 페이지에 해당하는 게시물 목록 표시
    st.subheader("게시물 목록")
    start_idx = (selected_page - 1) * posts_per_page
    end_idx = start_idx + posts_per_page
    for i, post in enumerate(posts[start_idx:end_idx]):
        with st.expander(f"{start_idx + i + 1}. {posts[i]['title']}"):
            st.write(posts[i]['contents'])
            