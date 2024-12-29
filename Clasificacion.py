import streamlit as st
import pandas as pd

# URLs de los archivos en GitHub
classification_url = "https://raw.githubusercontent.com/tu-usuario/tu-repositorio/main/Classification.csv"  # Reemplaza con la URL correcta
schedule_url = "https://raw.githubusercontent.com/tu-usuario/tu-repositorio/main/Schedule.csv"  # Reemplaza con la URL correcta

# Título de la página
st.title("Información de Clasificación y Calendario")

# Crear pestañas
tab1, tab2 = st.tabs(["Clasificación", "Schedule"])

# Pestaña Clasificación
with tab1:
    st.header("Clasificación General")
    
    try:
        # Cargar datos de clasificación
        df_classification = pd.read_csv("Classification.csv")
        
        # Limpiar datos de clasificación
        if 'Squad' in df_classification.columns:
            df_classification = df_classification[df_classification['Squad'].notna()]  # Eliminar filas con None en 'Squad'
        df_classification = df_classification.loc[:, ~df_classification.columns.str.contains('^Unnamed')]  # Eliminar columnas 'Unnamed'
        
        # Mostrar datos limpios
        #st.write("Datos completos (limpios):")
        #st.dataframe(df_classification)
        
        # Filtrar por liga
        if 'Competition' in df_classification.columns:
            ligas = df_classification['Competition'].unique()
            liga_seleccionada = st.selectbox("Selecciona una liga para filtrar:", ["Todas"] + list(ligas))
            
            # Filtrar datos si se selecciona una liga específica
            if liga_seleccionada != "Todas":
                df_filtrado = df_classification[df_classification['Competition'] == liga_seleccionada]
            else:
                df_filtrado = df_classification
            
            # Mostrar datos filtrados
            st.write(f"Clasificación para: {liga_seleccionada}")
            st.dataframe(df_filtrado)
        else:
            st.error("El archivo de clasificación no contiene la columna 'Competition'.")
    except Exception as e:
        st.error(f"Error al cargar el archivo de clasificación: {e}")

# Pestaña Schedule
with tab2:
    st.header("Calendario de Equipos")
    
    try:
        # Cargar datos del calendario
        df_schedule = pd.read_csv("Scheduler.csv")
        
        # Limpiar datos del calendario
        df_schedule = df_schedule.loc[:, ~df_schedule.columns.str.contains('^Unnamed')]  # Eliminar columnas 'Unnamed'
        
        # Mostrar datos del calendario
        st.write("Calendario completo:")
        st.dataframe(df_schedule)
        
        # Filtrar por equipo
        if 'Team' in df_schedule.columns:
            equipos = df_schedule['Team'].unique()
            equipo_seleccionado = st.selectbox("Selecciona un equipo para filtrar:", ["Todos"] + list(equipos))
            
            # Filtrar datos si se selecciona un equipo específico
            if equipo_seleccionado != "Todos":
                df_schedule_filtrado = df_schedule[df_schedule['Team'] == equipo_seleccionado]
            else:
                df_schedule_filtrado = df_schedule
            
            # Mostrar datos filtrados
            st.write(f"Calendario para: {equipo_seleccionado}")
            st.dataframe(df_schedule_filtrado)
        else:
            st.error("El archivo de calendario no contiene la columna 'Team'.")
    except Exception as e:
        st.error(f"Error al cargar el archivo de calendario: {e}")

