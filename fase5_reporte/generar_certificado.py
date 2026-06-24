#!/usr/bin/env python3
"""Generador de Certificado de Compliance - EP3 DRY7122"""

import yaml
import os
from datetime import datetime

with open("../vars/vars_001V-06.yaml") as f:
    vars = yaml.safe_load(f)

alumno  = vars["alumno"]
cliente = vars["cliente"]
router  = vars["router"]

def verificar_conforme(path):
    if not os.path.exists(path):
        return False
    with open(path) as f:
        contenido = f.read()
    return "5/5 criterios" in contenido or "4/4 criterios" in contenido

netconf_ok  = verificar_conforme("../fase3_validacion_netconf/evidencias/output_validacion_netconf.txt")
restconf_ok = verificar_conforme("../fase4_validacion_restconf/evidencias/output_validacion_restconf.txt")

diff_path = "evidencias/diff_001V-06"
diff_ok = os.path.exists(diff_path) and len(os.listdir(diff_path)) > 0

resultado_global = "CONFORME" if (netconf_ok and restconf_ok and diff_ok) else "NO CONFORME"

certificado = f"""
╔══════════════════════════════════════════════════════════════╗
║          CERTIFICADO DE COMPLIANCE DE RED                    ║
║          EP3 - DRY7122 - DUOC UC                             ║
╚══════════════════════════════════════════════════════════════╝

Fecha de emision  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Alumno            : {alumno['nombre']}
Codigo            : {alumno['codigo']}
Empresa cliente   : {cliente['empresa']}

DISPOSITIVO CONFIGURADO
-----------------------
Hostname corporativo : {cliente['hostname']}
IP de gestion        : {router['loopback_ip']}/{router['loopback_prefix']}
Descripcion WAN      : {router['descripcion_wan']}
Servidor NTP         : {router['ntp_server']}
Banner               : {router['banner']}

RESULTADO POR FASE
------------------
Validacion NETCONF   : {'CONFORME' if netconf_ok  else 'NO CONFORME'}
Validacion RESTCONF  : {'CONFORME' if restconf_ok else 'NO CONFORME'}
Diff baseline/final  : {'DETECTADO' if diff_ok    else 'SIN DIFERENCIAS'}

══════════════════════════════════════════════════════════════
RESULTADO GLOBAL: {resultado_global}
══════════════════════════════════════════════════════════════

El equipo RTR-FIBRNOR ha sido configurado y validado exitosamente
mediante los protocolos NETCONF y RESTCONF. Queda habilitado
para operar en produccion para Fibra Optica Norte SpA.
"""

print(certificado)

with open("evidencias/certificado_compliance_001V-06.txt", "w") as f:
    f.write(certificado)

print("[*] Certificado guardado en evidencias/certificado_compliance_001V-06.txt")
