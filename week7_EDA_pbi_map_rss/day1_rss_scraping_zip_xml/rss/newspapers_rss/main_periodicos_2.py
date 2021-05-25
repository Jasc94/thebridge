from urllib.request import urlopen
from xml.etree.ElementTree import parse
import pandas as pd
import json 
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

for i in newspapers:
    url_str = newspapers[i]
    var_url = urlopen(url_str)
    xmldoc = parse(var_url)

    for item in xmldoc.iterfind('channel/item'):

        if company in item.findtext('title').lower():
            tot_data['Periodico'].append(i)
            tot_data['Empresa'].append(company)
            tot_data['Noticia'].append(item.findtext('title'))
            tot_data['Fecha noticia'].append(item.findtext('pubDate'))
            tot_data['Link Noticia'].append(item.findtext('link'))

company_df = pd.DataFrame(tot_data)
print("company_df.shape:", company_df.shape)
company_df.to_excel('week7_EDA_pbi_map_rss/day1_rss_scraping_zip_xml/rss/newspapers_rss/newspapers_rss.xlsx')
company_df.to_csv('week7_EDA_pbi_map_rss/day1_rss_scraping_zip_xml/rss/newspapers_rss/newspapers_rss.csv')
company_df.to_json("week7_EDA_pbi_map_rss/day1_rss_scraping_zip_xml/rss/newspapers_rss/newspapers_rss.json")
print("\n FINISH \n")
company_df