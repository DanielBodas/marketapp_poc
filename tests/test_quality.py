from db import models
import re

MODELS = [
    models.Producto,
    models.Marca,
    models.Supermercado,
    models.Compra,
    models.ProductoMarca,
    models.Clasificacion,
]

def test_models_have_docstring():
    for model in MODELS:
        assert model.__doc__ is not None and model.__doc__.strip() != "", f"{model.__name__} debe tener docstring"

def test_tablename_format():
    for model in MODELS:
        tablename = getattr(model, "__tablename__", None)
        assert tablename is not None, f"{model.__name__} debe tener __tablename__"
        assert re.match(r"^[a-z0-9_]+$", tablename), f"{model.__name__}: __tablename__ '{tablename}' debe estar en minúsculas y sin espacios"
