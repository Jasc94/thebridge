# PARA SACAR INFORMACIÓN DE LOS RSS

from urllib.request import urlopen                  # nos va a permitir leer los rss como si fuera un diccionario
from xml.etree.ElementTree import parse
import pandas as pd
import json as js

# Este es el filtro que vamos a utilizar
# Es decir, vamos a buscar todas las noticias que tengan la palabra "gobierno"
company = 'gobierno'

newspapers = {
    'Expansion': 'https://e00-expansion.uecdn.es/rss/empresas.xml',
    'El economista': 'https://www.eleconomista.es/rss/rss-empresas.php',
    'Cinco dias': 'https://cincodias.elpais.com/seccion/rss/companias/',
    'El confidencial': 'https://rss.elconfidencial.com/empresas/'
}


tot_data = {
    'Periodico': [],
    'Empresa': [],
    'Noticia': [],
    'Fecha noticia': [],
    'Link Noticia': []
}

# Recorremos el dict newspapers
for i in newspapers:
    # Para cada elemento del dict, devuelveme el valor para la clave i (que es la url)
    url_str = newspapers[i]
    # Nos traemos la info de la url
    var_url = urlopen(url_str)
    # Leemos toda esta info como un objeto xml
    xmldoc = parse(var_url)

    # Dentro de la key "channel", vamos a iterar sobre cada "item" --> las noticias están divididas por items
    for item in xmldoc.iterfind('channel/item'):

        if company in item.findtext('title').lower():       # Lo paso todo a minúscula para que matchee mejor con "gobierno"
            tot_data['Periodico'].append(i)
            tot_data['Empresa'].append(company)
            tot_data['Noticia'].append(item.findtext('title'))
            tot_data['Fecha noticia'].append(item.findtext('pubDate'))
            tot_data['Link Noticia'].append(item.findtext('link'))

# Pasamos el dict a dataframe
company_df = pd.DataFrame(tot_data)
print("company_df.shape:", company_df.shape)

# Con esto creo un excel, un csv y un json
company_df.to_excel('./company_data.xlsx')
company_df.to_csv('./company_data.csv')

df_json = company_df.to_json(orient="columns")
df_parsed = js.loads(df_json, indent=4)
company_df.to_json('./company_data.json')

print("\n FINISH \n")