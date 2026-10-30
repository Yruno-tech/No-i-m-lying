const overlay = document.getElementById("modal-overlay");
const modalTitle = document.getElementById("modal-title");
const modalContent = document.getElementById("modal-content");

const room = document.querySelector(".room");
const transition = document.getElementById("scene-transition");

const dialogueContent = document.getElementById("dialogue-content");
const questionForm = document.getElementById("question-form");
const questionInput = document.getElementById("question-input");
const askButton = document.getElementById("ask-button");

const decisionPanel = document.getElementById("decision-panel");
const characterIntro = document.getElementById("character-intro");

let personajeActual = null;
let preguntasRestantes = 2;
let procesando = false;


// -----------------------------------------
// VENTANAS: EXPEDIENTE Y DIARIO
// -----------------------------------------

async function abrirVentana(tipo) {

    overlay.classList.remove("hidden");

    if (tipo === "expediente") {

        modalTitle.textContent = "EXPEDIENTE DEL CASO";

        modalContent.innerHTML = "<p>Consultando expediente...</p>";

        try {

            const respuesta = await fetch("/api/expediente");
            const datos = await respuesta.json();

            if (!respuesta.ok) {
                throw new Error(datos.error);
            }

            let html = `
                <h3>${datos.caso.titulo}</h3>

                <p>${datos.caso.acontecimiento}</p>

                <h3>DESCRIPCIÓN DEL INCIDENTE</h3>

                <p>${datos.caso.incidente}</p>

                <h3>EVIDENCIAS</h3>
            `;

            datos.caso.evidencias.forEach(evidencia => {

                html += `<p>• ${evidencia}</p>`;

            });

            html += `
                <h3>LISTA DE SOSPECHOSOS</h3>
            `;

            datos.sospechosos.forEach(sospechoso => {

                html += `
                    <p>
                        <strong>${sospechoso.nombre}</strong><br>
                        ${sospechoso.profesion}
                    </p>
                `;

            });

            modalContent.innerHTML = html;

        } catch (error) {

            modalContent.textContent =
                "No se pudo cargar el expediente: " + error.message;
        }
    }

    if (tipo === "diario") {

        modalTitle.textContent = "DIARIO DEL DETECTIVE";

        const notasGuardadas =
            localStorage.getItem("notas_detective") || "";

        modalContent.innerHTML = `
            <p>
                Tus anotaciones son privadas.
                Utilizá este espacio para registrar contradicciones,
                sospechas y detalles importantes.
            </p>

            <textarea
                id="diary-notes"
                class="diary-textarea"
                placeholder="Escribe tus observaciones..."
            ></textarea>
        `;

        const textarea = document.getElementById("diary-notes");

        textarea.value = notasGuardadas;

        textarea.addEventListener("input", () => {

            localStorage.setItem(
                "notas_detective",
                textarea.value
            );

        });
    }
}


function cerrarVentana() {

    overlay.classList.add("hidden");
}


overlay.addEventListener("click", event => {

    if (event.target === overlay) {
        cerrarVentana();
    }

});


document.addEventListener("keydown", event => {

    if (event.key === "Escape") {
        cerrarVentana();
    }

});


// -----------------------------------------
// AGREGAR MENSAJES AL DIÁLOGO
// -----------------------------------------

function agregarMensaje(clase, nombre, texto) {

    const mensaje = document.createElement("p");

    mensaje.className = clase;

    if (nombre) {

        const etiqueta = document.createElement("strong");

        etiqueta.textContent = nombre + ": ";

        mensaje.appendChild(etiqueta);
    }

    const contenido = document.createElement("span");

    contenido.textContent = texto;

    mensaje.appendChild(contenido);

    dialogueContent.appendChild(mensaje);

    dialogueContent.scrollTop = dialogueContent.scrollHeight;

    return contenido;
}


// -----------------------------------------
// ACTUALIZAR CONTADOR DE PREGUNTAS
// -----------------------------------------

function actualizarContador() {

    const puntos = document.querySelectorAll(".question-dot");

    puntos.forEach((punto, indice) => {

        punto.classList.toggle(
            "active",
            indice < preguntasRestantes
        );

    });

}


// -----------------------------------------
// TRANSICIONES
// -----------------------------------------

function esperar(ms) {

    return new Promise(resolve => setTimeout(resolve, ms));

}


async function cambiarEscena(personaje) {

    procesando = true;

    // Ocultar nombre anterior.
    characterIntro.classList.remove("visible");

    // Oscurecer habitación.
    transition.classList.add("active");

    await esperar(650);

    // Cambiar escenario.
    const imagen = personaje.genero === "mujer"
        ? "interrogatorio_mujer.png"
        : "interrogatorio_hombre.jpg";

    room.style.setProperty(
        "--scene-image",
        `url("/static/images/${imagen}")`
    );

    // Preparar identificación.
    document.getElementById("intro-name").textContent =
        personaje.nombre.toUpperCase();

    document.getElementById("intro-number").textContent =
        `SOSPECHOSO N.º ${String(personaje.numero).padStart(2, "0")}`;

    document.getElementById("intro-profession").textContent =
        personaje.profesion.toUpperCase();

    document.getElementById("nombre-sospechoso").textContent =
        personaje.nombre.toUpperCase();

    await esperar(300);

    // Iluminar habitación.
    transition.classList.remove("active");

    await esperar(300);

    // Mostrar presentación.
    characterIntro.classList.remove("visible");

    void characterIntro.offsetWidth;

    characterIntro.classList.add("visible");

    await esperar(2500);

    characterIntro.classList.remove("visible");

    procesando = false;

}


// -----------------------------------------
// INICIAR PARTIDA
// -----------------------------------------

async function iniciarPartida() {

    try {

        const respuesta = await fetch("/api/start", {
            method: "POST"
        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(datos.error);
        }

        dialogueContent.innerHTML = "";

        await mostrarPersonaje(datos.estado);

    } catch (error) {

        agregarMensaje(
            "system-message",
            null,
            "No se pudo iniciar la partida: " + error.message
        );

    }

}


// -----------------------------------------
// MOSTRAR SOSPECHOSO
// -----------------------------------------

async function mostrarPersonaje(estado) {

    personajeActual = estado.personaje;

    personajeActual.numero = estado.numero;

    preguntasRestantes = 2;

    actualizarContador();

    questionForm.classList.remove("hidden");

    decisionPanel.classList.add("hidden");

    questionInput.disabled = false;

    askButton.disabled = false;

    dialogueContent.innerHTML = "";

    await cambiarEscena(personajeActual);

    agregarMensaje(
        "system-message",
        null,
        "El interrogatorio ha comenzado. Tenés dos preguntas."
    );

    questionInput.focus();

}


// -----------------------------------------
// ENVIAR PREGUNTA CON STREAMING
// -----------------------------------------

questionForm.addEventListener("submit", async event => {

    event.preventDefault();

    if (procesando || preguntasRestantes <= 0) {
        return;
    }

    const pregunta = questionInput.value.trim();

    if (!pregunta) {
        return;
    }

    procesando = true;

    questionInput.value = "";

    questionInput.disabled = true;

    askButton.disabled = true;

    agregarMensaje(
        "player-message",
        "DETECTIVE",
        pregunta
    );

    const respuestaElemento = agregarMensaje(
        "suspect-message",
        personajeActual.nombre,
        ""
    );

    try {

        const respuesta = await fetch("/api/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                pregunta: pregunta
            })

        });

        if (!respuesta.ok) {

            const error = await respuesta.json();

            throw new Error(error.error);
        }

        const reader = respuesta.body.getReader();

        const decoder = new TextDecoder();

        let buffer = "";

        while (true) {

            const { value, done } = await reader.read();

            if (done) {
                break;
            }

            buffer += decoder.decode(value, {
                stream: true
            });

            const lineas = buffer.split("\n");

            buffer = lineas.pop();

            for (const linea of lineas) {

                if (!linea.trim()) {
                    continue;
                }

                const evento = JSON.parse(linea);

                if (evento.tipo === "inicio") {

                    preguntasRestantes =
                        evento.preguntas_restantes;

                    actualizarContador();

                }

                else if (evento.tipo === "fragmento") {

                    respuestaElemento.textContent += evento.texto;

                    dialogueContent.scrollTop =
                        dialogueContent.scrollHeight;

                }

                else if (evento.tipo === "error") {

                    respuestaElemento.textContent +=
                        evento.mensaje;

                }

            }

        }

        if (buffer.trim()) {

            const evento = JSON.parse(buffer);

            if (evento.tipo === "fragmento") {

                respuestaElemento.textContent += evento.texto;

            }

        }

        // Si ya utilizó las dos preguntas, habilitar decisiones.
        if (preguntasRestantes === 0) {

            questionForm.classList.add("hidden");

            decisionPanel.classList.remove("hidden");

        } else {

            questionInput.disabled = false;

            askButton.disabled = false;

            questionInput.focus();

        }

    } catch (error) {

        agregarMensaje(
            "system-message",
            null,
            "Error: " + error.message
        );

        // No permitir continuar si no sabemos si la pregunta
        // fue procesada correctamente.
        questionForm.classList.add("hidden");

        decisionPanel.classList.add("hidden");

    }

    procesando = false;

});


// -----------------------------------------
// DECIDIR SI CAPTURAR O LIBERAR
// -----------------------------------------

async function tomarDecision(decision) {

    if (procesando) {
        return;
    }

    procesando = true;

    decisionPanel.classList.add("hidden");

    agregarMensaje(
        "player-message",
        "DETECTIVE",
        decision === "capturar"
            ? "He decidido detenerte."
            : "Podés retirarte."
    );

    await esperar(1000);

    try {

        const respuesta = await fetch("/api/decision", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                decision: decision
            })

        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(datos.error);
        }

        if (datos.terminada) {

            await mostrarResultados();

            return;
        }

        await esperar(500);

        await mostrarPersonaje(datos.estado);

    } catch (error) {

        agregarMensaje(
            "system-message",
            null,
            "Error al procesar la decisión: " + error.message
        );

        procesando = false;

    }

}


// -----------------------------------------
// RESULTADOS FINALES
// -----------------------------------------

async function mostrarResultados() {

    const respuesta = await fetch("/api/results");

    const datos = await respuesta.json();

    transition.classList.add("active");

    await esperar(1200);

    dialogueContent.innerHTML = "";

    questionForm.classList.add("hidden");

    decisionPanel.classList.add("hidden");

    modalTitle.textContent =
        datos.resultado === "victoria"
            ? "CASO RESUELTO"
            : "INVESTIGACIÓN FALLIDA";

    let html = `
        <h3>${datos.resultado.toUpperCase()}</h3>

        <p>${datos.motivo}</p>

        <h3>RESULTADOS DE LA INVESTIGACIÓN</h3>
    `;

    datos.personajes.forEach(personaje => {

        html += `
            <p>
                <strong>${personaje.nombre}</strong><br>
                ${personaje.rol} — ${personaje.estado}
            </p>
        `;

    });

    modalContent.innerHTML = html;

    overlay.classList.remove("hidden");

    procesando = false;

}


// -----------------------------------------
// COMENZAR AUTOMÁTICAMENTE
// -----------------------------------------

document.addEventListener("DOMContentLoaded", () => {

    iniciarPartida();

});