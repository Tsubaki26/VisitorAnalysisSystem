import os

# フォルダを作成する関数
def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        print(f'フォルダ {folder_name} は既に存在します。')

# ひらがなのリスト
hiragana_list = ['あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ',
                 'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と',
                 'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ',
                 'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り',
                 'る', 'れ', 'ろ', 'わ', 'を', 'ん']

# フォルダを作成
for hiragana in hiragana_list:
    folder_name = hiragana
    create_folder(folder_name)
