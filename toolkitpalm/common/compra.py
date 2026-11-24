# -*- coding: utf-8 -*-
"""Ventana de compra de créditos: paquetes con descuento o cantidad libre.

El plugin NO calcula precios: muestra lo que dice el servidor y pide el pago.
CONTRATO PROVISIONAL (ajustar cuando el servidor lo confirme):
  GET  {PAGOS}/paquetes -> {"paquetes": [{"id", "creditos", "precio_cop", "descuento_pct"}],
                             "libre": {"min": int, "max": int}}
  POST {PAGOS}/cotizar  {"creditos": n} -> {"creditos", "precio_cop"}
  POST {PAGOS}/checkout {"client_id", "paquete_id" | "creditos", "codigo_descuento"} -> {"url", ...}
"""
from qgis.PyQt.QtCore import Qt, QTimer
from qgis.PyQt.QtWidgets import (QButtonGroup, QDialog, QHBoxLayout, QLabel, QPushButton,
                                 QRadioButton, QSpinBox, QVBoxLayout)


def _cop(v):
    return f"${float(v):,.0f} COP".replace(",", ".")


class CompraCreditosDialog(QDialog):
    """`peticion(metodo, ruta, datos)` -> (ok, datos) la hace el panel con su autenticación."""

    def __init__(self, parent, catalogo, peticion):
        super().__init__(parent)
        self.setWindowTitle("Comprar créditos")
        self.setMinimumWidth(380)
        self._peticion = peticion
        self.eleccion = None  # {"paquete_id": ...} o {"creditos": n}
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<b>Elige un paquete o escribe cuántos créditos quieres.</b><br>"
                             "1 crédito = hasta 5 ha."))
        self._grupo = QButtonGroup(self)
        for p in catalogo.get("paquetes", []):
            txt = f"{p.get('nombre') or str(p['creditos']) + ' créditos'}  —  {_cop(p['precio_cop'])}"
            if p.get("descuento_pct"):
                txt += f"   ({p['descuento_pct']}% de descuento)"
            rb = QRadioButton(txt)
            rb.setProperty("paquete_id", p["id"])
            rb.setProperty("creditos", p.get("creditos"))
            rb.setProperty("precio_cop", p.get("precio_cop"))
            self._grupo.addButton(rb)
            lay.addWidget(rb)
        libre = catalogo.get("libre")
        self._rb_libre = None
        if libre:
            fila = QHBoxLayout()
            self._rb_libre = QRadioButton("Otra cantidad:")
            self._grupo.addButton(self._rb_libre)
            self._spin = QSpinBox()
            self._spin.setRange(int(libre.get("min", 1)), int(libre.get("max", 10000)))
            self._precio_libre = QLabel("")
            fila.addWidget(self._rb_libre); fila.addWidget(self._spin); fila.addWidget(self._precio_libre, 1)
            lay.addLayout(fila)
            self._timer = QTimer(self); self._timer.setSingleShot(True)
            self._timer.timeout.connect(self._cotizar)
            self._spin.setValue(self._spin.minimum())
            self._min, self._max = self._spin.minimum(), self._spin.maximum()
            # Se reacciona a lo que se va digitando (no solo al valor confirmado),
            # para que el precio siempre corresponda al número que se ve.
            self._spin.lineEdit().textEdited.connect(self._al_digitar)
            self._spin.valueChanged.connect(lambda *_: self._al_digitar())
        self._total = QLabel("")
        self._total.setStyleSheet("font-weight: bold; color: #002856; padding: 6px 0;")
        lay.addWidget(self._total)
        # Aviso discreto: si la cantidad libre cuesta más que el paquete de 60, se sugiere el paquete.
        self._p60 = next((b for b in self._grupo.buttons()
                          if b is not self._rb_libre and "60" == str(b.property("creditos"))), None)
        self._aviso60 = QLabel('<a href="p60">Con 60 créditos pagas menos</a>')
        self._aviso60.setStyleSheet("color: #6b7280; font-size: 11px;")
        self._aviso60.linkActivated.connect(lambda *_: (self._p60.setChecked(True), self._actualizar()) if self._p60 else None)
        self._aviso60.setVisible(False)
        lay.addWidget(self._aviso60)
        botones = QHBoxLayout(); botones.addStretch(1)
        cancelar = QPushButton("Cancelar"); cancelar.clicked.connect(self.reject)
        self._pagar = QPushButton("Ir a pagar"); self._pagar.setEnabled(False)
        self._pagar.clicked.connect(self._aceptar)
        botones.addWidget(cancelar); botones.addWidget(self._pagar)
        lay.addLayout(botones)
        if self._rb_libre is not None:
            self._cotizar()
        self._grupo.buttonClicked.connect(lambda *_: self._actualizar())
        botones_g = self._grupo.buttons()
        if botones_g:
            botones_g[0].setChecked(True)
        self._actualizar()

    def _cantidad_digitada(self):
        try:
            return int(self._spin.lineEdit().text().replace(".", "").strip())
        except ValueError:
            return None

    def _al_digitar(self, *_):
        self._rb_libre.setChecked(True)
        n = self._cantidad_digitada()
        if n is None or n < self._min or n > self._max:
            self._timer.stop()
            self._precio_libre_valor = None
            self._precio_libre.setText(f"entre {self._min} y {self._max}")
            self._actualizar()
            return
        self._timer.start(400)

    def _cotizar(self):
        n = self._cantidad_digitada()
        if n is None or n < self._min or n > self._max:
            return self._al_digitar()
        ok, d = self._peticion("POST", "cotizar", {"creditos": n})
        self._precio_libre.setText(_cop(d["precio_cop"]) if ok else str(d)[:80])
        self._precio_libre_valor = d.get("precio_cop") if ok else None
        self._actualizar()

    def _actualizar(self):
        b = self._grupo.checkedButton()
        if hasattr(self, "_aviso60"):
            n = self._cantidad_digitada() if self._rb_libre is not None else None
            precio = getattr(self, "_precio_libre_valor", None)
            self._aviso60.setVisible(b is self._rb_libre and self._p60 is not None
                                     and precio is not None
                                     and n is not None and n < int(self._p60.property("creditos") or 60)
                                     and float(precio) > float(self._p60.property("precio_cop") or 0))
        if b is None:
            self._pagar.setEnabled(False); return
        if b is self._rb_libre:
            ok = getattr(self, "_precio_libre_valor", None) is not None
            self._total.setText(f"Total: {self._precio_libre.text()}" if ok else "")
        else:
            ok = True
            self._total.setText("Total: " + b.text().split("—")[1].split("(")[0].strip())
        self._pagar.setEnabled(ok)

    def _aceptar(self):
        b = self._grupo.checkedButton()
        self.eleccion = ({"creditos": self._spin.value()} if b is self._rb_libre
                         else {"paquete_id": b.property("paquete_id")})
        self.accept()
