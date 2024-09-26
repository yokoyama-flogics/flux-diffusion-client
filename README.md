# Black Forest Labs FLUX.1 Diffusion Model Python Client

A Python and Bash toolkit for interacting with the Black Forest Labs FLUX.1 Diffusion Model API

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Command-Line Arguments](#command-line-arguments)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Introduction

This Black Forest Labs FLUX.1 Diffusion Model Python Client is a Python script and macOS-specific Bash wrapper that facilitate easy interaction with the FLUX.1 Diffusion Model API as of September 2024. It allows users to input prompts directly from the clipboard, offers flexible seed value options, and provides verbose logging for better insights and debugging.

## Features

- **Bash Wrapper (macOS Only)**: Use `pbpaste` to pipe clipboard content directly to the Python script. Ideal for macOS users who copy prompt text using Cmd-C. Simplifies usage with confirmation prompts and argument handling.
- **Flexible Seed Handling**: Support for random, fixed, and null seed values.
- **Verbose Mode**: Enable detailed logging for debugging and insights.

## Installation

### Prerequisites

- **Python 3**: Ensure you have Python installed. Tested with Python 3.11.8.
- **pip**: Python package installer.

### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yokoyama-flogics/flux-diffusion-client.git
    cd flux-diffusion-client
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Make Bash Wrapper Executable**

    ```bash
    chmod +x gen_flux.sh
    ```

## Configuration

### Environment Variables

Create a `.env` file in your home directory or the project root directory and add your FLUX.1 API key:

```dotenv
BFL_API_KEY=your_api_key_here
```

### Python Script Configuration

Ensure that the Python script (`flux.py`) has access to the `.env` file for loading environment variables.

## Usage

### Using the Python Script Directly

You can run the Python script and provide the prompt via standard input:

```bash
echo "A beautiful sunset over the ocean." | python3 flux.py --width 800 --height 640
```

**Output:**

- Results are stored in the `output` directory in the current working directory.
- If the `output` directory does not exist, it is created automatically.
- Filenames include a timestamp followed by suffixes such as `_request.json`, `_result.json`, and `_result.jpg`.

### Using the Bash Wrapper (macOS Only)

The Bash wrapper simplifies usage by handling clipboard input and confirmation prompts. It is designed specifically for macOS.

#### Interactive Mode with Confirmation

```bash
./gen_flux.sh -wd 800 -ht 640
```

You will be prompted:
```
Are you sure you want to proceed? [y/N]:
```

#### Silent Mode Without Confirmation

```bash
./gen_flux.sh -y -wd 1024 -ht 768 --seed rand
```

#### Displaying Help

```bash
./gen_flux.sh -h
```

*This will display the help message from the Python script without prompting for confirmation.*

## Command-Line Arguments

### Python Script (`flux.py`)

| Argument              | Short | Description                                                                                       | Default        |
|-----------------------|-------|---------------------------------------------------------------------------------------------------|----------------|
| `--width`             | `-wd` | Width of the image in pixels                                                                       | `1024`         |
| `--height`            | `-ht` | Height of the image in pixels                                                                      | `1024`         |
| `--variant`           | `-v`  | Variant of the diffusion model                                                                     | `flux.1-pro`   |
| `--steps`             | `-s`  | Number of network evaluations. Higher values improve quality but increase computation time.         | `25`           |
| `--prompt_upsampling` | `-pu` | Enable prompt upsampling to improve image quality and fidelity to the prompt.                       | `False`        |
| `--seed`              |       | Fix the generation seed: provide an integer, `rand` to generate a random seed, or `null` to pass null.| `rand`         |
| `--guidance`          | `-g`  | Guidance scale to control the fidelity and creativity of the generated image. Higher values adhere more strictly to the prompt.| `2.5` |
| `--safety_tolerance`  | `-st` | Safety tolerance to control the strictness of content filters. Lower values apply stricter filters. | `2`            |
| `--interval`          | `-i`  | Interval parameter to control how the diffusion model progresses during image generation. Smaller values result in more consistent and stable outputs, while larger values allow for more diversity.| `2.0` |
| `--verbose`           | `-V`  | Enable verbose output for request and result details.                                              | `False`        |

### Bash Wrapper (`gen_flux.sh`)

| Argument    | Short | Description                                      |
|-------------|-------|--------------------------------------------------|
| `--yes`     | `-y`  | Proceed without confirmation prompt.            |
| `--help`    | `-h`  | Display help message.                           |
| Other arguments |   | Passed directly to the Python script (`flux.py`). |

## Examples

### Generate an Image with Default Seed (`rand`)

```bash
echo "A serene lake surrounded by mountains during sunrise." | python3 flux.py -wd 800 -ht 640
```

### Generate an Image Using the Bash Wrapper with Confirmation

```bash
./gen_flux.sh -wd 800 -ht 640
```

*You will be prompted:*
```
Are you sure you want to proceed? [y/N]:
```

### Generate an Image Silently with a Random Seed

```bash
./gen_flux.sh -y --seed rand -wd 1024 -ht 768
```

### Generate an Image with a Fixed Seed

```bash
./gen_flux.sh -y --seed 123456789 -wd 800 -ht 640
```

### Generate an Image with Seed Set to Null

```bash
./gen_flux.sh -y --seed null -wd 800 -ht 640
```

### Display Help Message

```bash
./gen_flux.sh -h
```

*This will display the help information from `flux.py` without prompting for confirmation.*

## Troubleshooting

### API Key Not Found

**Issue:**
```
Error: BFL_API_KEY not found in environment variables.
```

**Solution:**
- Ensure that the `.env` file is present in your home directory or the project root.
- Verify that `BFL_API_KEY` is correctly set in the `.env` file.

### Invalid Seed Value

**Issue:**
```
Error: --seed must be an integer, 'rand', or 'null'.
```

**Solution:**
- Provide a valid seed value:
    - An integer (e.g., `--seed 123456789`)
    - `rand` to generate a random seed (e.g., `--seed rand`)
    - `null` to pass null as the seed (e.g., `--seed null`)

### Dependencies Installation Errors

**Issue:**
Errors during `pip install -r requirements.txt`

**Solution:**
- Ensure you are using the correct Python version.
- Check for any network issues or permission errors.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**
    - Click the "Fork" button on the repository page.

2. **Clone Your Fork**

    ```bash
    git clone https://github.com/yokoyama-flogics/flux-diffusion-client.git
    cd flux-diffusion-client
    ```

3. **Create a New Branch**

    ```bash
    git checkout -b feature/your-feature-name
    ```

4. **Make Your Changes**
    - Implement your feature or fix.

5. **Commit Your Changes**

    ```bash
    git commit -m "Add feature: your feature description"
    ```

6. **Push to Your Fork**

    ```bash
    git push origin feature/your-feature-name
    ```

7. **Create a Pull Request**
    - Go to the original repository and click "New Pull Request".

## License

This project is licensed under the [BSD 2-Clause License](LICENSE).

## Acknowledgements

- [GitHub: black-forest-labs/flux](https://github.com/black-forest-labs/flux): Official inference repo for FLUX.1 models)

## Contact

For any questions or support, please reach out to [flogics.com](https://flogics.com/).
