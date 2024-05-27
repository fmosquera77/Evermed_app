import streamlit as st
import pandas as pd
import plotly.express as px
from procesamiento.stock_valorizado import procesar_stock_valorizado
from procesamiento.precio_venta_promedio import procesar_precio_venta_promedio
from procesamiento.cotizacion_dolar import dolar
from io import BytesIO
from login import login, crear_usuario, cargar_usuarios
import toml  # Importa la librería para trabajar con archivos TOML


# Cargar la configuración desde el archivo config.toml
config_path = "C:\\Users\\Usuario\\Desktop\\Evermed_app\\.streamlit\\config.toml"

config = toml.load(config_path)

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
    if "stock_file" not in st.session_state:
        st.session_state.stock_file = None
    if "markup_stock_file" not in st.session_state:
        st.session_state.markup_stock_file = None
    if "markup_sales_file" not in st.session_state:
        st.session_state.markup_sales_file = None
    if "sales_file" not in st.session_state:
        st.session_state.sales_file = None
    if "vencimiento_stock_file" not in st.session_state:
        st.session_state.vencimiento_stock_file = None
    if "vencimiento_vencimientos_file" not in st.session_state:
        st.session_state.vencimiento_vencimientos_file = None

    options = ["Stock Valorizado", "Markup", "Precio Venta Promedio", "Vencimiento Stock"]
    
    if not st.session_state.logged_in:
        # Mostrar el formulario de login si el usuario no ha iniciado sesión
        st.subheader("Por favor, inicie sesión")
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
        

        if not selected_options:
            st.write("Seleccione una opción para continuar")
           
           

        df_stock = None
        df_ventas = None
        df_vencimientos = None

        for option in selected_options:
            if option == "Stock Valorizado":
                st.subheader("Stock Valorizado")
                if st.session_state.stock_file is None:
                    stock_file = st.file_uploader("Cargar archivo de stock - stock valorizado", type=["xlsx"], key="stock_file_uploader_stock_valorizado")
                    if stock_file is not None:
                        # Validar el nombre del archivo
                        if validar_nombre_archivo(stock_file.name, "stock"):
                            df_stock = pd.read_excel(stock_file)
                            st.success(f"Archivo '{stock_file.name}' cargado correctamente.")
                            st.session_state.stock_file = stock_file.name
                            st.session_state.df_stock = df_stock  # Guardar el DataFrame en session_state
                            st.rerun()  # Forzar recarga de la página
                        else:
                            st.warning("El nombre del archivo de stock no es válido.")
                else:
                    st.write(f"Archivo cargado: {st.session_state.stock_file}")
                    df_stock = st.session_state.df_stock
                    # Agregamos un botón para limpiar el archivo seleccionado y permitir cargar otro
                if st.button("Cambiar archivo"):
                    st.session_state.stock_file = None
                    st.session_state.df_stock = None
                    

            elif option == "Markup":
                st.subheader("Markup")
                if st.session_state.markup_stock_file is None:
                    stock_file = st.file_uploader("Cargar archivo de stock - markup", type=["xlsx"], key="stock_file_uploader_markup")
                    if stock_file is not None:
                        # Validar el nombre del archivo
                        if validar_nombre_archivo(stock_file.name, "stock"):
                            df_stock = pd.read_excel(stock_file)
                            st.success(f"Archivo '{stock_file.name}' cargado correctamente.")
                            st.session_state.markup_stock_file = stock_file.name
                            st.session_state.df_stock = df_stock  # Guardar el DataFrame en session_state
                            st.rerun()  # Forzar recarga de la página
                        else:
                            st.warning("El nombre del archivo de stock no es válido.")
                else:
                    st.write(f"Archivo cargado: {st.session_state.markup_stock_file}")
                    df_stock = st.session_state.df_stock

                if st.session_state.markup_sales_file is None:
                    ventas_file = st.file_uploader("Cargar archivo de ventas - markup", type=["xlsx"], key="ventas_file_uploader_markup")
                    if ventas_file is not None:
                        df_ventas = pd.read_excel(ventas_file)
                        st.success(f"Archivo '{ventas_file.name}' cargado correctamente.")
                        st.session_state.markup_sales_file = ventas_file.name
                        st.session_state.df_ventas = df_ventas  # Guardar el DataFrame en session_state
                        st.rerun()  # Forzar recarga de la página
                else:
                    st.write(f"Archivo cargado: {st.session_state.markup_sales_file}")
                    df_ventas = st.session_state.df_ventas

            elif option == "Precio Venta Promedio":
                st.subheader("Precio Venta Promedio")
                if st.session_state.sales_file is None:
                    ventas_file = st.file_uploader("Cargar archivo de ventas - precio venta promedio", type=["xlsx"], key="ventas_file_uploader_precio_venta_promedio")
                    if ventas_file is not None:
                        # Validar el nombre del archivo
                        if validar_nombre_archivo(ventas_file.name, "ventas"):
                            df_ventas = pd.read_excel(ventas_file)
                            st.success(f"Archivo '{ventas_file.name}' cargado correctamente.")
                            st.session_state.sales_file = ventas_file.name
                            st.session_state.df_ventas = df_ventas  # Guardar el DataFrame en session_state
                            st.rerun()  # Forzar recarga de la página
                        else:
                            st.warning("El nombre del archivo de ventas no es válido.")
                else:
                    st.write(f"Archivo cargado: {st.session_state.sales_file}")
                    df_ventas = st.session_state.df_ventas

            elif option == "Vencimiento Stock":
                st.subheader("Vencimiento Stock")
                if st.session_state.vencimiento_stock_file is None:
                    stock_file = st.file_uploader("Cargar archivo de stock - vencimiento stock", type=["xlsx"], key="stock_file_uploader_vencimiento_stock")
                    if stock_file is not None:
                        # Validar el nombre del archivo
                        if validar_nombre_archivo(stock_file.name, "stock"):
                            df_stock = pd.read_excel(stock_file)
                            st.success(f"Archivo '{stock_file.name}' cargado correctamente.")
                            st.session_state.vencimiento_stock_file = stock_file.name
                            st.session_state.df_stock = df_stock  # Guardar el DataFrame en session_state
                            st.rerun()  # Forzar recarga de la página
                        else:
                            st.warning("El nombre del archivo de stock no es válido.")
                else:
                    st.write(f"Archivo cargado: {st.session_state.vencimiento_stock_file}")
                    df_stock = st.session_state.df_stock

                if st.session_state.vencimiento_vencimientos_file is None:
                    vencimientos_file = st.file_uploader("Cargar archivo de vencimientos - vencimiento stock", type=["xlsx"], key="vencimientos_file_uploader")
                    if vencimientos_file is not None:
                        df_vencimientos = pd.read_excel(vencimientos_file)
                        st.success(f"Archivo '{vencimientos_file.name}' cargado correctamente.")
                        st.session_state.vencimiento_vencimientos_file = vencimientos_file.name
                        st.session_state.df_vencimientos = df_vencimientos  # Guardar el DataFrame en session_state
                        st.rerun()  # Forzar recarga de la página
                else:
                    st.write(f"Archivo cargado: {st.session_state.vencimiento_vencimientos_file}")
                    df_vencimientos = st.session_state.df_vencimientos

        if st.button("Ejecutar procesamiento de datos"):
            for option in selected_options:
                output_df = None
                if option == "Stock Valorizado" and df_stock is not None:
                    output_df = rutas("Stock Valorizado", df_stock, None, None)
                elif option == "Precio Venta Promedio" and df_ventas is not None:
                    output_df = rutas("Precio Venta Promedio", None, df_ventas, None)
                
                if option == "Stock Valorizado":
                    st.write(f"Dolar: {dolar}")

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
