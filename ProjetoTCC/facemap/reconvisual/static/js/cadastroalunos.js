function capturaRosto() {
    fetch('/captura-rosto/', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        // Coloca a imagem base64 no campo escondido do formulário
        document.getElementById('imagem_rosto').value = data.imagem_rosto;
    })
    .catch(error => {
        console.error('Erro ao capturar a imagem:', error);
        alert('Falha na captura de imagem');
    });
}