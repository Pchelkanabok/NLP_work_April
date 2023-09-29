import pandas as pd
import numpy as np
import re
from datetime import datetime

df = pd.DataFrame() #Ну тут заносим нашу бд. Просто считываем откуда-то

def cor_1(df_who_where_poruch):
  arr = []
  for i in df_who_where_poruch:
    match_str_1 = re.search(r'\d{2}.\d{2}.\d{4}', i)
    match_str_2 = re.search(r'\d{2}.\d{2}.\d{4}', i[match_str_1.end():])
    date_por = datetime.strptime(match_str_1.group(), '%d.%m.%Y').date()
    date_pos = datetime.strptime(match_str_2.group(), '%d.%m.%Y').date()
    arr.append(date_pos - date_por)
  return arr

df["Время между поручительством и поставкой"] = cor_1(df["Кто поручил, когда"])



def cor_3(df):
  mas_isp = []
  res_slov = {}
  for i in df["Исполнитель"]:
    if i not in mas_isp:
      mas_isp.append(i)
  for i in mas_isp:
    res_slov[i] = df[df.loc[:, "Исполнитель"].isin([i])]["Откуда поступило, автор обращения"].value_counts()
  return res_slov

df_cor_3= pd.DataFrame(cor_3(df)) #Создаётся новая дф с этой корреляцией



def cor_4(df):
  df_cor= pd.DataFrame(cor_3(df))
  df.fillna('', inplace=True)
  for index, row in df.iterrows():
    arr_time = []
    str_time = ''
    if row['Срок исполнения'] != '':
      #arr_time = row['Срок исполнения'].split(" ")
      df_cor[row['Исполнитель']][row['Откуда поступило, автор обращения']] = row['Срок исполнения']
      df_cor[row['Исполнитель']][row['Откуда поступило, автор обращения']]
    else:
      df_cor[row['Исполнитель']][row['Откуда поступило, автор обращения']] = row['Срок исполнения / Снято с контроля']
  return df_cor

df_cor_4 =cor_4(df) #Создаётся новая дф с этой корреляцией



def cor_6(df):
  mas_isp = []
  res_slov = {}
  mas_aut = []
  df_ =df
  for i in range(len(df_)):
    comp_arr = []
    comp_arr = df_["Откуда поступило, автор обращения"][i].split(" -> ")
    df_["Откуда поступило, автор обращения"][i] = comp_arr[1]
  for i in df_["Исполнитель"]:
    if i not in mas_isp:
      mas_isp.append(i)
  for i in mas_isp:
    res_slov[i] = df_[df_.loc[:,"Исполнитель"].isin([i])]["Откуда поступило, автор обращения"].value_counts()
  return res_slov

df_cor_6 = pd.DataFrame(cor_6(df)) #Создаётся новая дф с этой корреляцией



def stepen_deleg_por(df):
  #df_ = DataFrame()
  return pd.DataFrame(df["Краткое содержание, что поручено"].value_counts())

df_cor_stepen_deleg_por = stepen_deleg_por(df)   #Создаётся новая дф с этой корреляцией



def kol_prodl_dl(df):
  res_slov = {}
  # df_ = df.reset_index(drop=True)
  for i in range(len(df)):
    a = 0
    df_0 = df[df.loc[:,"Краткое содержание, что поручено"].isin([df['Краткое содержание, что поручено'][i]])]
    df_0 = df_0.reset_index(drop=True)
    for j in range(len(df_0)):
      if "продл" in str(df_0["Дата исполнения"][j]):
        a += 1
    res_slov[df['Краткое содержание, что поручено'][i]] = a

    kol_prodl_dl_df = pd.DataFrame(columns=["Краткое содержание, что поручено", "Количество продлений"])
    for i in a:
      kol_prodl_dl_df.loc[len(kol_prodl_dl_df.index)] = [i, res_slov[i]]
  return kol_prodl_dl_df

kol_prodl_dl_df = kol_prodl_dl(df) #Создаётся новая дф с этой корреляцией



def cor_comp_zak_kol_por(df):
  res_slov = {}
  df_ = df
  for i in range(len(df_)):
    comp_arr = []
    comp_arr = df_["Откуда поступило, автор обращения"][i].split(" -> ")
    df_["Откуда поступило, автор обращения"][i] = comp_arr[1]
  a = df_["Откуда поступило, автор обращения"].value_counts()
  cor_comp_zak_kol_por_df = pd.DataFrame(columns=["Компания заказчик", "Количество поручений"])
  for i in a.index:
    cor_comp_zak_kol_por_df.loc[len(cor_comp_zak_kol_por_df.index)] = [i, a[i]]
  return   cor_comp_zak_kol_por_df

cor_comp_zak_kol_por_df = cor_comp_zak_kol_por(df) #Создаётся новая дф с этой корреляцией



def nalichie_curatora(df):
  curator_yes_pr = 0
  curator_yes_norm = 0
  curator_no_pr = 0
  curator_no_norm = 0
  df.fillna('', inplace=True)
  for i in range(len(df)):
    if df["Куратор"][i] != '':
      if df["Срок исполнения"][i] != '':
        if 'пр. ' in df["Срок исполнения"][i]:
          curator_yes_pr += 1
        else:
          curator_yes_norm += 1
      else:
        if 'пр. ' in df["Срок исполнения / Снято с контроля"][i]:
          curator_yes_pr += 1
        else:
          curator_yes_norm += 1
    else:
      if df["Срок исполнения"][i] != '':
        if 'пр. ' in df["Срок исполнения"][i]:
          curator_no_pr += 1
        else:
          curator_no_norm += 1
      else:
        if 'пр. ' in df["Срок исполнения / Снято с контроля"][i]:
          curator_no_pr += 1
        else:
          curator_no_norm += 1
  print("Процент просроченных дедлайно с куратором: ", curator_yes_pr/(curator_yes_pr+curator_yes_norm))
  print("Процент просроченных дедлайно без куратора: ", curator_no_pr/(curator_no_pr+curator_no_norm))
  return curator_yes_pr, curator_yes_norm, curator_no_pr, curator_no_norm

nalichie_curatora(df)
"""
Примерный вывод:
Процент просроченных дедлайно с куратором:  0.21188811188811188
Процент просроченных дедлайно без куратора:  0.43580683156654887
(909, 3381, 1110, 1437)
"""



def obsh_pokaz(df):
  res_df = pd.DataFrame(columns=["Сотрудник", "Количество выданных поручений",
                              "Количество выполненных поручений", "Процент просроченных дедлайнов",
                              "Количество курированных поручений"])
  res_slov_kol_isp ={}
  res_slov_kur = {}
  res_slov_kol_por = {}
  res_clov_percent = {}
  mas_sotr = []
  df.fillna('', inplace=True)
  for i in df["Исполнитель"]:
    if i != 'Внутренний контроль ("Технополис Москва" ОЭЗ" АО)':
      if i.split(' ("')[0] not in mas_sotr:
        mas_sotr.append(i.split(' ("')[0])
        res_slov_kol_isp[i.split(' ("')[0]] = 0
        res_slov_kur[i.split(' ("')[0]] = 0
        res_slov_kol_por[i.split(' ("')[0]] = 0
        res_clov_percent[i.split(' ("')[0]] = [0, 0]
      res_slov_kol_isp[i.split(' ("')[0]] += 1

  for i in df["Куратор"]:
    if i != '' and i != 'Внутренний контроль':
      ar = []
      s = '.'
      ar = i.split('. ')
      if len(ar) == 1:
        s = ''
      for j in range(len(ar)):
        if j == len(ar) - 1:
          s = ''
        if (ar[j]+s) not in mas_sotr:
          mas_sotr.append(ar[j]+s)
          res_slov_kol_isp[ar[j]+s] = 0
          res_slov_kur[ar[j]+s] = 0
          res_slov_kol_por[ar[j]+s] = 0
          res_clov_percent[ar[j]+s] = [0, 0]
        res_slov_kur[ar[j]+s] += 1

  for i in df["Кто поручил, когда"]:
    if (i.split(' ')[1] + ' ' + i.split(' ')[2]) not in mas_sotr:

      mas_sotr.append(i.split(' ')[1] + ' ' + i.split(' ')[2])
      res_slov_kol_isp[i.split(' ')[1] + ' ' + i.split(' ')[2]] = 0
      res_slov_kur[i.split(' ')[1] + ' ' + i.split(' ')[2]] = 0
      res_slov_kol_por[i.split(' ')[1] + ' ' + i.split(' ')[2]] = 0
      res_clov_percent[i.split(' ')[1] + ' ' + i.split(' ')[2]] = [0, 0]
    res_slov_kol_por[i.split(' ')[1] + ' ' + i.split(' ')[2]] += 1

  for i in range(len(df)):
    if df["Срок исполнения"][i] != '':
      if 'пр. ' in df["Срок исполнения"][i]:
        res_clov_percent[df["Исполнитель"][i].split(' ("')[0]][0] += 1
      else:
        res_clov_percent[df["Исполнитель"][i].split(' ("')[0]][1] += 1
    else:
      if 'пр. ' in df["Срок исполнения / Снято с контроля"][i]:
        res_clov_percent[df["Исполнитель"][i].split(' ("')[0]][0] += 1
      else:
        res_clov_percent[df["Исполнитель"][i].split(' ("')[0]][1] += 1

  for i in mas_sotr:
    res_df.loc[len(res_df.index)] = [
        i, res_slov_kol_por[i], res_slov_kol_isp[i], ('-' if res_clov_percent[i][0]+res_clov_percent[i][1]
         == 0 else 100*res_clov_percent[i][0]/(res_clov_percent[i][0]+res_clov_percent[i][1])), res_slov_kur[i]]
  return res_df

obsh_pokaz_df = obsh_pokaz(df) #Создаётся новая дф с этой корреляцией



