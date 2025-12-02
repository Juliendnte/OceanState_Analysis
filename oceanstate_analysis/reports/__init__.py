"""
Module reports pour OceanState Analysis
Import de toutes les fonctions de rapport
"""

from .reports import (
    report_acidification,
    report_acidification_co2_correlation,
    report_plastic_evolution,
    report_plastic_waste_countries,
    report_plastic_production_global,
    report_plastic_ocean_distribution,
    report_plastic_co2_correlation,
    report_glacier_heat_correlation,
    display_correlation_metrics,
    create_summary_stats,
    report_sealevel,
    report_heat,
    report_glaciermelting,
    report_glaciermelting_sealevel_correlation,
    report_redlist,
    report_acidification_redlist_correlation,
    report_global_warn
)

__all__ = [
    'report_acidification',
    'report_acidification_co2_correlation',
    'report_plastic_evolution',
    'report_plastic_waste_countries',
    'report_plastic_production_global',
    'report_plastic_ocean_distribution',
    'report_plastic_co2_correlation',
    'report_glacier_heat_correlation',
    'display_correlation_metrics',
    'create_summary_stats',
    'report_sealevel',
    'report_heat',
    'report_glaciermelting',
    'report_glaciermelting_sealevel_correlation',
    'report_redlist',
    'report_acidification_redlist_correlation',
    'report_global_warn'
]