from bs4 import BeautifulSoup
import requests as rq
from lxml import etree
import pandas as pd
import dask.dataframe as dd

comex_url = 'https://www.gov.br/produtividade-e-comercio-exterior/pt-br/assuntos/comercio-exterior/estatisticas/base' \
            '-de-dados-bruta'

export_url = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_{0}.csv"
import_url = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/IMP_{0}.csv"


def get_data():
    r = rq.get(comex_url)
    soup = BeautifulSoup(r.content, 'html5lib')
    dom = etree.HTML(str(soup))
    tr1 = dom.xpath('/html/body/div[3]/div[1]/main/div[2]/div/div[5]/div/table[1]/tbody')[0].getchildren()
    tr2 = dom.xpath('/html/body/div[3]/div[1]/main/div[2]/div/div[5]/div/table[2]/tbody')[0].getchildren()
    last_year_export = []
    last_year_import = []
    for tr in tr1:
        for a in tr.getchildren():
            if len(a.getchildren()):
                ano = a.getchildren()[0].text
                if ano:
                    last_year_export.append(ano)

    for tr in tr2:
        for a in tr.getchildren():
            if len(a.getchildren()):
                ano = a.getchildren()[0].text
                if ano:
                    last_year_import.append(ano)
    last_year_export.sort()  # just to ensure the correct order
    last_year_import.sort()
    return last_year_export[-3:], last_year_import[-3:]


def download_files():
    imp, expo = get_data()
    header = '"CO_ANO";"CO_MES";"CO_NCM";"CO_UNID";"CO_PAIS";"SG_UF_NCM";"CO_VIA";"CO_URF";"QT_ESTAT";"KG_LIQUIDO' \
             '";"VL_FOB";"VL_FRETE";"VL_SEGURO"'
    default_header = 'ANO;MES;COD_NCM;COD_UNIDADE;COD_PAIS;SG_UF;COD_VIA;COD_URF;VL_QUANTIDADE;VL_PESO_KG;' \
                     'VL_FOB;VL_FRETE;VL_SEGURO'
    header_expo = '"CO_ANO";"CO_MES";"CO_NCM";"CO_UNID";"CO_PAIS";"SG_UF_NCM";"CO_VIA";"CO_URF";"QT_ESTAT' \
                  '";"KG_LIQUIDO";"VL_FOB"'
    default_expo_header = 'ANO;MES;COD_NCM;COD_UNIDADE;COD_PAIS;SG_UF_NCM;COD_VIA;COD_URF;VL_QUANTIDADE;' \
                          'VL_PESO_KG;' \
                          'VL_FOB'
    for i in imp:
        print(f"Downloading IMP_{i}")
        r = rq.get(import_url.format(i), verify=False)
        fp = open(f"IMP_{i}.csv", 'w')
        fp.write(r.text.replace(header, default_header))
        fp.close()

    for i in expo:
        print(f"Downloading EXP_{i}")
        r = rq.get(export_url.format(i), verify=False)
        fp = open(f"EXP_{i}.csv", 'w')
        fp.write(r.text.replace(header_expo, default_expo_header))
        fp.close()
    # Fixme: insufficient memory to merge
    join_bases(imp, expo)


# Try to join
def join():
    # if on is None:
    #     on = ['ANO', 'MES', 'COD_NCM', 'COD_UNIDADE', 'COD_PAIS', 'COD_VIA',
    #           'COD_URF', 'VL_QUANTIDADE', 'VL_PESO_KG', 'VL_FOB', 'MOVIMENTACAO']
    # try:
    #     a = dd.merge(pd.Index(a.index.values - 1), pd.Index(b.index.values - 1), on=on)
    # except Exception as err:
    #     print(f"> {err}")
    #     a = b
    #
    # return a
    f_comex = open('f_comex.csv', 'w')
    f_comex.write('ANO;MES;COD_NCM;COD_UNIDADE;COD_PAIS;SG_UF;COD_VIA;COD_URF;VL_QUANTIDADE;VL_PESO_KG;VL_FOB\n')
    f_comex.close()
    import os
    import glob
    all_filenames = [i for i in glob.glob(f"*.csv")]
    for i in all_filenames:
        if i != "f_comex.csv":
            os.system(f'cat {i} >> f_comex.csv')


def join_bases(imp, expo):
    df_imp = None
    df_expo = None
    print("Putting bases together")
    print("Joining IMP")
    for i in imp:
        df = pd.read_csv(f'IMP_{i}.csv', sep=';')
        df['MOVIMENTACAO'] = u'Importação'
        df.drop(['VL_FRETE', 'VL_SEGURO'], axis='columns', inplace=True)
        # df_imp = join(df_imp, df)
        df.to_csv(f'IMP_{i}.csv', header=False, index=False, sep=';')

    print("Joining EXPO")
    for i in expo:
        df = pd.read_csv(f'EXP_{i}.csv', sep=';')
        df['MOVIMENTACAO'] = u'Exportação'
        # df_expo = join(df_expo, df)
        df.to_csv(f'EXP_{i}.csv', header=False, index=False, sep=';')

    join()


if __name__ == '__main__':
    download_files()
