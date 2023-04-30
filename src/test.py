from langchain.document_loaders import DataFrameLoader
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
import os
import pandas as pd
import json

os.environ["OPENAI_API_KEY"] = "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"

def CVStoVectorStoreIndex(path):
  df = pd.read_csv(path)
  csv_args = {"delimiter": ",",
            "quotechar": '"'}
  loader = CSVLoader(file_path=path,csv_args=csv_args)
    
#   loader = DataFrameLoader(df,page_content_column=df.columns[0])

  index_creator = VectorstoreIndexCreator()
  docsearch = index_creator.from_loaders([loader])
  return docsearch

def GetGeneratedQuestions(vector): 
    chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=vector.vectorstore.as_retriever(), input_key="question")
    query = f"""You are top performing
                 {role} working in an analytics department for a {customer} 
                    within a {industry} company. You are analyzing {data_type}, 
                        please generate 10 Top Questions to use to solve for:
                        {user_question}
                        IN THIS EXACT FORMAT = PYTHON ARRAY
                        [Question1,Question2,Question3,Question4,Question5]
                                """
    response = chain({"question":query})
    return response

def RunAgent(): 
    chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=vector.vectorstore.as_retriever(), input_key="question")
    query = f"""You are top performing
                 {role} working in an analytics department for a {customer} 
                    within a {industry} company. You are analyzing {data_type}, 
                        please generate 10 Top Questions to use to solve for:
                        {user_question}
                        IN THIS EXACT FORMAT = PYTHON ARRAY
                        [Question1,Question2,Question3,Question4,Question5]
                                """
    response = chain({"question":query})
    return response

    
def main():


    # Load JSON data from the neighboring directory
    with open("/Users/samsavage/AnalystAI/data/metricevaluation.json", "r") as file:
        roles_data = json.load(file)
        role = list(roles_data.keys())[1]

    # Get the role-specific data based on the selected role
    role_data = roles_data["💼 Financial Analyst"]
    print(role_data)

    # Get the variables from the role-specific data
    problem_statement = role_data["📉 Variance Analysis"]
    metrics = ", ".join(role_data["💰 Profitability Analysis"])
    bestpractices = ",".join(role_data["Best Practices"])
    reminder = ",".join(role_data["Reminder"])

    vector = CVStoVectorStoreIndex('/Users/samsavage/AnalystAI/data/KAG_conversion_data.csv')

    respsone = GetGeneratedQuestions(vector)

    print(respsone['result'])

main()
# import chardet

# def detect_encoding(file_path):
#     with open(file_path, 'rb') as f:
#         result = chardet.detect(f.read())
#     return result['encoding']

# file_path = '/Users/samsavage/AnalystAI/data/full_data_grailed.csv'
# encoding = detect_encoding(file_path)
# print(f'The encoding of the CSV file is: {encoding}')


# As a 
#             {role}  you are brainstorming how to solve the
            
#              {problem_statement} states by your boss.

#             which may involve solving {metrics} 

#             KEEP in MIND these {bestpractices} 

#             AND reminder that you are {reminder}

#               OUPUT:
            
#             Please output 5 QUESTIONS to help you solve
    
#             ALWAYS RETURN A PYTHON OBJECT LIKE THIS:
#             "LIST": ["Question 1", "Question 2", "Question 3", "Question 4", "Question 5"]

#             YOUR RESPONSE:
