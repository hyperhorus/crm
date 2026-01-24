from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Empresa, Contacto, Evento, Seguimiento
from datetime import date

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_app(app)


@app.route('/')
def index():
    hoy = date.today()

    alertas = Seguimiento.query.filter_by(fecha_proximo_contacto=hoy).all()
    return render_template('index.html', alertas=alertas)


@app.route('/empresas')
def ver_empresas():
    # Query all companies from MySQL
    lista_empresas = Empresa.query.order_by(Empresa.id.desc()).all()
    return render_template('listado.html', empresas=lista_empresas)


@app.route('/nueva-empresa', methods=['GET', 'POST'])
def crear_empresa():
    if request.method == 'POST':
        try:
            nueva = Empresa(
                nombre_comercial=request.form['nombre_comercial'],
                razon_social=request.form.get('razon_social'),
                giro=request.form.get('giro'),
                tamano_empresa=request.form.get('tamano_empresa'),
                ciudad=request.form.get('ciudad'),
                estado=request.form.get('estado'),
                pais=request.form.get('pais'),
                sitio_web=request.form.get('sitio_web'),
                linkedin_empresa=request.form.get('linkedin_empresa'),
                tipo_cliente=request.form.get('tipo_cliente'),
                proveedor_actual=request.form.get('proveedor_actual'),
                presupuesto_estimado=request.form.get('presupuesto') or 0,
                temporada_clave=request.form.get('temporada_clave'),
                prioridad_compra=request.form.get('prioridad_compra'),
                sensibilidad_precio=request.form.get('sensibilidad_precio'),
                objetivo_principal=request.form.get('objetivo_principal'),
                estatus_empresa='Prospecto', # Default status
                comentarios=request.form.get('comentarios')
            )

            db.session.add(nueva)
            db.session.commit()
            flash('Empresa creada exitosamente')
            return redirect(url_for('ver_empresas'))
        except Exception as e:
            return f"Error al guardar: {e}"

    return render_template('crear.html')


@app.route('/empresa/<int:id>')
def detalle_empresa(id):
    # Get specific company or show 404 error
    empresa = Empresa.query.get_or_404(id)
    return render_template('detalle.html', empresa=empresa)


@app.route('/contactos')
def ver_contactos():
    # Fetch all contacts, ordered by ID desc
    contactos = Contacto.query.order_by(Contacto.id.desc()).all()
    return render_template('contactos_listado.html', contactos=contactos)


@app.route('/nuevo-contacto', methods=['GET', 'POST'])
def crear_contacto():
    if request.method == 'POST':
        # Checkbox handling: if present in form, it's True, else False
        es_principal = True if request.form.get('contacto_principal') else False

        nuevo_contacto = Contacto(
            empresa_id=request.form['empresa_id'],
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            puesto=request.form['puesto'],
            departamento=request.form['departamento'],
            email=request.form['email'],
            telefono=request.form['telefono'],
            # New Fields
            whatsapp=request.form['whatsapp'],
            linkedin=request.form['linkedin'],
            nivel_decision=request.form['nivel_decision'],
            preferencia_contacto=request.form['preferencia_contacto'],
            contacto_principal=es_principal,

            comentarios=request.form['comentarios']
        )

        try:
            db.session.add(nuevo_contacto)
            db.session.commit()
            flash('Contacto creado exitosamente')
            # Redirect to the company detail to see it added
            return redirect(url_for('detalle_empresa', id=request.form['empresa_id']))
        except Exception as e:
            return f"Error: {e}"

    # GET Request
    preselected_empresa_id = request.args.get('empresa_id')
    empresas = Empresa.query.order_by(Empresa.nombre_comercial).all()
    return render_template('contactos_crear.html', empresas=empresas, preselected_id=preselected_empresa_id)


# --- NEW ROUTE: VIEW CONTACT DETAILS (READ ONLY) ---
@app.route('/contacto/ver/<int:id>')
def ver_contacto(id):
    # Fetch contact or 404
    contacto = Contacto.query.get_or_404(id)
    return render_template('ver_contacto.html', contacto=contacto)

# --- NEW ROUTE: EDITAR EMPRESA ---
@app.route('/empresa/editar/<int:id>', methods=['GET', 'POST'])
def editar_empresa(id):
    empresa = Empresa.query.get_or_404(id)

    if request.method == 'POST':
        try:
            empresa.nombre_comercial = request.form['nombre_comercial']
            empresa.razon_social = request.form.get('razon_social')
            empresa.giro = request.form.get('giro')
            empresa.tamano_empresa = request.form.get('tamano_empresa')
            empresa.ciudad = request.form.get('ciudad')
            empresa.estado = request.form.get('estado')
            empresa.pais = request.form.get('pais')
            empresa.sitio_web = request.form.get('sitio_web')
            empresa.linkedin_empresa = request.form.get('linkedin_empresa')
            empresa.tipo_cliente = request.form.get('tipo_cliente')
            empresa.proveedor_actual = request.form.get('proveedor_actual')

            presupuesto = request.form.get('presupuesto')
            empresa.presupuesto_estimado = presupuesto if presupuesto else 0

            empresa.temporada_clave = request.form.get('temporada_clave')
            empresa.prioridad_compra = request.form.get('prioridad_compra')
            empresa.sensibilidad_precio = request.form.get('sensibilidad_precio')
            empresa.objetivo_principal = request.form.get('objetivo_principal')
            empresa.estatus_empresa = request.form.get('estatus_empresa')
            empresa.comentarios = request.form.get('comentarios')

            db.session.commit()
            flash('Información actualizada correctamente')
            return redirect(url_for('detalle_empresa', id=empresa.id))
        except Exception as e:
            return f"Error al actualizar: {e}"

    return render_template('editar_empresa.html', empresa=empresa)

@app.route('/contacto/editar/<int:id>', methods=['GET', 'POST'])
def editar_contacto(id):
    contacto = Contacto.query.get_or_404(id)

    if request.method == 'POST':
        contacto.empresa_id = request.form['empresa_id']
        contacto.nombre = request.form['nombre']
        contacto.apellido = request.form['apellido']
        contacto.puesto = request.form['puesto']
        contacto.departamento = request.form['departamento']
        contacto.email = request.form['email']
        contacto.telefono = request.form['telefono']

        # New Fields
        contacto.whatsapp = request.form['whatsapp']
        contacto.linkedin = request.form['linkedin']
        contacto.nivel_decision = request.form['nivel_decision']
        contacto.preferencia_contacto = request.form['preferencia_contacto']
        # Checkbox logic for edit
        contacto.contacto_principal = True if request.form.get('contacto_principal') else False

        contacto.comentarios = request.form['comentarios']

        try:
            db.session.commit()
            flash('Contacto actualizado correctamente')
            return redirect(url_for('detalle_empresa', id=contacto.empresa_id))
        except Exception as e:
            return f"Error al actualizar: {e}"

    empresas = Empresa.query.order_by(Empresa.nombre_comercial).all()
    return render_template('contactos_editar.html', contacto=contacto, empresas=empresas)

#####Formateo del telefono
# app.py

@app.template_filter('formatea_telefono')
def formatea_telefono(value):
    """Convierte un número de 10 dígitos en formato xxx-xxx-xxxx"""
    if not value:
        return "No registrado"
    digits = ''.join(filter(str.isdigit, str(value)))
    if len(digits) == 10:
        return f"{digits[0:3]}-{digits[3:6]}-{digits[6:10]}"
    return value  # Si no tiene 10 dígitos, lo devuelve tal cual


# --- RUTAS SEGUIMIENTO (FOLLOW-UP) ---

@app.route('/seguimiento/nuevo/<int:empresa_id>', methods=['GET', 'POST'])
def crear_seguimiento(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)

    if request.method == 'POST':
        nuevo = Seguimiento(
            empresa_id=empresa_id,
            contacto_id=request.form.get('contacto_id') or None,
            fecha_contacto=request.form['fecha_contacto'],
            tipo_contacto=request.form['tipo_contacto'],
            etapa_venta=request.form['etapa_venta'],
            resultado=request.form['resultado'],
            proximo_paso=request.form['proximo_paso'],
            fecha_proximo_contacto=request.form['fecha_proximo_contacto'] or None,
            probabilidad_cierre=request.form['probabilidad_cierre'] or 0,
            responsable=request.form['responsable'],
            comentarios=request.form['comentarios']
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Seguimiento registrado')
        return redirect(url_for('detalle_empresa', id=empresa_id))

    return render_template('seguimiento_form.html', empresa=empresa, seguimiento=None)


@app.route('/seguimiento/editar/<int:id>', methods=['GET', 'POST'])
def editar_seguimiento(id):
    seg = Seguimiento.query.get_or_404(id)
    empresa = Empresa.query.get(seg.empresa_id)

    if request.method == 'POST':
        seg.contacto_id = request.form.get('contacto_id') or None
        seg.fecha_contacto = request.form['fecha_contacto']
        seg.tipo_contacto = request.form['tipo_contacto']
        seg.etapa_venta = request.form['etapa_venta']
        seg.resultado = request.form['resultado']
        seg.proximo_paso = request.form['proximo_paso']
        seg.fecha_proximo_contacto = request.form['fecha_proximo_contacto'] or None
        seg.probabilidad_cierre = request.form['probabilidad_cierre'] or 0
        seg.responsable = request.form['responsable']
        seg.comentarios = request.form['comentarios']

        db.session.commit()
        flash('Seguimiento actualizado')
        return redirect(url_for('detalle_empresa', id=seg.empresa_id))

    return render_template('seguimiento_form.html', empresa=empresa, seguimiento=seg)


@app.route('/seguimiento/eliminar/<int:id>')
def eliminar_seguimiento(id):
    seg = Seguimiento.query.get_or_404(id)
    empresa_id = seg.empresa_id
    db.session.delete(seg)
    db.session.commit()
    flash('Registro eliminado')
    return redirect(url_for('detalle_empresa', id=empresa_id))


# --- RUTAS EVENTOS ---

@app.route('/evento/nuevo/<int:empresa_id>', methods=['GET', 'POST'])
def crear_evento(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)

    if request.method == 'POST':
        nuevo = Evento(
            empresa_id=empresa_id,
            tipo_evento=request.form['tipo_evento'],
            nombre_evento=request.form['nombre_evento'],
            fecha_evento=request.form['fecha_evento'],
            cantidad_personas=request.form['cantidad_personas'] or 0,
            servicios=request.form['servicios'],
            presupuesto=request.form['presupuesto'] or 0,
            estatus_evento=request.form['estatus_evento'],
            comentarios=request.form['comentarios']
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Evento creado exitosamente')
        return redirect(url_for('detalle_empresa', id=empresa_id))

    return render_template('eventos_form.html', empresa=empresa, evento=None)


@app.route('/evento/editar/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):
    evt = Evento.query.get_or_404(id)
    empresa = Empresa.query.get(evt.empresa_id)

    if request.method == 'POST':
        evt.tipo_evento = request.form['tipo_evento']
        evt.nombre_evento = request.form['nombre_evento']
        evt.fecha_evento = request.form['fecha_evento']
        evt.cantidad_personas = request.form['cantidad_personas'] or 0
        evt.servicios = request.form['servicios']
        evt.presupuesto = request.form['presupuesto'] or 0
        evt.estatus_evento = request.form['estatus_evento']
        evt.comentarios = request.form['comentarios']

        db.session.commit()
        flash('Evento actualizado')
        return redirect(url_for('detalle_empresa', id=evt.empresa_id))

    return render_template('eventos_form.html', empresa=empresa, evento=evt)


@app.route('/evento/eliminar/<int:id>')
def eliminar_evento(id):
    evt = Evento.query.get_or_404(id)
    empresa_id = evt.empresa_id
    db.session.delete(evt)
    db.session.commit()
    flash('Evento eliminado')
    return redirect(url_for('detalle_empresa', id=empresa_id))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
