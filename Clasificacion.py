import streamlit as st
import pandas as pd

# Configurar la barra lateral para selección de páginas
st.sidebar.title("Navegación")
page = st.sidebar.radio("Selecciona una página:", ["Clasificación y Calendario", "Bet Stats"])

# Página Clasificación y Calendario
if page == "Clasificación y Calendario":
    st.title("Clasificación y Calendario")
    
    # Crear tabs dentro de la página
    tab1, tab2 = st.tabs(["Clasificación", "Schedule"])
    
    # Tab Clasificación
    with tab1:
        st.header("Clasificación General")
        try:
            # Cargar datos de clasificación
            df_classification = pd.read_csv("Classification.csv")
            
            # Limpiar datos de clasificación
            if 'Squad' in df_classification.columns:
                df_classification = df_classification[df_classification['Squad'].notna()]  # Eliminar filas con None en 'Squad'
            df_classification = df_classification.loc[:, ~df_classification.columns.str.contains('^Unnamed')]  # Eliminar columnas 'Unnamed'
            
            # Filtrar por liga
            if 'Competition' in df_classification.columns:
                ligas = df_classification['Competition'].unique()
                liga_seleccionada = st.selectbox("Selecciona una liga para filtrar:", ["Todas"] + list(ligas), key="liga_select")
                
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
    
    # Tab Schedule
    with tab2:
        st.header("Calendario de Equipos")
        try:
            # Cargar datos del calendario
            df_schedule = pd.read_csv("Scheduler.csv")
            
            # Limpiar datos del calendario
            df_schedule = df_schedule[df_schedule['Home'].notna()]
            df_schedule = df_schedule.loc[:, ~df_schedule.columns.str.contains('^Unnamed')]  # Eliminar columnas 'Unnamed'
            df_schedule = df_schedule[df_schedule['Home'] != "Home"]
            df_schedule = df_schedule.rename(columns={'xG':'xG_h','xG.1':'xG_a'})
            df_schedule = df_schedule[['Wk', 'Day', 'Date', 'Time', 'Home', 'xG_h', 'Score','xG_a', 'Away','Attendance', 
                                       'Venue', 'Referee','Competition','Round']]
            
            # Filtrar por equipo
            if 'Home' in df_schedule.columns and 'Away' in df_schedule.columns:
                # Combinar equipos de las columnas 'Home' y 'Away' para generar una lista única
                equipos = pd.unique(df_schedule[['Home', 'Away']].values.ravel())
                
                # Crear el selectbox con la lista de equipos únicos
                equipo_seleccionado = st.selectbox("Selecciona un equipo para filtrar:", ["Todos"] + list(equipos), key="equipo_select")
                
                # Filtrar datos si se selecciona un equipo específico
                if equipo_seleccionado != "Todos":
                    # Filtrar donde el equipo sea 'Home' o 'Away'
                    df_schedule_filtrado = df_schedule[(df_schedule['Home'] == equipo_seleccionado) | (df_schedule['Away'] == equipo_seleccionado)]
                else:
                    # Mostrar todos los datos si no se selecciona un equipo específico
                    df_schedule_filtrado = df_schedule
                
                # Mostrar datos filtrados
                st.write(f"Calendario para: {equipo_seleccionado}")
                st.dataframe(df_schedule_filtrado)
            else:
                st.error("El archivo de calendario no contiene las columnas 'Home' y 'Away'.")
        except Exception as e:
            st.error(f"Error al cargar el archivo de calendario: {e}")

# Página Datos Adicionales
elif page == "Bet Stats":
    st.title("Bet Stats")
    try:
        # Cargar datos adicionales
        df_extra = pd.read_csv("Bet_Report.csv")
        
        # Limpiar datos adicionales
        df_extra = df_extra.loc[:, ~df_extra.columns.str.contains('^Unnamed')]  # Eliminar columnas 'Unnamed'
        
        # Mostrar la tabla completa
        st.write("Tabla de datos adicionales:")
        st.dataframe(df_extra)
    except Exception as e:
        st.error(f"Error al cargar el archivo de datos adicionales: {e}")


