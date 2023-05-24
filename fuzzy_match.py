import pandas as pd
import difflib

# 讀取 CSV 檔案
usecols_df1 = ["sna", "sarea"]
df1 = pd.read_csv("Youbike2.0_2.csv", 
                    encoding = "ANSI",
                    usecols = usecols_df1)
#df2 = pd.read_csv("Ubike_test.csv", encoding = "ANSI")
usecols = ["rent_station"]
df2 = pd.read_csv("C:/Users/elena.hsieh.LEADER/Downloads/2022_Ubile2.0/202207_YouBike2.0票證刷卡資料.csv", 
                    encoding = "utf_8_sig",
                    usecols = usecols,
                    dtype = {"rent_station": str},
                    chunksize = 10000)

print(df2)


# 建立比對函式
def fuzzy_match(a, b):
    # 將字串轉為小寫 if the string is Eng.
    # a = str(a).lower()
    # b = str(b).lower()
    # 使用 difflib 的 SequenceMatcher 計算相似度
    similarity = difflib.SequenceMatcher(None, a, b).ratio()
    return similarity

# 建立 sarea 與 rent_station(sna) 的對應表
sarea_dict = {}
for i, row in df1.iterrows():
    sna = row["sna"]
    sarea = row["sarea"]
    sarea_dict[sna] = sarea

# 建立新的欄位 area
# apply() function can make a new column
# 對於每個 rent_station 值，使用 max 函式找出 sarea_dict 中最相似的鍵值(sna)，其中相似度的比較是透過 fuzzy_match 函式進行的。這樣就找到了最相似的 sna 值。
# 再根據 sarea_dict 找到對應的sarea，儲存在新的欄位sarea中

for data_chunk in df2:
    data_chunk["match_station"] = data_chunk["rent_station"].apply(lambda x: max(sarea_dict.keys(), key=lambda y: fuzzy_match(x, y)))
    data_chunk["sarea"] = data_chunk["match_station"].apply(lambda x: sarea_dict[x])
    data_chunk.to_csv('202207_YouBike2.0_count.csv', index = False, encoding = "utf_8_sig", mode = "a", header=False)
