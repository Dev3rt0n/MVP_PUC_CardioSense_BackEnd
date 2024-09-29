# Sobre o projeto

Este projeto foi realizado como atividade no curso de pós-gradução em Engenharia de Software pela PUC-Rio.

# CardioSense

CardioSense é um sistema de inteligência artificial que utiliza o **Cardiovascular Disease dataset** para prever se um paciente tem ou não doenças cardíacas, com base nos dados de entrada fornecidos. Este repositório contém o **Backend** da aplicação, desenvolvido com **Flask** para a API e **Scikit-learn** para o treinamento e a predição do modelo.

## Índice
- [Descrição](#descrição)
- [Instalação](#instalação)
- [Uso](#uso)
- [Rotas da API](#rotas-da-api)
- [Modelo](#modelo)

## Descrição

O **CardioSense** foi criado para fornecer um sistema rápido e eficaz para a previsão de doenças cardíacas, com base em um modelo de machine learning. A aplicação utiliza o conjunto de dados **Cardiovascular Disease** para treinar um modelo de classificação que prevê a probabilidade de um paciente ter doenças cardíacas, dados atributos como idade, sexo, pressão arterial, colesterol, entre outros.

A API é desenvolvida em **Flask** e utiliza **Scikit-learn** para o treinamento e predição do modelo. Este repositório é focado exclusivamente na parte **Backend** da aplicação.

## Instalação

Para executar o projeto localmente, siga os passos abaixo:

### Pré-requisitos

- **Python 3.7+**
- **pip** (gerenciador de pacotes Python)
- **virtualenv** (opcional, mas recomendado)

### Passos para instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/CardioSense.git
cd CardioSense
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python3 -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Inicie o servidor Flask:

```bash
python app.py
```

A API estará disponível em http://localhost:5000.

## Uso
Após configurar e iniciar o servidor Flask, você pode interagir com a API para fazer predições. Os dados devem ser enviados no formato JSON para a rota /predict e a API retornará a predição baseada nos dados do paciente.

### Exemplo de requisição (via curl ou Postman):

```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{
    "age": 50,
    "sex": 1,
    "cp": 3,
    "trestbps": 130,
    "chol": 245,
    "fbs": 0,
    "restecg": 1,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 1.2,
    "slope": 2,
    "ca": 0,
    "thal": 3
}'
```

### Exemplo de resposta:

```json
{
    "prediction": 1,
    "probability": 0.85
}
```

Neste exemplo:

* "prediction": 1 indica que o paciente tem uma probabilidade alta de ter doença cardíaca.
* "probability": 0.85 indica uma confiança de 85% no resultado.

## Rotas da API

POST /predict: Recebe os dados do paciente e retorna uma predição se ele tem ou não doença cardíaca.
GET /: Rota inicial que exibe uma mensagem simples de boas-vindas à API.

### Parâmetros esperados na rota /predict

* age: Idade do paciente (int)
* sex: Sexo do paciente (1 = homem, 0 = mulher)
* cp: Tipo de dor no peito (0-3)
* trestbps: Pressão arterial em repouso (int)
* chol: Nível de colesterol (int)
* fbs: Glicemia de jejum (1 se > 120 mg/dl, 0 caso contrário)
* restecg: Resultados do eletrocardiograma (0-2)
* thalach: Frequência cardíaca máxima alcançada (int)
* exang: Angina induzida por exercício (1 = sim, 0 = não)
* oldpeak: Depressão do ST induzida por exercício (float)
* slope: Inclinação do segmento ST (0-2)
* ca: Número de vasos sanguíneos principais coloridos por fluoroscopia (int)
* thal: Valor da talassemia (1-3)

## Modelo

O modelo de machine learning foi treinado usando Scikit-learn com o seguinte pipeline:

1. Pré-processamento dos dados: Limpeza e normalização.
2. Treinamento: Algoritmos como Random Forest, Logistic Regression, entre outros, foram testados para encontrar o melhor desempenho.
3. Validação: O modelo foi validado utilizando métricas como acurácia, precisão, recall e F1-score.

### Dataset

* O Cardiovascular Disease dataset contém atributos médicos que foram utilizados para treinar o modelo.
* Mais informações sobre o dataset podem ser encontradas [aqui](https://archive.ics.uci.edu/dataset/45/heart+disease).