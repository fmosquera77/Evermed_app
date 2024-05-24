import streamlit as st
import pandas as pd
import plotly.express as px
from procesamiento.stock_valorizado import procesar_stock_valorizado
from procesamiento.precio_venta_promedio import procesar_precio_venta_promedio
from io import BytesIO
from login import login, crear_usuario, cargar_usuarios


# Función que reemplaza a la función `rutas` original
def rutas(option, df_stock, df_ventas, df_vencimientos):
    if option == "Stock Valorizado":
        return procesar_stock_valorizado(df_stock)
    if option == "Precio Venta Promedio":
        return procesar_precio_venta_promedio(df_ventas)
    
    return None

# Función para validar el nombre del archivo
def validar_nombre_archivo(ruta_archivo, palabra_clave):
    return palabra_clave.lower() in ruta_archivo.lower()

# Cargar usuarios desde el archivo JSON
users = cargar_usuarios()

# Función principal de la aplicación Streamlit
def main():
    st.title("Reportes Evermed")
    
    # Verificar si el usuario ha iniciado sesión
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "show_create_user_form" not in st.session_state:
        st.session_state.show_create_user_form = False

    options = ["Stock Valorizado", "Markup", "Precio Venta Promedio", "Vencimiento Stock"]
    
    if not st.session_state.logged_in:
        # Mostrar el formulario de login si el usuario no ha iniciado sesión
        st.subheader("Por favor, inicie sesión para acceder a la aplicación")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Iniciar Sesión"):
            if login(username, password, users):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Por favor, inténtelo nuevamente.")
        
        # Botón para mostrar el formulario para crear un nuevo usuario
        if st.button("Nuevo Usuario"):
            st.session_state.show_create_user_form = True

        # Mostrar el formulario para crear un nuevo usuario si el botón fue clickeado
        if st.session_state.show_create_user_form:
            st.subheader("Crear Nuevo Usuario")
            nuevo_usuario = st.text_input("Nuevo Usuario", key="nuevo_usuario")
            nueva_contraseña = st.text_input("Nueva Contraseña", type="password", key="nueva_contraseña")
            if st.button("Confirmar"):
                if crear_usuario(nuevo_usuario, nueva_contraseña, users):
                    st.success("Usuario creado exitosamente.")
                    st.session_state.show_create_user_form = False
                else:
                    st.error("No se pudo crear el usuario. El nombre de usuario ya existe.")
    
    else:
        # Mostrar la página principal de la aplicación si el usuario ha iniciado sesión
        selected_options = st.multiselect("Seleccione una opción", options)

        df_stock = None
        df_ventas = None
        df_vencimientos = None

        for option in selected_options:
            if option == "Stock Valorizado":
                stock_file = st.file_uploader("Cargar archivo de stock", type=["xlsx"])
                if stock_file is not None:
                    # Validar el nombre del archivo
                    if validar_nombre_archivo(stock_file.name, "stock"):
                        df_stock = pd.read_excel(stock_file)
                    else:
                        st.warning("El nombre del archivo de stock no es válido.")
            
            elif option == "Markup":
                stock_file = st.file_uploader("Cargar archivo de stock", type=["xlsx"])
                ventas_file = st.file_uploader("Cargar archivo de ventas", type=["xlsx"])
                if stock_file is not None:
                    # Validar el nombre del archivo
                    if validar_nombre_archivo(stock_file.name, "stock"):
                        df_stock = pd.read_excel(stock_file)
                    else:
                        st.warning("El nombre del archivo de stock no es válido.")
                if ventas_file is not None:
                    df_ventas = pd.read_excel(ventas_file)
            
            elif option == "Precio Venta Promedio":
                ventas_file = st.file_uploader("Cargar archivo de ventas", type=["xlsx"])
                if ventas_file is not None:
                    # Validar el nombre del archivo
                    if validar_nombre_archivo(ventas_file.name, "ventas"):
                        df_ventas = pd.read_excel(ventas_file)
                    else:
                        st.warning("El nombre del archivo de ventas no es válido.")
            
            elif option == "Vencimiento Stock":
                stock_file = st.file_uploader("Cargar archivo de stock", type=["xlsx"])
                vencimientos_file = st.file_uploader("Cargar archivo de vencimientos", type=["xlsx"])
                if stock_file is not None:
                    # Validar el nombre del archivo
                    if validar_nombre_archivo(stock_file.name, "stock"):
                        df_stock = pd.read_excel(stock_file)
                    else:
                        st.warning("El nombre del archivo de stock no es válido.")
                if vencimientos_file is not None:
                    df_vencimientos = pd.read_excel(vencimientos_file)

        if st.button("Ejecutar procesamiento de datos"):
            for option in selected_options:
                output_df = None
                if option == "Stock Valorizado" and df_stock is not None:
                    output_df = rutas("Stock Valorizado", df_stock, None, None)
                elif option == "Precio Venta Promedio" and df_ventas is not None:
                    output_df = rutas("Precio Venta Promedio", None, df_ventas, None)
                

                if output_df is not None:
                    # Mostrar el DataFrame en pantalla
                    st.write(f"**{option}**")
                    st.dataframe(output_df)

                    # Crea un gráfico de barras para las opciones seleccionadas
                    x_column = output_df.columns[0]  # Tomar el nombre de la primera columna
                    y_column = output_df.columns[1]  # Tomar el nombre de la segunda columna
                    fig = px.bar(output_df, x=x_column, y=y_column, title=f'{y_column} por {x_column}')
                    st.plotly_chart(fig)

                    # Crear un BytesIO object para escribir los datos de Excel
                    excel_buffer = BytesIO()
                    # Escribir los datos en el objeto BytesIO
                    output_df.to_excel(excel_writer=excel_buffer, index=False, header=True)
                    # Mover el cursor al inicio del objeto BytesIO
                    excel_buffer.seek(0)
                    
                    # Proveer opción de descarga en formato Excel
                    st.download_button(
                        label=f"Descargar en formato XLSX ({option.replace(' ', '_')})",
                        data=excel_buffer,
                        file_name=f"{option.replace(' ', '_')}_resultado.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

if __name__ == "__main__":
    main()
