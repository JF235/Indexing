# Python Examples

## Docker

To run the Python examples in a Docker container, you can use the provided `Dockerfile` to build an image and run a container.

```bash
# Build the Docker image
docker build --label "owner=jfcm" -t jfcm_miniconda_cpu:2025.01.06 . -f Dockerfile

# Run the Docker container
docker run --name jfcm_miniconda_cpu_C --label "owner=jfcm" -v ${PWD}:/examples -it jfcm_miniconda_cpu:2025.01.06 /bin/bash
```

## Edit the examples

To edit the examples, you can use tools like `nano` or `vim` to edit the files.

For a more complete IDE, you can use `Visual Studio Code` with the `Dev Containers` extension.

`Ctrl+Shift+P` -> `Dev Containers: Attach to Running Container`


## Info

To see the installed packages, you can run the following command:

```bash
conda list
```