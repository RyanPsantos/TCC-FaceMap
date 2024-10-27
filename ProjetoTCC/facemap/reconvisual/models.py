from mongoengine import Document, StringField, EmailField, DateField, BinaryField

class Aluno(Document):
    nome_completo = StringField(required=True, max_length=200)
    email_institucional = EmailField(required=True, max_length=100)
    telefone = StringField(required=True, max_length=15)
    endereco = StringField(required=True, max_length=300)
    rg = StringField(required=True, max_length=12)
    registro_matricula = StringField(required=True, max_length=15)
    data_nascimento = DateField(required=True)
    curso = StringField(required=True, max_length=100)
    genero = StringField(required=True, choices=["masculino", "feminino", "outros", "prefiro_nao_dizer"])
    foto_rosto = BinaryField(required=False)  # Removendo obrigatoriedade da imagem

class Professor(Document):
    username = StringField(required=True, unique=True, max_length=100)
    email_institucional = EmailField(required=True, max_length=100)
    telefone = StringField(required=True, max_lenght=15)
    senha = StringField(required=True, max_length=100)