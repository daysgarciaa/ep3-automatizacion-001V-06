#!/usr/bin/env python3
"""Validacion NETCONF - EP3 DRY7122"""

import yaml
import socket
from datetime import datetime
from ncclient import manager
from lxml import etree

print("=" * 55)
print("Script  : validacion_netconf.py")
print(f"Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Host VM : {socket.gethostname()}")
print("=" * 55)

with open("../vars/vars_001V-06.yaml") as f:
    vars = yaml.safe_load(f)

router = vars["router"]
cliente = vars["cliente"]

filtro_xml = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname/>
    <interface>
      <Loopback/>
      <GigabitEthernet/>
    </interface>
    <ntp/>
    <banner/>
  </native>
</filter>
"""

print("\n[*] Conectando al router via NETCONF...")

with manager.connect(
    host=router["ip"],
    port=830,
    username=router["usuario"],
    password=router["password"],
    hostkey_verify=False,
    allow_agent=False,
    look_for_keys=False
) as m:
    print("[*] Conexion NETCONF establecida.")
    respuesta = m.get_config(source="running", filter=filtro_xml)
    xml_raw = respuesta.xml

    with open("evidencias/rpc_reply_raw.xml", "w") as f:
        f.write(xml_raw)
    print("[*] XML guardado en evidencias/rpc_reply_raw.xml")

    root = etree.fromstring(xml_raw.encode())
    ns_native = "http://cisco.com/ns/yang/Cisco-IOS-XE-native"
    ns_ntp    = "http://cisco.com/ns/yang/Cisco-IOS-XE-ntp"

    def extraer(xpath, ns):
        nodo = root.find(xpath, ns)
        return nodo.text.strip() if nodo is not None and nodo.text else None

    ns = {"ios": ns_native}

    hostname_actual     = extraer(".//ios:native/ios:hostname", ns)
    loopback_ip_actual  = extraer(".//ios:native/ios:interface/ios:Loopback/ios:ip/ios:address/ios:primary/ios:address", ns)
    loopback_msk_actual = extraer(".//ios:native/ios:interface/ios:Loopback/ios:ip/ios:address/ios:primary/ios:mask", ns)
    wan_desc_actual     = extraer(".//ios:native/ios:interface/ios:GigabitEthernet[ios:name='1']/ios:description", ns)

    # NTP con su propio namespace
    ntp_tag = f"{{{ns_ntp}}}ip-address"
    ntp_nodo = root.find(f".//{ntp_tag}")
    ntp_actual = ntp_nodo.text.strip() if ntp_nodo is not None and ntp_nodo.text else None

print("\n" + "=" * 55)
print("REPORTE DE VALIDACION NETCONF")
print("=" * 55)

criterios = {
    "Hostname corporativo": (hostname_actual,     cliente["hostname"]),
    "IP Loopback":          (loopback_ip_actual,  router["loopback_ip"]),
    "Mascara Loopback":     (loopback_msk_actual, router["loopback_mask"]),
    "Descripcion WAN":      (wan_desc_actual,     router["descripcion_wan"]),
    "Servidor NTP":         (ntp_actual,          router["ntp_server"]),
}

ok_count = 0
for criterio, (actual, esperado) in criterios.items():
    if actual == esperado:
        print(f"[OK]   {criterio}: {actual}")
        ok_count += 1
    else:
        print(f"[FAIL] {criterio}: obtenido='{actual}' esperado='{esperado}'")

print("-" * 55)
resultado = "CONFORME" if ok_count == 5 else "NO CONFORME"
print(f"Resultado: {ok_count}/5 criterios — {resultado}")
print("=" * 55)
