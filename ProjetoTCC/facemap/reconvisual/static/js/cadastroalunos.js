let video = document.getElementById('video');
let imagemRosto = document.getElementById('imagem_rosto');
let cameraContainer = document.getElementById('camera-container');

// Função para abrir a câmera
function abrirCamera() {
    cameraContainer.style.display = 'block';
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
            })
            .catch(function (error) {
                alert("Erro ao acessar a câmera: " + error.message);
            });
    } else {
        alert("Acesso à câmera não é suportado neste navegador.");
    }
}

// Função para capturar a imagem da câmera
function tirarFoto() {
    let canvas = document.createElement('canvas');
    canvas.width = 320;
    canvas.height = 240;
    let context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Converte a imagem em base64
    let imagemBase64 = canvas.toDataURL('image/jpeg');
    
    // Armazena a imagem no campo oculto do formulário
    imagemRosto.value = imagemBase64;

    // Opcional: parar o vídeo após a captura
    let stream = video.srcObject;
    let tracks = stream.getTracks();
    tracks.forEach(track => track.stop());
    video.srcObject = null;

    alert('Foto capturada com sucesso!');
}