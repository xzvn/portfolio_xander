from pathlib import Path

from flask import Flask
from jinja2 import ChoiceLoader, DictLoader

from embedded_templates import EMBEDDED_TEMPLATES


def configure_template_loader(
    app: Flask,
    template_directory: Path,
) -> None:
    """
    Memakai file template biasa ketika tersedia, lalu memakai template
    yang tertanam di embedded_templates.py sebagai cadangan di Vercel.
    """
    loaders = []

    if app.jinja_loader is not None:
        loaders.append(app.jinja_loader)

    loaders.append(DictLoader(EMBEDDED_TEMPLATES))
    app.jinja_loader = ChoiceLoader(loaders)

    app.logger.info(
        "Template loader configured. filesystem=%s embedded=%s",
        template_directory.is_dir(),
        len(EMBEDDED_TEMPLATES),
    )
