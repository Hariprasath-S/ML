import pickle

__model = None
__vectoriser = None

def load_model():
    global __model
    global __vectoriser
    if __model is None:
        with open('sentiment.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("Model loaded")
    if __vectoriser is None:
        with open('vectorisor.pickle', 'rb') as w:
            __vectoriser = pickle.load(w)
    print("Vectorisor loaded")


def get_sentiment(text2):
    text = [text2]
    return __model.predict(__vectoriser.transform(text))[0]


if __name__ == '__main__':
    load_model()
    print(get_sentiment('this movie is amazing'))
