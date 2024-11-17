let video = document.getElementById('video');
let imagemRosto = document.getElementById('imagem_rosto');
let cameraContainer = document.getElementById('camera-container');

// Abre a câmera ao clicar no botão "Capturar"
function abrirCamera() {
    var cameraContainer = document.getElementById("camera-container");
    var video = document.getElementById("video");

    // Mostra a câmera
    cameraContainer.style.display = "block";

    // Acessa a webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            video.srcObject = stream;
        })
        .catch(function(err) {
            console.log("Erro ao acessar a câmera: " + err);
        });
}

// Tira uma foto e preenche o campo de input com a imagem capturada
function tirarFoto() {
    var video = document.getElementById("video");
    var canvas = document.createElement("canvas");
    var context = canvas.getContext("2d");

    // Configura o tamanho do canvas de acordo com a resolução do vídeo
    canvas.width = 320;
    canvas.height = 240;

    // Captura o quadro da webcam
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Cria um arquivo de imagem a partir da captura (aqui continuamos com binário)
    canvas.toBlob(function(blob) {
        // Cria um objeto File a partir do blob
        var file = new File([blob], "foto_rosto.png", { type: "image/png" });

        // Preenche o campo de input de tipo file com o arquivo da foto
        var inputFile = document.getElementById("imagem_rosto");
        inputFile.files = new FileListItems([file]);

        // Oculta o container da câmera
        document.getElementById("camera-container").style.display = "none";
    }, "image/png");
}

// Função para criar um FileList (necessário para simular a atribuição do arquivo no input[type="file"])
function FileListItems(files) {
    var dataTransfer = new DataTransfer();
    files.forEach(file => dataTransfer.items.add(file));
    return dataTransfer.files;
}