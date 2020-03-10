import xlrd
import pandas as pd
import numpy as np
import xlwt

excelFile = r'./file/2020.xls'


def extract(filepath, head):
    df_2020 = read_excel(filepath, head)
    df_2020 = df_2020[['姓名', '身份证号']]  # 筛选某些列
    # df2 = df1.loc[df1['性别'] == '女']   筛选符合条件的行
    df_new = read_excel('./file/new.xls', head)
    df_new = df_new[['姓名', '身份证号']]
    pd.merge(df_2020, df_new,)


def read_excel(filename, head):
    excel = pd.read_excel(filename, header=head)
    df = pd.DataFrame(excel)

    return df


if __name__ == '__main__':
    extract(excelFile, head=1)
