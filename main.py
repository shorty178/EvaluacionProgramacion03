from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal con dos botones para los ejercicios"""
    return render_template('index.html')

@app.route('/ejercicio1', methods=['GET', 'POST'])
def ejercicio1():
    """Ejercicio 1: Formulario de notas y asistencia"""
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            nota1 = float(request.form.get('nota1', 0))
            nota2 = float(request.form.get('nota2', 0))
            nota3 = float(request.form.get('nota3', 0))
            asistencia = float(request.form.get('asistencia', 0))
            
            # Validar rangos
            if not (10 <= nota1 <= 70) or not (10 <= nota2 <= 70) or not (10 <= nota3 <= 70):
                abort(400)  # Bad Request - valores fuera de rango
            
            if not (0 <= asistencia <= 100):
                abort(400)  # Bad Request - asistencia fuera de rango
            
            # Calcular el promedio
            promedio = (nota1 + nota2 + nota3) / 3
            
            # Determinar si está aprobado o reprobado
            # Condiciones: promedio >= 40 Y asistencia >= 75%
            aprobado = promedio >= 40 and asistencia >= 75
            estado = "APROBADO" if aprobado else "REPROBADO"
            
            return render_template('ejercicio1.html', 
                                 nota1=nota1, 
                                 nota2=nota2, 
                                 nota3=nota3, 
                                 asistencia=asistencia,
                                 promedio=round(promedio, 2), 
                                 estado=estado,
                                 mostrar_resultado=True)
        except (ValueError, TypeError):
            abort(400)  # Bad Request - datos inválidos
    
    return render_template('ejercicio1.html', mostrar_resultado=False)

@app.route('/ejercicio2', methods=['GET', 'POST'])
def ejercicio2():
    """Ejercicio 2: Formulario de nombres"""
    if request.method == 'POST':
        # Obtener los tres nombres
        nombre1 = request.form.get('nombre1', '').strip()
        nombre2 = request.form.get('nombre2', '').strip()
        nombre3 = request.form.get('nombre3', '').strip()
        
        # Validar que los nombres no estén vacíos
        if not nombre1 or not nombre2 or not nombre3:
            abort(400)  # Bad Request - nombres vacíos
        
        # Encontrar el nombre con más caracteres
        nombres = [nombre1, nombre2, nombre3]
        nombre_mas_largo = max(nombres, key=len)
        cantidad_caracteres = len(nombre_mas_largo)
        
        return render_template('ejercicio2.html',
                             nombre1=nombre1,
                             nombre2=nombre2,
                             nombre3=nombre3,
                             nombre_mas_largo=nombre_mas_largo,
                             cantidad_caracteres=cantidad_caracteres,
                             mostrar_resultado=True)
    
    return render_template('ejercicio2.html', mostrar_resultado=False)

@app.route('/ejercicio1/<int:nota_param>')
def ejercicio1_con_parametro(nota_param):
    """Ejemplo de enrutamiento con parámetro en URL (método GET)"""
    # Validar que el parámetro esté en el rango válido
    if not (10 <= nota_param <= 70):
        abort(400)  # Bad Request
    # Redirigir al formulario con el parámetro prellenado
    return redirect(url_for('ejercicio1', nota_predefinida=nota_param))

@app.errorhandler(400)
def bad_request(error):
    """Manejo de errores 400 - Bad Request"""
    return render_template('error.html', 
                         codigo=400, 
                         mensaje="Solicitud inválida. Por favor, verifica los datos ingresados."), 400

@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404 - Not Found"""
    return render_template('error.html', 
                         codigo=404, 
                         mensaje="Página no encontrada."), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500 - Internal Server Error"""
    return render_template('error.html', 
                         codigo=500, 
                         mensaje="Error interno del servidor."), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

