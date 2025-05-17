from modelos.zona_geografica import ZonaGeografica

zona_centro_madrid = ZonaGeografica("Centro", "España", [])
zona_norte_madrid = ZonaGeografica("Norte", "España", [])
zona_sur_madrid = ZonaGeografica("Sur", "España", [])

zona_casco_antiguo_toledo = ZonaGeografica("Casco Antiguo", "España", [])
zona_playa_valencia = ZonaGeografica("Playa", "España", [])
zona_rural_asturias = ZonaGeografica("Rural", "España", [])
zona_centro_barcelona = ZonaGeografica("Centro", "España", [])
zona_monte_bilbao = ZonaGeografica("Monte", "España", [])

zona_residencial_sevilla = ZonaGeografica("Residencial", "España", [])
zona_costa_malaga = ZonaGeografica("Costa", "España", [])

zonas = {
    "centro_madrid": zona_centro_madrid,
    "norte_madrid": zona_norte_madrid,
    "sur_madrid": zona_sur_madrid,
    "casco_toledo": zona_casco_antiguo_toledo,
    "playa_valencia": zona_playa_valencia,
    "rural_asturias": zona_rural_asturias,
    "centro_barcelona": zona_centro_barcelona,
    "monte_bilbao": zona_monte_bilbao,
    "residencial_sevilla": zona_residencial_sevilla,
    "costa_malaga": zona_costa_malaga
}

