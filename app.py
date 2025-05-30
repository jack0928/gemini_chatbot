import streamlit as st
import google.generativeai as genai

# Gemini API 키 로드
genai.configure(api_key=st.secrets["gcp"]["gemini_api_key"])

# 모델 초기화
model = genai.GenerativeModel("gemini-1.5-flash")

# 페이지 설정
st.set_page_config(page_title="Gemini 챗봇", page_icon="🌠")

# 세션 상태 초기화
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# 제목과 설명
st.title("🌠 Gemini 챗봇")
st.markdown("당신의 질문을 Gemini에게 물어보세요!")

# 이전 대화 내용 표시
for role, message in st.session_state.chat_log:
    if role == "🙋 사용자":
        st.markdown(f"**{role}**: {message}")
    else:
        st.markdown(f"**{role}**: {message}")
    st.markdown("---")

# 대화 입력 폼
with st.form("chat_form"):
    user_input = st.text_input("✍️ 질문을 입력해 주세요", placeholder="예: 오늘의 운세는?")
    submitted = st.form_submit_button("질문하기")

# 폼 제출 처리
if submitted:
    if not user_input.strip():
        st.warning("❗ 질문을 입력해 주세요.")
    else:
        try:
            response = model.generate_content(user_input)
            if not response.text.strip():
                st.warning("⚠️ 응답이 비어 있어요. 다시 시도해 주세요.")
            else:
                st.session_state.chat_log.append(("🙋 사용자", user_input))
                st.session_state.chat_log.append(("🤖 Gemini", response.text))
        except Exception as e:
            st.error(f"🚫 오류 발생: {e}")

# 안내 문구
st.markdown("""\n---\n🔐 *이 서비스는 Gemini-1.5-Flash를 사용하며, 재미와 정보 제공을 위한 용도입니다.*\n""")
