$.ajax({
    url: '/iniciar_reconhecimento/',
    type: 'POST',
    success: function(response) {
        if (response.status === 'sucesso') {
            $('#recognition-textbox').val(response.nome);  // Atualiza o campo com o nome do aluno
        } else {
            alert("Erro: " + response.mensagem);
        }
    },
    error: function(xhr, status, error) {
        console.error("Erro AJAX:", {
            status: status,
            error: error,
            responseText: xhr.responseText
        });
        alert(`Erro (${status}): ${error}`);
    }
});
