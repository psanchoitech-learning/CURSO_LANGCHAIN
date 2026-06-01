from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# =================================================================================================================
# DEPRECATED
# ==================================================================================================================
# from langchain.chains import LLMChain


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def print_tree(obj, label: str = "root", max_str_len: int = 80) -> None:
    """Imprime recursivamente un objeto en formato árbol hacia stdout."""

    def _to_dict(node):
        if hasattr(node, "__dict__"):
            return {k: _to_dict(v) for k, v in vars(node).items()}
        if isinstance(node, dict):
            return {k: _to_dict(v) for k, v in node.items()}
        if isinstance(node, list):
            return [_to_dict(i) for i in node]
        return node

    def _is_leaf(value) -> bool:
        return not isinstance(value, (dict, list)) or (
            isinstance(value, list)
            and all(not isinstance(i, (dict, list)) for i in value)
        )

    def _fmt_value(value) -> str:
        if isinstance(value, str) and len(value) > max_str_len:
            return repr(value[: max_str_len - 3] + "...")
        return str(value)

    def _walk(node, prefix: str) -> None:
        if isinstance(node, dict):
            entries = list(node.items())
            for i, (key, value) in enumerate(entries):
                is_last = i == len(entries) - 1
                connector = "└── " if is_last else "├── "
                child_prefix = prefix + ("    " if is_last else "│   ")
                if _is_leaf(value):
                    print(f"{prefix}{connector}{key}: {_fmt_value(value)}")
                else:
                    print(f"{prefix}{connector}{key}:")
                    _walk(value, child_prefix)

        elif isinstance(node, list):
            for i, item in enumerate(node):
                is_last = i == len(node) - 1
                connector = "└── " if is_last else "├── "
                child_prefix = prefix + ("    " if is_last else "│   ")
                if _is_leaf(item):
                    print(f"{prefix}{connector}[{i}]: {_fmt_value(item)}")
                else:
                    print(f"{prefix}{connector}[{i}]:")
                    _walk(item, child_prefix)

    print(label)
    _walk(_to_dict(obj), prefix="")

# ---------------------------------------------------------------------------
# Cuerpo del programa
# ---------------------------------------------------------------------------    

chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario por su nombre.\nNombre del usuario: {nombre}\nAsistente:"
)

# =================================================================================================================
# OLD STYLE (DEPRECATED)
# ==================================================================================================================
# chain = LLMChain(
#     llm=chat,
#     prompt=plantilla
# )
# 
# resultado = chain.run(nombre="Pablo")
# print(resultado)

# =================================================================================================================
# NEW STYLE: LCEL (LangChain Expression Language)
# En el código nuevo con LCEL, no hay ningún objeto chain de un paquete específico — 
# es simplemente el resultado del operador | encadenando n objetos
# ==================================================================================================================
# Cadena LCEL: prompt | llm | parser
chain = plantilla | chat 

resultado = chain.invoke({"nombre": "Pablo"})
print_tree(resultado, "resultado")
print(resultado.content)