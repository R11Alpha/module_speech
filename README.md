# Modulo Basico de Voz

## Contenido
1. [Concepto](#concepto)
2. [Librerías](#librerias)
3. [Offline Whisper](#offline-whisper)

<a name="concepto"></a>
### Concepto

<a name="librerias"></a>
### Librerías

<a name="offline-whisper"></a>
### Offline Whisper

Para poder usar whisper completamente offline, se necesita descargar archivos necesarios que se pueden encontrar en las librerias que estan en el path de las librerías de python descargados. Tambien puedes descargar los archivos necesarios en este repositorio.

- ```Descargar los arhivos desde "__init__.py" y "openai_public.py":``` Todos los archivos que se mencionan se encuentran en el directorio "/.local/lib/python3.X/site-packages".
El archivo "__init__.py" se encuentra en la carpeta de Whisper:

![](https://github.com/R11Alpha/module_speech/blob/main/Resources/Whisper.gif)

El archivo "openai_public.py" se encuentra en la carpeta tiktoken_ext:

![](https://github.com/R11Alpha/module_speech/blob/main/Resources/Tiktoken.gif)

Una vez encontrados los archivos ya podras descargar los modelos que se encuentran en estos archivos, en el "__init__.py" podremos encontrar los modelos que Whisper usa. En el archivo "openai_public.py" se encuentran los archivos "vocab.bpe" y "encoder.json" que son muy importantes para que whisper pueda funcionar de manera completamente offline.

- ```Descargar los archivos de internet:``` Los archivos se pueden descargar desde los siguientes links:
```Modelos de Whisper:```

- tiny.en: https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt