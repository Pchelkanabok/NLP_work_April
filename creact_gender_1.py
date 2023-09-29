import pandas as pd

df_fio_gender = pd.read_excel("tabels_original/df_fio_gender.xlsx")
df_orig = pd.read_excel("tabels_original/name.xlsx")

gender_slov = {}
c = 0
mas_isp = []
for i in df_orig["Исполнитель"]:
    str_isp = i.split(" ")
    if (str_isp[0] + ' ' + str_isp[1][0]) not in mas_isp:
        mas_isp.append(str_isp[0] + ' ' + str_isp[1][0])
for i in mas_isp:
    print(c)
    r = df_fio_gender["Пол"][df_fio_gender["ФизическоеЛицо"].str.contains(i)]
    if len(r) != 0:
        a = r.reset_index(drop=True)[0]
    else:
        a = "Не найдено"
    gender_slov[i] = a
    c += 1
print(gender_slov)
gend_mas = []
for i in df_orig["Исполнитель"]:
    str_isp = i.split(" ")
    gend_mas.append(gender_slov[str_isp[0] + ' ' + str_isp[1][0]])
df_orig["Пол Исполнителя"] = gend_mas
df_orig.to_excel("tabel_ready/with_g.xlsx")








