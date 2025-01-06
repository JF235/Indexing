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

## Results

### Flat Indexing

- My Setup (Intel Core i7-5500U Dual-Core 2.4GHz)

```console
DB.shape: (1000000, 128), Q.shape: (100, 128)
IndexFlatL2: 326.51 ms
naive search (cpu): 1.19 s
Hash(indexes): 5fb8f22432f521449dd8d824f908f51d      
Hash(indexes_naive): 5fb8f22432f521449dd8d824f908f51d
Ok
```

- Google Colab

```console
DB.shape: (1000000, 128), Q.shape: (100, 128)
IndexFlatL2: 585.32 ms
naive search (cuda): 590.74 us
Hash(indexes): 5fb8f22432f521449dd8d824f908f51d
Hash(indexes_naive): 5fb8f22432f521449dd8d824f908f51d
Ok
```

### Flat Indexing GPU

- Google Colab

```console
DB.shape: (1000000, 128), Q.shape: (100, 128)
IndexFlatL2 CPU: 882.28 ms
IndexFlatL2 GPU: 29.33 ms
naive search (cuda): 622.70 us
Hash(indexes): 5fb8f22432f521449dd8d824f908f51d
Hash(indexes_naive): 5fb8f22432f521449dd8d824f908f51d
Ok
```

## Info

To see the installed packages, you can run the following command:

```bash
conda list
```