import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="Gemini Chatbot",
    layout="centered"
)

# Gemini API 설정
# Note: API 키는 Streamlit Cloud Secrets Manager를 통해 등록해야 합니다.
# .streamlit/secrets.toml 파일에 다음과 같이 설정:
# [gcp]
# gemini_api_key = "your-api-key-here"
genai.configure(api_key=st.secrets["gcp"]["gemini_api_key"])

# Gemini 모델 설정
model = genai.GenerativeModel('gemini-1.5-flash')

# 제목
st.title("Gemini Chatbot")

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 채팅 입력
user_input = st.chat_input("메시지를 입력하세요...")

# 사용자 입력이 있을 경우 처리
if user_input:
    try:
        # 사용자 메시지를 채팅 히스토리에 추가
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Gemini에 전송할 메시지 구성
        messages = []
        for message in st.session_state.chat_history:
            messages.append({"role": message["role"], "parts": [message["content"]]})
        
        # Gemini API 호출
        response = model.generate_content(messages)
        
        # Gemini 응답을 채팅 히스토리에 추가
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")

# 채팅 히스토리 표시
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])
