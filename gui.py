import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS

# from recognition.NPrecognition_v3 import number_plate_recognize
from recognition import NPrecognition_v3 as npr

class App(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.root = root
        self.root.title('ナンバープレート認識システム')
        self.root.geometry('1000x700')
        self.root.minsize(1000,700)
        self.pack()
        self.main_color = '#34363B'
        self.sub_color = '#202124'
        self.accent_color = '#85CEFF'
        self.accent_dark_color = '#2B4252'
        self.root.config(bg=self.main_color)

        self.console_pos = 1

        self.video_path = None

        self.root.update()
        self.create_widget()
        
        self.root.bind('<Configure>', self.on_window_configure)

    #ウィジェット等の作成
    def create_widget(self):
        self.window_width = root.winfo_width()

        #画像表示フレーム
        # self.img_frame = tk.Frame(root, bd=3, relief=tk.GROOVE)
        self.img_frame = tk.Frame(root, relief='groove', bg=self.main_color, bd=2)
        self.img_frame.propagate(False)
        self.img_frame.pack(side=tk.LEFT, anchor=tk.NW,expand=True,fill=tk.BOTH,padx=(10,2),pady=10)
        self.import_frame = tk.Frame(self.img_frame, bg=self.main_color)
        self.import_frame.pack(side=tk.TOP, fill=tk.X,padx=5, pady=(5,0))
        # self.file_button = ttk.Button(self.import_frame, text='画像ファイルを選択',
        #                               command = self.menu_file_open_click, padding=[10,3],
        #                               takefocus=False)
        self.file_button = tk.Button(self.import_frame, text='画像ファイルを選択',
                                      command = self.menu_file_open_click, bg='#44464D',
                                      font=("meiryo",10), fg='white', padx=10)
        self.file_button.pack(side=tk.LEFT, padx=10, pady=3)
        self.file_button = tk.Button(self.import_frame, text='Reload',
                                      command = self.upadate_img, bg='#44464D',
                                      font=("meiryo",10), fg='white', padx=10)
        self.file_button.pack(side=tk.LEFT, padx=10, pady=3)
        self.canvas = tk.Canvas(self.img_frame, width=int(self.window_width/2), height=int(self.window_width/4),
                                highlightbackground='gray', highlightthickness=2, bg=self.sub_color)
        self.canvas.pack(side=tk.TOP,padx=10,pady=10,fill=tk.X,expand=True)

        #画像情報
        self.info_frame = tk.Frame(self.img_frame, relief=tk.GROOVE, bg=self.main_color, bd=2)
        self.info_frame.pack(side=tk.TOP, padx=10, pady=(0,10), fill=tk.X)
        self.info_label = tk.Label(self.info_frame, text='ー画像情報ー', bg=self.main_color,
                                   fg='white', font=("meiryo",10))
        self.date_label = tk.Label(self.info_frame, bg=self.main_color, fg='white', font=("meiryo",10))
        self.width_label = tk.Label(self.info_frame, bg=self.main_color, fg='white', font=("meiryo",10))
        self.height_label = tk.Label(self.info_frame, bg=self.main_color, fg='white', font=("meiryo",10))
        self.info_label.pack(side=tk.TOP, pady=5)
        self.date_label.pack(side=tk.TOP, anchor=tk.W, padx=10)
        self.width_label.pack(side=tk.TOP, anchor=tk.W, padx=10)
        self.height_label.pack(side=tk.TOP, anchor=tk.W, padx=10,pady=(0,10))
        #コンソール
        self.console = scrolledtext.ScrolledText(self.img_frame, bg=self.sub_color,
                                                 fg='white', blockcursor=False,
                                                 insertbackground=self.accent_color, insertwidth=2,
                                                 padx=10, selectbackground=self.accent_dark_color,
                                                 font=("meiryo",10), state='normal')
        self.console.config(state='disabled')
        self.console.pack(side=tk.TOP, padx=10, pady=(0,10), fill=tk.BOTH, expand=True)
        # self.console_frame = tk.Frame(self.img_frame, relief=tk.RAISED, bg='#000033')
        # self.console_frame.pack(side=tk.TOP, padx=10, pady=(0,10), fill=tk.BOTH, expand=True)
        # self.scrollbar = tk.Scrollbar(self.img_frame, orient=tk.VERTICAL, command=self.console_frame.yview,width=20)
        # self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        #解析フーム
        self.analysis_frame = tk.Frame(root, relief=tk.GROOVE, bg=self.main_color, bd=2)
        self.analysis_frame.propagate(False)
        self.analysis_frame.pack(side=tk.RIGHT, anchor=tk.NW,expand=True,fill=tk.BOTH,padx=(2,10),pady=10)
        self.analysis_label = tk.Label(self.analysis_frame, text='ー認識結果ー', bg=self.main_color,
                                       fg='white', font=("meiryo",10))
        self.analysis_label.pack(side=tk.TOP, pady=5)
        self.result_frame = tk.Frame(self.analysis_frame, relief='groove', bg=self.main_color, bd=2)
        self.result_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.area_label = tk.Label(self.result_frame, bg=self.main_color, fg='white', font=("meiryo",10))
        self.num1_label = tk.Label(self.result_frame, bg=self.main_color, fg='white', font=("meiryo",10))
        self.kana_label = tk.Label(self.result_frame, bg=self.main_color, fg='white', font=("meiryo",10))
        self.num2_label = tk.Label(self.result_frame, bg=self.main_color, fg='white', font=("meiryo",10))
        self.area_label.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=3)
        self.num1_label.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=3)
        self.kana_label.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=3)
        self.num2_label.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=3)

    #ファイルの選択
    def menu_file_open_click(self, event=None):
        filename = filedialog.askopenfilename(
            title = "ファイルを開く",
            initialdir = "./" # 自分自身のディレクトリ
            )
        print(filename)
        if len(filename) == 0:
            self.console_message('ファイルの選択がキャンセルされました．\n')
        else:
            self.console_message(f'{filename}を読み込みました.\n')
            self.disp_image(filename)

    def console_message(self, text):
        self.console.config(state='normal')
        self.console.insert(f'{self.console_pos}.0', f'> {text}')
        self.console.config(state='disabled')
        self.console.see('end')
        self.console_pos += 1

    #画像を表示
    def disp_image(self, img_path):
        self.window_width = root.winfo_width()
        self.canvas.config(width=int(self.window_width/2), height=int(self.window_width/4))
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.pil_img = Image.open(img_path)
        self.get_info(self.pil_img)
        self.pil_img_width = self.pil_img.width
        self.pil_img_height = self.pil_img.height
        self.pil_img = self.resize_img(self.pil_img)
        self.tk_pil_img = ImageTk.PhotoImage(image=self.pil_img)
        self.canvas_image = self.canvas.create_image(int(self.canvas_width/2),int(self.canvas_height/2),image=self.tk_pil_img)
        self.root.update()
        self.console_message('文字認識中...\n')
        self.root.update()
        self.recognize(self.pil_img)

    def recognize(self, pil_img):
        cv2_img = np.array(pil_img, dtype=np.uint8)
        results, p_time, s_time, a_time, n1_time, k_time, n2_time, pros_time = npr.number_plate_recognize(cv2_img)
        self.area_label.config(text=f"地名\t\t| {results['area']}")
        self.num1_label.config(text=f"分類番号\t\t| {results['num1']}")
        self.kana_label.config(text=f"ひらがな\t\t| {results['kana']}")
        self.num2_label.config(text=f"一連指定番号\t| {results['num2']}")

        self.console_message(f'前処理時間: {p_time:.4f} [s]\n')
        self.console_message(f'画像分割時間: {s_time:.4f} [s]\n')
        self.console_message(f'認識時間_地名: {a_time:.4f} [s]\n')
        self.console_message(f'認識時間_分類番号: {n1_time:.4f} [s]\n')
        self.console_message(f'認識時間_ひらがな: {k_time:.4f} [s]\n')
        self.console_message(f'認識時間_一連指定番号: {n2_time:.4f} [s]\n')
        self.console_message(f'総処理時間: {pros_time:.4f} [s]\n')

    #画像情報を取得し，表示する
    def get_info(self, img):
        exif_dict = img._getexif()
        date = '不明'
        if exif_dict:
            for id, value in exif_dict.items():
                if TAGS.get(id, id) == "DateTimeOriginal":
                    date = value
        width = img.width
        height = img.height
        self.date_label.config(text=f'撮影日\t| {date}')
        self.width_label.config(text=f'幅\t| {width}px')
        self.height_label.config(text=f'高さ\t| {height}px')

    #画像をキャンバスサイズにリサイズ
    def resize_img(self,img):
        self.root.update()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        width = 0
        height = 0
        print(abs(self.pil_img_width-self.canvas_width))
        print(abs(self.pil_img_height-self.canvas_height))
        if self.pil_img_width-self.canvas_width > self.pil_img_height-self.canvas_height:
            width = self.canvas_width
            height = int(self.pil_img_height*(self.canvas_width/self.pil_img_width))
            img = img.resize((width, height))
        else:
            width = int(self.pil_img_width*(self.canvas_height/self.pil_img_height))
            height = self.canvas_height
            img = img.resize((width, height))
        # self.canvas.config(width=width, height=height)
        return img

    def on_window_configure(self, event):
        self.window_width = root.winfo_width()
        self.canvas.config(width=int(self.window_width/2), height=int(self.window_width/4))

    def upadate_img(self):
        self.pil_img = self.resize_img(self.pil_img)
        self.tk_pil_img = ImageTk.PhotoImage(image=self.pil_img)
        self.canvas_image = self.canvas.create_image(int(self.canvas_width/2),int(self.canvas_height/2),image=self.tk_pil_img)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.run()