from dataclasses import dataclass

from sim.core.resources.resources_types import ResourceCategory
from sim.core.resources.resources import ResourceDefinition


# =========================================================
# DEFINICIÓN DE RECURSO
# =========================================================
@dataclass(slots=True)
class ResourceDefinition:

    name: str
    category: ResourceCategory

    # Economía
    base_price: float = 1

    # Supervivencia
    nutrition: float = 0

    # Producción / utilidad
    durability: float = 0
    industrial_value: float = 0

    # Social
    happiness_bonus: float = 0
    stress_reduction: float = 0

    # Riesgo
    perishability: float = 0
    illegality: float = 0

    # Otros
    energy_value: float = 0

RESOURCES = {

    # =====================================================
    # FOOD
    # =====================================================

    "wheat": ResourceDefinition(
        name="wheat",
        category=ResourceCategory.FOOD,

        base_price=2,

        nutrition=15,

        perishability=0.05
    ),

    "vegetables": ResourceDefinition(
        name="vegetables",
        category=ResourceCategory.FOOD,

        base_price=3,

        nutrition=20,

        perishability=0.12
    ),

    "meat": ResourceDefinition(
        name="meat",
        category=ResourceCategory.FOOD,

        base_price=7,

        nutrition=40,

        happiness_bonus=2,

        perishability=0.25
    ),

    "fish": ResourceDefinition(
        name="fish",
        category=ResourceCategory.FOOD,

        base_price=6,

        nutrition=35,

        happiness_bonus=1,

        perishability=0.3
    ),

    # =====================================================
    # MATERIAL
    # =====================================================

    "wood": ResourceDefinition(
        name="wood",
        category=ResourceCategory.MATERIAL,

        base_price=5,

        durability=25,

        industrial_value=10
    ),

    "stone": ResourceDefinition(
        name="stone",
        category=ResourceCategory.MATERIAL,

        base_price=4,

        durability=40,

        industrial_value=8
    ),

    "steel": ResourceDefinition(
        name="steel",
        category=ResourceCategory.MATERIAL,

        base_price=14,

        durability=80,

        industrial_value=35
    ),

    # =====================================================
    # INDUSTRIAL
    # =====================================================

    "tools": ResourceDefinition(
        name="tools",
        category=ResourceCategory.INDUSTRIAL,

        base_price=18,

        durability=60,

        industrial_value=45
    ),

    "machine_parts": ResourceDefinition(
        name="machine_parts",
        category=ResourceCategory.INDUSTRIAL,

        base_price=35,

        durability=90,

        industrial_value=80
    ),

    "electronics": ResourceDefinition(
        name="electronics",
        category=ResourceCategory.INDUSTRIAL,

        base_price=50,

        industrial_value=100
    ),

    # =====================================================
    # CONSUMER
    # =====================================================

    "clothes": ResourceDefinition(
        name="clothes",
        category=ResourceCategory.CONSUMER,

        base_price=12,

        happiness_bonus=3,

        durability=25
    ),

    "furniture": ResourceDefinition(
        name="furniture",
        category=ResourceCategory.CONSUMER,

        base_price=25,

        happiness_bonus=5,

        durability=50
    ),

    "household_goods": ResourceDefinition(
        name="household_goods",
        category=ResourceCategory.CONSUMER,

        base_price=20,

        happiness_bonus=4
    ),

    # =====================================================
    # LUXURY
    # =====================================================

    "alcohol": ResourceDefinition(
        name="alcohol",
        category=ResourceCategory.LUXURY,

        base_price=10,

        happiness_bonus=8,

        stress_reduction=5
    ),

    "jewelry": ResourceDefinition(
        name="jewelry",
        category=ResourceCategory.LUXURY,

        base_price=120,

        happiness_bonus=15
    ),

    "entertainment": ResourceDefinition(
        name="entertainment",
        category=ResourceCategory.LUXURY,

        base_price=30,

        happiness_bonus=10,

        stress_reduction=8
    ),

    # =====================================================
    # ENERGY
    # =====================================================

    "coal": ResourceDefinition(
        name="coal",
        category=ResourceCategory.ENERGY,

        base_price=8,

        energy_value=40,

        industrial_value=20
    ),

    "fuel": ResourceDefinition(
        name="fuel",
        category=ResourceCategory.ENERGY,

        base_price=20,

        energy_value=80,

        industrial_value=50
    ),

    # =====================================================
    # ILLEGAL
    # =====================================================

    "scrap": ResourceDefinition(
        name="scrap",
        category=ResourceCategory.ILLEGAL,

        base_price=3,

        industrial_value=5
    ),

    "stolen_goods": ResourceDefinition(
        name="stolen_goods",
        category=ResourceCategory.ILLEGAL,

        base_price=15,

        happiness_bonus=2,

        illegality=40
    ),

    "drugs": ResourceDefinition(
        name="drugs",
        category=ResourceCategory.ILLEGAL,

        base_price=50,

        happiness_bonus=15,

        stress_reduction=20,

        illegality=90
    ),
}