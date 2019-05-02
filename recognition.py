#分類する動物
words=["犬","馬","猫","イルカ"]
#保存するフォルダー名
image_folder_name="./image_folder"


#wordsに対するdictを作成
detection_words={}
for i in range(len(words)):
    detection_words[words[i]]=i
    

