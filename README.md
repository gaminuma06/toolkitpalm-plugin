# ToolkitPalm

Complemento de QGIS para plantaciones de palma de aceite, sobre ortomosaicos de dron:

- **Detector de Palmas**: cuenta y ubica cada palma, con edición manual de los
  puntos, numeración por líneas de siembra, palmas faltantes y resaltado de
  palmas fuera de patrón.
- **Recortar bordes de ortofoto**: quita el marco plano (gris, blanco o negro)
  alrededor de la zona fotografiada.

Desarrollado por **Ing. Adán Arias**.

## Instalación

Desde QGIS: *Complementos → Administrar e instalar complementos*, buscar
**ToolkitPalm**. Requiere QGIS 3.16 o posterior.

## Cómo funciona

El complemento es solo la interfaz: prepara los datos en QGIS (recorta la
ortoimagen al lote y divide los lotes grandes en bloques) y todo el
procesamiento se hace en el servidor de ToolkitPalm. Los resultados vuelven como
capas del proyecto.

El uso requiere iniciar sesión con una cuenta de Google. La detección consume
créditos: 1 crédito cubre hasta 5 ha por lote, y cada cuenta nueva recibe 1
crédito de prueba.

El código de este repositorio se publica bajo **GPL v2 o posterior** (ver
[LICENSE](toolkitpalm/LICENSE)). Los modelos, los métodos de procesamiento y el
código del servidor **no forman parte de esta distribución** y son propiedad del
autor. Ver [AVISO_LEGAL.txt](toolkitpalm/AVISO_LEGAL.txt).

El complemento no contiene ningún secreto: el `client_id` de Google es público
por diseño y el intercambio de credenciales lo completa el servidor.

Política de privacidad: [PRIVACIDAD.md](PRIVACIDAD.md) · Condiciones: [TERMINOS.md](TERMINOS.md)
