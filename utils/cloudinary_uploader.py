from pathlib import Path

import cloudinary.uploader


ALLOWED_IMAGE_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp",
}


def validate_image_file(image_file):
    if not image_file or not image_file.filename:
        return False, "Gambar belum dipilih."

    extension = Path(
        image_file.filename
    ).suffix.lower().replace(".", "")

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return (
            False,
            "Format gambar harus PNG, JPG, JPEG, atau WEBP.",
        )

    return True, None


def upload_project_image(image_file):
    is_valid, message = validate_image_file(
        image_file
    )

    if not is_valid:
        raise ValueError(message)

    upload_result = cloudinary.uploader.upload(
        image_file.stream,
        folder="portfolio_xander/projects",
        resource_type="image",
        transformation=[
            {
                "width": 1600,
                "height": 900,
                "crop": "limit",
                "quality": "auto",
                "fetch_format": "auto",
            }
        ],
    )

    return (
        upload_result["secure_url"],
        upload_result["public_id"],
    )


def delete_cloudinary_image(public_id):
    if not public_id:
        return

    cloudinary.uploader.destroy(
        public_id,
        resource_type="image",
        invalidate=True,
    )

def upload_profile_image(image_file):
    is_valid, message = validate_image_file(image_file)

    if not is_valid:
        raise ValueError(message)

    upload_result = cloudinary.uploader.upload(
        image_file.stream,
        folder="portfolio_xander/profile",
        resource_type="image",
        transformation=[
            {
                "width": 800,
                "height": 800,
                "crop": "fill",
                "gravity": "face",
                "quality": "auto",
                "fetch_format": "auto",
            }
        ],
    )

    return (
        upload_result["secure_url"],
        upload_result["public_id"],
    )