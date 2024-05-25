import pandas as pd
from procesamiento.cotizacion_dolar import obtener_cotizacion_dolar
import requests

def procesar_stock_valorizado(df_stock_stock_valorizado):
    try:
        dolar = obtener_cotizacion_dolar()
    except requests.exceptions.RequestException as e:
        print("No se pudo obtener la cotización del dólar. Error:", e)
        return None

    def stock_dolar_peso(row):
        if row['Tipo'] == 'Distribucion':
            return row['Último Precio de Compra']
        else:
            return row['Último Precio de Compra'] * 1.45 * dolar

    df_stock_stock_valorizado['Último Precio de Compra'] = df_stock_stock_valorizado.apply(stock_dolar_peso, axis=1).astype(int)
    df_stock_stock_valorizado['Stock Valorizado'] = df_stock_stock_valorizado['Stock Total'] * df_stock_stock_valorizado['Último Precio de Compra']
    df_stock_valorizado = df_stock_stock_valorizado[['Código', 'Stock Valorizado','Tipo']]

    return df_stock_valorizado
