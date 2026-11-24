# -*- coding: utf-8 -*-
"""Términos y condiciones de ToolkitPalm.

Se piden al instalar y cada vez que cambia la versión del plugin o la de los
términos (TERMINOS_VERSION). Sin aceptarlos no se puede usar el plugin.

BORRADOR pendiente de aprobación de Adán Arias antes de publicar.
"""
import configparser
import os

from qgis.PyQt.QtCore import QSettings, Qt
from qgis.PyQt.QtWidgets import (QDialog, QHBoxLayout, QLabel, QPushButton,
                                 QScrollArea, QVBoxLayout)

# Subir esta fecha cuando cambie el texto: obliga a todos a aceptar de nuevo.
TERMINOS_VERSION = "1.0"
_CLAVE = "ToolkitPalm/terminos_aceptados"

AZUL = "#002856"

TERMINOS_HTML = """
<div style='font-size: 11px; line-height: 1.45; color: #222;'>
<h3 style='color:#002856;'>Términos y condiciones de ToolkitPalm</h3>
<p><i>Versión de los términos: {version}. Vigentes desde: la fecha de su publicación en el plugin.</i></p>
<h4 style='color:#002856; margin:10px 0 4px 0;'>1. Quién ofrece el servicio</h4>
<p>ToolkitPalm es un complemento (plugin) para QGIS y un servicio en línea ofrecido por Adan Arias, con domicilio en El Carmen de Bolívar, Colombia ("nosotros"). Contacto para cualquier tema de estos términos y de datos personales: adan@adanarias.com.</p>
<h4 style='color:#002856; margin:10px 0 4px 0;'>2. Aceptación</h4>
<p>Para usar ToolkitPalm debes leer y aceptar estos términos. Se te mostrarán al instalar el plugin y cada vez que cambien en una actualización. Si no los aceptas, el plugin no se podrá usar. Puedes volver a leerlos cuando quieras con el ícono (!) junto a "Desarrollado por" en la ventana del plugin.</p>
<h4 style='color:#002856; margin:10px 0 4px 0;'>3. Qué hace el servicio</h4>
<p>ToolkitPalm detecta, numera y analiza palmas en ortofotos. Para hacerlo, el plugin envía a nuestros servidores recortes de la ortofoto (bloques de hasta 5 ha) y los datos necesarios del lote. El procesamiento se hace en nuestros servidores y los resultados vuelven a tu QGIS.</p>
<h4 style='color:#002856; margin:10px 0 4px 0;'>4. Tu cuenta y los créditos</h4>
<ul>
<li>Ingresas con tu cuenta de Google. Eres responsable de lo que se haga con tu cuenta.</li>
<li>Algunas funciones consumen créditos. Los créditos comprados no son reembolsables salvo que la ley lo exija o que el servicio falle por causa nuestra.</li>
<li>No puedes compartir tu cuenta, revender el servicio, ni intentar copiar, desarmar o extraer el método de detección o numeración.</li>
</ul>
<h4 style='color:#002856; margin:10px 0 4px 0;'>5. Qué información recibimos</h4>
<ul>
<li><b>Datos de la cuenta:</b> nombre, correo y foto de perfil de Google; historial de uso y de créditos.</li>
<li><b>Información de los lotes:</b> los recortes de ortofoto que envías, las detecciones que genera el servicio y los ajustes que haces (palmas agregadas, borradas, movidas o marcadas como viva, muerta o para revisar), que se envían al usar el botón "Validar ajustes".</li>
<li><b>Datos técnicos:</b> versión del plugin y de QGIS, fecha y hora de uso, y errores.</li>
</ul>
<p>No pedimos ni guardamos el nombre de tu finca ni datos de terceros. Te pedimos no incluir en las imágenes información personal de otras personas.</p>
<h4 style='color:#002856; margin:10px 0 4px 0;'>6. Para qué la usamos</h4>
<ol>
<li>Prestarte el servicio: detectar, numerar y analizar tus lotes.</li>
<li>Manejar tu cuenta, tus créditos y darte soporte.</li>
<li><b>Mejorar el detector.</b> Al aceptar estos términos autorizas que los recortes de ortofoto y los ajustes que validas se usen para entrenar y evaluar nuestros modelos, con el fin de mejorar las detecciones para todos los usuarios. Antes de usarlos, los revisamos (manual y automáticamente) y los guardamos sin datos que te identifiquen directamente.</li>
<li>Cumplir obligaciones legales y proteger el servicio contra abusos.</li>
</ol>
<h4 style='color:#002856; margin:10px 0 4px 0;'>7. Lo que NO hacemos</h4>
<ul>
<li>No vendemos ni compartimos tus imágenes ni tus datos con otras empresas.</li>
<li>No publicamos tus imágenes ni las subimos a plataformas públicas.</li>
<li>Los modelos entrenados no permiten reconstruir tus imágenes. Lo que se comparte con otros usuarios es solo un detector que funciona mejor.</li>
<li>Solo usamos proveedores de servidores y de inicio de sesión (como el servidor donde corre el servicio y Google) que nos ayudan a prestar el servicio, bajo obligaciones de confidencialidad.</li>
</ul>
<h4 style='color:#002856; margin:10px 0 4px 0;'>8. Propiedad</h4>
<ul>
<li>Tus ortofotos y tus resultados son tuyos.</li>
<li>El plugin, el método, los modelos y sus mejoras son nuestros. La licencia que te damos para usarlos es personal, no exclusiva e intransferible.</li>
<li>Al aceptar el punto 6.3 nos das una licencia gratuita, no exclusiva y por tiempo indefinido para usar los recortes y ajustes con el fin de entrenar y evaluar los modelos.</li>
</ul>
<h4 style='color:#002856; margin:10px 0 4px 0;'>9. Tus derechos (Ley 1581 de 2012)</h4>
<p>Como titular de datos personales puedes:</p>
<ul>
<li>Conocer, actualizar y corregir tus datos.</li>
<li>Pedir prueba de esta autorización.</li>
<li>Saber cómo usamos tus datos.</li>
<li>Revocar la autorización o pedir que borremos tus datos, salvo los que debamos guardar por ley o por contrato.</li>
<li>Presentar quejas ante la Superintendencia de Industria y Comercio.</li>
</ul>
<p>Para ejercerlos, escribe a adan@adanarias.com. Respondemos consultas en máximo 10 días hábiles y reclamos en máximo 15 días hábiles.</p>
<p>Si pides que no se usen tus lotes para entrenar, dejamos de incluirlos en entrenamientos nuevos y los borramos de nuestra base de entrenamiento. Como el uso para entrenar es parte de las condiciones del servicio, retirar esa autorización puede implicar que dejes de usar el plugin.</p>
<h4 style='color:#002856; margin:10px 0 4px 0;'>10. Cuánto tiempo guardamos la información</h4>
<ul>
<li>Datos de cuenta y créditos: mientras tengas la cuenta y hasta 10 años después, por obligaciones contables.</li>
<li>Recortes y ajustes para entrenamiento: mientras sirvan para mejorar el detector, o hasta que pidas borrarlos.</li>
<li>Recortes que solo se usaron para procesar y no fueron validados: se borran a los 30 días.</li>
</ul>
<h4 style='color:#002856; margin:10px 0 4px 0;'>11. Seguridad</h4>
<p>Usamos conexiones cifradas, servidores con acceso restringido y respaldos privados. Ningún sistema es 100 % seguro, pero te avisaremos si ocurre un incidente que afecte tus datos.</p>
<h4 style='color:#002856; margin:10px 0 4px 0;'>12. Límites de responsabilidad</h4>
<p>Las detecciones y los conteos son una ayuda técnica y pueden tener errores. Revisa los resultados antes de tomar decisiones agronómicas, comerciales o de pago. No respondemos por pérdidas que vengan de usar los resultados sin revisarlos, ni por fallas de internet, de QGIS o de tu computador.</p>
<h4 style='color:#002856; margin:10px 0 4px 0;'>13. Cambios a estos términos</h4>
<p>Podemos actualizar estos términos. Cuando cambien, el plugin te mostrará la nueva versión y tendrás que aceptarla para seguir usándolo.</p>
<h4 style='color:#002856; margin:10px 0 4px 0;'>14. Ley aplicable</h4>
<p>Estos términos se rigen por las leyes de Colombia. Cualquier diferencia se intentará resolver primero de forma directa, y si no, ante los jueces de El Carmen de Bolívar.</p>
</div>
"""


def version_plugin():
    try:
        meta = configparser.ConfigParser()
        meta.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), "metadata.txt"),
                  encoding="utf-8")
        return meta.get("general", "version", fallback="")
    except Exception:
        return ""


def _firma():
    return f"{TERMINOS_VERSION}|{version_plugin()}"


def terminos_aceptados():
    return QSettings().value(_CLAVE, "", type=str) == _firma()


def _registrar_aceptacion():
    QSettings().setValue(_CLAVE, _firma())


class TerminosDialog(QDialog):
    def __init__(self, parent=None, obligatorio=False):
        super().__init__(parent)
        self.setWindowTitle("Términos y condiciones de ToolkitPalm")
        self.setMinimumSize(560, 560)
        layout = QVBoxLayout(self)

        if obligatorio:
            aviso = QLabel("Para usar ToolkitPalm debe leer y aceptar los términos y condiciones.")
            aviso.setWordWrap(True)
            aviso.setStyleSheet(f"color: {AZUL}; font-weight: bold; padding: 4px;")
            layout.addWidget(aviso)

        texto = QLabel(TERMINOS_HTML.format(version=TERMINOS_VERSION))
        texto.setWordWrap(True)
        texto.setTextFormat(Qt.TextFormat.RichText)
        texto.setAlignment(Qt.AlignmentFlag.AlignTop)
        texto.setStyleSheet("padding: 8px; background: white;")
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(texto)
        layout.addWidget(scroll, 1)

        botones = QHBoxLayout()
        botones.addStretch(1)
        if obligatorio:
            no = QPushButton("No acepto")
            no.clicked.connect(self.reject)
            si = QPushButton("Acepto los términos y condiciones")
            si.setStyleSheet(f"background:{AZUL}; color:white; padding:8px 14px; border-radius:4px;")
            si.clicked.connect(self.accept)
            botones.addWidget(no)
            botones.addWidget(si)
        else:
            cerrar = QPushButton("Cerrar")
            cerrar.clicked.connect(self.accept)
            botones.addWidget(cerrar)
        layout.addLayout(botones)


def mostrar_terminos(parent=None):
    """Solo lectura (desde el ícono ⓘ del pie del panel)."""
    TerminosDialog(parent, obligatorio=False).exec()


def pedir_aceptacion(parent=None):
    """True si ya estaban aceptados o el usuario los acepta ahora."""
    if terminos_aceptados():
        return True
    if TerminosDialog(parent, obligatorio=True).exec() == QDialog.DialogCode.Accepted:
        _registrar_aceptacion()
        return True
    return False
