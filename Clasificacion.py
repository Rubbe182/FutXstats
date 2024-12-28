import streamlit as st
import pandas as pd

# Título de la página
st.title("Clasificación General")

# URL del archivo CSV en GitHub
csv_url = "https://raw.githubusercontent.com/tu-usuario/tu-repositorio/main/Classification.csv"  # Reemplaza con la URL correcta

try:
    # Leer archivo CSV desde la URL
    df = pd.read_csv(csv_url)
    
    # Limpiar datos
    if 'Squad' in df.columns:
        df = df[df['Squad'].notna()]  # Eliminar filas con None en la columna 'Squad'
    
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Eliminar columnas con 'Unnamed' en su nombre
    
    # Mostrar datos limpios
    st.write("Datos completos (limpios):")
    st.dataframe(df)
    
    # Verificar que la columna 'Competition' existe
    if 'Competition' in df.columns:
        # Crear un filtro para seleccionar una liga específica
        ligas = df['Competition'].unique()
        liga_seleccionada = st.selectbox("Selecciona una liga para filtrar:", ["Todas"] + list(ligas))
        
        # Filtrar datos si se selecciona una liga específica
        if liga_seleccionada != "Todas":
            df_filtrado = df[df['Competition'] == liga_seleccionada]
        else:
            df_filtrado = df
        
        # Mostrar datos filtrados
        st.write(f"Clasificación para: {liga_seleccionada}")
        st.dataframe(df_filtrado)
    else:
        st.error("El archivo no contiene la columna 'Competition'.")
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")

