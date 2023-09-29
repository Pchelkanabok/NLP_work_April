import pandas as pd

df_orig = pd.read_excel("tabel_ready/with_g.xlsx")

def gender_cor(df):
    result_df = pd.DataFrame(
        columns=['Автор', 'Количество задач решенных с мужским полом', 'Количество задач решенных с женским полом'])
    mas_avt = []
    res_slov = {}
    for i in df["Откуда поступило, автор обращения"]:
        if i not in mas_avt:
            mas_avt.append(i)
    for i in mas_avt:
        res_slov[i] = df[df.loc[:, "Откуда поступило, автор обращения"].isin([i])][
            "Пол Исполнителя"].value_counts()
    res_str = {}
    for i in res_slov:
        res_str = {}
        res_str["Автор"] = i
        try:
            res_str["Количество задач решенных с мужским полом"] = res_slov[i]['Мужской']
        except Exception as kk:
            res_str["Количество задач решенных с мужским полом"] = 0
        try:
            res_str["Количество задач решенных с женским полом"] = res_slov[i]['Женский']
        except Exception as kk:
            res_str["Количество задач решенных с женским полом"] = 0
        result_df = result_df.append(res_str, ignore_index= True)
    return result_df

def gender_cor_prosroch(df):
    res_df = gender_cor(df)
    res_man_m = []
    res_wom_m = []
    for i in range(len(res_df)):
        res_man = 0
        res_wom = 0
        df_w = df[df["Откуда поступило, автор обращения"] == res_df["Автор"][i]][df["Пол Исполнителя"] == "Женский"]
        df_m = df[df["Откуда поступило, автор обращения"] == res_df["Автор"][i]][df["Пол Исполнителя"] == "Мужской"]
        df_w = df_w.reset_index(drop=True)
        df_m = df_m.reset_index(drop=True)
        df_w.fillna('', inplace=True)
        df_m.fillna('', inplace=True)
        for j in range(len(df_w)):
            if df_w["Срок исполнения"][j] != '':
                if 'пр. ' in df_w["Срок исполнения"][j]:
                    res_wom += 1
            else:
                if 'пр. ' in df_w["Срок исполнения / Снято с контроля"][j]:
                    res_wom += 1

        for j in range(len(df_m)):
            if df_m["Срок исполнения"][j] != '':
                if 'пр. ' in df_m["Срок исполнения"][j]:
                    res_man += 1
            else:
                if 'пр. ' in df_m["Срок исполнения / Снято с контроля"][j]:
                    res_man += 1
        if len(df_m) != 0:
            res_man_m.append(100*res_man/len(df_m))
        else:
            res_man_m.append(0)
        if len(df_w) != 0:
            res_wom_m.append(100*res_wom/len(df_w))
        else:
            res_wom_m.append(0)
    res_df["Процент просроченных поручений женщинами"] = res_wom_m
    res_df["Процент просроченных поручений мужчинами"] = res_man_m
    return res_df



def gender_prosroch(df):
    pros_w = 0
    pros_m = 0
    df_w = df[df["Пол Исполнителя"] == "Женский"]
    df_m = df[df["Пол Исполнителя"] == "Мужской"]
    df_w = df_w.reset_index(drop=True)
    df_m = df_m.reset_index(drop=True)
    df_w.fillna('', inplace=True)
    df_m.fillna('', inplace=True)

    for i in range(len(df_w)):
        if df_w["Срок исполнения"][i] != '':
            if 'пр. ' in df_w["Срок исполнения"][i]:
                pros_w += 1
        else:
            if 'пр. ' in df_w["Срок исполнения / Снято с контроля"][i]:
                pros_w += 1


    for i in range(len(df_m)):
        if df_m["Срок исполнения"][i] != '':
            if 'пр. ' in df_m["Срок исполнения"][i]:
                pros_m += 1
        else:
            if 'пр. ' in df_m["Срок исполнения / Снято с контроля"][i]:
                pros_m += 1
    print("Просроченно женским полом: " + str(100 * pros_w / len(df_w)) + "%")
    print("Просроченно мужским полом: " + str(100 * pros_m / len(df_m)) + "%")
    return pros_w, pros_m

gender_prosroch(df_orig)

#gender_cor_prosroch(df_orig).to_excel("tabel_ready/cor_gender_prosroch.xlsx")
#gender_cor(df_orig).to_excel("tabel_ready/cor_gender.xlsx")