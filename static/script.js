// En static/script.js
let scriptControl = {
    ejecutando: false,
    cancelar: false
};

function mostrarMensajeEjecucion() {
    // Muestra el mensaje de ejecución
    document.getElementById("mensajeEjecucion").style.display = "block";
}

function ocultarMensajePausa() {
    // Oculta el mensaje "Pausado"
    document.getElementById("mensajeDespuesDePausa").style.display = "none";
}

// Solicita cancelar la ejecución del script
function cancelarEjecucionScript() {
    scriptControl.cancelar = true;
    ocultarMensajePausa();
}
