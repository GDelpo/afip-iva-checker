import tkinter as tk
from tkinter import filedialog, messagebox

from core.exceptions import ProcessingError
from orchestrator import run_book_comparison


class Application(tk.Frame):
    def __init__(self, root):
        # Colores personalizados
        self.bg_main_color = "#d2d3d4"
        self.bg_button_main_color = "#20a8d8"
        self.bg_font_color = "black"
        # Valores constantes
        self.archivo_default_value = "Ningún archivo seleccionado"
        self.carpeta_default_value = "Ninguna carpeta seleccionada"
        # Variables de estado
        self.archivo_ventas = tk.StringVar(value=self.archivo_default_value)
        self.archivo_alicuota = tk.StringVar(value=self.archivo_default_value)
        self.final_path = tk.StringVar(value=self.carpeta_default_value)
        self.current_page_index = 0
        # Definición de páginas
        self.pages = [self.etapa_1, self.etapa_2, self.etapa_3, self.etapa_4]

        super().__init__(root, bg=self.bg_main_color)
        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.load_main_widgets()

    def load_main_widgets(self):
        self.create_page_container()
        self.create_pager()
        self.pages[self.current_page_index]()  # Cargar la primera página

    def create_page_container(self):
        """Crea el contenedor principal de cada página."""
        self.page_container = tk.Frame(self.main_frame, background=self.bg_main_color)

        self.page_container.columnconfigure(0, weight=1)
        self.page_container.rowconfigure(0, weight=0)
        self.page_container.rowconfigure(1, weight=1)
        self.page_container.grid(column=0, row=0, sticky=tk.NSEW)

        self.title = tk.Label(
            self.page_container,
            background=self.bg_main_color,
            foreground="black",
            height=3,
            font=("Arial", 20, "bold"),
        )

        self.title.grid(column=0, row=0)

        self.content = tk.Label(
            self.page_container,
            background="white",
            foreground=self.bg_font_color,
            justify=tk.CENTER,
            anchor=tk.N,
            height=10,
            wraplength=550,
            font=("Arial", 14),
        )
        self.content.grid(
            column=0,
            row=1,
            sticky=tk.NSEW,
        )

        self.label = tk.Label(
            self.page_container,
            font=("Arial", 14),
            anchor=tk.N,
            wraplength=500,
            background="white",
            foreground="black",
        )
        self.label.columnconfigure(0, weight=1)
        self.label.rowconfigure(0, weight=0)
        self.label.rowconfigure(1, weight=1)
        self.label.grid(column=0, row=2, sticky=tk.NSEW)

        self.button = tk.Button(
            self.page_container,
            font=("Arial", 16),
            background=self.bg_button_main_color,
            foreground="white",
            activebackground=self.bg_button_main_color,
            activeforeground="white",
            highlightthickness=0,
            width=8,
            relief=tk.FLAT,
            cursor="hand2",
        )

        self.button.grid(column=0, row=3, sticky=tk.NSEW)

    def create_pager(self):
        """Crea los botones de navegación."""
        self.pager = tk.Frame(
            self.main_frame, bg=self.bg_main_color, height=50, pady=20
        )
        self.pager.columnconfigure([0, 1, 2], weight=1)
        self.pager.grid(column=0, row=1, sticky=tk.EW)

        self.prev_button = tk.Button(
            self.pager,
            text="Anterior",
            font=("Arial", 16),
            bg=self.bg_button_main_color,
            fg="white",
            relief=tk.FLAT,
            state=tk.DISABLED,
            cursor="hand2",
            command=lambda: self.change_page(-1),
        )
        self.prev_button.grid(column=0, row=0)

        self.page_number = tk.Label(
            self.pager,
            bg=self.bg_main_color,
            fg=self.bg_font_color,
            font=("Arial", 18),
            text=f"Etapa {self.current_page_index + 1} de {len(self.pages)}",
        )
        self.page_number.grid(column=1, row=0)

        self.next_button = tk.Button(
            self.pager,
            text="Siguiente",
            font=("Arial", 16),
            bg=self.bg_button_main_color,
            fg="white",
            relief=tk.FLAT,
            state=tk.DISABLED,
            cursor="hand2",
            command=lambda: self.change_page(1),
        )
        self.next_button.grid(column=2, row=0)

    def change_page(self, direction):
        """Cambia entre páginas según la dirección."""
        new_index = self.current_page_index + direction
        if 0 <= new_index < len(self.pages):
            self.current_page_index = new_index
            self.update_label()
            self.update_buttons()
            self.pages[self.current_page_index]()  # Carga la nueva página
            self.page_number.config(
                text=f"Etapa {self.current_page_index + 1} de {len(self.pages)}"
            )

    def update_buttons(self):
        """Actualiza el estado de los botones de navegación."""
        self.prev_button.config(
            state=tk.NORMAL if self.current_page_index > 0 else tk.DISABLED
        )
        self.next_button.config(
            state=tk.NORMAL if self.is_stage_ready() else tk.DISABLED
        )

    def is_stage_ready(self):
        """Verifica si la etapa actual tiene los datos necesarios."""
        if self.current_page_index == 0:
            return self.archivo_ventas.get() != self.archivo_default_value
        elif self.current_page_index == 1:
            return self.archivo_alicuota.get() != self.archivo_default_value
        elif self.current_page_index == 2:
            return self.final_path.get() != self.carpeta_default_value
        return True

    def get_name_label(self):
        """Obtiene el valor actual o el valor por defecto de cada etapa."""
        if self.current_page_index == 0:
            return self.archivo_ventas.get() or self.archivo_default_value
        elif self.current_page_index == 1:
            return self.archivo_alicuota.get() or self.archivo_default_value
        elif self.current_page_index == 2:
            return self.final_path.get() or self.carpeta_default_value
        return ""  # Por si la etapa es inválida

    def update_label(self):
        """Actualiza el texto de la etiqueta según la etapa actual."""
        self.label.config(text=self.get_name_label())

    def explorar_archivo(self, etapa_index):
        """Abre un diálogo para seleccionar un archivo o carpeta."""
        if etapa_index < 2:
            archivo = filedialog.askopenfilename(filetypes=[("Archivos TXT", "*.txt")])
            if archivo:
                if etapa_index == 0:
                    self.archivo_ventas.set(archivo)
                elif etapa_index == 1:
                    self.archivo_alicuota.set(archivo)
        else:
            carpeta = filedialog.askdirectory()
            if carpeta:
                self.final_path.set(carpeta)

        self.update_label()
        self.update_buttons()

    def etapa_1(self):
        """Primera etapa: Selección del archivo de ventas."""
        self.title.config(text="Seleccionar archivo de IVA Ventas CBTE")
        self.content.config(
            text="Los archivos de este tipo siguen el siguiente formato de nombre:\nventas_cbte_YYYYMM.txt\nEjemplo: ventas_cbte202210.txt"
        )
        self.update_label()
        self.button.config(
            text="Seleccionar archivo", command=lambda: self.explorar_archivo(0)
        )

    def etapa_2(self):
        """Segunda etapa: Selección del archivo de alícuotas."""
        self.title.config(text="Seleccionar archivo de IVA Ventas Alícuotas")
        self.content.config(
            text="Los archivos de este tipo siguen el siguiente formato de nombre:\nventas_alicuota_YYYYMM.txt\nEjemplo: ventas_alicuota_202210.txt"
        )
        self.button.config(
            text="Seleccionar archivo", command=lambda: self.explorar_archivo(1)
        )

    def etapa_3(self):
        """Tercera etapa: Selección de la carpeta de destino."""
        self.title.config(text="Seleccionar carpeta de destino")
        self.content.config(
            text="Seleccione la carpeta en la que se guardarán los archivos finales: el archivo modificado y el reporte en formato .json."
        )
        self.button.config(
            text="Seleccionar carpeta", command=lambda: self.explorar_archivo(2)
        )

    def etapa_4(self):
        """Cuarta etapa: Confirmación y ejecución del proceso."""
        self.title.config(text="Confirmar y ejecutar proceso")
        self.content.config(
            text="Ejecute el proceso una vez seleccionados los archivos correspondientes y la carpeta destino."
        )
        self.button.config(text="Ejecutar proceso", command=self.ejecutar_proceso)
        self.next_button.config(state=tk.DISABLED)

    def ejecutar_proceso(self):
        """Ejecuta el proceso y maneja errores."""
        ventas = self.archivo_ventas.get()
        alicuota = self.archivo_alicuota.get()
        destino = self.final_path.get()

        if (
            ventas == self.archivo_default_value
            or alicuota == self.archivo_default_value
            or destino == self.carpeta_default_value
        ):
            messagebox.showerror(
                "Error", "Debe seleccionar ambos archivos y la carpeta de destino."
            )
            return

        try:
            resultado, message = run_book_comparison(
                book_1_file_path=ventas,
                book_1_key="libro_iva_digital_ventas_cbte",
                book_2_file_path=alicuota,
                book_2_key="libro_iva_digital_ventas_alicuota",
                output_folder_path=destino,
            )
            messagebox.showinfo("Resultado", message)
        except ProcessingError as e:
            messagebox.showerror("Error de procesamiento", e.message)
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Procesamiento de Archivos IVA Ventas AFIP")
    root.geometry("600x350")
    app = Application(root)
    root.mainloop()
