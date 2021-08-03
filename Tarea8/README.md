# Editor

## Adrián García Pérez - 315131224

El editor fue programado utilizando Python 3 y Tkinter, ejecutado en
Ubuntu 20.04.

## Instalación manual

### Instalación de Python

```sh
sudo apt install python3
```

### Instalación de Tkinter

```sh
sudo apt install python-tk
```

### Instalación de PIP

```sh
sudo apt install python-pip
```

### Instalación de Pillow

```sh
sudo pip install pillow
```

### Instalación de Numpy

```sh
sudo pip install numpy
```

### Instalación de Pyinstaller

```sh
sudo pip install pyinstaller
```

## Instalación con make

Se puede utilizar la herramienta de make para realizar todos los comandos
anteriores fácilmente, al hacer:

```sh
make install
```

## Ejecución

Para ejecutar el programa, puede hacerse desde consola:

```sh
make run
```

O también se puede generar el archivo ejecutable con Pyinstaller y posteriormente
ejecutarse:

```sh
make ex && ./dist/Editor
```

Así, el programa inicia con tres opciones en la parte superior,
donde la primera nos permite elegir una imagen desde el almacenamiento,
y la segunda permite elegir el filtro de dithering deseado.

Finalmente, la imagen generada puede guardarse en el almacenamiento
con la pestaña File > Save y también se crea automáticamente la
imagen en out.jpg
