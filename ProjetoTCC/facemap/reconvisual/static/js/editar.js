document.getElementById('form-busca').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('form-busca').style.display = 'none'; // Oculta a div de busca
    document.getElementById('resultado-busca').style.display = 'block';
});