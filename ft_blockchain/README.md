
# ft_blockchains

Cadena de Bloques con API Rest

Para ejecutar api rest:

`uvicorn blkapp:app --host=127.0.0.1 --port=8000`
> Agregar la opción `--reload`, mientras esté en desarrollo o debuging

Lanzar el navegador web con la URL:
_http://127.0.0.1:8000/docs_

Con Docker.
Construir la imagen (_blkc_).
```shell
docker build -t blkc .
docker run -ti --name blkc --rm -e PORT=8000 -p8000:8000 blkc
```