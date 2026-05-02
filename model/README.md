# Model Pipeline

Pipeline modular para Sign Language MNIST.

## Estructura

- `model_pipeline/data.py`: carga y split de datos
- `model_pipeline/model.py`: definicion CNN y genoma
- `model_pipeline/search_ga.py`: busqueda genetica
- `model_pipeline/train.py`: entrenamiento/evaluacion
- `model_pipeline/export.py`: export de artefactos
- `model_pipeline/infer.py`: inferencia por imagen
- `model_pipeline/cli.py`: interfaz CLI

## Instalar

```bash
py -m pip install -r requirements.txt
```

## Uso CLI

```bash
py -m model_pipeline --help
py -m model_pipeline search --data-dir <ruta_csv_sign_mnist>
py -m model_pipeline train-final --data-dir <ruta_csv_sign_mnist> --genome 1 1 1 1 2 --output-dir model/artifacts
py -m model_pipeline infer --image-path <imagen.png> --artifacts-dir model/artifacts
```

## Ejecutable

```bash
py -m PyInstaller --onefile --name sign_infer build_executable.py
```

El binario queda en `model/dist/sign_infer.exe`.
