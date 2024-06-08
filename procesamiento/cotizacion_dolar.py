import requests
from bs4 import BeautifulSoup

def obtener_cotizacion_dolar():
    try:
        url = 'https://www.bna.com.ar/Personas'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tabla = soup.find('table', class_='table cotizacion')
            valor_buscado = "Dolar U.S.A"

            fila_valor_buscado = None
            for fila in tabla.find_all('tr'):
                celdas = fila.find_all('td')
                for celda in celdas:
                    if celda.get_text() == valor_buscado:
                        fila_valor_buscado = fila
                        break
                if fila_valor_buscado:
                    break

            if fila_valor_buscado:
                datos_fila = fila_valor_buscado.find_all('td')
                venta = datos_fila[2].get_text().replace(',', '.')
                return float(venta)
        else:
            raise Exception("No se pudo obtener la cotización del dólar.")
    except Exception as e:
        raise Exception(f"Ocurrió un error: {str(e)}")

dolar = obtener_cotizacion_dolar()
