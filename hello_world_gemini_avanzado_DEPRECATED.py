from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# =================================================================================================================
# DEPRECATED
# Además dará error
# El problema es de compatibilidad: estás usando Python 3.14 (que cambió el comportamiento de Optional/type hints)
# con una versión de pydantic o langchain que aún no lo soporta.
# Se vá a requerir Bajar la versión de Python a 3.11 o 3.12
# Además, LLMChain está deprecado en LangChain moderno.
# ==================================================================================================================
from langchain.chains import LLMChain


chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario por su nombre.\nNombre del usuario: {nombre}\nAsistente:"
)

## OLD STYLE CON LLMChain 
chain = LLMChain(
    llm=chat,
    prompt=plantilla
)

resultado = chain.run(nombre="Pablo")
print(resultado)