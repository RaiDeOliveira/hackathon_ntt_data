from dotenv import load_dotenv
import google.generativeai as genai
import os

from src.models.repository.chat_repository import ChatRepository

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave API do Gemini não foi encontrada nas variáveis de ambiente.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

class ChatService():
  def __init__(self) -> None:
    self.__path_csv = "data/audit.csv"
    self.__history_repository = ChatRepository(self.__path_csv)
  
  def context_generate(self) -> str:
    dataset = self.__history_repository.load().to_string(index=False)
    
    if not dataset:
      raise Exception("Dataset not found")
    
    context = f"""
    Este é um sistema que coleta e classifica a qualidade do trabalho em escritórios.
    Aqui estão alguns dados coletados:
    {dataset}
    """
    
    return context
    
  def generate_response(self, message: str) -> str:
    context = self.context_generate()
    context += f"\n\nUsuário: {message}\n"
    print(context)
    
    response = model.generate_content(context)
    
    output = ""
    for chunk in response:
      output += chunk.text
      output += "\n"
      
    return output