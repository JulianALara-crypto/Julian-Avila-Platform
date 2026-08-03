import pandas as pd

from database.medidas import obtener_medidas_cliente
from database.gimnasio import buscar_cliente_gym



def resumen_cliente(cedula):


    datos = {}



    cliente = buscar_cliente_gym(
        cedula
    )


    if not cliente.empty:

        datos["cliente"] = cliente.iloc[0]



    medidas = obtener_medidas_cliente(
        cedula
    )



    if not medidas.empty:


        medidas = medidas.sort_index()


        datos["inicial"] = medidas.iloc[0]

        datos["actual"] = medidas.iloc[-1]


        datos["historial"] = medidas



    return datos
