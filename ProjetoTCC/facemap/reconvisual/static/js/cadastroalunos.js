let video = document.getElementById('video');
let imagemRosto = document.getElementById('imagem_rosto');
let cameraContainer = document.getElementById('camera-container');
let fotosCapturadas = [];
const maxFotos = 25;
const intervaloEntreFotos = 2000; // 2 segundos
let statusMessage = document.getElementById('status-message');
let finalMessage = document.getElementById('final-message');

// Abre a câmera ao clicar no botão "Capturar"
function iniciarCaptura() {
    cameraContainer.style.display = "block";

    // Acessa a webcam
    navigator.mediaDevices.getUserMedia({ 
        video:{ width: { ideal: 1200 }, height: {ideal: 720} }
    })
        .then(function(stream) {
            video.srcObject = stream;
            statusMessage.textContent = "A câmera está ligada. Clique em 'Tirar Fotos' para começar a captura.";
        })
        .catch(function(err) {
            console.log("Erro ao acessar a câmera: " + err);
            statusMessage.textContent = "Erro ao acessar a câmera. Por favor, verifique suas configurações.";
        });
}
// Tira várias fotos e armazena em uma lista
function tirarFotos() {
    if (fotosCapturadas.length < maxFotos) {
        var canvas = document.createElement("canvas");
        var context = canvas.getContext("2d");

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Adiciona flash na captura
        video.style.filter = "brightness(1.5)";
        setTimeout(() => video.style.filter = "brightness(1)", 200); // Retorna ao normal

        canvas.toBlob(function(blob) {
            var file = new File([blob], `foto_rosto_${fotosCapturadas.length + 1}.jpeg`, { type: "image/jpeg" });
            fotosCapturadas.push(file);

            if (fotosCapturadas.length < maxFotos) {
                statusMessage.textContent = `Capturando foto ${fotosCapturadas.length + 1} de ${maxFotos}. Por favor, mova-se levemente.`;
                setTimeout(tirarFotos, intervaloEntreFotos); // Espera 2 segundos antes de tirar a próxima foto
            } else {
                preencherInput();
                statusMessage.style.display = "none";
                finalMessage.style.display = "block";
            }
        }, "image/jpeg", 0.95);
    }
}
// Preenche o campo de input com todas as fotos capturadas
function preencherInput() {
    var dataTransfer = new DataTransfer();
    fotosCapturadas.forEach(file => dataTransfer.items.add(file));
    imagemRosto.files = dataTransfer.files;

    // Oculta o container da câmera
    cameraContainer.style.display = "none";
}
function FileListItems(files) {
    var dataTransfer = new DataTransfer();
    files.forEach(file => dataTransfer.items.add(file));
    return dataTransfer.files;
}