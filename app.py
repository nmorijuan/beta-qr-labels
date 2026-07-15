"""
Aplicación Flask para generar e imprimir etiquetas QR de colmenas
"""

import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from pathlib import Path
import tempfile
from src.generar_zpl_web import generar_zpl_desde_excel, generar_preview_excel

# =====================================================
# CONFIGURACIÓN
# =====================================================

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Crear carpeta de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =====================================================
# RUTAS
# =====================================================

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Maneja la carga del archivo Excel"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use .xlsx or .xls'}), 400
        
        # Guardar archivo temporalmente
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generar preview
        try:
            preview = generar_preview_excel(filepath)
            return jsonify({
                'success': True,
                'file': filename,
                'preview': preview
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Upload error: {str(e)}'}), 500

@app.route('/api/generate-zpl', methods=['POST'])
def generate_zpl():
    """Genera las etiquetas ZPL"""
    try:
        data = request.get_json()
        filename = data.get('file')
        
        if not filename:
            return jsonify({'error': 'No file specified'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 400
        
        # Generar ZPL
        zpl_content = generar_zpl_desde_excel(filepath)
        
        # Guardar ZPL temporalmente
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}.zpl')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(zpl_content)
        
        # Contar etiquetas
        cantidad = zpl_content.count('^XA')
        
        return jsonify({
            'success': True,
            'cantidad': cantidad,
            'zpl_file': f'{filename}.zpl',
            'preview': zpl_content[:500] + '...' if len(zpl_content) > 500 else zpl_content
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Generation error: {str(e)}'}), 500

@app.route('/api/print', methods=['POST'])
def print_zpl():
    """Envía a imprimir"""
    try:
        data = request.get_json()
        zpl_file = data.get('zpl_file')
        printer_name = data.get('printer', None)
        
        if not zpl_file:
            return jsonify({'error': 'No ZPL file specified'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(zpl_file))
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'ZPL file not found'}), 400
        
        # Intentar imprimir
        try:
            import win32print
            with open(filepath, 'r', encoding='utf-8') as f:
                zpl_content = f.read()
            
            printer = printer_name or win32print.GetDefaultPrinter()
            
            # Enviar a la impresora
            hprinter = win32print.OpenPrinter(printer)
            win32print.WritePrinter(hprinter, zpl_content.encode('utf-8'))
            win32print.ClosePrinter(hprinter)
            
            return jsonify({
                'success': True,
                'message': f'Enviado a imprimir en: {printer}'
            }), 200
        
        except ImportError:
            # Si no está en Windows, solo mostrar mensaje
            return jsonify({
                'success': True,
                'message': 'Sistema no Windows. Archivo ZPL generado correctamente.',
                'warning': 'Para imprimir, descargue el archivo ZPL y envíelo manualmente a su impresora Zebra.'
            }), 200
    
    except Exception as e:
        return jsonify({'error': f'Print error: {str(e)}'}), 500

@app.route('/api/download-zpl/<filename>')
def download_zpl(filename):
    """Descarga el archivo ZPL"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/api/printers', methods=['GET'])
def get_printers():
    """Obtiene lista de impresoras disponibles"""
    try:
        import win32print
        printers = win32print.EnumPrinters(2)  # PRINTER_ENUM_LOCAL
        printer_list = [p[2] for p in printers]
        
        return jsonify({
            'success': True,
            'printers': printer_list,
            'default': win32print.GetDefaultPrinter()
        }), 200
    
    except ImportError:
        return jsonify({
            'success': False,
            'message': 'Sistema no Windows. Funcionalidad de impresoras no disponible.'
        }), 200
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

# =====================================================
# ERROR HANDLERS
# =====================================================

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum 5MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

# =====================================================
# MAIN
# =====================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
