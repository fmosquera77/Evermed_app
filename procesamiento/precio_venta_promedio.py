import pandas as pd

def procesar_precio_venta_promedio(df_ventas):
    # Aquí va tu lógica para procesar el precio de venta promedio
    # ELimina las primeras tres filas de df_ventas y el "Total" por ser str en vez de int
    df_ventas = df_ventas.drop(df_ventas.index[0:4])
    df_ventas = df_ventas.drop(df_ventas.index[-1])

    # Establece la primera fila como los nombres de las columnas y elimínala del DataFrame
    df_ventas.columns = df_ventas.iloc[0]
    df_ventas = df_ventas[1:]

    # Elimina "Subtotal" de ventas y lo devuelve en formato Excel
    df_ventas = df_ventas[df_ventas['Nº Factura'] != 'Subtotal'].copy()

    # Calcula el precio unitario y agrégalo al DataFrame
    df_ventas['Precio Unitario'] = (df_ventas['Precio de Venta'] / df_ventas['Cantidad']).round(2)

    # Agrupa df_ventas por 'Código', suma las cantidades y obtén el precio de venta promedio
    df_precio_vta_prom = df_ventas.groupby('Código')['Precio Unitario'].mean().reset_index()
    df_precio_vta_prom = df_precio_vta_prom.rename(columns={'Precio Unitario': 'Precio de Venta Promedio'})
    df_precio_vta_prom['Precio de Venta Promedio'] = df_precio_vta_prom['Precio de Venta Promedio'].apply(lambda x: round(x, 2))
          
    return df_precio_vta_prom
