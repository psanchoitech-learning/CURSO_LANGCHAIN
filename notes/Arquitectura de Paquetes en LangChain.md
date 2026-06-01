# Lectura: Arquitectura de Paquetes en LangChain

En esta lección nos detendremos a comprender la arquitectura general de LangChain y su ecosistema al día de hoy.

Esto nos dará un mapa mental de cómo encajan las piezas: modelos, cadenas, agentes, memoria, herramientas, y también cómo LangGraph expande las capacidades de LangChain. Aunque no escribamos mucho código nuevo aquí, este conocimiento conceptual será muy útil cuando abordemos proyectos más complejos en secciones posteriores.

## Arquitectura de Paquetes LangChain

Antes de entrar en los componentes específicos, es importante entender cómo se organiza LangChain. El ecosistema se ha modularizado significativamente para mejorar la mantenibilidad, reducir dependencias y permitir instalaciones más ligeras:

### Estructura modular:

    ┌─────────────────────────────────────────────────────────┐
    │                    Aplicación de Usuario                │
    └─────────────────────────┬───────────────────────────────┘
                              │
    ┌─────────────────────────┴───────────────────────────────┐
    │                      langchain                          │
    │  (Chains, Agents, Memory, Callbacks de alto nivel)      │
    └─────────────────────────┬───────────────────────────────┘
                              │
            ┌─────────────────┼────────────────┐
            │                 │                │
    ┌───────┴──────┐ ┌────────┴──────┐ ┌───────┴────────┐
    │              │ │               │ │                │
    │langchain-core│ │  langchain-   │ │Partner Packages│
    │              │ │  community    │ │                │
    │ Abstracciones│ │ Integraciones │ │ - openai       │
    │ Interfaces   │ │ de terceros   │ │ - anthropic    │
    │ LCEL         │ │               │ │ - ollama       │
    │              │ │               │ │ - groq         │
    └──────────────┘ └───────────────┘ └────────────────┘


Los cuatro niveles principales:

- **`langchain-core`**: Contiene las abstracciones fundamentales e interfaces base. Aquí están las clases abstractas como **`BaseLanguageModel`**, **`BasePromptTemplate`**, **`Runnable`**, y el corazón del **`LCEL (LangChain Expression Language)`**. Es la base sobre la que se construye todo lo demás.

- **`langchain-community`**: Integraciones con servicios y herramientas de terceros que no tienen soporte oficial optimizado. Incluye conectores para bases de datos vectoriales de código abierto, loaders de documentos, herramientas diversas, etc.

- **`Partner Packages`**: Paquetes separados mantenidos oficialmente para integraciones específicas con proveedores principales (**`langchain-openai`**, **`langchain-anthropic`**, **`langchain-ollama`**, etc.). Estos están optimizados y tienen mejor soporte que las integraciones genéricas.

### Ventajas de esta arquitectura:

- **Instalaciones ligeras**: Solo instalas lo que necesitas. Si solo usas OpenAI, instalas **`langchain-core`** y **`langchain-openai`**.

- **Mejor mantenimiento**: Cada integración puede evolucionar independientemente.

- **Menos conflictos de dependencias**: Las integraciones específicas no afectan al core.

- **Actualizaciones más rápidas**: Los partner packages se pueden actualizar sin esperar releases del paquete principal.

## Implicaciones prácticas:

En la actualidad, cuando veas ejemplos de código, notarás imports como:

```python

from langchain_core.prompts import ChatPromptTemplate       # Abstracciones base
from langchain_classic.chains import ConversationChain      # Funcionalidad de alto nivel
from langchain_openai import ChatOpenAI                     # Integración específica
from langchain_community.vectorstores import FAISS          # Herramienta de terceros
```

Esta estructura te ayuda a entender qué está pasando bajo el capó y te permite hacer instalaciones más selectivas según tus necesidades.
