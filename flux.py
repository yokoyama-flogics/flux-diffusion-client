"""
Black Forest Labs FLUX.1 Diffusion Model Python Client

This script interacts with the FLUX.1 Diffusion Model API to generate images
based on user-provided prompts. It handles seed generation, API communication,
and result retrieval.

https://github.com/yokoyama-flogics/flux-diffusion-client
"""

import argparse
import json
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import requests
from dotenv import find_dotenv, load_dotenv

# Set as a constant
OUTPUT_DIR_NAME = "output"
POLLING_SLEEP_INTERVAL = 1  # seconds


def load_api_key() -> str:
    """
    Load BFL_API_KEY from .env files.
    """
    # Load .env from the home directory first
    home_env_path = Path.home() / ".env"
    load_dotenv(home_env_path)

    # Then, load .env from the current directory or its parents
    load_dotenv(find_dotenv())

    api_key = os.getenv("BFL_API_KEY")
    if not api_key:
        sys.exit("Error: BFL_API_KEY not found in environment variables.")
    return api_key


def parse_arguments(defaults: Dict[str, Any]) -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Diffusion Model Image Generation Script",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-wd",
        "--width",
        type=int,
        default=defaults["width"],
        help="Width of the image in pixels",
    )
    parser.add_argument(
        "-ht",
        "--height",
        type=int,
        default=defaults["height"],
        help="Height of the image in pixels",
    )
    parser.add_argument(
        "-v",
        "--variant",
        type=str,
        default=defaults["variant"],
        help="Variant of the diffusion model",
    )
    parser.add_argument(
        "-s",
        "--steps",
        type=int,
        default=defaults["steps"],
        help=(
            "Number of network evaluations. Determines how many steps the "
            "diffusion model takes to generate the image. Higher values "
            " improve quality but increase computation time."
        ),
    )
    parser.add_argument(
        "-pu",
        "--prompt_upsampling",
        action="store_true",
        default=defaults["prompt_upsampling"],
        help=(
            "Enable prompt upsampling to improve the quality and fidelity of "
            "the generated image to the prompt."
        ),
    )
    parser.add_argument(
        "--seed",
        type=str,
        default=defaults["seed"],
        help=(
            "Fix the generation seed: provide an integer, 'rand' to generate "
            "a random seed, or 'null' to pass null."
        ),
    )
    parser.add_argument(
        "-g",
        "--guidance",
        type=float,
        default=defaults["guidance"],
        help=(
            "Guidance scale to control the fidelity and creativity of the "
            "generated image. Higher values make the image adhere more "
            "strictly to the prompt."
        ),
    )
    parser.add_argument(
        "-st",
        "--safety_tolerance",
        type=int,
        default=defaults["safety_tolerance"],
        help=(
            "Safety tolerance to control the strictness of content filters. "
            "Lower values apply stricter filters to prevent inappropriate "
            "content."
        ),
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=defaults["interval"],
        help=(
            "Interval parameter to control how the diffusion model progresses "
            "during image generation. A smaller value results in more "
            "consistent and stable outputs, while a larger value allows for "
            "more diversity."
        ),
    )
    parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        help="Enable verbose output for request and result details",
    )

    return parser.parse_args()


def get_prompt() -> str:
    """
    Read prompt from standard input. If input is from a terminal, prompt the
    user.
    """
    if sys.stdin.isatty():
        print("Enter your prompt:")
    prompt = sys.stdin.read().strip()
    if not prompt:
        sys.exit("Error: Prompt cannot be empty.")
    return prompt


def create_output_directory(directory: Path) -> None:
    """
    Create output directory if it does not exist.
    """
    if not directory.exists():
        directory.mkdir(parents=True)
        print(f"Created directory: {OUTPUT_DIR_NAME}")


def generate_filename(base: str, timestamp: str, extension: str) -> str:
    """
    Generate a filename based on the timestamp and type.
    """
    return f"{timestamp}_{base}.{extension}"


def save_json(data: Dict[str, Any], filepath: Path) -> None:
    """
    Save dictionary as pretty-formatted JSON.
    """
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def download_image(url: str, filepath: Path) -> None:
    """
    Download an image from a URL and save it as JPEG within the output
    directory.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Construct the full path by joining OUTPUT_DIR_NAME and filepath
        full_path = Path(OUTPUT_DIR_NAME) / filepath
        with full_path.open("wb") as f:
            f.write(response.content)
        print(f"Image saved to {OUTPUT_DIR_NAME}/{filepath.name}")
    except requests.RequestException as e:
        print(f"Failed to download image from {url}: {e}")


def main() -> None:
    # Define default parameters
    defaults = {
        "width": 1024,
        "height": 1024,
        "variant": "flux.1-pro",
        "steps": 25,
        "prompt_upsampling": False,
        "seed": "rand",
        "guidance": 2.5,
        "safety_tolerance": 2,
        "interval": 2.0,
    }

    # Parse arguments
    args = parse_arguments(defaults)

    # Load API key
    api_key = load_api_key()

    # Get prompt from standard input
    prompt = get_prompt()

    # Handle seed parameter
    seed_input = args.seed.lower()
    if seed_input == "rand":
        seed = random.randint(0, 2**64 - 1)
    elif seed_input == "null":
        seed = None
    else:
        try:
            seed = int(args.seed)
        except ValueError:
            sys.exit("Error: --seed must be an integer, 'rand', or 'null'.")

    # Prepare parameters
    parameters = {
        "prompt": prompt,
        "width": args.width,
        "height": args.height,
        "variant": args.variant,
        "steps": args.steps,
        "prompt_upsampling": args.prompt_upsampling,
        "seed": seed,
        "guidance": args.guidance,
        "safety_tolerance": args.safety_tolerance,
        "interval": args.interval,
    }

    # Create output directory
    output_dir = Path.cwd() / OUTPUT_DIR_NAME
    create_output_directory(output_dir)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Define filenames
    request_filename = generate_filename("request", timestamp, "json")
    result_filename = generate_filename("result", timestamp, "json")
    image_filename = generate_filename("result", timestamp, "jpg")

    # Save request JSON
    request_filepath = output_dir / request_filename
    save_json(parameters, request_filepath)

    if args.verbose:
        print("Request JSON:")
        print(json.dumps(parameters, indent=4, ensure_ascii=False))

    # Make POST request
    try:
        response = requests.post(
            "https://api.bfl.ml/v1/image",
            headers={
                "accept": "application/json",
                "x-key": api_key,
                "Content-Type": "application/json",
            },
            json=parameters,
        )
        response.raise_for_status()
        request_response = response.json()
    except requests.RequestException as e:
        sys.exit(f"Error during POST request: {e}")

    if args.verbose:
        print("Response from POST request:")
        print(json.dumps(request_response, indent=4, ensure_ascii=False))

    request_id = request_response.get("id")
    if not request_id:
        sys.exit("Error: 'id' not found in the POST response.")

    # Polling for result
    while True:
        time.sleep(POLLING_SLEEP_INTERVAL)
        try:
            result_response = requests.get(
                "https://api.bfl.ml/v1/get_result",
                headers={
                    "accept": "application/json",
                    "x-key": api_key,
                },
                params={"id": request_id},
            )
            result_response.raise_for_status()
            result_data = result_response.json()
        except requests.RequestException as e:
            print(f"Error during GET request: {e}")
            continue

        if args.verbose:
            print("Result Response:")
            print(json.dumps(result_data, indent=4, ensure_ascii=False))

        if result_data.get("status") == "Ready":
            print("Result is ready.")
            break
        else:
            print(f"Status: {result_data.get('status')}")

    # Save result JSON
    result_filepath = output_dir / result_filename
    save_json(result_data, result_filepath)

    # Extract image URL and download
    sample_url = result_data.get("result", {}).get("sample")
    if sample_url:
        download_image(sample_url, Path(image_filename))
    else:
        print("No image URL found in the result.")


if __name__ == "__main__":
    main()
