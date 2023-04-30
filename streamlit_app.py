import ast
from langchain.llms import OpenAI
import pandas as pd
import os
import json
from langchain.agents import create_csv_agent
from pydantic import BaseModel, Field
from langchain.llms import OpenAI
import streamlit as st
from streamlit import session_state
import pandas as pd
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import DataFrameLoader
from langchain.chains import RetrievalQA
from langchain.chat_models.openai import ChatOpenAI
import emoji
import chromadb
import ast

import regex as re
from tempfile import NamedTemporaryFile


def apply_custom_css():
    st.markdown(
        """
        <style>
            .hacker-text {
                background-color: black;
                color: lime;
                font-family: 'Courier New', monospace;
                padding: 10px;
                border-radius: 5px;
                white-space: pre-wrap;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
def apply_custom_css2():
    st.markdown(
        """
        <style>
            .slack-container {
                display: flex;
                flex-direction: column;
                gap: 10px;
                padding: 10px;
                background-color: #f8f8f8;
                font-family: 'Lato', sans-serif;
                border-radius: 5px;
            }
            .slack-question {
                font-weight: bold;
                color: #2c2d30;
            }
            .slack-answer {
                background-color: #e4f0f5;
                color: #2c2d30;
                padding: 10px;
                border-radius: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def file_selector(folder_path="."):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox("Select a file", filenames)
    return os.path.join(folder_path, selected_filename)


def CVStoVectorStoreIndex(path):
    csv_args = {"delimiter": ",", "quotechar": '"'}
    loader = CSVLoader(file_path=path, csv_args=csv_args)
    #   loader = DataFrameLoader(df,page_content_column=df.columns[0])
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])
    return docsearch


def GetGeneratedQuestions(
    vector, role, user_question, industry, customer_role, data_type
):
    chain = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=vector.vectorstore.as_retriever(),
        input_key="question",
    )
    query = f"""You are top performing
                 {role} working in an analytics department for a {customer_role} 
                    within a {industry} company. You are analyzing {data_type}, 
                        please generate 10 Top Questions to use to solve for:
                        {user_question}
    
            ALWAYS RETURN A PYTHON ARRAY LIKE THIS:
            
            ["Question 1", "Question 2", "Question 3", "Question 4", "Question 5"]

            YOUR RESPONSE:

            """
    response = chain({"question": query})
    return response


def main():
    # Set page configuration
    st.set_page_config(
        page_title="AI Intern🚀",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Header
    st.title("InternAI🚀")

    css = """
    <style>
        [data-testid="stSidebar"]{
            min-width: 200;
            max-width: 800px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Initialize session state if not already initialized
    if not session_state.get("init"):
        session_state.init = True
        session_state.role = "📊 Data Analyst"
        session_state.assignment_type = "🔍 Exploratory Data Analysis"

    role = st.sidebar.selectbox(
        "Your Role",
        [   "🎯 Marketing Analyst",
            "⚙️ Operations Analyst",
            "💰 Sales Analyst",
            "💼 Financial Analyst",
            "📊 Data Analyst",
            "📈 Business Analyst"
        ],
        on_change=session_state.clear,
    )

    with open("data/assignmenttypes.json", "r") as file:
        # Load the JSON content into a Python dictionary
        assignment_types = json.load(file)

    # Load JSON data from the neighboring directory
    with open("/Users/samsavage/AnalystAI/data/metricevaluation.json", "r") as file:
        instruction_data = json.load(file)

    # Update session state if role changes
    if role != session_state.role:
        session_state.role = role
        session_state.assignment_type = assignment_types[role][0]

    industry = st.sidebar.selectbox(
        "Industry",
        [
            "🏦 Banking & Finance",
            "🏥 Healthcare",
            "💻 Technology",
            "🛍️ Retail",
            "🏭 Manufacturing",
            "📚 Education",
            "🚀 Aerospace & Defense",
            "🔋 Energy",
            "🛢️ Oil & Gas",
            "🧪 Pharmaceuticals",
            "🌾 Agriculture",
            "🏨 Hospitality",
            "🚢 Shipping & Logistics",
            "🏡 Real Estate",
            "📺 Media & Entertainment",
            "🔌 Utilities",
            "🚧 Construction",
            "📡 Telecommunications",
            "🚗 Automotive",
            "🍽️ Food & Beverage",
            "👔 Fashion & Apparel",
            "🌐 E-commerce",
            "👩‍🔬 Research & Development",
        ],
        key="industry",
    )

    customer_role = st.sidebar.selectbox(
        "Your Customer",
        [   "📈 Data Analytics Manager",
            "🔬 Research Manager",
            "🖥️ IT Manager",
            "🔒 Security Manager",
            "🛠️ Maintenance Manager",
            "📦 Supply Chain Manager",
            "👨‍🔬 Quality Manager",
            "🚆 Transportation Manager",
            "🎯 Marketing Manager",
            "💰 Sales Manager",
            "👩‍💼 CEO",
            "📈 CFO",
            "🔒 CISO",
            "💻 CIO",
            "📊 CDO",
            "🔧 COO",
            "🌐 CTO",
            "📢 CMO",
            "👨‍🔬 CRO",
            "👩‍⚖️ Legal Counsel",
            "💼 Controller",
            "👥 HR Manager"
        ],
    )

    assignment_type = st.sidebar.selectbox(
        "Type of Assignment",
        assignment_types[role] + ["🔧 Ad-hoc Analysis", "❓ Other"],
        index=assignment_types[role].index(session_state.assignment_type),
        on_change=session_state.clear,
    )

    # Update session state if assignment type changes
    if assignment_type != session_state.assignment_type:
        session_state.assignment_type = assignment_type

    api_key = st.sidebar.text_input("Enter your GPT API key", type="password")

    model_version = st.selectbox("Choose the Model Version", ["gpt-3.5-turbo","Davincci"])


    temperature = st.sidebar.slider("Choose the style you want the AI to write in: 0 is most rational, 1 is least", 0.0, 1.0, step=0.1)
    
    os.environ["OPENAI_API_KEY"] = api_key.lstrip("\"").rstrip("\"")



    st.subheader(
        f" Automating your {session_state.assignment_type} work for your {customer_role}"
    )
    col1, col2 = st.columns(2)

    st.markdown(
        "<h4 style='font-weight: bold;'>In a few sentences, describe in detail what you want to accomplish with this analysis</h4>",
        unsafe_allow_html=True,
    )
    problem_statement = st.text_area("", key="problem_statement")

    instructions = instruction_data[role]
    # Get the variables from the role-specific data
    user_question = problem_statement

    with col1:
        uploaded_file = st.sidebar.file_uploader("Upload Excel or CSV", type=["csv"])

    if uploaded_file is not None:
        if st.button("Click to Analyze Your Data!"):
            with NamedTemporaryFile(dir=".", suffix=".csv") as f:
                f.write(uploaded_file.getbuffer())
                docsearch = CVStoVectorStoreIndex(f.name)

                response = GetGeneratedQuestions(
                    docsearch,
                    role=role,
                    user_question=user_question,
                    customer_role=customer_role,
                    industry=industry,
                    data_type=assignment_type,
                )

                list_from_string = ast.literal_eval(response["result"])

                st.subheader("Question and Answers have been generated by InternAI🚀")

                agent = create_csv_agent(OpenAI(temperature=temperature), f.name)

                gpt4_agent  = create_csv_agent(OpenAI(temperature=temperature, model_name='gpt-3.5-turbo'),f.name)
                
                if api_key:

                    if model_version == "gpt-3.5-turbo":
                        # apply_custom_css()
                        apply_custom_css2()
                        try:
                            for i, k in enumerate(list_from_string):
                                st.markdown(f"<div class='slack-container'><div class='slack-question'>Question {i}: {k}</div><div class='slack-answer'>{gpt4_agent.run(k)}</div></div>", unsafe_allow_html=True)
                        except TypeError as e:
                            print(e)
                    else:
                        apply_custom_css2()
                        try:
                            for i, k in enumerate(list_from_string):
                                st.markdown(f"<div class='slack-container'><div class='slack-question'>Question {i}: {k}</div><div class='slack-answer'>{agent.run(k)}</div></div>", unsafe_allow_html=True)
                        except TypeError as e:
                            print(e)

                        

                # with open("user_output.txt", 'a') as output_file:
                #     for i, (question, answer) in enumerate(zip(list_from_string, answers)):
                #         output_file.write(f"Question {i}: {question}\n")
                #         output_file.write(f"Answer {i}: {answer}\n\n")

                # st.markdown(output_file, "user_output.txt", unsafe_allow_html=True)

    # col1, col2, col3 = st.columns(3)

    # # Add a button to the first column for generating a docx report
    # with col1:
    #     st.button("Generate DOCX")

    # # Add a button to the second column for generating a PowerPoint pptx
    # with col2:
    #     st.button("Generate PPTX")

    # # Add a button to the third column for generating an Excel/CSV file
    # with col3:
    #     st.button("Generate CSV")


main()
