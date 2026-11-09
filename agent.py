import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from forecast_logic import ejecutar_forecast_pipeline

@tool
def consultar_forecast(query: str) -> str:
    """Útil para obtener los datos de la demanda estimada, promedios o totales del modelo de forecast de 12 meses."""
    df = ejecutar_forecast_pipeline(12)
    soma_demanda = df["Demanda_Estimada"].sum()
    promedio_mensual = df["Demanda_Estimada"].mean()
    
    resumen = (
        f"Resultados del modelo de forecast:\n"
        f"- Demanda total acumulada (12 meses): {soma_demanda:,.0f} unidades.\n"
        f"- Promedio mensual estimado: {promedio_mensual:,.2f} unidades.\n"
        f"Detalle por mes:\n{df.to_pandas().to_string(index=False)}"
    )
    return resumen

# Lista y diccionario de herramientas disponibles
tools = [consultar_forecast]
tools_dict = {tool.name: tool for tool in tools}

def ejecutar_agente_forecast(mensajes_historial):
    """
    Ejecuta el modelo con soporte de herramientas utilizando LCEL puro,
    recibiendo el historial de Streamlit y devolviendo la respuesta final del agente.
    """
    # Inicializa el modelo (asegúrate de tener tu OPENAI_API_KEY configurada en tus variables de entorno)
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    llm_with_tools = llm.bind_tools(tools)
    
    # Mensaje de sistema para guiar el comportamiento del analista
    system_prompt = (
        "Eres un asistente analítico experto en forecasting y análisis de demanda. "
        "Utiliza la herramienta 'consultar_forecast' siempre que necesites acceder a los datos numéricos, "
        "totales o tendencias para responder con absoluta precisión a las consultas del usuario."
    )
    
    # Mapear el historial de Streamlit a objetos de mensaje de LangChain
    chat_messages = [AIMessage(content=system_prompt)] # Opcional: inyectar instrucción inicial
    for msg in mensajes_historial:
        if msg["role"] == "user":
            chat_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            chat_messages.append(AIMessage(content=msg["content"]))
            
    # Primera llamada al modelo con las herramientas vinculadas
    response = llm_with_tools.invoke(chat_messages)
    
    # Si el modelo decide invocar una o varias herramientas
    if response.tool_calls:
        chat_messages.append(response)
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_to_call = tools_dict.get(tool_name)
            
            if tool_to_call:
                # Ejecutar la función de la herramienta y adjuntar el resultado como ToolMessage
                tool_output = tool_to_call.invoke(tool_args)
                chat_messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"]))
                
        # Segunda llamada al modelo con el resultado de la herramienta para que formule la respuesta final al usuario
        final_response = llm_with_tools.invoke(chat_messages)
        return final_response.content
    else:
        # Si no requirió herramientas, devuelve la respuesta directa
        return response.content