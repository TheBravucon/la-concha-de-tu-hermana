🪟 Aplicación Tkinter con ttkbootstrap, pandas y SQLite

Esta aplicación utiliza Tkinter con el tema moderno ttkbootstrap, junto con pandas para manejo de datos y SQLite3 como base de datos local.
Permite ejecutar el programa tanto desde el entorno de desarrollo como en formato ejecutable .exe.

📦 Requisitos previos

Antes de comenzar, asegúrate de tener instalado Python 3.9 o superior en tu sistema.
Puedes verificarlo ejecutando:

python --version


o en algunos sistemas:

python3 --version

⚙️ Instalación de dependencias

Abre una terminal o consola en la carpeta del proyecto.

Ejecuta el siguiente comando para instalar las librerías necesarias:

pip install ttkbootstrap pandas pyinstaller


💡 Nota: No necesitas instalar sqlite3 porque ya viene incluido con Python.

▶️ Ejecución del proyecto

Para ejecutar el programa directamente desde el código fuente:

python main.py


Si usas Linux o macOS, podrías necesitar:

python3 main.py

🧱 Empaquetado a ejecutable (.exe)

Puedes crear un archivo ejecutable autónomo (sin necesidad de tener Python instalado) utilizando PyInstaller.

Ejecuta el siguiente comando dentro de la carpeta del proyecto:

pyinstaller --onefile --windowed --add-data "productos.py;." --add-data "ticket.py;." --add-data "usuarios.py;." main.py

📁 Resultado

El ejecutable se generará dentro de la carpeta dist/.

Por ejemplo:

dist/main.exe


Puedes mover este archivo .exe a cualquier ubicación y ejecutarlo directamente.

🧰 Opcional: Limpieza de archivos temporales

PyInstaller genera carpetas y archivos adicionales (build/, .spec, etc.).
Puedes eliminarlos con:

rmdir /s /q build
del main.spec


o en Linux/macOS:

rm -rf build main.spec

🧾 Dependencias utilizadas
Librería	Descripción breve
ttkbootstrap	Estilos modernos para interfaces Tkinter
pandas	Manejo y análisis de datos en tablas
sqlite3	Base de datos embebida incluida en Python
pyinstaller	Empaquetado de scripts Python a ejecutables .exe

🪪 Autor

Tomas Bravi

💻 Final de programación desarrollado en Python