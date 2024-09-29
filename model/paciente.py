from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    name= Column("Name", String(50))
    age = Column("age", Integer)
    sex = Column("sex", Integer)
    cp = Column("cp", Integer)
    trestbps = Column("trestbps", Integer)
    chol = Column("chol", Integer)
    fbs = Column("fbs", Integer)
    restecg = Column("restecg", Integer)
    thalach = Column("thalach", Integer)
    exang = Column("exang", Integer)
    oldpeak = Column("oldpeak", Float)
    slope = Column("slope", Integer)
    ca = Column("ca", Integer)
    thal = Column("thal", Integer)
    target = Column("target", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, age:int, sex:int, cp:int, trestbps:int,
                 chol:int, fbs:int, restecg:int, name:str,
                 thalach:int, exang:int, oldpeak:float, 
                 slope:int, ca:int, thal:int, target:int, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Paciente

        Arguments:
            name: nome do paciente
            age: Idade do paciente
            sex: Sexo do paciente (1 = masculino, 0 = feminino)
            cp: Tipo de dor no peito (0: Angina típica, 1: Angina atípica, 2: Dor não anginosa, 3: Assintomático)
            trestbps: Pressão arterial em repouso (em mm Hg)
            chol: Colesterol sérico (em mg/dl).
            fbs: Açúcar no sangue em jejum > 120 mg/dl (1 = verdadeiro, 0 = falso)
            restecg: Resultados do eletrocardiograma em repouso: (0: Normal, 1: Anormalidade na onda ST-T, 2: Hipertrofia ventricular esquerda provável ou definitiva)
            thalach: Frequência cardíaca máxima alcançada
            exang: Angina induzida por exercício (1 = sim, 0 = não)
            oldpeak: Depressão do segmento ST induzida por exercício em relação ao repouso
            slope: Inclinação do segmento ST no pico do exercício (0: Ascendente, 1: Plano, 2: Descendente)
            ca: Número de vasos principais (0-3) coloridos por fluoroscopia
            thal: Talassemia (0: Normal, 1: Defeito fixo, 2: Defeito reversível)
            target: Diagnóstico de doença cardíaca (1 = presença de doença, 0 = ausência de doença)
            data_insercao: data de quando o paciente foi inserido à base
        """

        self.name=name
        self.age = age
        self.sex = sex
        self.cp = cp
        self.trestbps = trestbps
        self.chol = chol
        self.fbs = fbs
        self.restecg = restecg
        self.thalach = thalach
        self.exang = exang
        self.oldpeak = oldpeak
        self.slope = slope
        self.ca = ca
        self.thal = thal
        self.target = target

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao