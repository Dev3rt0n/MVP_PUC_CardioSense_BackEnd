from pydantic import BaseModel
from typing import Optional, List
from model.paciente import Paciente
import json
import numpy as np

class PacienteSchema(BaseModel):
    """ Define como um novo paciente a ser inserido deve ser representado
    """
    name: str = "Maria"
    age: int = 63
    sex: int = 1
    cp: int = 3
    trestbps: int = 145
    chol: int = 233
    fbs: int = 1
    restecg: int = 0
    thalach: int = 150
    exang: int = 0
    oldpeak: float = 2.3
    slope: int = 0
    ca: int = 0
    thal: int = 1
    
class PacienteViewSchema(BaseModel):
    """Define como um paciente será retornado
    """
    id: int = 1
    name: str = "Maria"
    age: int = 63
    sex: int = 1
    cp: int = 3
    trestbps: int = 145
    chol: int = 233
    fbs: int = 1
    restecg: int = 0
    thalach: int = 150
    exang: int = 0
    oldpeak: float = 2.3
    slope: int = 0
    ca: int = 0
    thal: int = 1
    target: int = 1
    
class PacienteBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do paciente.
    """
    name: str = "Maria"

class ListaPacientesSchema(BaseModel):
    """Define como uma lista de pacientes será representada
    """
    pacientes: List[PacienteSchema]

    
class PacienteDelSchema(BaseModel):
    """Define como um paciente para deleção será representado
    """
    name: str = "Maria"
    
# Apresenta apenas os dados de um paciente    
def apresenta_paciente(paciente: Paciente):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PacienteViewSchema.
    """
    return {
        "id": paciente.id,
        "name": paciente.name,
        "age": paciente.age,
        "sex": paciente.sex,
        "cp": paciente.cp,
        "trestbps": paciente.trestbps,
        "chol": paciente.chol,
        "fbs": paciente.fbs,
        "restecg": paciente.restecg,
        "thalach": paciente.thalach,
        "exang": paciente.exang,
        "oldpeak": paciente.oldpeak,
        "slope": paciente.slope,
        "ca": paciente.ca,
        "thal": paciente.thal,
        "target": paciente.target
    }
    
# Apresenta uma lista de pacientes
def apresenta_pacientes(pacientes: List[Paciente]):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PacienteViewSchema.
    """
    result = []
    for paciente in pacientes:
        result.append({
            "id": paciente.id,
            "name": paciente.name,
            "age": paciente.age,
            "sex": paciente.sex,
            "cp": paciente.cp,
            "trestbps": paciente.trestbps,
            "chol": paciente.chol,
            "fbs": paciente.fbs,
            "restecg": paciente.restecg,
            "thalach": paciente.thalach,
            "exang": paciente.exang,
            "oldpeak": paciente.oldpeak,
            "slope": paciente.slope,
            "ca": paciente.ca,
            "thal": paciente.thal,
            "target": paciente.target
        })

    return {"pacientes": result}

