import streamlit as st
import pandas as pd

# Título de la página
st.title("Clasificación General")

# Subir archivo CSV
uploaded_file = st.file_uploader("Sube el archivo Classification.csv", type="csv")

if uploaded_file:
    # Leer archivo CSV
    df = pd.read_csv(uploaded_file)
    
    # Mostrar todos los datos
    #st.write("Datos completos:")
    #st.dataframe(df)
    if 'Squad' in df.columns:
        df = df[df['Squad'].notna()]  # Eliminar filas con None en la columna 'Squad'
    
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
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
else:
    st.info("Por favor, sube un archivo CSV para continuar.")
