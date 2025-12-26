import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class MemeMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("表情包制作工具 - 文字添加器")
        self.root.geometry("900x700")
        
        # 初始化变量
        self.image_path = None
        self.original_image = None
        self.edited_image = None
        self.tk_image = None
        self.text_content = tk.StringVar(value="输入你的文字")
        self.text_size = tk.IntVar(value=30)
        self.text_color = tk.StringVar(value="#FF0000")  # 默认红色
        self.text_x = tk.IntVar(value=50)
        self.text_y = tk.IntVar(value=50)
        
        # 创建界面布局
        self.create_widgets()
    
    def create_widgets(self):
        # 顶部操作区
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 打开图片按钮
        open_btn = tk.Button(top_frame, text="打开图片", command=self.open_image, width=10)
        open_btn.pack(side=tk.LEFT, padx=5)
        
        # 保存图片按钮
        save_btn = tk.Button(top_frame, text="保存表情包", command=self.save_image, width=10)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # 文字设置区
        setting_frame = tk.Frame(self.root)
        setting_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 文字内容
        tk.Label(setting_frame, text="文字内容：").grid(row=0, column=0, sticky=tk.W, padx=5)
        text_entry = tk.Entry(setting_frame, textvariable=self.text_content, width=30)
        text_entry.grid(row=0, column=1, padx=5)
        
        # 文字大小
        tk.Label(setting_frame, text="文字大小：").grid(row=0, column=2, sticky=tk.W, padx=5)
        size_spin = tk.Spinbox(setting_frame, from_=10, to=100, textvariable=self.text_size, width=5)
        size_spin.grid(row=0, column=3, padx=5)
        
        # 文字颜色
        tk.Label(setting_frame, text="文字颜色：").grid(row=0, column=4, sticky=tk.W, padx=5)
        color_btn = tk.Button(setting_frame, text="选择颜色", command=self.choose_color, width=8)
        color_btn.grid(row=0, column=5, padx=5)
        color_preview = tk.Label(setting_frame, bg=self.text_color.get(), width=3)
        color_preview.grid(row=0, column=6, padx=2)
        
        # 文字位置
        tk.Label(setting_frame, text="X坐标：").grid(row=0, column=7, sticky=tk.W, padx=5)
        x_spin = tk.Spinbox(setting_frame, from_=0, to=1000, textvariable=self.text_x, width=5)
        x_spin.grid(row=0, column=8, padx=5)
        
        tk.Label(setting_frame, text="Y坐标：").grid(row=0, column=9, sticky=tk.W, padx=5)
        y_spin = tk.Spinbox(setting_frame, from_=0, to=1000, textvariable=self.text_y, width=5)
        y_spin.grid(row=0, column=10, padx=5)
        
        # 应用文字按钮
        apply_btn = tk.Button(setting_frame, text="应用文字", command=self.apply_text, width=10)
        apply_btn.grid(row=0, column=11, padx=10)
        
        # 图片预览区
        self.preview_frame = tk.Frame(self.root, bg="#EEEEEE", width=880, height=550)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.preview_label = tk.Label(self.preview_frame, bg="#EEEEEE")
        self.preview_label.pack(expand=True)
        
        # 绑定颜色变化事件
        self.text_color.trace('w', lambda *args: setattr(color_preview, 'bg', self.text_color.get()))
    
    def open_image(self):
        """打开图片文件"""
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                self.image_path = file_path
                self.original_image = Image.open(file_path).convert("RGB")
                # 调整图片大小适配预览区
                self.resize_preview_image()
                self.edited_image = self.original_image.copy()
                self.update_preview()
            except Exception as e:
                messagebox.showerror("错误", f"打开图片失败：{str(e)}")
    
    def resize_preview_image(self):
        """调整图片大小适配预览窗口"""
        max_width = 860
        max_height = 530
        width, height = self.original_image.size
        
        # 计算缩放比例
        scale = min(max_width/width, max_height/height, 1)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        self.preview_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def choose_color(self):
        """选择文字颜色"""
        color = colorchooser.askcolor(title="选择文字颜色", initialcolor=self.text_color.get())
        if color[1]:
            self.text_color.set(color[1])
    
    def apply_text(self):
        """应用文字到图片"""
        if not self.original_image:
            messagebox.showwarning("警告", "请先打开图片！")
            return
        
        try:
            # 复制原图避免叠加
            self.edited_image = self.original_image.copy()
            draw = ImageDraw.Draw(self.edited_image)
            
            # 设置字体（优先使用系统字体，兼容不同系统）
            try:
                # Windows系统
                font = ImageFont.truetype("simhei.ttf", self.text_size.get())
            except:
                try:
                    # Mac/Linux系统
                    font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", self.text_size.get())
                except:
                    # 备用字体
                    font = ImageFont.load_default(size=self.text_size.get())
            
            # 添加文字
            text = self.text_content.get()
            color = self.text_color.get()
            x = self.text_x.get()
            y = self.text_y.get()
            
            # 支持多行文字
            lines = text.split('\n')
            line_height = self.text_size.get() + 5
            for i, line in enumerate(lines):
                draw.text((x, y + i * line_height), line, font=font, fill=color)
            
            # 更新预览
            self.resize_preview_image()  # 重新调整大小
            self.update_preview()
            messagebox.showinfo("成功", "文字添加成功！")
        except Exception as e:
            messagebox.showerror("错误", f"添加文字失败：{str(e)}")
    
    def update_preview(self):
        """更新预览窗口"""
        # 生成预览图
        preview_edited = self.edited_image.resize(self.preview_image.size, Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(preview_edited)
        self.preview_label.config(image=self.tk_image)
        self.preview_label.image = self.tk_image
    
    def save_image(self):
        """保存制作好的表情包"""
        if not self.edited_image:
            messagebox.showwarning("警告", "请先打开并编辑图片！")
            return
        
        # 获取原文件名和路径
        if self.image_path:
            dir_name = os.path.dirname(self.image_path)
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            default_name = f"{base_name}_表情包.png"
        else:
            dir_name = ""
            default_name = "我的表情包.png"
        
        # 选择保存路径
        save_path = filedialog.asksaveasfilename(
            title="保存表情包",
            initialdir=dir_name,
            initialfile=default_name,
            filetypes=[("PNG图片", "*.png"), ("JPG图片", "*.jpg"), ("所有文件", "*.*")]
        )
        
        if save_path:
            try:
                # 补充文件后缀
                if not save_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    save_path += '.png'
                
                self.edited_image.save(save_path)
                messagebox.showinfo("成功", f"表情包已保存到：{save_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存图片失败：{str(e)}")

if __name__ == "__main__":
    # 检查依赖
    try:
        import PIL
    except ImportError:
        print("正在安装必要依赖...")
        os.system("pip install pillow")
        import PIL
    
    root = tk.Tk()
    app = MemeMaker(root)
    root.mainloop()
