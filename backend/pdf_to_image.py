from pdf2image import convert_from_path

def convert_pdf_to_image(file_path, output_folder="output_images", dpi=300):
    """
    Converts a PDF to images, saving each page as an image file.

    :param file_path: Path to the input PDF file.
    :param output_folder: Folder where images will be saved.
    :param dpi: Resolution of the output images.
    :return: List of image file paths.
    """
    import os

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Convert PDF to images
    images = convert_from_path(file_path, dpi=dpi, first_page=1, last_page=1)

    if images:
        image_path = os.path.join(output_folder, "page_1.png")
        images[0].save(image_path, "PNG")  # Save the first page
        return image_path
    else:
        return None

# Example usage
pdf_path = "newResume.pdf"
output_images = convert_pdf_to_image(pdf_path)
print("Images saved at:", output_images)
