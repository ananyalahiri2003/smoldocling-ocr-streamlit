"""
This file runs batch inference with SmolDocling OCR modelnon an input dir of images.
Run it like so
python src/inference.py \
--input-dir \
--output-dir \
--device \
--prompt
"""
import click
import os
import tempfile
from pathlib import Path
from PIL import Image

from huggingface_hub import ImageToImageTargetSize

from app import (
    load_dotenv,
    load_model,
    process_single_image,
)


# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
CACHE_DIR = os.getenv("CACHE_DIR", os.path.join(tempfile.gettempdir(), "smoldocling_cache"))


@click.command()
@click.option(
    "--input-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
     help="Input directory for images",
)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    help="Output directory for processed files",
)
@click.option(
    "--device",
    default="cpu",
    help="Torch device for inference, 'cpu' or 'cuda:0'"
)
@click.option(
    "--prompt",
    default="Convert this page to docling.",
    help="Custom prompt for each image",
)
def main(
        input_dir: Path,
        output_dir: Path,
        device: str,
        prompt: str,
):
    """
    Processes each image {jpg, jpeg, png, pdf} in input_dir and writes
    .md, .txt, .html outputs to output_dir.
    """
    output_dir.mkdir(exist_ok=True, parents=True)

    # Load model once
    processor, model = load_model(device)

    # Process each file
    for img_path in input_dir.iterdir():
        if img_path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.pdf']:
            continue
        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            click.echo(f"Cannot open image: {img_path.name} error:{e}, skipping..")
            continue

        # Run inference
        result = process_single_image(image, prompt_text=prompt, device=device, show_progress=None)

        # Write output
        file_stem = img_path.stem
        (output_dir / f"{file_stem}.md").write_text(result['markdown'], encoding='utf-8')
        (output_dir / f"{file_stem}.txt").write_text(result['text'], encoding='utf-8')
        (output_dir / f"{file_stem}.html").write_text(result['html'], encoding='utf-8')

        click.echo(
            f"Processed {img_path.name}"
            f"md={len(result['markdown'])} chars "
            f"text={len(result['text'])} chars "
            f"html={len(result['html'])} chars"
        )


if __name__ == "__main__":
    main()