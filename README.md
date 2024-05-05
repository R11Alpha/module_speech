# Modulo Basico de Voz

## Contenido
1. [Concepto](#concepto)
2. [Librerías](#librerias)
3. [Offline Whisper](#offline-whisper)
4. [Entorno Conda](#entorno-conda)

<a name="concepto"></a>
### Concepto

Este script funciona como un modulo básico del robot de servicio Markovito. Esta diseñado para que el script funcione como el dispositivo Alexa en donde el usuario mande a llamar al script con una palabra clave y el robot pueda avisar al usuario por medio de otro modulo que esta almacenado en la unidad abordo del robot llamado ```/pocket_listener/talk``` mandando un mensaje de formato String a este modulo para que diga las palabras "yes" para avisar que ya esta grabando y "ok" para avisar que ya dejo de grabar. Igualmente el script de whisper manda la información a otro script que procesa el texto crudo que obtiene de la voz al script ```speech_basicmodule.py``` para que pueda saber que texto es considerado un comando de stop, o un comando con complejidad para que el robot pueda hacer las actividades dictadas por el usuario.

<a name="librerias"></a>
### Librerías

- ```Whisper AI:``` Para instalar esta librería hay que copiar y pegar estos comandos en la terminal de Ubuntu.

    Utilizamos Python 3.9.9 y [PyTorch](https://pytorch.org/) 1.10.1 para entrenar y probar nuestros modelos, pero se espera que la base de código sea compatible con Python 3.8-3.11 y versiones recientes de PyTorch. La base de código también depende de algunos paquetes de Python, especialmente de [OpenAI's tiktoken](https://github.com/openai/tiktoken) para su implementación de tokenizador rápido. Puedes descargar e instalar (o actualizar a) la última versión de Whisper con el siguiente comando:

        pip install -U openai-whisper

    Alternativamente, el siguiente comando descargará e instalará el último commit de este repositorio, junto con sus dependencias de Python.

        pip install git+https://github.com/openai/whisper.git

    Para actualizar el paquete a la última versión de este repositorio, por favor ejecuta:

        pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

    También requiere que la herramienta de línea de comandos ['ffmpeg'](https://ffmpeg.org/) esté instalada en tu sistema, la cual está disponible en la mayoría de los gestores de paquetes:

        sudo apt update && sudo apt install ffmpeg

- ```SpeechRecognition:``` Esta librería sirve para poder utilizar el microfono y transcribir lo que recibe el microfono en tiempo real sin necesidad de estar guardando la información de voz en archivos de audio. Para instalarlo utilizamos el siguiente comando en la terminal.

        pip install SpeechRecognition

- ```PyAudio:``` Esta librería sirve para abrir el microfono y empezar a grabar según el tiempo que se necesite para capturar la voz y transcribir el audio a texto.

        pip install PyAudio

- ```SoundDevice:``` Esta librería sirve para eliminar los avisos de advertencia de los drivers de ALSA y evitar futuros problemas en nuestro script.

        pip install sounddevice

- ```Wave:``` Esta librería sirve para guardar la información en formato de audio en un archivo .wav para que sirva para transcribir el audio a texto.

        pip install Wave

<a name="offline-whisper"></a>
### Offline Whisper

Para poder usar whisper completamente offline, se necesita descargar archivos necesarios que se pueden encontrar en las librerias que estan en el path de las librerías de python descargados. Tambien puedes descargar los archivos necesarios en este repositorio.

- ```Descargar los arhivos desde __init__.py y openai_public.py:``` Todos los archivos que se mencionan se encuentran en el directorio "/.local/lib/python3.X/site-packages".
El archivo ```__init__.py``` se encuentra en la carpeta de Whisper:

![](https://github.com/R11Alpha/module_speech/blob/main/Resources/Whisper.gif)

El archivo ```openai_public.py``` se encuentra en la carpeta tiktoken_ext:

![](https://github.com/R11Alpha/module_speech/blob/main/Resources/Tiktoken.gif)

Una vez encontrados los archivos ya podras descargar los modelos que se encuentran en estos archivos, en el ```__init__.py``` podremos encontrar los modelos que Whisper usa. En el archivo ```openai_public.py``` se encuentran los archivos ```vocab.bpe``` y ```encoder.json``` que son muy importantes para que whisper pueda funcionar de manera completamente offline.

- ```Descargar los modelos de Whisper AI de internet:``` Los modelos se pueden descargar desde los siguientes links:

    - tiny.en: https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt

    - tiny: https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt

    - base.en: https://openaipublic.azureedge.net/main/whisper/models/25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead/base.en.pt

    - base: https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt

    - small.en: https://openaipublic.azureedge.net/main/whisper/models/f953ad0fd29cacd07d5a9eda5624af0f6bcf2258be67c92b79389873d91e0872/small.en.pt

    - small: https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt

    - medium.en: https://openaipublic.azureedge.net/main/whisper/models/d7440d1dc186f76616474e0ff0b3b6b879abc9d1a4926b7adfa41db2d497ab4f/medium.en.pt

    - medium: https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt

    - large-v1: https://openaipublic.azureedge.net/main/whisper/models/e4b87e7e0bf463eb8e6956e646f1e277e901512310def2c24bf0e11bd3c28e9a/large-v1.pt

    - large-v2: https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt

    - large-v3: https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt

    - large: https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt

Hay que recordar que mientras mas grande sea el modelo a utilizar mucho mayor será el uso de recursos computacionales que tendra que usar.

|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
|:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |

- ```Descargar "vocab.bpe" y encoder.json:``` Estos modelos son los que se descargan para el archivo ```openai_public.py``` y se pueden descargar de los siguientes links:

    - encoder.json: https://openaipublic.blob.core.windows.net/gpt-2/encodings/main/encoder.json

    - vocab.bpe: https://openaipublic.blob.core.windows.net/gpt-2/encodings/main/vocab.bpe

- ```Implementar los modelos descargados en nuestro codigo y en nuestras librerias:``` En este caso primero sustituiremos los links que estan en el archivo de ```openai_public.py``` por el directorio en donde se encuentran los archivos ```encoder.json``` y ```vocab.bpe``` (Una recomendación es poner los archivos descargados dentro de la carpeta de whisper para tener un orden y no sea tan complicado buscar los archivos).

![](https://github.com/R11Alpha/module_speech/blob/main/Resources/tik.gif)

<a name="entorno-conda"></a>
### Entorno Conda

