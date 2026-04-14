import os
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Features from Project 1.md:
# duration, total_packets, total_bytes, mean_pkt_size, std_pkt_size,
# mean_iat, std_iat, protocol, src_port, dst_port, pkt_size_ratio
FEATURE_NAMES = [
    "duration",
    "total_packets",
    "total_bytes",
    "mean_pkt_size",
    "std_pkt_size",
    "mean_iat",
    "std_iat",
    "protocol",
    "src_port",
    "dst_port",
    "pkt_size_ratio",
]

# Classes (0=VoIP, 1=Video, 2=HTTP, 3=FTP, 4=DNS, 5=Background)
CLASS_NAMES = ["VoIP", "Video", "HTTP", "FTP", "DNS", "Background"]


def generate_synthetic_data(num_samples_per_class=500):
    """
    Since we don't have Mininet PCAP data yet, this function generates
    synthetic flow statistics that vaguely resemble our 6 target classes.
    This allows us to train a dummy model and test the Ryu integration immediately.
    """
    print(f"Generating {num_samples_per_class} synthetic samples per class...")
    data = []
    labels = []

    for label in range(6):
        for _ in range(num_samples_per_class):
            if label == 0:  # VoIP (UDP, small packets, steady IAT)
                proto, sport, dport = 17, np.random.randint(10000, 60000), 5060
                mean_sz, std_sz = np.random.normal(160, 10), np.random.uniform(0, 5)
                mean_iat, std_iat = (
                    np.random.normal(0.02, 0.005),
                    np.random.uniform(0, 0.001),
                )
                dur = np.random.uniform(10, 60)
            elif label == 1:  # Video (UDP, large packets, bursty, port 554 RTSP)
                proto, sport, dport = 17, np.random.randint(10000, 60000), 554
                mean_sz, std_sz = (
                    np.random.normal(1000, 200),
                    np.random.uniform(100, 300),
                )
                mean_iat, std_iat = (
                    np.random.normal(0.01, 0.008),
                    np.random.uniform(0.005, 0.01),
                )
                dur = np.random.uniform(20, 120)
            elif label == 2:  # HTTP (TCP, port 80/443)
                proto, sport, dport = (
                    6,
                    np.random.randint(10000, 60000),
                    np.random.choice([80, 443]),
                )
                mean_sz, std_sz = np.random.normal(500, 300), np.random.uniform(50, 400)
                mean_iat, std_iat = (
                    np.random.normal(0.1, 0.05),
                    np.random.uniform(0.01, 0.1),
                )
                dur = np.random.uniform(1, 30)
            elif label == 3:  # FTP (TCP, port 21)
                proto, sport, dport = 6, np.random.randint(10000, 60000), 21
                mean_sz, std_sz = np.random.normal(1400, 50), np.random.uniform(0, 20)
                mean_iat, std_iat = (
                    np.random.normal(0.005, 0.001),
                    np.random.uniform(0, 0.002),
                )
                dur = np.random.uniform(5, 60)
            elif label == 4:  # DNS (UDP, port 53, very short)
                proto, sport, dport = 17, np.random.randint(10000, 60000), 53
                mean_sz, std_sz = np.random.normal(70, 10), np.random.uniform(0, 5)
                mean_iat, std_iat = (
                    np.random.normal(0.05, 0.01),
                    np.random.uniform(0, 0.01),
                )
                dur = np.random.uniform(0.1, 2)
            elif label == 5:  # Background (TCP, port 5201)
                proto, sport, dport = 6, np.random.randint(10000, 60000), 5201
                mean_sz, std_sz = (
                    np.random.normal(800, 400),
                    np.random.uniform(100, 500),
                )
                mean_iat, std_iat = (
                    np.random.normal(0.5, 0.2),
                    np.random.uniform(0.1, 0.5),
                )
                dur = np.random.uniform(10, 300)

            # Derived fields
            pkts = int(max(1, dur / max(0.0001, mean_iat)))
            byts = int(pkts * mean_sz)
            pkt_size_ratio = np.mean(
                [max(1, mean_sz + np.random.normal(0, std_sz * 0.5)) for _ in range(5)]
            ) / max(1, mean_sz)

            data.append(
                [
                    dur,
                    pkts,
                    byts,
                    mean_sz,
                    std_sz,
                    mean_iat,
                    std_iat,
                    proto,
                    sport,
                    dport,
                    pkt_size_ratio,
                ]
            )
            labels.append(label)

    df = pd.DataFrame(data, columns=FEATURE_NAMES)
    df["label"] = labels
    return df


def train_and_save_model(data_path=None, model_path="data/dt_model.pkl"):
    # Ensure data directory exists
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    if data_path and os.path.exists(data_path):
        print(f"Loading data from {data_path}...")
        df = pd.read_csv(data_path)
    else:
        print("No real dataset found. Generating synthetic dataset for prototyping...")
        df = generate_synthetic_data(num_samples_per_class=500)
        # Save synthetic data for reference
        df.to_csv("data/synthetic_flows.csv", index=False)

    X = df[FEATURE_NAMES]
    y = df["label"]

    # 70% Train, 15% Val, 15% Test logic (we'll just do 80/20 train/test for the script)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training Decision Tree Classifier...")
    clf = DecisionTreeClassifier(max_depth=10, random_state=42)
    clf.fit(X_train, y_train)

    print("Evaluating Model...")
    y_pred = clf.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=CLASS_NAMES))

    print("\nFeature Importances:")
    for name, imp in sorted(
        zip(FEATURE_NAMES, clf.feature_importances_), key=lambda x: -x[1]
    ):
        print(f"  {name}: {imp:.4f}")

    print(f"Saving model to {model_path}...")
    joblib.dump(clf, model_path)
    print("Done!")


if __name__ == "__main__":
    train_and_save_model()
