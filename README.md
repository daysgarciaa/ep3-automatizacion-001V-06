# EP3 — Automatización de Red | 001V-06

## 1. Objetivo del proyecto
Se implementó la configuración corporativa completa del router RTR-FIBRNOR para la empresa Fibra Optica Norte SpA, aplicando automatización de red mediante pyATS, Ansible, NETCONF y RESTCONF, con el objetivo de dejar el equipo operativo y auditado según los estándares corporativos.

## 2. Alcance
Se configuró hostname corporativo, interfaz Loopback de gestión, descripción de interfaz WAN, banner de acceso y servidor NTP. Se habilitaron los protocolos NETCONF y RESTCONF para gestión automatizada. Quedó fuera del alcance la configuración de routing dinámico y políticas de seguridad avanzada. Herramientas utilizadas: pyATS/Genie, Ansible, ncclient, Python requests.

## 3. Infraestructura utilizada
| Componente | Detalle |
|---|---|
| Router | Cisco CSR1kv — IP 192.168.56.101 — IOS-XE |
| Estación de trabajo | DEVASC labvm — Ubuntu |
| Ansible | Red Hat Ansible (network_cli) |
| Python | Python 3.x con ncclient y requests |
| pyATS / Genie | Captura de snapshots y diff de configuración |

## 4. Tecnologías empleadas y justificación
- **pyATS/Genie**: usado en Fase 1 y 5 porque permite capturar el estado completo del router vía SSH sin necesitar NETCONF habilitado previamente.
- **Ansible**: usado en Fase 2 porque es idempotente y declarativo, garantizando que la configuración sea reproducible y verificable.
- **NETCONF**: usado en Fase 3 porque devuelve el árbol XML completo de configuración, permitiendo validar múltiples parámetros en una sola consulta.
- **RESTCONF**: usado en Fase 4 porque permite consultar recursos específicos mediante URLs HTTP en formato JSON, complementando la validación de NETCONF.

## 5. Configuración aplicada
| Parámetro | Valor configurado |
|---|---|
| Hostname corporativo | RTR-FIBRNOR |
| Interfaz Loopback | Loopback10 — 10.1.6.1/24 |
| Descripción GigabitEthernet1 | Enlace-WAN-Temuco |
| Servidor NTP | 8.8.8.8 |
| Banner de acceso | ACCESO RESTRINGIDO - FIBRNOR |
| NETCONF | Habilitado (puerto 830) |
| RESTCONF | Habilitado (HTTPS) |

## 6. Resultados de validación
| Criterio verificado | NETCONF | RESTCONF |
|---|---|---|
| Hostname corporativo (RTR-FIBRNOR) | CONFORME | CONFORME |
| IP Loopback (10.1.6.1) | CONFORME | CONFORME |
| Máscara Loopback (255.255.255.0) | CONFORME | — |
| Descripción WAN (Enlace-WAN-Temuco) | CONFORME | CONFORME |
| Servidor NTP (8.8.8.8) | CONFORME | CONFORME |

## 7. Conclusiones
El router RTR-FIBRNOR fue aprovisionado exitosamente mediante Ansible y validado de forma independiente via NETCONF (5/5 criterios CONFORMES) y RESTCONF (4/4 criterios CONFORMES). El equipo cumple con los estándares corporativos de Fibra Optica Norte SpA y queda habilitado para operar en producción. Todo el proceso quedó registrado y auditado en este repositorio GitHub.
