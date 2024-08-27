class QualityIndex:
    def __init__(self, angulos_atuais, angulos_ideais, angulos_maximos, pesos_articulacoes,
                 ibtug_atual, ibtug_ideal, ibtug_max, peso_ibutg, ruido_atual, ruido_ideal, ruido_max, peso_ruido,
                 luminosidade_atual, luminosidade_ideal, luminosidade_max, peso_luminosidade,
                 umidade_atual, umidade_ideal, umidade_max, peso_umidade,lotacao_atual, lotacao_ideal, lotacao_max, peso_lotacao,area_sala):
        """
        Inicializa a classe com os ângulos das articulações e o IBTUG.
        
        :param angulos_atuais: Dicionário com os ângulos atuais das articulações
        :param angulos_ideais: Dicionário com os ângulos ideais das articulações
        :param angulos_maximos: Dicionário com os ângulos máximos aceitáveis das articulações
        :param pesos_articulacoes: Dicionário com os pesos atribuídos a cada articulação
        :param ibtug_atual: Valor atual do IBTUG
        :param ibtug_ideal: Valor ideal do IBTUG
        :param ibtug_max: Valor máximo aceitável do IBTUG
        :param peso_ibutg: Peso atribuído ao IBTUG
        """
        self.angulos_atuais = angulos_atuais
        self.angulos_ideais = angulos_ideais
        self.angulos_maximos = angulos_maximos
        self.pesos_articulacoes = pesos_articulacoes
        self.ibtug_atual = ibtug_atual
        self.ibtug_ideal = ibtug_ideal
        self.ibtug_max = ibtug_max
        self.peso_ibutg = peso_ibutg
        self.ruido_atual = ruido_atual
        self.ruido_ideal = ruido_ideal
        self.ruido_max = ruido_max
        self.peso_ruido = peso_ruido
        self.luminosidade_atual = luminosidade_atual
        self.luminosidade_ideal = luminosidade_ideal
        self.luminosidade_max = luminosidade_max
        self.peso_luminosidade = peso_luminosidade
        self.umidade_atual = umidade_atual
        self.umidade_ideal = umidade_ideal
        self.umidade_max = umidade_max
        self.peso_umidade = peso_umidade
        self.lotacao_max = lotacao_max
        self.peso_lotacao = peso_lotacao
        self.area_sala = area_sala  # Área total da sala em m²
        self.n_pessoas = lotacao_atual  # Número de pessoas na sala
        self.e_ideal = lotacao_ideal  # Espaço ideal por pessoa em m²
        self.e_min = 5  # Espaço mínimo aceitável por pessoa em m²
        self.e_max = lotacao_max  # Espaço máximo aceitável por pessoa em m²
        self.ErgonomicsIndex =0
        self.quality_index = 0
    

    def calcular_penalidade_articulacao(self, angulo_atual, angulo_ideal, angulo_maximo):
        """
        Calcula a penalidade para um ângulo específico.
        
        :param angulo_atual: O ângulo medido atualmente
        :param angulo_ideal: O ângulo ideal para a articulação
        :param angulo_maximo: O ângulo máximo aceitável antes de um risco severo
        :return: Penalidade calculada
        """
        if angulo_atual < angulo_ideal:
            penalidade = ((angulo_ideal - angulo_atual) / angulo_ideal) ** 2
        elif angulo_atual > angulo_maximo:
            penalidade = ((angulo_atual - angulo_maximo) / (angulo_maximo - angulo_ideal)) ** 2
        else:
            penalidade = 0
        return penalidade

    def calcular_penalidade_ibutg(self):
        """
        Calcula a penalidade para o IBTUG.
        
        :return: Penalidade calculada para o IBTUG
        """
        if self.ibtug_atual < self.ibtug_ideal:
            penalidade = ((self.ibtug_ideal - self.ibtug_atual) / self.ibtug_ideal) ** 2
        elif self.ibtug_atual > self.ibtug_max:
            penalidade = ((self.ibtug_atual - self.ibtug_max) / (self.ibtug_max - self.ibtug_ideal)) ** 2
        else:
            penalidade = 0
        return penalidade

    def calcular_indice_ergonomia(self):
        """
        Calcula a penalidade total baseada nas articulações.
        
        :return: Penalidade total das articulações
        """
        penalidades_articulacoes = []
        pesos_articulacoes = []
        
        for articulacao in self.angulos_atuais:
            for people  in range(len(angulos_atuais[articulacao])):
                angulo_atual = self.angulos_atuais[articulacao][people]
                angulo_ideal = self.angulos_ideais[articulacao]
                angulo_maximo = self.angulos_maximos[articulacao]
                peso = self.pesos_articulacoes[articulacao]
                
                penalidade = self.calcular_penalidade_articulacao(angulo_atual, angulo_ideal, angulo_maximo)
                penalidades_articulacoes.append(penalidade * peso)
                pesos_articulacoes.append(peso)
        
        soma_penalidades_articulacoes = sum(penalidades_articulacoes)
        soma_pesos_articulacoes = sum(pesos_articulacoes)*len(angulos_atuais["braco"])
        
        if soma_pesos_articulacoes == 0:
            return 0  # Se não há pesos, assume-se a menor penalidade possível
        self.ErgonomicsIndex = soma_penalidades_articulacoes / soma_pesos_articulacoes
        return self.ErgonomicsIndex
    
    def get_ErgonomicsIndex(self):
        return self.ErgonomicsIndex
    
    def calcular_penalidade_ruido(self):
        """
        Calcula a penalidade para o nível de ruído.
        
        :return: Penalidade calculada para o ruído
        """
        if self.ruido_atual < self.ruido_ideal:
            penalidade = ((self.ruido_ideal - self.ruido_atual) / self.ruido_ideal) ** 2
        elif self.ruido_atual > self.ruido_max:
            penalidade = ((self.ruido_atual - self.ruido_max) / (self.ruido_max - self.ruido_ideal)) ** 2
        else:
            penalidade = 0
        return penalidade

    def calcular_espaco_por_pessoa(self):
        return self.area_sala / self.n_pessoas
    
    def penalidade_superlotacao(self, espaco_por_pessoa):
        if espaco_por_pessoa < self.e_min:
            return ((self.e_min - espaco_por_pessoa) / self.e_min) ** 2
        return 0
    
    def penalidade_sublotacao(self, espaco_por_pessoa):
        if espaco_por_pessoa > self.e_max:
            return ((espaco_por_pessoa - self.e_max) / self.e_max) ** 2
        return 0
    
    def penalidade_total_lotacao(self):
        espaco_por_pessoa = self.calcular_espaco_por_pessoa()
        penalidade_super = self.penalidade_superlotacao(espaco_por_pessoa)
        penalidade_sub = self.penalidade_sublotacao(espaco_por_pessoa)
        return penalidade_super + penalidade_sub



    def calcular_penalidade_luminosidade(self):
        """
        Calcula a penalidade para o nível de luminosidade.
        
        :return: Penalidade calculada para a luminosidade
        """
        if self.luminosidade_atual < self.luminosidade_ideal:
            penalidade = ((self.luminosidade_ideal - self.luminosidade_atual) / self.luminosidade_ideal) ** 2
        elif self.luminosidade_atual > self.luminosidade_max:
            penalidade = ((self.luminosidade_atual - self.luminosidade_max) / (self.luminosidade_max - self.luminosidade_ideal)) ** 2
        else:
            penalidade = 0
        return penalidade

    def calcular_penalidade_umidade(self):
        """
        Calcula a penalidade para o nível de umidade.
        
        :return: Penalidade calculada para a umidade
        """
        if self.umidade_atual < self.umidade_ideal:
            penalidade = ((self.umidade_ideal - self.umidade_atual) / self.umidade_ideal) ** 2
        elif self.umidade_atual > self.umidade_max:
            penalidade = ((self.umidade_atual - self.umidade_max) / (self.umidade_max - self.umidade_ideal)) ** 2
        else:
            penalidade = 0
        return penalidade

    def calcular_indice_qualidade(self):
        """
        Calcula o índice de qualidade do ambiente de trabalho com base em todas as penalidades.
        
        :return: O índice de qualidade do ambiente de trabalho
        """
        penalidade_ergonomia = self.calcular_indice_ergonomia()
        penalidade_ibutg = self.calcular_penalidade_ibutg() * self.peso_ibutg
        
        penalidade_ruido = self.calcular_penalidade_ruido() * self.peso_ruido
        penalidade_luminosidade = self.calcular_penalidade_luminosidade() * self.peso_luminosidade
        penalidade_umidade = self.calcular_penalidade_umidade() * self.peso_umidade
        penalidade_lotacao = self.penalidade_total_lotacao() * self.peso_lotacao
 
        penalidade_total = (penalidade_ergonomia + penalidade_ibutg + penalidade_ruido + 
                            penalidade_luminosidade + penalidade_umidade+penalidade_lotacao)
        peso_total = (self.peso_ibutg + self.peso_ruido + 
                      self.peso_luminosidade + self.peso_umidade+self.peso_lotacao)
        self.quality_index = penalidade_total / peso_total if peso_total != 0 else 0
        return self.quality_index
    def get_quality_index(self):
        return self.quality_index
# Definição dos parâmetros para o teste
angulos_atuais = {"braco": [19], "cabeça": [9]}
angulos_ideais = {"braco": 20, "cabeça": 10}
angulos_maximos = {"braco": 45, "cabeça": 25}
pesos_articulacoes = {"braco": 0.2, "cabeça": 0.2}

ibtug_atual = 19    
ibtug_ideal = 20
ibtug_max = 30
peso_ibutg = 0.2


ruido_atual = 45
ruido_ideal = 50
ruido_max = 85
peso_ruido = 0.2

luminosidade_atual = 450
luminosidade_ideal = 500
luminosidade_max = 1000
peso_luminosidade = 0.1

umidade_atual = 45
umidade_ideal = 50
umidade_max = 70
peso_umidade = 0.1

lotacao_atual = 10
lotacao_ideal = 10
lotacao_max = 20
peso_lotacao = 0.1
area_sala = 100

quality_index = QualityIndex(angulos_atuais, angulos_ideais, angulos_maximos, pesos_articulacoes,
                             ibtug_atual, ibtug_ideal, ibtug_max, peso_ibutg, ruido_atual, ruido_ideal, ruido_max, peso_ruido,
                                      luminosidade_atual, luminosidade_ideal, luminosidade_max, peso_luminosidade,
                                      umidade_atual, umidade_ideal, umidade_max, peso_umidade,lotacao_atual, lotacao_ideal, lotacao_max, peso_lotacao,area_sala)


# Cálculo do índice de qualidade
indice_qualidade = quality_index.calcular_indice_qualidade()
print(f"Índice de Qualidade do Ambiente de Trabalho: {indice_qualidade:.4f}")
print(f"Índice de Qual/: {quality_index.get_quality_index():.4f}")
print(f"Índice de Ergo Qual/: {quality_index.get_ErgonomicsIndex():.4f}")