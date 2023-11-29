// En static/script.js
let ejecutandoScript = false;
let cancelarEjecucion = false;

function ejecutarScript() {
    // Llamas a la función para mostrar el mensaje cuando comienza la ejecución del script
    mostrarMensajeBoton();

    // Marca el script como en ejecución
    ejecutandoScript = true;

    // Lógica para ejecutar el script

    // Enviar la solicitud POST a /execute
    fetch('/execute', {
        method: 'POST',
        body: new URLSearchParams(new FormData(document.querySelector('form'))),
    })
    .then(response => response.json())
    .then(data => {
        // Manejar la respuesta del servidor
        console.log(data.result);
        console.log(data.resultado);
    })
    .catch(error => {
        console.error('Error al enviar la solicitud:', error);
    })
    .finally(() => {
        // Marca el script como no en ejecución después de la pausa
        ejecutandoScript = false;

        // Oculta el mensaje después de unos segundos (puedes ajustar el tiempo)
        document.getElementById("mensajeEjecucion").style.display = "none";
        document.getElementById("mensajeDespuesDePausa").style.display = "none";
    });
}

function cancelarEjecucionScript() {
    // Solicita cancelar la ejecución del script
    cancelarEjecucion = true;

    // Oculta el mensaje "Pausado"
    document.getElementById("mensajeDespuesDePausa").style.display = "none";
}

function mostrarMensajeBoton() {
    // Muestra el mensaje de ejecución
    document.getElementById("mensajeEjecucion").style.display = "block";
}