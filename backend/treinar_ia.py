import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Dados rigorosamente sincronizados (12 itens por categoria)
dados = {
    'texto': [
        # PAGAMENTO (12)
        'Como pago meu boleto?', 'Segunda via da fatura', 'Pagar com cartão', 'boleto', 
        'pagar', 'fatura', 'cartão', 'dinheiro', 'custo', 'vencimento', 'pix', 'débito',
        
        # SUPORTE (12)
        'App não abre', 'Erro na senha', 'Sistema fora do ar', 'ajuda', 'suporte', 
        'erro', 'não funciona', 'bug', 'travou', 'instabilidade', 'conexão', 'senha',
        
        # RECLAMAÇÃO (12)
        'Quero cancelar', 'Vou reclamar no Procon', 'Atendimento ruim', 'horrível', 
        'reclamar', 'procon', 'odiei', 'péssimo', 'lixo', 'insatisfeito', 'ruim', 'queixa',
        
        # CONSULTA (12)
        'Qual meu saldo?', 'Ver limite disponível', 'Extrato da conta', 'saldo', 
        'extrato', 'quanto tenho', 'limite', 'conta', 'meu dinheiro', 'consultar', 'valor', 'disponível'
    ],
    'categoria': [
        'Pagamento'] * 12 + ['Suporte'] * 12 + ['Reclamação'] * 12 + ['Consulta'] * 12
}

df = pd.DataFrame(dados)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['texto'])
modelo = MultinomialNB()
modelo.fit(X, df['categoria'])

# Salva os arquivos novos
joblib.dump(modelo, 'models/modelo_ia.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')

print("Modelo sincronizado e salvo com sucesso!")