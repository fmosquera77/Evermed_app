from io import BytesIO
import streamlit as st
import pandas as pd
import plotly.express as px
from procesamiento.stock_valorizado import procesar_stock_valorizado
from procesamiento.precio_venta_promedio import procesar_precio_venta_promedio
from auth.login import login
from auth.user_management import crear_usuario, cargar_usuarios
from utils.file_validation import validar_nombre_archivo
from utils.session_management import (
    delete_file,
    initialize_session_state,
)
from utils.plot_util import mostrar_en_pestanas
import toml
import os

# Cargar la configuración desde el archivo
config_path = os.path.join(".streamlit", "config.toml")
config = toml.load(config_path)

def rutas(option, df_stock, df_ventas, df_vencimientos):
    if option == "Stock Valorizado":
        return procesar_stock_valorizado(df_stock)
    if option == "Precio Venta Promedio":
        return procesar_precio_venta_promedio(df_ventas)
    return None

def main():
    st.title("Reportes Evermed")
    initialize_session_state()

    options = ["Stock Valorizado", "Markup", "Precio Venta Promedio", "Vencimiento Stock", ""]
    
    if not st.session_state.logged_in:
        # Login and user creation form
        st.subheader("Por favor, inicie sesión")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Iniciar Sesión"):
            if login(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Por favor, inténtelo nuevamente.")
        
        if st.button("Nuevo Usuario"):
            st.session_state.show_create_user_form = True

        if st.session_state.show_create_user_form:
            st.subheader("Crear Nuevo Usuario")
            nuevo_usuario = st.text_input("Nuevo Usuario", key="nuevo_usuario")
            nueva_contraseña = st.text_input("Nueva Contraseña", type="password", key="nueva_contraseña")
            if st.button("Confirmar"):
                if crear_usuario(nuevo_usuario, nueva_contraseña):
                    st.success("Usuario creado exitosamente.")
                    st.session_state.show_create_user_form = False
                else:
                    st.error("No se pudo crear el usuario. El nombre de usuario ya existe.")
    else:
        # Main application form
        selected_options = st.session_state.get("selected_options", [])
        new_selected_options = st.multiselect("Seleccione una opción", options, default=selected_options)

        if new_selected_options != selected_options:
            st.session_state.selected_options = new_selected_options
            st.rerun()

        if not new_selected_options:
            st.write("Seleccione una opción para continuar")

        df_stock = None
        df_ventas = None
        df_vencimientos = None

        for option in new_selected_options:
            if option == "Stock Valorizado":
                # Handling Stock Valorizado
                handle_file_upload(option, "stock", "stock_file", "stock_valorizado")

            elif option == "Markup":
                # Handling Markup
                handle_file_upload(option, "stock", "markup_stock_file", "markup")
                handle_file_upload(option, "ventas", "markup_sales_file", "markup")

            elif option == "Precio Venta Promedio":
                # Handling Precio Venta Promedio
                handle_file_upload(option, "ventas", "sales_file", "precio_venta_promedio")

            elif option == "Vencimiento Stock":
                # Handling Vencimiento Stock
                handle_file_upload(option, "stock", "vencimiento_stock_file", "vencimiento_stock")
                handle_file_upload(option, "vencimientos", "vencimiento_vencimientos_file", "vencimiento_stock")

        if st.button("Ejecutar procesamiento de datos"):
            for option in new_selected_options:
                process_data(option)

def handle_file_upload(option, file_type, session_key, label):
    if st.session_state[session_key] is None:
        file = st.file_uploader(f"Cargar archivo de {file_type} - {label}", type=["xlsx"], key=f"{file_type}_file_uploader_{label}")
        if file is not None:
            if validar_nombre_archivo(file.name, file_type):
                df = pd.read_excel(file)
                st.success(f"Archivo '{file.name}' cargado correctamente.")
                st.session_state[session_key] = file.name
                st.session_state[f"df_{file_type}"] = df
                st.rerun()
            else:
                st.warning(f"El nombre del archivo de {file_type} no es válido.")
    else:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(f"Archivo cargado: {st.session_state[session_key]}")
            df = st.session_state[f"df_{file_type}"]
        with col2:
            if st.button("Cambiar archivo"):
                delete_file (session_key, file_type)
                
def process_data(option):
    df_stock = st.session_state.get("df_stock")
    df_ventas = st.session_state.get("df_ventas")
    output_df = None
    if option == "Stock Valorizado" and df_stock is not None:
        output_df = rutas("Stock Valorizado", df_stock, None, None)
    elif option == "Precio Venta Promedio" and df_ventas is not None:
        output_df = rutas("Precio Venta Promedio", None, df_ventas, None)
    
    if output_df is not None:
        x_column, y_column = output_df.columns[:2]
        fig = px.bar(output_df, x=x_column, y=y_column)
        mostrar_en_pestanas(output_df, fig, option)
        
        excel_buffer = BytesIO()
        output_df.to_excel(excel_writer=excel_buffer, index=False, header=True)
        excel_buffer.seek(0)
        
        st.download_button(
            label=f"Descargar en formato XLSX ({option.replace(' ', '_')})",
            data=excel_buffer,
            file_name=f"{option.replace(' ', '_')}_resultado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
