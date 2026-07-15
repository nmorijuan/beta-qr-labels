/* ============================================== */
/* VARIABLES GLOBALES */
/* ============================================== */

let currentFile = null;
let currentZplFile = null;

/* ============================================== */
/* ELEMENTOS DEL DOM */
/* ============================================== */

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadSection = document.getElementById('upload-section');
const previewSection = document.getElementById('preview-section');
const generationSection = document.getElementById('generation-section');
const fileName = document.getElementById('fileName');
const totalRecords = document.getElementById('totalRecords');
const previewTable = document.getElementById('previewTable');
const tableHeader = document.getElementById('tableHeader');
const tableBody = document.getElementById('tableBody');
const changeFileBtn = document.getElementById('changeFileBtn');
const generateBtn = document.getElementById('generateBtn');
const newFileBtn = document.getElementById('newFileBtn');
const printBtn = document.getElementById('printBtn');
const downloadBtn = document.getElementById('downloadBtn');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');
const quantity = document.getElementById('quantity');
const zplPreview = document.getElementById('zplPreview');
const printerSection = document.getElementById('printerSection');
const printerSelect = document.getElementById('printerSelect');

/* ============================================== */
/* EVENT LISTENERS - CARGA DE ARCHIVO */
/* ============================================== */

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        handleFileSelection();
    }
});

fileInput.addEventListener('change', handleFileSelection);

/* ============================================== */
/* MANEJADORES DE EVENTOS */
/* ============================================== */

function handleFileSelection() {
    const file = fileInput.files[0];
    
    if (!file) {
        showToast('No se seleccionó archivo', 'error');
        return;
    }
    
    // Validar extensión
    if (!['xlsx', 'xls'].includes(file.name.split('.').pop().toLowerCase())) {
        showToast('Formato de archivo no válido. Usa .xlsx o .xls', 'error');
        fileInput.value = '';
        return;
    }
    
    // Validar tamaño (5MB)
    if (file.size > 5 * 1024 * 1024) {
        showToast('Archivo demasiado grande. Máximo 5MB', 'error');
        fileInput.value = '';
        return;
    }
    
    currentFile = file.name;
    uploadFile(file);
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Mostrar estado de carga
    uploadArea.style.opacity = '0.6';
    uploadArea.style.pointerEvents = 'none';
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        uploadArea.style.opacity = '1';
        uploadArea.style.pointerEvents = 'auto';
        
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Error en la carga');
            });
        }
        return response.json();
    })
    .then(data => {
        showToast('Archivo cargado exitosamente', 'success');
        displayPreview(data);
    })
    .catch(error => {
        showToast(error.message, 'error');
        fileInput.value = '';
        currentFile = null;
    });
}

function displayPreview(data) {
    fileName.textContent = data.file;
    totalRecords.textContent = data.preview.total;
    
    // Llenar tabla
    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';
    
    if (data.preview.columnas && data.preview.columnas.length > 0) {
        // Encabezados
        data.preview.columnas.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col;
            tableHeader.appendChild(th);
        });
        
        // Datos
        data.preview.datos.forEach(row => {
            const tr = document.createElement('tr');
            data.preview.columnas.forEach(col => {
                const td = document.createElement('td');
                td.textContent = row[col] || '-';
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });
    }
    
    // Mostrar sección de preview
    uploadSection.classList.add('hidden');
    previewSection.classList.remove('hidden');
    
    // Scroll al preview
    previewSection.scrollIntoView({ behavior: 'smooth' });
}

changeFileBtn.addEventListener('click', () => {
    uploadSection.classList.remove('hidden');
    previewSection.classList.add('hidden');
    generationSection.classList.add('hidden');
    fileInput.value = '';
    currentFile = null;
    currentZplFile = null;
});

generateBtn.addEventListener('click', () => {
    if (!currentFile) {
        showToast('No hay archivo seleccionado', 'error');
        return;
    }
    
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="spinner"></span> Generando...';
    
    fetch('/api/generate-zpl', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ file: currentFile })
    })
    .then(response => {
        generateBtn.disabled = false;
        generateBtn.innerHTML = 'Generar Etiquetas →';
        
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Error generando etiquetas');
            });
        }
        return response.json();
    })
    .then(data => {
        showToast('Etiquetas generadas correctamente', 'success');
        displayGeneration(data);
    })
    .catch(error => {
        generateBtn.disabled = false;
        generateBtn.innerHTML = 'Generar Etiquetas →';
        showToast(error.message, 'error');
    });
});

function displayGeneration(data) {
    currentZplFile = data.zpl_file;
    quantity.textContent = data.cantidad;
    zplPreview.textContent = data.preview;
    
    // Mostrar sección de generación
    previewSection.classList.add('hidden');
    generationSection.classList.remove('hidden');
    
    // Cargar impresoras
    loadPrinters();
    
    // Scroll a la sección
    generationSection.scrollIntoView({ behavior: 'smooth' });
}

newFileBtn.addEventListener('click', () => {
    uploadSection.classList.remove('hidden');
    generationSection.classList.add('hidden');
    fileInput.value = '';
    currentFile = null;
    currentZplFile = null;
});

downloadBtn.addEventListener('click', () => {
    if (!currentZplFile) {
        showToast('No hay archivo ZPL disponible', 'error');
        return;
    }
    
    downloadBtn.disabled = true;
    downloadBtn.innerHTML = '<span class="spinner"></span> Descargando...';
    
    fetch(`/api/download-zpl/${encodeURIComponent(currentZplFile)}`)
    .then(response => {
        downloadBtn.disabled = false;
        downloadBtn.innerHTML = '⬇ Descargar ZPL';
        
        if (!response.ok) throw new Error('Error descargando archivo');
        
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = currentZplFile;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        showToast('Archivo descargado', 'success');
    })
    .catch(error => {
        downloadBtn.disabled = false;
        downloadBtn.innerHTML = '⬇ Descargar ZPL';
        showToast('Error descargando archivo', 'error');
    });
});

printBtn.addEventListener('click', () => {
    if (!currentZplFile) {
        showToast('No hay archivo ZPL disponible', 'error');
        return;
    }
    
    printBtn.disabled = true;
    printBtn.innerHTML = '<span class="spinner"></span> Imprimiendo...';
    
    fetch('/api/print', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            zpl_file: currentZplFile,
            printer: printerSelect.value || null
        })
    })
    .then(response => {
        printBtn.disabled = false;
        printBtn.innerHTML = '🖨 Enviar a Imprimir';
        
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Error imprimiendo');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.warning) {
            showToast(data.message, 'warning');
        } else {
            showToast(data.message, 'success');
        }
    })
    .catch(error => {
        printBtn.disabled = false;
        printBtn.innerHTML = '🖨 Enviar a Imprimir';
        showToast(error.message, 'error');
    });
});

/* ============================================== */
/* FUNCIONES AUXILIARES */
/* ============================================== */

function showToast(message, type = 'info') {
    toastMessage.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 5000);
}

function loadPrinters() {
    fetch('/api/printers')
    .then(response => response.json())
    .then(data => {
        if (data.success && data.printers && data.printers.length > 0) {
            printerSelect.innerHTML = '<option value="">Impresora predeterminada</option>';
            
            data.printers.forEach(printer => {
                const option = document.createElement('option');
                option.value = printer;
                option.textContent = printer;
                if (printer === data.default) {
                    option.selected = true;
                    option.textContent += ' (predeterminada)';
                }
                printerSelect.appendChild(option);
            });
            
            printerSection.classList.remove('hidden');
        } else {
            printerSection.classList.add('hidden');
        }
    })
    .catch(error => {
        console.warn('No se pudieron cargar las impresoras:', error);
        printerSection.classList.add('hidden');
    });
}

/* ============================================== */
/* INICIALIZACIÓN */
/* ============================================== */

console.log('✓ Aplicación QR Colmenas iniciada');
