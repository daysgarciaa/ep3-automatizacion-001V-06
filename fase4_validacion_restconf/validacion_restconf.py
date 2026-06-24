#!/usr/bin/env python3
"""Validacion RESTCONF - EP3 DRY7122"""

import yaml
import json
import socket
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("=" * 55)
print("Script  : validacion_restconf.py")
print(f"Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Host VM : {socket.gethostname()}")
print("=" * 55)

with open("../vars/vars_001V-06.yaml") as f:
    vars = yaml.safe_load(f)

router = vars["router"]
cliente = vars["cliente"]

BASE = f"https://{router['ip']}:443/restconf/data"
AUTH = (router["usuario"], router["password"])
HEADERS = {"Accept": "application/yang-data+json"}

import os
os.makedirs("evidencias/responses", exist_ok=True)

def consultar(endpoint, archivo):
    url = f"{BASE}/{endpoint}"
    print(f"[*] GET {url}")
    r = requests.get(url, auth=AUTH, headers=HEADERS, verify=False)
    data = r.json()
    path = f"evidencias/responses/{archivo}"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"    -> Guardado en {path}")
    return data

print("\n[*] Ejecutando consultas RESTCONF...")
d_hostname  = consultar("Cisco-IOS-XE-native:native/hostname", "get_hostname.json")
d_loopback  = consultar(f"ietf-interfaces:interfaces/interface=Loopback{router['loopback_id']}", "get_loopback.json")
d_interface = consultar("ietf-interfaces:interfaces/interface=GigabitEthernet1", "get_interfaces.json")
d_ntp       = consultar("Cisco-IOS-XE-native:native/ntp", "get_ntp.json")

hostname_actual = d_hostname.get("Cisco-IOS-XE-native:hostname", "")

try:
    loopback_ip_actual = d_loopback["ietf-interfaces:interface"]["ietf-ip:ipv4"]["address"][0]["ip"]
except:
    loopback_ip_actual = None

try:
    wan_desc_actual = d_interface["ietf-interfaces:interface"]["description"]
except:
    wan_desc_actual = None

try:
    ntp_actual = d_ntp["Cisco-IOS-XE-native:ntp"]["Cisco-IOS-XE-ntp:server"]["server-list"][0]["ip-address"]
except:
    ntp_actual = None

print("\n" + "=" * 55)
print("REPORTE DE VALIDACION RESTCONF")
print("=" * 55)

criterios = {
    "Hostname corporativo": (hostname_actual,    cliente["hostname"]),
    "IP Loopback":          (loopback_ip_actual, router["loopback_ip"]),
    "Descripcion WAN":      (wan_desc_actual,    router["descripcion_wan"]),
    "Servidor NTP":         (ntp_actual,         router["ntp_server"]),
}

ok_count = 0
for criterio, (actual, esperado) in criterios.items():
    if actual == esperado:
        print(f"[OK]   {criterio}: {actual}")
        ok_count += 1
    else:
        print(f"[FAIL] {criterio}: obtenido='{actual}' esperado='{esperado}'")

print("-" * 55)
resultado = "CONFORME" if ok_count == 4 else "NO CONFORME"
print(f"Resultado: {ok_count}/4 criterios — {resultado}")
print("=" * 55)
