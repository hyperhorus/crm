from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Empresa, Contacto

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/empresas')
def ver_empresas():
    # Query all companies from MySQL
    lista_empresas = Empresa.query.order_by(Empresa.id.desc()).all()
    return render_template('listado.html', empresas=lista_empresas)


@app.route('/nueva-empresa', methods=['GET', 'POST'])
def crear_empresa():
    if request.method == 'POST':
        # Get data from HTML form
        nombre = request.form['nombre_comercial']
        razon = request.form['razon_social']
        giro = request.form['giro']
        ciudad = request.form['ciudad']
        web = request.form['sitio_web']
        presupuesto = request.form['presupuesto'] or 0

        # Create Object
        nueva = Empresa(
            nombre_comercial=nombre,
            razon_social=razon,
            giro=giro,
            ciudad=ciudad,
            sitio_web=web,
            presupuesto_estimado=presupuesto,
            estatus_empresa='Prospecto'
        )

        # Save to DB
        try:
            db.session.add(nueva)
            db.session.commit()
            flash('Empresa agregada correctamente')
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
        # Create the object from form data
        nuevo_contacto = Contacto(
            empresa_id=request.form['empresa_id'],
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            puesto=request.form['puesto'],
            departamento=request.form['departamento'],
            email=request.form['email'],
            telefono=request.form['telefono'],
            comentarios=request.form['comentarios']
        )
        db.session.add(nuevo_contacto)
        db.session.commit()
        flash('Contacto creado exitosamente')

        # Redirect back to the Company Detail page if possible, otherwise list
        return redirect(url_for('detalle_empresa', id=request.form['empresa_id']))

        # --- GET REQUEST CHANGES ---
        # Check if we clicked "Add Contact" from a specific company page
    preselected_empresa_id = request.args.get('empresa_id')

    empresas = Empresa.query.order_by(Empresa.nombre_comercial).all()

    return render_template('contactos_crear.html',
                           empresas=empresas,
                           preselected_id=preselected_empresa_id)


# --- NEW ROUTE: EDITAR EMPRESA ---
@app.route('/empresa/editar/<int:id>', methods=['GET', 'POST'])
def editar_empresa(id):
    empresa = Empresa.query.get_or_404(id)

    if request.method == 'POST':
        # Update fields
        empresa.nombre_comercial = request.form['nombre_comercial']
        empresa.razon_social = request.form['razon_social']
        empresa.giro = request.form['giro']
        empresa.ciudad = request.form['ciudad']
        empresa.sitio_web = request.form['sitio_web']
        empresa.presupuesto_estimado = request.form['presupuesto'] or 0

        try:
            db.session.commit()
            flash('Información actualizada correctamente')
            return redirect(url_for('detalle_empresa', id=empresa.id))
        except Exception as e:
            return f"Error al actualizar: {e}"

    return render_template('editar_empresa.html', empresa=empresa)

# ... existing imports and code ...

# --- NEW ROUTE: EDIT CONTACT ---
@app.route('/contacto/editar/<int:id>', methods=['GET', 'POST'])
def editar_contacto(id):
    contacto = Contacto.query.get_or_404(id)

    if request.method == 'POST':
        # Update fields with form data
        contacto.empresa_id = request.form['empresa_id']
        contacto.nombre = request.form['nombre']
        contacto.apellido = request.form['apellido']
        contacto.puesto = request.form['puesto']
        contacto.departamento = request.form['departamento']
        contacto.email = request.form['email']
        contacto.telefono = request.form['telefono']
        contacto.comentarios = request.form['comentarios']

        try:
            db.session.commit()
            flash('Contacto actualizado correctamente')
            # Redirect back to the Company Detail page to see the result
            return redirect(url_for('detalle_empresa', id=contacto.empresa_id))
        except Exception as e:
            return f"Error al actualizar: {e}"

    # GET Request: Fetch all companies for the dropdown
    empresas = Empresa.query.order_by(Empresa.nombre_comercial).all()
    return render_template('contactos_editar.html', contacto=contacto, empresas=empresas)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
