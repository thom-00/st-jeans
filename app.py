import streamlit as st
import posts
# 게시물 데이터를 저장하는 리스트


# 게시물 추가 폼
st.title("JEANS 커뮤니티")
post_title = st.text_input("게시물 제목")
post_content = st.text_area("게시물 내용")

posts = posts.posts

if st.button("게시물 추가"):
    if post_title and post_content:
        post = {"제목": post_title, "내용": post_content}
        posts.append(post)
        st.success("게시물이 추가되었습니다.")
    else:
        st.warning("게시물 제목과 내용을 모두 입력하세요.")

search_query = st.text_input("게시물 검색")




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
    with st.expander(f"{start_idx + i + 1}. {post['제목']}"):
        st.write(post['내용'])
