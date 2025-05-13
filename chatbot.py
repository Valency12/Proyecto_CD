import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar la API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("No se encontró la API key de Google. Por favor, asegúrate de tener un archivo .env con GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

# Cargar los datos
try:
    df = pd.read_csv('students.csv')
except FileNotFoundError:
    raise FileNotFoundError("No se encontró el archivo students.csv")

# Configurar el modelo
try:
    modelo_gemini = genai.GenerativeModel('models/gemini-1.5-pro')
except Exception as e:
    print(f"Error al inicializar el modelo: {str(e)}")
    print("\nModelos disponibles:")
    for m in genai.list_models():
        print(m.name)
    raise

def get_context():
    """Genera un contexto con estadísticas básicas del dataset"""
    total_students = len(df)
    graduates = len(df[df['target'] == 'Graduate'])
    dropouts = len(df[df['target'] == 'Dropout'])
    enrolled = len(df[df['target'] == 'Enrolled'])
    
    context = f"""
    Base de datos de estudiantes universitarios con {total_students} registros.
    Estadísticas generales:
    - Graduados: {graduates} ({graduates/total_students*100:.1f}%)
    - Abandonos: {dropouts} ({dropouts/total_students*100:.1f}%)
    - En curso: {enrolled} ({enrolled/total_students*100:.1f}%)
    
    Columnas disponibles:
    {', '.join(df.columns)}
    """
    return context

def chat_with_gemini(user_input):
    pregunta = user_input.lower()
    # Preguntas simples con pandas
    if "edad promedio" in pregunta:
        avg_age = df['Age at enrollment'].mean()
        return f"La edad promedio de los estudiantes al matricularse es {avg_age:.2f} años."
    if "beca" in pregunta:
        becados = df[df['Scholarship holder'] == 1]
        return f"Hay {len(becados)} estudiantes con beca."
    if ("total" in pregunta or "hay" in pregunta) and "estudiantes" in pregunta:
        return f"Hay {len(df)} estudiantes en total."
    if "graduad" in pregunta:
        graduados = df[df['target'] == 'Graduate']
        return f"Hay {len(graduados)} estudiantes graduados."
    if "abandon" in pregunta or "desert" in pregunta:
        abandonos = df[df['target'] == 'Dropout']
        return f"Hay {len(abandonos)} estudiantes que abandonaron."
    if "inscrito" in pregunta or "en curso" in pregunta:
        inscritos = df[df['target'] == 'Enrolled']
        return f"Hay {len(inscritos)} estudiantes actualmente inscritos."
    if "porcentaje" in pregunta and "graduad" in pregunta:
        porcentaje = len(df[df['target'] == 'Graduate']) / len(df) * 100
        return f"El porcentaje de estudiantes graduados es {porcentaje:.2f}%."
    if "porcentaje" in pregunta and ("abandon" in pregunta or "desert" in pregunta):
        porcentaje = len(df[df['target'] == 'Dropout']) / len(df) * 100
        return f"El porcentaje de estudiantes que abandonaron es {porcentaje:.2f}%."
    if "calificacion de admision promedio" in pregunta or "nota de admision promedio" in pregunta:
        promedio = df['Admission grade'].mean()
        return f"La calificación de admisión promedio es {promedio:.2f}."
    if "genero" in pregunta or "hombres" in pregunta or "mujeres" in pregunta:
        hombres = len(df[df['Gender'] == 1])
        mujeres = len(df[df['Gender'] == 0])
        return f"Hay {hombres} hombres y {mujeres} mujeres en la base de datos."
    if "necesidades educativas especiales" in pregunta:
        especiales = len(df[df['Educational special needs'] == 1])
        return f"Hay {especiales} estudiantes con necesidades educativas especiales."
    if "internacional" in pregunta:
        internacionales = len(df[df['International'] == 1])
        return f"Hay {internacionales} estudiantes internacionales."
    if "curso con mas estudiantes" in pregunta:
        curso = df['Course'].value_counts().idxmax()
        cantidad = df['Course'].value_counts().max()
        return f"El curso con más estudiantes es el código {curso} con {cantidad} estudiantes."
    if "nacionalidad mas comun" in pregunta:
        nacionalidad = df['Nacionality'].value_counts().idxmax()
        cantidad = df['Nacionality'].value_counts().max()
        return f"La nacionalidad más común es el código {nacionalidad} con {cantidad} estudiantes."
    if "deuda" in pregunta or "deudor" in pregunta:
        deudores = len(df[df['Debtor'] == 1])
        return f"Hay {deudores} estudiantes con deudas pendientes."
    if "calificacion promedio primer semestre" in pregunta:
        promedio = df['Curricular units 1st sem (grade)'].mean()
        return f"La calificación promedio en la primera unidad curricular es {promedio:.2f}."
    if "padre" in pregunta and ("universidad" in pregunta or "universitarios" in pregunta):
        padres_uni = len(df[(df["Father's qualification"] == 19) | (df["Mother's qualification"] == 19)])
        return f"Hay {padres_uni} estudiantes con al menos un padre con estudios universitarios."
    if "diurno" in pregunta or "vespertino" in pregunta or "asisten en horario" in pregunta:
        diurno = len(df[df['Daytime/evening attendance'] == 1])
        vespertino = len(df[df['Daytime/evening attendance'] == 0])
        return f"Hay {diurno} estudiantes en horario diurno y {vespertino} en horario vespertino."
    if "edad minima" in pregunta:
        edad_min = df['Age at enrollment'].min()
        return f"La edad mínima de los estudiantes es {edad_min} años."
    if "edad maxima" in pregunta:
        edad_max = df['Age at enrollment'].max()
        return f"La edad máxima de los estudiantes es {edad_max} años."
    if "creditos primer semestre" in pregunta:
        creditos = df['Curricular units 1st sem (credited)'].sum()
        return f"Se han otorgado {creditos} créditos en el primer semestre en total."
    
    # Si no es una pregunta directa, usar el modelo de IA
    try:
        prompt = f"""
        Basado en los siguientes datos de estudiantes:
        {df.to_string()}
        
        Responde a esta pregunta: {user_input}
        
        Por favor, proporciona una respuesta clara y concisa.
        """
        
        response = modelo_gemini.generate_content(prompt)
        return response.text
    except Exception as e:
        # Manejo específico para error de cuota excedida
        if hasattr(e, 'status_code') and e.status_code == 429:
            return "Has alcanzado el límite de uso gratuito del modelo Gemini. Por favor, espera un tiempo o revisa tu cuota en Google Cloud."
        if '429' in str(e) or 'quota' in str(e).lower():
            return "Has alcanzado el límite de uso gratuito del modelo Gemini. Por favor, espera un tiempo o revisa tu cuota en Google Cloud."
        return f"Lo siento, ocurrió un error al procesar tu pregunta: {str(e)}"

def main():
    print("¡Bienvenido al Chatbot de Análisis de Estudiantes!")
    print("Puedes hacer preguntas sobre los datos de estudiantes universitarios.")
    print("Escribe 'salir' para terminar la conversación.")
    
    while True:
        user_input = input("\nTú: ")
        if user_input.lower() == 'salir':
            print("¡Hasta luego!")
            break
            
        try:
            response = chat_with_gemini(user_input)
            print("\nChatbot:", response)
        except Exception as e:
            print("\nError:", str(e))

if __name__ == "__main__":
    main() 