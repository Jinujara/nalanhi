import os
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# from gensim.summarization.summarizer import summarize

load_dotenv()

def create_text(query: str) -> str:
    embeddings_model = OpenAIEmbeddings()

    # load db
    vectorstore = FAISS.load_local('C:/Users/nyj/nalanhi/Projects/db/faiss', embeddings_model,
                                allow_dangerous_deserialization=True)



    # Prompt 템플릿 생성
    template = '''
    "당신은 장애인에 대한 정보를 한국인에게 전달하는 한국인 크리에이터이며, 정보전달 게시물 형식으로 인스타그램 게시물을 생성합니다.
    아래 요구사항에 맞추어 게시글을 출력하며, 그 이외의 다른 답변은 하지 않습니다.

    1) 사용자의 입력에 대하여, "제공받은 context만을 기반으로" 게시글을 생성합니다.\
    2) 게시글의 내용을 분석하여 주요 주제와 관련된 해시태그를 제안해주세요.
    해쉬 태그는 8개 이상 작성되어야 한며 #나란히 # 상생 은 고정적으로 존재합니다.
    (예시: 게시글에서 '장애인식 개선'과 '포용 사회'가 주요 주제로 다뤄진다면, 관련 해시태그로 #장애인식개선, #포용사회 등을 제안할 수 있습니다.\
    최종적으로 #나란히 #상생 #장애인식개선 #포용사회 #청각장애인 #수화 #의사소통 #함께하는세상 과 같이 출력되어야 합니다.)
    3) 마크다운 형식이 아닌 게시글의 형태로 출력하고, 이모지를 사용해서 사람들의 시선을 끌 수 있도록 만듭니다.

    : {context}

    Question: {question}
    '''

    prompt = ChatPromptTemplate.from_template(template)

    # LLM
    model = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0)

    # Rretriever
    retriever = vectorstore.as_retriever()

    def format_docs(docs):
        return '\n\n'.join([d.page_content for d in docs])

    # RAG Chain 연결
    rag_chain = (
        {'context': retriever | format_docs, 'question': RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    # Chain 실행
    return rag_chain.invoke(query)

def create_image(caption: str) -> str:
    client = OpenAI()

    response = client.images.generate(
    model="dall-e-2",
    prompt=caption,
    size="512x512",
    quality="standard",
    n=1,
    )

    return response.data[0].url

def create() -> str:
    query = input('인스타그램 업로드 게시물 주제(질문형식도 ok): ')
    
    posting_text = create_text(query)
    
    # summary= summarize(posting_text)
    posting_image_url= create_image(posting_text)
    
    return posting_text, posting_image_url
