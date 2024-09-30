import pytest
from model import *

# Para executar: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros    
url_dados = "./MachineLearning/data/test_dataset_cardiosense.csv"
colunas = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']

# Carga dos dados
dataset = Carregador.carregar_dados(url_dados, colunas)
array = dataset.values
X = array[:, 0:-1]
y = array[:, -1]

# Método para testar pipeline Random Forest a partir do arquivo correspondente
def test_modelo_rf():
    # Importando pipeline de Random Forest
    rf_path = './MachineLearning/pipelines/rf_cardiosense_pipeline.pkl'
    modelo_rf = Pipeline.carrega_pipeline(rf_path)

    # Obtendo as métricas do Random Forest
    acuracia_rf = Avaliador.avaliar(modelo_rf, X, y)
        # Verificando se o modelo foi carregado corretamente
    assert modelo_rf is not None, "O modelo não pôde ser carregado."

    # Obtendo as métricas do Random Forest
    acuracia_rf = Avaliador.avaliar(modelo_rf, X, y)
    
    # Testando as métricas do Random Forest
    assert acuracia_rf >= 0.78, f"Acurácia do modelo RF esperada >= 0.78, mas obtida: {acuracia_rf}"

    # Testar previsões com dados de entrada válidos
    previsoes = modelo_rf.predict(X)
    
    # Verifique se as previsões têm o mesmo número de entradas que o conjunto de testes
    assert len(previsoes) == len(y), "O número de previsões não corresponde ao número de exemplos de teste."
    
    # Testar se as previsões são apenas 0 ou 1 (caso do problema binário)
    assert set(previsoes).issubset({0, 1}), "As previsões devem ser 0 ou 1."

# Método para testar a carga de dados
def test_carregar_dados():
    # Testa a carga do dataset
    dataset_carregado = Carregador.carregar_dados(url_dados, colunas)
    
    # Verifique se o dataset foi carregado corretamente
    assert dataset_carregado is not None, "O dataset não foi carregado."
    assert not dataset_carregado.empty, "O dataset carregado está vazio."
    
    # Verifique se contém as colunas esperadas
    assert all(col in dataset_carregado.columns for col in colunas), "Nem todas as colunas esperadas estão presentes no dataset."
