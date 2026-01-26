import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .logic import split_pdf
from PIL import Image, ImageTk
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

class PDFSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter Pro")
        self.root.geometry("520x420")
        self.root.resizable(False, False)
        self.root.configure(bg='#2C2C2C')
        self.pdf_path = None
        
        # Establecer icono de la ventana
        try:
            import sys
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, 'assets', 'icon.png')
            else:
                icon_path = os.path.join('assets', 'icon.png')
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((32, 32), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, icon_photo)
            self.root.icon_photo = icon_photo
        except Exception:
            pass  # Si no se encuentra el icono, continuar sin él

        # Frame principal con fondo gris oscuro elegante
        self.frame = tk.Frame(self.root, bg='#F5F5F5', relief='flat')
        self.frame.pack(fill='both', expand=True, padx=2, pady=2)

        # Barra superior roja elegante
        header = tk.Frame(self.frame, bg='#D32F2F', height=85)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título profesional
        title_label = tk.Label(header, text="PDF Splitter Pro", 
                              font=('Segoe UI', 22, 'bold'), bg='#D32F2F', fg='white')
        title_label.pack(pady=(15, 5))

        subtitle_label = tk.Label(header, text="Herramienta profesional para dividir documentos PDF", 
                                 font=('Segoe UI', 9), bg='#D32F2F', fg='white')
        subtitle_label.pack(pady=(0, 5))

        # Contenedor principal con fondo blanco
        main_container = tk.Frame(self.frame, bg='white')
        main_container.pack(fill='both', expand=True, padx=25, pady=20)

        # Área de arrastre con borde discontinuo elegante
        self.drop_canvas = tk.Canvas(main_container, width=450, height=100, bg='#FAFAFA', highlightthickness=0)
        self.drop_canvas.pack(pady=(0, 15))
        
        # Crear borde discontinuo (dashed)
        dash_pattern = (8, 4)  # 8 píxeles de línea, 4 de espacio
        self.drop_canvas.create_rectangle(5, 5, 445, 95, outline='#E57373', width=2, dash=dash_pattern)
        
        # Icono PNG de la app redimensionado dentro del recuadro
        try:
            import sys
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, 'assets', 'icon.png')
            else:
                icon_path = os.path.join('assets', 'icon.png')
            # Abrir PNG con transparencia completa
            app_icon_img = Image.open(icon_path)
            if app_icon_img.mode != 'RGBA':
                app_icon_img = app_icon_img.convert('RGBA')
            app_icon_img = app_icon_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.app_icon_photo = ImageTk.PhotoImage(app_icon_img)
            # Canvas sin borde y con fondo igual al área de arrastre
            self.icon_canvas = tk.Canvas(self.drop_canvas, width=40, height=40, 
                                       bg='#FAFAFA', highlightthickness=0, bd=0, relief='flat')
            self.icon_canvas.place(x=15, y=30)
            self.icon_canvas.create_image(20, 20, image=self.app_icon_photo, anchor='center')
        except Exception:
            pass  # Si no se encuentra el icono, continuar sin él

        # Texto de arrastre elegante
        self.drop_text = self.drop_canvas.create_text(260, 50, 
                                                       text="Arrastra tu archivo PDF aquí o haz clic para seleccionar", 
                                                       fill='#757575', font=('Segoe UI', 10))
        
        # Hacer clickeable toda el área
        self.drop_canvas.bind('<Button-1>', self.select_pdf)
        self.drop_canvas.config(cursor='hand2')
        
        # Configurar drag and drop
        self.setup_drag_drop()
        
        # Efecto hover leve para la zona de arrastre
        # Efecto hover leve para la zona de arrastre
        def drop_on_enter(e):
            if self.pdf_path: return
            self.drop_canvas.config(bg='#FFEBEE')  # Rojo muy suave
            if hasattr(self, 'icon_canvas'):
                self.icon_canvas.config(bg='#FFEBEE')
        def drop_on_leave(e):
            if self.pdf_path: return
            self.drop_canvas.config(bg='#FAFAFA')  # Fondo original
            if hasattr(self, 'icon_canvas'):
                self.icon_canvas.config(bg='#FAFAFA')
        self.drop_canvas.bind('<Enter>', drop_on_enter)
        self.drop_canvas.bind('<Leave>', drop_on_leave)

        # Información del archivo seleccionado
        self.info_label = tk.Label(main_container, text="No hay archivo seleccionado", 
                                   bg='white', fg='#9E9E9E', font=('Segoe UI', 9))
        self.info_label.pack(pady=(0, 15))

        # Frame de selección de páginas elegante
        page_container = tk.Frame(main_container, bg='white')
        page_container.pack(pady=(0, 20))

        # Página inicial con diseño minimalista
        start_frame = tk.Frame(page_container, bg='#FFEBEE', relief='flat', borderwidth=0)
        start_frame.grid(row=0, column=0, padx=10)
        
        tk.Label(start_frame, text="Página inicial", bg='#FFEBEE', fg='#D32F2F', 
                font=('Segoe UI', 9, 'bold')).pack(pady=(10, 2))
        self.start_entry = tk.Entry(start_frame, width=7, font=('Segoe UI', 18, 'bold'), justify='center', 
                                    bg='white', fg='#D32F2F', relief='flat', borderwidth=2, 
                                    highlightthickness=2, highlightbackground='#D32F2F', highlightcolor='#D32F2F',
                                    insertbackground='#D32F2F')
        self.start_entry.pack(pady=(2, 10), padx=20)

        # Flecha elegante
        arrow_label = tk.Label(page_container, text="→", bg='white', fg='#D32F2F', 
                              font=('Segoe UI', 22, 'bold'))
        arrow_label.grid(row=0, column=1, padx=10)

        # Página final con diseño minimalista
        end_frame = tk.Frame(page_container, bg='#FFEBEE', relief='flat', borderwidth=0)
        end_frame.grid(row=0, column=2, padx=10)
        
        tk.Label(end_frame, text="Página final", bg='#FFEBEE', fg='#D32F2F', 
                font=('Segoe UI', 9, 'bold')).pack(pady=(10, 2))
        self.end_entry = tk.Entry(end_frame, width=7, font=('Segoe UI', 18, 'bold'), justify='center', 
                                  bg='white', fg='#D32F2F', relief='flat', borderwidth=2,
                                  highlightthickness=2, highlightbackground='#D32F2F', highlightcolor='#D32F2F',
                                  insertbackground='#D32F2F')
        self.end_entry.pack(pady=(2, 10), padx=20)

        # Botón de dividir profesional con margen adecuado
        self.split_btn = tk.Button(main_container, text="DIVIDIR PDF", command=self.split_pdf, 
                                   font=('Segoe UI', 12, 'bold'), bg='#D32F2F', fg='#FFFFFF', 
                                   activebackground='#B71C1C', activeforeground='#FFFFFF',
                                   relief='flat', cursor='hand2', state='disabled',
                                   padx=50, pady=14, borderwidth=0, disabledforeground='#FFFFFF')
        self.split_btn.pack(pady=(0, 10))
        
        # Efecto hover para el botón
        def on_enter(e):
            self.split_btn.config(bg='#B71C1C', fg='#FFFFFF')
        def on_leave(e):
            self.split_btn.config(bg='#D32F2F', fg='#FFFFFF')
        self.split_btn.bind('<Enter>', on_enter)
        self.split_btn.bind('<Leave>', on_leave)
        
        # Texto de ayuda discreto
        help_label = tk.Label(main_container, text="Tip: Presiona Ctrl+V para pegar la ruta del archivo", 
                             bg='white', fg='#BDBDBD', font=('Segoe UI', 8))
        help_label.pack(pady=(5, 0))

        # Atajo de teclado
        self.root.bind('<Control-v>', self.paste_pdf)

    def setup_drag_drop(self):
        """Configurar drag and drop para archivos PDF"""
        if DND_AVAILABLE:
            # Configurar drag and drop con tkinterdnd2
            self.drop_canvas.drop_target_register(DND_FILES)
            self.drop_canvas.dnd_bind('<<Drop>>', self.on_drop)
            self.drop_canvas.dnd_bind('<<DragEnter>>', self.on_drag_enter)
            self.drop_canvas.dnd_bind('<<DragLeave>>', self.on_drag_leave)

    def on_drag_enter(self, event):
        """Cuando se arrastra un archivo sobre el área"""
        self.drop_canvas.config(bg='#E3F2FD')  # Azul claro para indicar drop zone
        if hasattr(self, 'icon_canvas'):
            self.icon_canvas.config(bg='#E3F2FD')

    def on_drag_leave(self, event):
        """Cuando se sale del área de arrastre"""
        self.drop_canvas.config(bg='#FAFAFA')
        if hasattr(self, 'icon_canvas'):
            self.icon_canvas.config(bg='#FAFAFA')

    def on_drop(self, event):
        """Cuando se suelta un archivo"""
        try:
            # Restaurar color normal
            self.drop_canvas.config(bg='#FAFAFA')
            if hasattr(self, 'icon_canvas'):
                self.icon_canvas.config(bg='#FAFAFA')
            
            # Obtener archivos arrastrados
            files = self.root.tk.splitlist(event.data)
            
            # Buscar el primer archivo PDF
            for file_path in files:
                # Limpiar la ruta de archivos (quitar llaves si las tiene)
                file_path = file_path.strip('{}')
                if file_path.lower().endswith('.pdf') and os.path.isfile(file_path):
                    self.set_pdf(file_path)
                    break
        except Exception as e:
            print(f"Error en drag & drop: {e}")
            pass

    def select_pdf(self, event=None):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.set_pdf(path)

    def paste_pdf(self, event):
        # Permite pegar ruta desde portapapeles
        try:
            path = self.root.clipboard_get()
            if os.path.isfile(path) and path.lower().endswith('.pdf'):
                self.set_pdf(path)
        except:
            pass

    def set_pdf(self, path):
        self.pdf_path = path
        filename = os.path.basename(path)
        
        try:
            # Obtener el número de páginas
            _, num_pages = split_pdf(path, 1, 1, os.devnull)
            self.num_pages = num_pages
            
            # Cambiar a estado de éxito con diseño elegante
            self.drop_canvas.config(bg='#E8F5E9')
            self.icon_canvas.config(bg='#E8F5E9')
            
            # Cambiar borde a verde
            self.drop_canvas.delete('all')
            dash_pattern = (8, 4)
            self.drop_canvas.create_rectangle(5, 5, 445, 95, outline='#4CAF50', width=2, dash=dash_pattern)
            
            # Cambiar icono a checkmark mejorado
            self.icon_canvas.delete('all')
            # Fondo del círculo verde
            self.icon_canvas.create_oval(8, 8, 32, 32, fill='#4CAF50', outline='#388E3C', width=1)
            # Tick verde más suave y profesional
            self.icon_canvas.create_line(13, 20, 17, 24, fill='white', width=3, capstyle='round')
            self.icon_canvas.create_line(17, 24, 27, 14, fill='white', width=3, capstyle='round')
            
            # Botón X para quitar archivo (esquina superior derecha del canvas)
            self.clear_btn_canvas = tk.Canvas(self.drop_canvas, width=20, height=20, 
                                            bg='#E8F5E9', highlightthickness=0, bd=0, relief='flat')
            self.clear_btn_canvas.place(x=420, y=10)
            # Solo círculo rojo para la X (sin fondo del canvas)
            self.clear_btn_canvas.create_oval(2, 2, 18, 18, fill='#F44336', outline='#D32F2F', width=1)
            # X blanca
            self.clear_btn_canvas.create_line(6, 6, 14, 14, fill='white', width=2, capstyle='round')
            self.clear_btn_canvas.create_line(14, 6, 6, 14, fill='white', width=2, capstyle='round')
            # Hacer clickeable
            self.clear_btn_canvas.bind('<Button-1>', self.clear_pdf)
            self.clear_btn_canvas.config(cursor='hand2')
            # Hover effect para el botón X
            def clear_on_enter(e):
                self.clear_btn_canvas.config(bg='#E8F5E9')  # Mantener fondo igual
                self.clear_btn_canvas.delete('all')
                self.clear_btn_canvas.create_oval(2, 2, 18, 18, fill='#D32F2F', outline='#B71C1C', width=1)
                self.clear_btn_canvas.create_line(6, 6, 14, 14, fill='white', width=2, capstyle='round')
                self.clear_btn_canvas.create_line(14, 6, 6, 14, fill='white', width=2, capstyle='round')
            def clear_on_leave(e):
                self.clear_btn_canvas.config(bg='#E8F5E9')  # Mantener fondo igual
                self.clear_btn_canvas.delete('all')
                self.clear_btn_canvas.create_oval(2, 2, 18, 18, fill='#F44336', outline='#D32F2F', width=1)
                self.clear_btn_canvas.create_line(6, 6, 14, 14, fill='white', width=2, capstyle='round')
                self.clear_btn_canvas.create_line(14, 6, 6, 14, fill='white', width=2, capstyle='round')
            self.clear_btn_canvas.bind('<Enter>', clear_on_enter)
            self.clear_btn_canvas.bind('<Leave>', clear_on_leave)
            
            # Actualizar texto en el canvas
            if len(filename) > 40:
                filename = filename[:37] + '...'
            self.drop_canvas.create_text(260, 50, 
                                         text=f"Archivo cargado: {filename}\n{num_pages} página{'s' if num_pages > 1 else ''}", 
                                         fill='#2E7D32', font=('Segoe UI', 10, 'bold'), justify='center')
            
            # Actualizar información
            self.info_label.config(text=f"✓ Listo para dividir ({num_pages} páginas)", fg='#4CAF50', font=('Segoe UI', 9, 'bold'))
            
            # Habilitar botón
            self.split_btn.config(state='normal', bg='#D32F2F')
            
            # Rellenar campos
            self.start_entry.delete(0, tk.END)
            self.end_entry.delete(0, tk.END)
            self.start_entry.insert(0, '1')
            self.end_entry.insert(0, str(self.num_pages))
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el PDF:\n{e}")
            
            # Estado de error elegante
            self.drop_canvas.config(bg='#FFEBEE')
            self.icon_canvas.config(bg='#FFEBEE')
            
            # Cambiar borde a rojo
            self.drop_canvas.delete('all')
            dash_pattern = (8, 4)
            self.drop_canvas.create_rectangle(5, 5, 445, 95, outline='#F44336', width=2, dash=dash_pattern)
            
            # Icono de error
            self.icon_canvas.delete('all')
            self.icon_canvas.create_oval(12, 12, 38, 38, fill='#F44336', outline='#D32F2F', width=2)
            self.icon_canvas.create_text(25, 25, text='✗', fill='white', font=('Segoe UI', 16, 'bold'))
            
            # Texto de error
            self.drop_canvas.create_text(260, 50, 
                                         text="Error al cargar el archivo\nIntenta con otro PDF", 
                                         fill='#C62828', font=('Segoe UI', 10), justify='center')
            
            self.info_label.config(text="✗ Error al cargar el archivo", fg='#F44336', font=('Segoe UI', 9, 'bold'))

    def clear_pdf(self, event=None):
        """Limpiar archivo cargado y restaurar estado inicial"""
        self.pdf_path = None
        self.num_pages = None
        
        # Restaurar estado inicial del canvas
        self.drop_canvas.config(bg='#FAFAFA')
        if hasattr(self, 'icon_canvas'):
            self.icon_canvas.config(bg='#FAFAFA')
        
        # Limpiar canvas y restaurar elementos iniciales
        self.drop_canvas.delete('all')
        
        # Recrear borde discontinuo original
        dash_pattern = (8, 4)
        self.drop_canvas.create_rectangle(5, 5, 445, 95, outline='#E57373', width=2, dash=dash_pattern)
        
        # Restaurar icono original de la app
        if hasattr(self, 'app_icon_photo'):
            self.icon_canvas.delete('all')
            self.icon_canvas.create_image(20, 20, image=self.app_icon_photo, anchor='center')
        
        # Restaurar texto original
        self.drop_text = self.drop_canvas.create_text(260, 50, 
                                                       text="Arrastra tu archivo PDF aquí o haz clic para seleccionar", 
                                                       fill='#757575', font=('Segoe UI', 10))
        
        # Quitar botón X si existe
        if hasattr(self, 'clear_btn_canvas'):
            self.clear_btn_canvas.destroy()
            delattr(self, 'clear_btn_canvas')
        
        # Restaurar estado de la información
        self.info_label.config(text="No hay archivo seleccionado", fg='#9E9E9E', font=('Segoe UI', 9))
        
        # Deshabilitar botón de dividir
        self.split_btn.config(state='disabled')
        
        # Limpiar campos de entrada
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)

    def split_pdf(self):
        if not self.pdf_path:
            return
        try:
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())
            if start < 1 or end > self.num_pages or start > end:
                messagebox.showerror("Error", "Rango de páginas inválido.")
                return
            out_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=f"split_{start}-{end}.pdf")
            if out_path:
                split_pdf(self.pdf_path, start, end, out_path)
                messagebox.showinfo("Éxito", f"PDF guardado en {out_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo dividir el PDF: {e}")