Here is a well-structured README for your repository:

---

# Compressor MPI

This repository contains a set of scripts for compressing and decompressing files using a custom algorithm, along with verification and MPI parallelization enhancements.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Scripts Overview](#scripts-overview)
  - [compresor.py](#compresorpy)
  - [compresorp.py](#compresorppy)
  - [descompresor.py](#descompresorpy)
  - [descompresorp.py](#descompresorppy)
  - [verificador.py](#verificadorpy)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project provides tools to compress and decompress files using a custom compression algorithm. Additionally, there are parallelized versions of the compression and decompression scripts using MPI (Message Passing Interface). The repository also includes a script to verify the integrity of the compressed and decompressed files.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Sconstante/Constante_Mendoza_Saenz.git
    ```

2. Navigate to the project directory:
    ```sh
    cd Constante_Mendoza_Saenz
    ```

3. (Optional) Set up a virtual environment:
    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

4. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

The scripts are designed to be run from the command line with specific arguments. Below are the usage instructions for each script.

### Scripts Overview

#### compresor.py

This script compresses a given file using a custom compression algorithm.

**Usage:**
```sh
python compresor.py <input_file>
```

**Example:**
```sh
python compresor.py example.txt
```

#### compresorp.py

This is the MPI parallelized version of the `compresor.py` script.

**Usage:**
```sh
mpiexec -n <number_of_processes> python compresorp.py <input_file>
```

**Example:**
```sh
mpiexec -n 4 python compresorp.py example.txt
```

#### descompresor.py

This script decompresses a given file that was compressed using `compresor.py`.

**Usage:**
```sh
python descompresor.py <compressed_file>
```

**Example:**
```sh
python descompresor.py comprimido.elmejorprofesor
```

#### descompresorp.py

This is the MPI parallelized version of the `descompresor.py` script.

**Usage:**
```sh
mpiexec -n <number_of_processes> python descompresorp.py <compressed_file>
```

**Example:**
```sh
mpiexec -n 4 python descompresorp.py comprimido.elmejorprofesor
```

#### verificador.py

This script verifies the integrity of the original and decompressed files by comparing their contents.

**Usage:**
```sh
python verificador.py <original_file> <decompressed_file>
```

**Example:**
```sh
python verificador.py example.txt descomprimido-elmejorprofesor.txt
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to modify the README to better suit your needs.
