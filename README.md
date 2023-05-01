# InternAI 🚀 Chatbot

InternAI is a chatbot designed to automate various data analysis tasks. By uploading a CSV or Excel file, users can quickly obtain a summary of the data, generate questions, and get answers to those questions.

## Features

- Automatically analyze data from a CSV or Excel file.
- Generate relevant questions based on user's role, industry, and assignment type.
- Obtain answers to generated questions using OpenAI's GPT-3.5-turbo or Davincci models.
- Customizable temperature setting for AI's writing style.

## Requirements

- Python 3.7+
- streamlit
- pandas
- openai
- ast
- pydantic
- regex
- emoji
- chromadb

## Installation

1. Clone the repository
```
git clone https://github.com/yourusername/InternAI.git
```

2. Change the working directory to the cloned repository
```
cd InternAI
```

3. Install required Python packages
```
pip install -r requirements.txt
```

4. Set your OpenAI API key as an environment variable
```
export OPENAI_API_KEY="your_openai_api_key"
```

5. Run the Streamlit app
```
streamlit run main.py
```

## Usage

1. Open your browser and go to `localhost:8501`.
2. Use the sidebar to select your role, industry, and customer.
3. Choose the assignment type.
4. Enter your OpenAI API key (if not set as an environment variable).
5. Choose the model version (GPT-3.5-turbo or Davincci).
6. Adjust the temperature slider for the AI's writing style.
7. Upload your CSV or Excel file.
8. Press the "Click to Analyze Your Data!" button to generate questions and answers based on your data.

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).
