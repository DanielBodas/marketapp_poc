"""Lógica de negocio relacionada con las compras y productos"""

from typing import List, Optional
from db.models import Marca, Unidad

def get_marcas_para_producto(producto_id: int, relaciones_pm: List, marcas: List[Marca]) -> List[Marca]:
    """Obtiene las marcas disponibles para un producto dado"""
    if producto_id is None:
        return []
    return [
        m for rel in relaciones_pm 
        if rel.id_producto == producto_id 
        for m in marcas 
        if m.id_marca == rel.id_marca
    ]

def get_unidad_para_producto(producto_id: int, relaciones_pu: List, unidades: List[Unidad]) -> Optional[Unidad]:
    """Obtiene la unidad para un producto, o la unidad por defecto si no tiene"""
    if producto_id is None:
        return None
        
    # Buscar unidades relacionadas
    unidades_producto = [
        u for rel in relaciones_pu 
        if rel.id_producto == producto_id 
        for u in unidades 
        if u.id_unidad == rel.id_unidad
    ]
    
    if unidades_producto:
        return unidades_producto[0]
    
    # Si no hay unidad relacionada, buscar "unidad" por defecto
    return next((u for u in unidades if u.nombre_unidad.lower() == "unidad"), None)