# test_demo.py

import pickle
from scipy.sparse import hstack

# Load saved models and vectorizers
model_lr = pickle.load(open("model_lr.pkl", "rb"))
model_svc = pickle.load(open("model_svc.pkl", "rb"))
word_vectorizer = pickle.load(open("word_vectorizer.pkl", "rb"))
char_vectorizer = pickle.load(open("char_vectorizer.pkl", "rb"))

# ----------- 1. PREPROCESSING DEMO -----------
text = "Play MUSIC!!!"

cleaned = text.lower().replace("!", "")
tokens = cleaned.split()

print("\n🔹 Preprocessing Example")
print("Original:", text)
print("Processed:", tokens)


# ----------- 2. TF-IDF DEMO -----------
sample = ["play music"]

vec = hstack([
    word_vectorizer.transform(sample),
    char_vectorizer.transform(sample)
])

arr = vec.toarray()[0]

# show only non-zero values
non_zero_indices = arr.nonzero()[0]

print("Non-zero indices:", non_zero_indices[:10])
print("Non-zero values:", arr[non_zero_indices][:10])


# ----------- 3. PREDICTION DEMO -----------
command = "open chrome"

vec = hstack([
    word_vectorizer.transform([command]),
    char_vectorizer.transform([command])
])

pred_lr = model_lr.predict(vec)
pred_svc = model_svc.predict(vec)

print("\n🔹 Prediction Example")
print("Input:", command)
print("LR Prediction:", pred_lr)
print("SVC Prediction:", pred_svc)