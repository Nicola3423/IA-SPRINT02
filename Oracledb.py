from sqlalchemy import create_engine
import pandas as pd

def conectar_oracle():
    try:
        dsn_tns = "oracle+cx_oracle://rm554227:081204@oracle.fiap.com.br:1521/ORCL"
        engine = create_engine(dsn_tns)
        print("Conexão bem-sucedida!")
        return engine
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

def carregar_dados_pacientes():
    engine = conectar_oracle()
    if engine:
        query = """
        SELECT ID_PACIENTE, NOME, EMAIL, DATA_NASCIMENTO, TELEFONE
        FROM PACIENTE
        """
        paciente_data = pd.read_sql(query, engine)
        engine.dispose()
        return paciente_data
    else:
        return pd.DataFrame()
def carregar_dados_sintoma():
    engine = conectar_oracle()
    if engine:
        query = """
        SELECT DATA ID_SINTOMA,SINTOMA_DESCRICAO,GRAVIDADE
        FROM SINTOMA
        """
        sintoma_data = pd.read_sql(query, engine)
        engine.dispose()
        return sintoma_data
    else:
        return pd.DataFrame()

# Teste de conexão e exibição dos dados
if __name__ == "__main__":
    dados = carregar_dados_pacientes()
    if not dados.empty:
        print(dados)
    else:
        print("Nenhum dado encontrado.") 
