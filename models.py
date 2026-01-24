from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


# 1. EMPRESAS
# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class Empresa(db.Model):
    __tablename__ = 'empresas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_comercial = db.Column(db.String(150), nullable=False)
    razon_social = db.Column(db.String(200))
    giro = db.Column(db.String(100))
    tamano_empresa = db.Column(db.String(50))  # New
    ciudad = db.Column(db.String(100))
    estado = db.Column(db.String(100))  # New
    pais = db.Column(db.String(100))  # New
    sitio_web = db.Column(db.String(200))
    linkedin_empresa = db.Column(db.String(200))  # New
    tipo_cliente = db.Column(db.String(50))  # New
    proveedor_actual = db.Column(db.String(150))  # New
    presupuesto_estimado = db.Column(db.Numeric(12, 2))
    temporada_clave = db.Column(db.String(100))  # New
    prioridad_compra = db.Column(db.String(50))  # New
    sensibilidad_precio = db.Column(db.String(50))  # New
    objetivo_principal = db.Column(db.String(150))  # New
    estatus_empresa = db.Column(db.String(50))
    fecha_alta = db.Column(db.Date, default=date.today)
    comentarios = db.Column(db.Text)

    # Relationships
    contactos = db.relationship('Contacto', backref='empresa', lazy=True)
    intereses = db.relationship('Interes', backref='empresa', lazy=True)
    seguimientos = db.relationship('Seguimiento', backref='empresa', lazy=True)
    eventos = db.relationship('Evento', backref='empresa', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre_comercial': self.nombre_comercial,
            'ciudad': self.ciudad,
            'estatus': self.estatus_empresa
        }


# 2. CONTACTOS
# models.py (Partial Update)

class Contacto(db.Model):
    __tablename__ = 'contactos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'))
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    puesto = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    email = db.Column(db.String(150))
    telefono = db.Column(db.String(50))

    # --- NEW FIELDS ---
    whatsapp = db.Column(db.String(50))
    linkedin = db.Column(db.String(200))
    nivel_decision = db.Column(db.String(50))
    contacto_principal = db.Column(db.Boolean, default=False)
    preferencia_contacto = db.Column(db.String(50))
    # ------------------

    comentarios = db.Column(db.Text)


# 3. INTERESES
class Interes(db.Model):
    __tablename__ = 'intereses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'))
    tipo_interes = db.Column(db.String(50))
    producto = db.Column(db.String(100))
    volumen_estimado = db.Column(db.Integer)
    frecuencia_compra = db.Column(db.String(50))
    fecha_probable = db.Column(db.Date)
    nivel_urgencia = db.Column(db.String(50))
    comentarios = db.Column(db.Text)


# models.py (Ensure these classes are present/updated)

class Seguimiento(db.Model):
    __tablename__ = 'seguimiento'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    contacto_id = db.Column(db.Integer, db.ForeignKey('contactos.id'))
    fecha_contacto = db.Column(db.Date, nullable=False)
    tipo_contacto = db.Column(db.String(50))  # Call, Email, Meeting
    etapa_venta = db.Column(db.String(50))  # Prospecting, Negotiation, Closed
    resultado = db.Column(db.String(100))
    proximo_paso = db.Column(db.String(150))
    fecha_proximo_contacto = db.Column(db.Date)
    probabilidad_cierre = db.Column(db.Integer)  # 0-100
    responsable = db.Column(db.String(100))
    comentarios = db.Column(db.Text)

    # Relationship to access Contact name easily
    contacto = db.relationship('Contacto', backref='seguimientos')


class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'))
    tipo_evento = db.Column(db.String(100))
    nombre_evento = db.Column(db.String(150))
    fecha_evento = db.Column(db.Date)
    cantidad_personas = db.Column(db.Integer)
    servicios = db.Column(db.String(200))
    presupuesto = db.Column(db.Numeric(12, 2))
    estatus_evento = db.Column(db.String(50))
    comentarios = db.Column(db.Text)