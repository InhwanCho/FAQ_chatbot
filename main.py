from streamlit_extras.stoggle import stoggle
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


def init():
    # API_KEY를 '.env'파일에서 받아오기
    load_dotenv()

    # 페이지 세팅
    st.set_page_config(
        page_title="FAQ Chatbot",
        page_icon="🦈"
    )


def faq():
    
    ''' FAQ는 GPT3.5-turbo를 아래의 지시문을 사용하여 얻었습니다.
        --- INSTRUCTION ---
        로그인 FAQ 예시를 JSON포맷으로 작성해줘.
        넘버, 질문, 답변이 있어야되며 답변을 3문장으로 넘버 6까지 작성해줘
        답변의 경우 문단 사이를 {<br>}로 표시하고 넘버링으로 순차적으로 알려줘
        --- RESULT EXAMPLE ---
        {"FAQ": [
                {
                "number": 1,
                "question": "비밀번호를 5회 이상 틀렸어요",
                "answer": "1. aaa<br>2. bbb<br>3. ccc", ...  }'''
    # 테스트용으로 {"number": 7}은 추가 작성
    examples = {
    "FAQ": [
        {
            "number": 1,
            "question": "비밀번호를 5회 이상 틀렸어요",
            "answer": "1. 패스워드를 재설정해주세요.<br>2. 계정 잠금이 될 수 있으니 주의해주세요.<br>3. 이메일을 통해 임시 비밀번호를 발급받으실 수 있습니다."
        },
        {
            "number": 2,
            "question": "아이디를 잊어버렸어요",
            "answer": "1. 아이디 복구를 위해 이메일 주소로 문의해주세요.<br>2. 본인 인증 절차를 거친 후 아이디를 찾을 수 있습니다.<br>3. 등록한 전화번호로 아이디를 찾을 수도 있습니다."
        },
        {
            "number": 3,
            "question": "이메일 인증 메일이 오지 않았어요",
            "answer": "1. 스팸 메일함을 확인해주세요.<br>2. 이메일 주소를 정확히 입력했는지 확인해주세요.<br>3. 일정 시간이 지나도록 메일이 오지 않는 경우, 고객센터에 문의해주세요."
        },
        {
            "number": 4,
            "question": "계정 활성화를 어떻게 하나요",
            "answer": "1. 회원가입 시 받은 이메일에서 활성화 링크를 클릭해주세요.<br>2. 계정 활성화를 위해 SMS 인증을 완료해주세요.<br>3. 계정 정보 수정 페이지에서 계정 활성화를 진행할 수 있습니다."
        },
        {
            "number": 5,
            "question": "계정 정보를 어떻게 수정하나요",
            "answer": "1. 로그인 후 계정 정보 메뉴에서 수정할 수 있습니다.<br>2. 비밀번호, 이메일 주소 등을 변경할 수 있습니다.<br>3. 고객센터를 통해 계정 정보 수정을 도와드릴 수 있습니다."
        },
        {
            "number": 6,
            "question": "로그인이 되지 않아요",
            "answer": "1. 인터넷 연결 상태를 확인해주세요.<br>2. ID와 패스워드를 정확히 입력했는지 확인해주세요.<br>3. 로그인 시도 횟수를 확인하고 일시적인 장애일 수도 있으니 잠시 후에 시도해주세요."
        },
        {
            "number": 7,
            "question": "아이디에 등록된 이메일이 생각나지 않아요",
            "answer": "1. 로그인 화면에서 '비밀번호 찾기' 링크를 클릭합니다.<br>2. 등록한 아이디를 입력하고 '확인' 버튼을 클릭합니다.<br>3. 등록된 이메일 주소로 안내 메일이 발송되며, 해당 이메일을 확인하세요."
        },
    ]}
    # 아이디가 생각나지 않아요, 아이디 복구를 위한 이메일 주소도 생각나지 않아요, 위의 질문에 대한 답변들을 합쳐서 제공해주세요.




    return examples

        

def main():
    init()


    st.header('FAQs about login')
    st.info('👻 사용 방법  👻 : \n1. 아래 "질문하기"에 질문을 입력하세요.\n2. FAQ에 대해 질문 하려면 "FAQ 질문"을 눌러주세요.\n3. 질문을 구글링하려면 "구글링 하기"를 눌러주세요.')

    # FAQ 데이터
    ex_faq = faq()
    for i in ex_faq['FAQ']:
        stoggle(f"Q{i['number']} : {i['question']}",i['answer'])

    # Chatbot 모델 선택
    chat = ChatOpenAI(temperature=0.1,max_tokens=512,model='gpt-4')

    # 메시지 세션 활성화(초기화) 및 챗봇의 역할 부여
    text = f"""당신은 {ex_faq}에 답변해주는 챗봇입니다. 질문에 대해서 {ex_faq}만 참고하여 답변해주세요. 답변 할 수 없는 질문이면 확인 할 수 없다고 말해주세요."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=text)
        ]
        st.session_state.users = []

    # 챗봇 질문할 경우 활성화
    # 질문 입력 후 FAQ질문 or 구글링 버튼 생성
    # 버튼의 위치 UI를 위한 레이아웃 변경
    with st.form('chat_input_form', clear_on_submit=True):
        col1, col2, col3 = st.columns([7,1,1.2]) 
        instr = 'Hi there! Enter what you want to let me know here.'
        with col1 :
            user_input = st.text_input('질문하기 : ', '',placeholder=instr, key='user_input')
        with col2 :
            submitted = st.form_submit_button('FAQ질문')
        with col3 :
            serpapi = st.form_submit_button('구글링 하기')
        

    # FAQ에 대해 질문하기
    if submitted and user_input:
        # 유저 질문
        st.session_state.messages.append(HumanMessage(content=user_input))
        st.session_state.users.append('user')

        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        
        # AI답변
        st.session_state.messages.append(AIMessage(content=response.content))
        st.session_state.users.append('chatbot')

    # serpapi를 활용하기 위한 포맷 작성
    if user_input and serpapi :
        llm = OpenAI(temperature=0.1,max_tokens=512)
        tool_names = ["serpapi"]
        tools = load_tools(tool_names)
        agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
        # 유저 질문
        st.session_state.messages.append(HumanMessage(content=''))
        st.session_state.users.append('serpapi_user:'+user_input)

        with st.spinner("Thinking..."):
            # serpapi 답변
            # response = 'Windows 10을 사용하면 시작 버튼을 누른 다음 설정을 입력하여 설정 > 네트워크 및 인터넷을 선택하면 네트워크 연결 상태가 상단에 표시됩니다.'
            response = agent.run(user_input)
            st.session_state.messages.append(HumanMessage(content=''))

            st.session_state.users.append('serpapi_chatbot:'+response)
            
                



    messages = st.session_state.get('messages', [])
    users = st.session_state.users

    # 챗봇의 메시지 출력 포맷을 설정
    for i, (user, msg) in enumerate(zip(users,messages[1:])):
        if user == 'skip':
            continue
        elif user == 'user' :
            message(msg.content, is_user=True, key=str(i)+'_user')
        elif user == 'chatbot':
            message(msg.content, is_user=False, key=str(i)+'_ai')
        elif user.startswith('serpapi_user'):
            message('google : ' + user[13:], is_user = True, key=str(i)+'_user')
        elif user.startswith('serpapi_chatbot'):
            message('google : ' + user[16:], is_user=False, key=str(i)+'_ai')
    


if __name__ == '__main__':
    main()
    
