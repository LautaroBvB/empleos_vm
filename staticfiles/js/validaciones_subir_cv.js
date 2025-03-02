document.querySelector('form').addEventListener('submit', async function(e) {
    e.preventDefault(); // Prevenir el envío hasta verificar todo

    var dni = document.getElementById('id_dni').value;
    var contraseña = document.getElementById('id_contraseña').value;
    var confirmarContraseña = document.getElementById('id_confirmar_contraseña').value;
    var email = document.getElementById('id_email').value;
    var dia = parseInt(document.getElementById('id_dia').value, 10);
    var mes = parseInt(document.getElementById('id_mes').value, 10);
    var año = parseInt(document.getElementById('id_año').value, 10);
    var errorContainer = document.getElementById('error-container');
    var errors = [];

    // Verificar si el DNI ya existe en la base de datos mediante AJAX
    let dniExists = await fetch(`/verificar_dni/?dni=${dni}`)
        .then(response => response.json())
        .then(data => data.exists);

    if (dniExists) {
        errors.push("El DNI ya está registrado.");
    }

    // Verificar si el email ya existe en la base de datos mediante AJAX
    let emailExists = await fetch(`/verificar_email/?email=${email}`)
        .then(response => response.json())
        .then(data => data.exists);

    if (emailExists) {
        errors.push("El correo electrónico ya está registrado.");
    }

    // Verifica si las contraseñas coinciden
    if (contraseña !== confirmarContraseña) {
        errors.push("Las contraseñas no coinciden.");
    }

    // Validación de correo electrónico
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        errors.push("Correo electrónico inválido.");
    }

    // Validación de fecha
    var diasPorMes = [
        31, (año % 4 === 0 && año % 100 !== 0) || (año % 400 === 0) ? 29 : 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    ];

    if (mes < 1 || mes > 12 || dia < 1 || dia > diasPorMes[mes - 1]) {
        errors.push("Fecha inválida.");
    }

    if (errors.length > 0) {
        errorContainer.innerHTML = errors.join("<br>");
        errorContainer.style.display = 'block';
    } else {
        errorContainer.style.display = 'none';
        this.submit(); // Enviar formulario si no hay errores
    }
});
