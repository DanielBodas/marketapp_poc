# 🛒 MarketApp POC

**MarketApp POC** es una aplicación modular construida con Streamlit para registrar compras y hacer seguimiento de la evolución de precios de productos a lo largo del tiempo. Actualmente permite introducir información básica (productos, marcas, supermercados y tickets), y está diseñada para escalar con visualizaciones y consultas inteligentes que ayuden a tomar mejores decisiones al momento de comprar.

---

## 🚀 Funcionalidades

- 📦 Registro de productos, marcas y supermercados
- 🧾 Formulario dinámico para cargar tickets de compra
- 📈 Preparada para incluir gráficas y análisis de precios en futuras versiones

---

## 🧪 Tests y calidad

Para ejecutar los tests y comprobar la calidad antes de hacer un pull request:

1. Instala las dependencias de desarrollo:
	```powershell
	python -m pip install -r requirements-dev.txt
	```
2. Ejecuta los tests:
	```powershell
	python -m pytest -q
	```

Opcional: crea un entorno virtual limpio para aislar dependencias:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Los tests se ejecutan automáticamente en GitHub Actions en cada push y pull request.
