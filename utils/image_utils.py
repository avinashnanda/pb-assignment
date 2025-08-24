import base64
from IPython.display import display
from IPython.display import Image as IPyImage, display

def display_base64_image(base64_code):
    """Display a base64-encoded image in Jupyter/Colab."""
    image_data = base64.b64decode(base64_code)
    display(IPyImage(data=image_data))  # Explicitly use IPython's Image

def get_images_base64(chunks):
    """Extract base64-encoded images from CompositeElement objects."""
    images_b64 = []
    for chunk in chunks:
        if "CompositeElement" in str(type(chunk)):
            chunk_els = chunk.metadata.orig_elements
            for el in chunk_els:
                if "Image" in str(type(el)):
                    if hasattr(el.metadata, "image_base64"):
                        images_b64.append(el.metadata.image_base64)
    return images_b64
