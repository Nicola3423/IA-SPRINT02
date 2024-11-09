import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# Caminho do modelo salvo
model_path = "modelo_pacientes_odontologia.pkl"

# Carregar os dados atualizados
data_path = "updated_pacientes_odontologia_ml.csv"
data = pd.read_csv(data_path)

# Tratar valores ausentes no conjunto de dados
data = data.dropna()

# Codificação dos sintomas
le = LabelEncoder()
data['Sintomas_encoded'] = le.fit_transform(data['Sintomas'])

# Definir os recursos e o alvo para treinamento
X = data[['gravidade_sintoma', 'Sintomas_encoded']]
y = data['tratamento_necessario']  # Coluna alvo atualizada

# Verificar se o modelo já está salvo, caso contrário, treiná-lo
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    # Dividir o conjunto de dados em treino e teste (opcional)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    # Salvar o modelo treinado
    joblib.dump(model, model_path)

# Interface do Streamlit para entrada do usuário
st.title("Dashboard de Predição - Pacientes Odontológicos")
st.write("Visualização dos Dados:")
st.dataframe(data)

# Formulário para inserção de dados de entrada para predição
st.header("Inserir Dados para Predição")
nome = st.text_input("Nome do Paciente")
sintomas = st.selectbox("Sintomas", options=data['Sintomas'].unique())
gravidade = st.slider("Gravidade do Sintoma (1-3)", min_value=1, max_value=3, value=2)
feedback = st.slider("Feedback (1-5)", min_value=1, max_value=5, value=3)

# Codificar o sintoma inserido
if sintomas in le.classes_:
    sintomas_encoded = le.transform([sintomas])[0]
else:
    sintomas_encoded = 0  # Defina um valor padrão caso o sintoma não seja encontrado

# Dados de entrada para a predição
input_data = pd.DataFrame([[gravidade, sintomas_encoded]], 
                          columns=['gravidade_sintoma', 'Sintomas_encoded'])

# Fazer a predição com os dados de entrada
if st.button("Fazer Predição"):
    prediction = model.predict(input_data)[0]
    st.write(f"Predição para {nome}: {'Necessita tratamento' if prediction == 1 else 'Não necessita tratamento'}")
