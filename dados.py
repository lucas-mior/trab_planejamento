import pandas as pd

dados_termeletricas = pd.DataFrame({
    'usina': [1, 2, 3],
    'GTmin': [100, 50, 0],
    'GTmax': [500, 500, 'infinito'],
    'A': [15, 250, 3000],
    'B': [1000, 100, 0],
    'Ton': [8,    6,   0],
    'Toff': [4, 6, 0],
    'C': [50, 75, 'infinito']})

lim_hidro = pd.DataFrame({
    'usina': [1, 2, 3],
    'montante': [0, 1, 2],
    'vol_min': [2300, 4300, 1420],
    'vol_max': [3340, 5100, 1500],
    'unidades': [3, 5, 4],
    'GHmin': [300, 200, 150],
    'GHmax': [430, 300, 210]})

coef_fcm = pd.DataFrame({
    'usina': [1, 2, 3],
    'F0': [401.217, 331.649, 244.787],
    'F1': [0.0500965, 0.0075202, 0.0134591],
    'F2': [-0.0000157, 0, 0],
    'F3': [3.30e-09, 0, 0],
    'F4': [-2.88e-13, 0, 0]})

coef_fcj = pd.DataFrame({
    'usina': [1, 2, 3],
    'G0':  [371.936,  261.363,  210.708],
    'G1':  [0.00193242,  0.00301186,  0.00154505],
    'G2':  [-8.530000e-8,  -0.000000564,  -0.000000159],
    'G3':  [2.38e-12,  6.79e-11,  1.22e-11],
    'G4':  [-2.62e-17,  -3.03e-15,  -3.69e-16]})

coef_perda_hidraulica = pd.DataFrame({
    'usina': [1, 2, 3],
    'perda': [7.5e-6, 2.2e-5, 5.0e-6]})

coef_rend_hidraulico = pd.DataFrame({
    'usina': [1, 2, 3],
    'I0': [0.3587300, 0.2518621, -6.65554162],
    'I1': [0.0023513, 0.0028912, 0.03689946],
    'I2': [0.0036111, 0.0065000, 0],
    'I3': [0.0000081, 0.0000186, 0],
    'I4': [-0.0000049, -0.0000092, -0.00004493],
    'I5': [-0.00003120, -0.00005650, 0]})

dados_afluencias = pd.DataFrame({
    'usina': [1, 2, 3],
    'phi': [1.15,  0.80,  1.10],
    'a': [-300,  150,  -200],
    'b': [300,  500,  100]})

dados_velocidade_ventos = {
    'phi': 0.15,
    'eta_media': 20,
    'eta_desvio': 5
}

dados_geracao_eolica = {
    'Cp': 0.55,
    'AR': 1000,
}

demanda = [2750, 3200, 2800, 2400,
           2100, 1900, 2300, 2450,
           2700, 3300, 3200, 3350]

vazao_por_usina = pd.DataFrame({
    'estagio': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'H1': [1050, 1100, 900, 800, 1025, 700, 750, 430, 360, 690, 750, 1100],
    'H2': [850, 1100, 1200, 1050, 800, 800, 700, 620, 550, 900, 1050, 1150],
    'H3': [1150, 1275, 880, 760, 375, 390, 780, 1500, 1800, 1650, 1300, 1100]})
