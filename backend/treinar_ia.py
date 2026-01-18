import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

# Base de dados expandida: 30 itens por categoria (Total 120)
dados = [
    # PAGAMENTO (30)
    ('pagar boleto', 'Pagamento'), ('segunda via fatura', 'Pagamento'), ('código de barras', 'Pagamento'),
    ('quitar conta', 'Pagamento'), ('boleto luz', 'Pagamento'), ('pagar com cartão', 'Pagamento'),
    ('vencimento fatura', 'Pagamento'), ('boleto PDF', 'Pagamento'), ('pix pagamento', 'Pagamento'),
    ('débito automático', 'Pagamento'), ('agendar conta', 'Pagamento'), ('fatura digital', 'Pagamento'),
    ('pagar agora', 'Pagamento'), ('escanear código', 'Pagamento'), ('pagamento pendente', 'Pagamento'),
    ('confirmar pagamento', 'Pagamento'), ('comprovante', 'Pagamento'), ('fatura atrasada', 'Pagamento'),
    ('parcelar boleto', 'Pagamento'), ('valor da conta', 'Pagamento'), ('boleto internet', 'Pagamento'),
    ('pagar faculdade', 'Pagamento'), ('onde pago', 'Pagamento'), ('limite boleto', 'Pagamento'),
    ('pagamento via app', 'Pagamento'), ('quitar dívida', 'Pagamento'), ('fatura cartão', 'Pagamento'),
    ('pagamento efetuado', 'Pagamento'), ('gerar boleto', 'Pagamento'), ('pagar', 'Pagamento'),

    # SUPORTE (30)
    ('app não abre', 'Suporte'), ('esqueci a senha', 'Suporte'), ('ajuda técnica', 'Suporte'),
    ('sistema fora do ar', 'Suporte'), ('erro login', 'Suporte'), ('token não funciona', 'Suporte'),
    ('travou tudo', 'Suporte'), ('biometria erro', 'Suporte'), ('suporte agora', 'Suporte'),
    ('falar com atendente', 'Suporte'), ('não recebo sms', 'Suporte'), ('atualizar app', 'Suporte'),
    ('celular novo', 'Suporte'), ('bug no sistema', 'Suporte'), ('senha bloqueada', 'Suporte'),
    ('ajuda com cadastro', 'Suporte'), ('configurações', 'Suporte'), ('instabilidade', 'Suporte'),
    ('conexão falhou', 'Suporte'), ('resetar senha', 'Suporte'), ('app parou', 'Suporte'),
    ('ajuda suporte', 'Suporte'), ('mudar e-mail', 'Suporte'), ('telefone suporte', 'Suporte'),
    ('problema acesso', 'Suporte'), ('site não carrega', 'Suporte'), ('erro conexão', 'Suporte'),
    ('senha 6 digitos', 'Suporte'), ('ativar cartão', 'Suporte'), ('suporte', 'Suporte'),

    # RECLAMAÇÃO (30)
    ('quero cancelar', 'Reclamação'), ('atendimento ruim', 'Reclamação'), ('vou no procon', 'Reclamação'),
    ('cobrança indevida', 'Reclamação'), ('odiei o serviço', 'Reclamação'), ('péssimo banco', 'Reclamação'),
    ('taxa abusiva', 'Reclamação'), ('insatisfeito', 'Reclamação'), ('reclamar gerente', 'Reclamação'),
    ('ouvidoria', 'Reclamação'), ('processar vocês', 'Reclamação'), ('horrível o chat', 'Reclamação'),
    ('estorno não caiu', 'Reclamação'), ('compra indevida', 'Reclamação'), ('cartão clonado', 'Reclamação'),
    ('demora no chat', 'Reclamação'), ('propaganda enganosa', 'Reclamação'), ('juros altos', 'Reclamação'),
    ('serviço lixo', 'Reclamação'), ('queixa formal', 'Reclamação'), ('estou bravo', 'Reclamação'),
    ('dinheiro sumiu', 'Reclamação'), ('atendimento nota zero', 'Reclamação'), ('venda casada', 'Reclamação'),
    ('cancelar conta', 'Reclamação'), ('resolvam logo', 'Reclamação'), ('problema sério', 'Reclamação'),
    ('sistema falho', 'Reclamação'), ('atendimento demorado', 'Reclamação'), ('reclamação', 'Reclamação'),

    # CONSULTA (30)
    ('qual meu saldo', 'Consulta'), ('ver extrato', 'Consulta'), ('limite disponível', 'Consulta'),
    ('extrato 30 dias', 'Consulta'), ('quanto tenho', 'Consulta'), ('saldo atual', 'Consulta'),
    ('ver movimentação', 'Consulta'), ('entradas e saídas', 'Consulta'), ('quanto gastei', 'Consulta'),
    ('consultar limite', 'Consulta'), ('extrato PDF', 'Consulta'), ('meu dinheiro', 'Consulta'),
    ('saldo poupança', 'Consulta'), ('rendimento', 'Consulta'), ('lançamentos futuros', 'Consulta'),
    ('ver pix recebidos', 'Consulta'), ('meu saldo', 'Consulta'), ('saldo de hoje', 'Consulta'),
    ('histórico compras', 'Consulta'), ('saldo disponível', 'Consulta'), ('limite cartão', 'Consulta'),
    ('quanto sobrou', 'Consulta'), ('extrato mensal', 'Consulta'), ('conferir saldo', 'Consulta'),
    ('resumo conta', 'Consulta'), ('checar extrato', 'Consulta'), ('valor na conta', 'Consulta'),
    ('saldo atualizado', 'Consulta'), ('consultar gastos', 'Consulta'), ('consulta', 'Consulta')
]

# Criar DataFrame
df = pd.DataFrame(dados, columns=['texto', 'categoria'])

# Criar Modelo com Pipeline (TF-IDF + Random Forest)
# O TF-IDF ignora palavras comuns e foca nas que definem a categoria
modelo_ia = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2)), # (1, 2) ensina a IA a ler grupos de até 2 palavras
    RandomForestClassifier(n_estimators=200, random_state=42)
)

# Treinar
modelo_ia.fit(df['texto'], df['categoria'])

# Criar pasta models se não existir
if not os.path.exists('models'):
    os.makedirs('models')

# Salvar
joblib.dump(modelo_ia.steps[1][1], 'models/modelo_ia.pkl')
joblib.dump(modelo_ia.steps[0][1], 'models/vectorizer.pkl')

print(f"✅ IA Bancária treinada com {len(dados)} exemplos e salva!")