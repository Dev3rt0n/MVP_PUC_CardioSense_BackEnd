from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
paciente_tag = Tag(name="Paciente", description="Adição, visualização, remoção e predição de pacientes com doença cardíaca")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de pacientes
@app.get('/pacientes', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_pacientes():
    """Lista todos os pacientes cadastrados na base
    Args:
       none
        
    Returns:
        list: lista de pacientes cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os pacientes")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os pacientes
    pacientes = session.query(Paciente).all()
    
    if not pacientes:
        # Se não houver pacientes
        return {"pacientes": []}, 200
    else:
        logger.debug(f"%d pacientes econtrados" % len(pacientes))
        print(pacientes)
        return apresenta_pacientes(pacientes), 200


# Rota de adição de paciente
@app.post('/paciente', tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: PacienteSchema):
    """Adiciona um novo paciente à base de dados
    Retorna uma representação dos pacientes e diagnósticos associados.
    
    Args:
        name (str): nome do paciente
        age (int): Idade do paciente
        sex (int): Sexo do paciente (1 = masculino, 0 = feminino)
        cp (int): Tipo de dor no peito (0: Angina típica, 1: Angina atípica, 2: Dor não anginosa, 3: Assintomático)
        trestbps (int): Pressão arterial em repouso (em mm Hg)
        chol (int): Colesterol sérico (em mg/dl).
        fbs (int): Açúcar no sangue em jejum > 120 mg/dl (1 = verdadeiro, 0 = falso)
        restecg (int): Resultados do eletrocardiograma em repouso: (
            0: Normal, 1: Anormalidade na onda ST-T, 2: Hipertrofia ventricular esquerda provável ou definitiva
        )
        thalach (int): Frequência cardíaca máxima alcançada
        exang (int): Angina induzida por exercício (1 = sim, 0 = não)
        oldpeak (float): Depressão do segmento ST induzida por exercício em relação ao repouso
        slope (int): Inclinação do segmento ST no pico do exercício (0: Ascendente, 1: Plano, 2: Descendente)
        ca (int): Número de vasos principais (0-3) coloridos por fluoroscopia
        thal (int): Talassemia (0: Normal, 1: Defeito fixo, 2: Defeito reversível)
        
    Returns:
        dict: representação do paciente e diagnóstico associado
    """
    # TODO: Instanciar classes

    # Recuperando os dados do formulário
    name = form.name
    age = form.age
    sex = form.sex
    cp = form.cp
    trestbps = form.trestbps
    chol = form.chol
    fbs = form.fbs
    restecg = form.restecg
    thalach = form.thalach
    exang = form.exang
    oldpeak = form.oldpeak
    slope = form.slope
    ca = form.ca
    thal = form.thal
        
    # Preparando os dados para o modelo
    X_input = PreProcessador.preparar_form(form)
    # Carregando modelo
    model_path = './MachineLearning/pipelines/rf_cardiosense_pipeline.pkl'
    # modelo = Model.carrega_modelo(ml_path)
    modelo = Pipeline.carrega_pipeline(model_path)
    # Realizando a predição
    target = int(Model.preditor(modelo, X_input)[0])
    
    paciente = Paciente(
        name=name,
        age = age,
        sex = sex,
        cp = cp,
        trestbps = trestbps,
        chol = chol,
        fbs = fbs,
        restecg = restecg,
        thalach = thalach,
        exang = exang,
        oldpeak = oldpeak,
        slope = slope,
        ca = ca,
        thal = thal,
        target = target
    )
    logger.debug(f"Adicionando produto de nome: '{paciente.name}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        
        # Checando se paciente já existe na base
        if session.query(Paciente).filter(Paciente.name == form.name).first():
            error_msg = "Paciente já existente na base :/"
            logger.warning(f"Erro ao adicionar paciente '{paciente.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        # Adicionando paciente
        session.add(paciente)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado paciente de nome: '{paciente.name}'")
        return apresenta_paciente(paciente), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item."
        logger.warning(f"Erro ao adicionar paciente '{paciente.name}', {error_msg}")
        return {"message": error_msg}, 400
    

# Métodos baseados em nome
# Rota de busca de paciente por nome
@app.get('/paciente', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_paciente(query: PacienteBuscaSchema):    
    """Faz a busca por um paciente cadastrado na base a partir do nome

    Args:
        nome (str): nome do paciente
        
    Returns:
        dict: representação do paciente e diagnóstico associado
    """
    
    paciente_nome = query.name
    logger.debug(f"Coletando dados sobre produto #{paciente_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
    
    if not paciente:
        # se o paciente não foi encontrado
        error_msg = f"Paciente {paciente_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{paciente_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Paciente econtrado: '{paciente.name}'")
        # retorna a representação do paciente
        return apresenta_paciente(paciente), 200
   
    
# Rota de remoção de paciente por nome
@app.delete('/paciente', tags=[paciente_tag],
            responses={"200": PacienteViewSchema, "404": ErrorSchema})
def delete_paciente(query: PacienteBuscaSchema):
    """Remove um paciente cadastrado na base a partir do nome

    Args:
        nome (str): nome do paciente
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    paciente_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre paciente #{paciente_nome}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando paciente
    paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
    
    if not paciente:
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente '{paciente_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(paciente)
        session.commit()
        logger.debug(f"Deletado paciente #{paciente_nome}")
        return {"message": f"Paciente {paciente_nome} removido com sucesso!"}, 200
    
if __name__ == '__main__':
    app.run(debug=True)