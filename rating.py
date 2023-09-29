import pandas as pd
import psycopg2


def rating(df, df_in_advance):
    res_df = pd.DataFrame(columns=["Сотрудник",
                                "Выданные", "Выполненные всрок", "Выполненные наперёд",
                                "Показатель рейтинга"])
    res_slov_kol_por_not_pros ={}
    res_slov_kol_por = {}
    res_slov_kol_in_ad = {}
    mas_sotr = []
    df.fillna('', inplace=True)
    for i in df["Исполнитель ФИО"]:
        if i != 'Внутренний контроль':
            if i.split(' ("')[0] not in mas_sotr:
                mas_sotr.append(i.split(' ("')[0])
                res_slov_kol_por[i.split(' ("')[0]] = 0
                res_slov_kol_por_not_pros[i.split(' ("')[0]] = 0
                res_slov_kol_in_ad[i.split(' ("')[0]] = 0
            res_slov_kol_por[i.split(' ("')[0]] += 1

    for i in df_in_advance["Исполнитель ФИО"]:
        if i != 'Внутренний контроль':
            if i.split(' ("')[0] not in mas_sotr:
                mas_sotr.append(i.split(' ("')[0])
                res_slov_kol_por[i.split(' ("')[0]] = 0
                res_slov_kol_por_not_pros[i.split(' ("')[0]] = 0
                res_slov_kol_in_ad[i.split(' ("')[0]] = 0

    for i in range(len(df_in_advance)):
        if df_in_advance["Исполнитель ФИО"][i] != 'Внутренний контроль':
            if ((df_in_advance["Срок исполнения"][i] - df_in_advance["Дата снятия с контроля"][i]).days) >= 7:
                res_slov_kol_por[df_in_advance["Исполнитель ФИО"][i].split(' ("')[0]] += 1


    for i in range(len(df)):
        if df["Исполнитель ФИО"][i] != 'Внутренний контроль':
            if df["Статус исполнения"][i] != 'просрочено':
                res_slov_kol_por_not_pros[df["Исполнитель ФИО"][i].split(' ("')[0]] += 1

    k = 0
    for i in res_slov_kol_por:
        k += res_slov_kol_por[i]


    for i in range(len(df_in_advance)):
        if df_in_advance["Исполнитель ФИО"][i] != 'Внутренний контроль':
            if int((df_in_advance["Срок исполнения"][i] - df_in_advance["Дата снятия с контроля"][i]).days) >= 7:
                res_slov_kol_in_ad[df_in_advance["Исполнитель ФИО"][i].split(' ("')[0]] += 1
    #print(res_slov_kol_in_ad)

    for i in mas_sotr:
        res_df.loc[len(res_df.index)] = [
            i, res_slov_kol_por[i], res_slov_kol_por_not_pros[i], res_slov_kol_in_ad[i],
            (0 if res_slov_kol_por[i]+res_slov_kol_por_not_pros[i] == 0
            else ((res_slov_kol_por_not_pros[i]/res_slov_kol_por[i] * (1 + res_slov_kol_por_not_pros[i] / k)) + 0.1*res_slov_kol_in_ad[i]))]
    res_df = res_df.sort_values(by="Показатель рейтинга", ascending=False)
    res_df = res_df.reset_index(drop=True)
    res_df["Номер в рейтинге"] = res_df.index
    res_df = res_df[["Номер в рейтинге",
                     "Сотрудник", "Выданные", "Выполненные всрок",
                     "Выполненные наперёд", "Показатель рейтинга"]]

    return res_df


def rating_2(df):
    res_df = pd.DataFrame(columns=["Сотрудник",
                                   "Выданные", "Выполненные всрок",
                                   "Показатель рейтинга"])
    res_slov_kol_por_not_pros = {}
    res_slov_kol_por = {}
    res_slov_kol_in_ad = {}
    mas_sotr = []
    df.fillna('', inplace=True)
    for i in df["Исполнитель ФИО"]:
        if i != 'Внутренний контроль':
            if i.split(' ("')[0] not in mas_sotr:
                mas_sotr.append(i.split(' ("')[0])
                res_slov_kol_por[i.split(' ("')[0]] = 0
                res_slov_kol_por_not_pros[i.split(' ("')[0]] = 0
                res_slov_kol_in_ad[i.split(' ("')[0]] = 0
            res_slov_kol_por[i.split(' ("')[0]] += 1


    for i in range(len(df)):
        if df["Исполнитель ФИО"][i] != 'Внутренний контроль':
            if df["Статус исполнения"][i] != 'просрочено':
                res_slov_kol_por_not_pros[df["Исполнитель ФИО"][i].split(' ("')[0]] += 1

    k = 0
    for i in res_slov_kol_por:
        k += res_slov_kol_por[i]

    m = 0
    for i in res_slov_kol_por_not_pros:
        m += res_slov_kol_por_not_pros[i]


    for i in mas_sotr:
        res_df.loc[len(res_df.index)] = [
            i, res_slov_kol_por[i], res_slov_kol_por_not_pros[i],
            (0 if res_slov_kol_por[i] + res_slov_kol_por_not_pros[i] == 0
             else ((res_slov_kol_por_not_pros[i] / res_slov_kol_por[i] - m/k)))]
    res_df = res_df.sort_values(by="Показатель рейтинга", ascending=False)
    res_df = res_df.reset_index(drop=True)
    res_df["Номер в рейтинге"] = res_df.index
    res_df = res_df[["Номер в рейтинге",
                    "Сотрудник",
                    "Выданные", "Выполненные всрок",
                    "Показатель рейтинга"]]

    return res_df


connection = psycopg2.connect(host="192.168.80.72", port="5432", password="User$@Smart90", dbname="DWHBI", user="UserRazrab")

str_sel = 'SELECT * FROM "MosEDO_list_Control-NoControl_HOT" ' \
          'WHERE "Срок исполнения" '+\
          ' BETWEEN NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7 AND NOW()::DATE-EXTRACT(DOW from NOW())::INTEGER+7'
str_sel_2 = 'SELECT * FROM "MosEDO_list_Control-NoControl_HOT" ' \
            'WHERE "Дата снятия с контроля" '+\
            ' BETWEEN NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7 AND NOW()::DATE-EXTRACT(DOW from NOW())::INTEGER+7'
df_orig = pd.read_sql(str_sel, connection)
df_orig_in_advance = pd.read_sql(str_sel_2, connection)
df_itog = rating(df_orig, df_orig_in_advance)
df_itog_2 = rating_2(df_orig)
df_itog.to_excel('raiting.xlsx')
df_itog_2.to_excel('raiting_2.xlsx')
#print(rating(df_orig))
