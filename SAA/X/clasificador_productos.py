
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

def preprocesar_texto(texto):
    tokens = word_tokenize(texto.lower())
    
    stop_words = set(stopwords.words('spanish'))
    
    
    palabras_clave = {'no', 'ni', 'nunca', 'tampoco', 'sin', 'pero', 'mas', 'más', 'nada'}
    stop_words = stop_words - palabras_clave
    
    filtrado = [w for w in tokens if w.isalnum() and w not in stop_words]
    return " ".join(filtrado)


data_valoraciones = [
    
    ("Increíble producto, muy recomendado", "buena valoracion"),
    ("Me encanta", "buena valoracion"),
    ("Funciona perfecto", "buena valoracion"),
    ("Excelente calidad", "buena valoracion"),
    ("Muy contento con la compra", "buena valoracion"),
    ("Es una maravilla", "buena valoracion"),
    ("La mejor compra que he hecho", "buena valoracion"),
    ("Diseño espectacular", "buena valoracion"),
    ("Atención al cliente de diez", "buena valoracion"),
    ("Rapidez en el envío y todo perfecto", "buena valoracion"),
    ("Calidad premium", "buena valoracion"),
    ("Supera mis expectativas", "buena valoracion"),
    ("Muy útil y fácil de usar", "buena valoracion"),
    ("Vale cada céntimo", "buena valoracion"),
    ("No puedo estar más satisfecho", "buena valoracion"),
    ("Genial, lo volvería a comprar", "buena valoracion"),
    ("Es justo lo que buscaba", "buena valoracion"),
    ("Muy potente y estable", "buena valoracion"),
    ("No es caro para lo que ofrece", "buena valoracion"),
    ("Me gusta mucho", "buena valoracion"),
    ("Muy Bueno", "buena valoracion"),

    
    ("No funciona", "mala valoracion"),
    ("Es una basura", "mala valoracion"),
    ("Vaya decepción", "mala valoracion"),
    ("No lo compréis", "mala valoracion"),
    ("No me gusta nada", "mala valoracion"),
    ("Pésima calidad", "mala valoracion"),
    ("Se rompió al primer uso", "mala valoracion"),
    ("Servicio técnico fatal", "mala valoracion"),
    ("Caro y malo", "mala valoracion"),
    ("No cumple lo que promete", "mala valoracion"),
    ("Publicidad engañosa", "mala valoracion"),
    ("Lento y se calienta demasiado", "mala valoracion"),
    ("Me siento estafado", "mala valoracion"),
    ("Materiales muy baratos y frágiles", "mala valoracion"),
    ("No vale para nada", "mala valoracion"),
    ("Dinero tirado a la basura", "mala valoracion"),
    ("No responde bien", "mala valoracion"),
    ("Es un desastre", "mala valoracion"),
    ("Nunca más compraré aquí", "mala valoracion"),
    ("No me sirve de nada", "mala valoracion"),
    ("Me decepcionó mucho", "mala valoracion"),
    ("Llegó roto y tarde", "mala valoracion")
]

textos, etiquetas = zip(*data_valoraciones)
textos_limpios = [preprocesar_texto(t) for t in textos]

vectorizador = CountVectorizer(ngram_range=(1,2))
X = vectorizador.fit_transform(textos_limpios)

modelo = MultinomialNB()
modelo.fit(X, etiquetas)

def clasificar_comentario(comentario):
    limpio = preprocesar_texto(comentario)
    vectorizado = vectorizador.transform([limpio])
    prediccion = modelo.predict(vectorizado)
    return prediccion[0]

if __name__ == "__main__":
    
    print("Introduce un comentario para probar (o escribe 'salir'):")
    
    
    while True:
        user_input = input("> ")
        if user_input.lower() in ['salir']:
            break
        if not user_input.strip():
            continue
        res = clasificar_comentario(user_input)
        print(f"Predicción: {res.upper()}")
