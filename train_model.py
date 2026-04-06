# train_model.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score
from dataset import data, expand_dataset
import pickle
from scipy.sparse import hstack
import numpy as np


# 🔥 SPLIT
train_data, test_data = train_test_split(
    data,
    test_size=0.2,
    random_state=42,
    stratify=[x[1] for x in data]
)

train_data = expand_dataset(train_data)

X_train = [x[0] for x in train_data]
y_train = [x[1] for x in train_data]

X_test = [x[0] for x in test_data]
y_test = [x[1] for x in test_data]


# 🔥 VECTORIZERS (BEST CONFIG)
word_vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),
    sublinear_tf=True,
    min_df=1,
    max_df=0.9
)

char_vectorizer = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(3, 6),
    min_df=1
)

X_train_vec = hstack([
    word_vectorizer.fit_transform(X_train),
    char_vectorizer.fit_transform(X_train)
])

X_test_vec = hstack([
    word_vectorizer.transform(X_test),
    char_vectorizer.transform(X_test)
])


# 🔥 MODEL 1 (Logistic)
model_lr = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    C=2.0
)

# 🔥 MODEL 2 (SVM)
model_svc = LinearSVC(
    class_weight="balanced",
    C=1.2
)

# Train both
model_lr.fit(X_train_vec, y_train)
model_svc.fit(X_train_vec, y_train)


# 🔥 ENSEMBLE PREDICTION
pred_lr = model_lr.predict(X_test_vec)
pred_svc = model_svc.predict(X_test_vec)

# Combine (majority vote)
y_pred = []

for i in range(len(pred_lr)):
    if pred_lr[i] == pred_svc[i]:
        y_pred.append(pred_lr[i])
    else:
        y_pred.append(pred_lr[i])  # fallback to LR (more stable)

y_pred = np.array(y_pred)


# 🔥 EVALUATE
print("\n📊 Model Evaluation:")
print("Accuracy:", round(accuracy_score(y_test, y_pred), 2))
print("Precision:", round(precision_score(y_test, y_pred, average="weighted"), 2))
print("F1 Score:", round(f1_score(y_test, y_pred, average="weighted"), 2))


# 🔥 FINAL TRAIN ON FULL DATA
full_data = expand_dataset(data)

X_full = [x[0] for x in full_data]
y_full = [x[1] for x in full_data]

X_full_vec = hstack([
    word_vectorizer.fit_transform(X_full),
    char_vectorizer.fit_transform(X_full)
])

model_lr.fit(X_full_vec, y_full)
model_svc.fit(X_full_vec, y_full)


# 🔥 SAVE BOTH MODELS
pickle.dump(model_lr, open("model_lr.pkl", "wb"))
pickle.dump(model_svc, open("model_svc.pkl", "wb"))
pickle.dump(word_vectorizer, open("word_vectorizer.pkl", "wb"))
pickle.dump(char_vectorizer, open("char_vectorizer.pkl", "wb"))

print("\n✅ Model saved!")