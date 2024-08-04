import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import jinja2
import json
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback


app = Flask(__name__)

load_dotenv() 
KEY=os.getenv("OPENAI_API_KEY")

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/chatbot",methods=["POST"])
def chatbot():
    product = request.form["catagory"]
    company = request.form["company"]
    channel = request.form["channel"]
    userInput = request.form["comments"]   
#    chatbot_response = f"Catagory:{product}, Company:{company}, Channel:{channel}, Comments:{userInput}"
    chatbot_response = callmodel(product,company,channel,userInput)
    return render_template('chatbot.html',user_input=userInput,chatbot_response=chatbot_response)


def callmodel(product,company,channel,userInput):

    TEMPLATE = """
    You are an expert in product advertising campaign creator for {product} products.
    Please help me create an advertising campaign for {product} from {company} for {channel} given the below text.
    Text={userInput}
    """
    campaign_generation_prompt = PromptTemplate(
    input_variables=["product","company","channel","userInput"],
    template=TEMPLATE
    )
    llm=ChatOpenAI(openai_api_key=KEY,model_name="gpt-3.5-turbo", temperature=0.5)
    quiz_chain=LLMChain(llm=llm, prompt=campaign_generation_prompt, output_key="response", verbose=True)
    llmOutput = quiz_chain.invoke({"product":product,"company":company,"channel":channel,"userInput":userInput})
    return llmOutput['response']
    
    

if __name__ == '__main__':
    app.run(debug=True)