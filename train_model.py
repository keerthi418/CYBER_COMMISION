import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


print("🔄 Starting Cybercrime Model Training...\n")

# ==================================================
# 1️⃣ Load Dataset
# ==================================================

FILE_NAME = "cybercrime_dataset.csv"

if not os.path.exists(FILE_NAME):
    print(f"❌ ERROR: '{FILE_NAME}' not found in this folder!")
    print("Make sure dataset file is inside project folder.")
    exit()

data = pd.read_csv(FILE_NAME)

print("✅ Dataset Loaded Successfully!")
print("📊 Total Records:", len(data))
print("\nFirst 5 rows:")
print(data.head())


# ==================================================
# 2️⃣ Validate Columns
# ==================================================

if "text" not in data.columns or "label" not in data.columns:
    print("\n❌ Dataset must contain 'text' and 'label' columns!")
    exit()

X = data["text"]
y = data["label"]


# ==================================================
# 3️⃣ Convert Text to TF-IDF Features
# ==================================================

print("\n🔄 Converting text into numerical features (TF-IDF)...")

vectorizer = TfidfVectorizer(stop_words="english")
X_vectorized = vectorizer.fit_transform(X)

print("✅ Text Vectorization Completed!")


# ==================================================
# 4️⃣ Train Test Split
# ==================================================

print("\n🔄 Splitting dataset into train & test...")

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

print("✅ Data Split Completed!")


# ==================================================
# 5️⃣ Train Model
# ==================================================

print("\n🚀 Training Logistic Regression Model...")

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print("✅ Model Training Completed!")


# ==================================================
# 6️⃣ Evaluate Model
# ==================================================

print("\n📈 Evaluating Model...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n🎯 Model Accuracy:", round(accuracy * 100, 2), "%")
print("\n📄 Classification Report:\n")
print(classification_report(y_test, y_pred))


# ==================================================
# 7️⃣ Confusion Matrix
# ==================================================

print("\n📊 Generating Confusion Matrix...")

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=model.classes_,
    yticklabels=model.classes_
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()

plt.savefig("confusion_matrix.png")
plt.show()

print("✅ Confusion Matrix saved as 'confusion_matrix.png'")


# ==================================================
# 8️⃣ Save Model & Vectorizer
# ==================================================

print("\n💾 Saving Model & Vectorizer...")

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model Saved Successfully!")
print("\n🎉 Training Completed Successfully!")
