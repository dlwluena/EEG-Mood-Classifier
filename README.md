# EEG-Mood-Classifier Project

# 🎯 Project Aim

The primary goal of this project is to provide an interactive desktop application that enables users to analyze EEG (Electroencephalogram) data and predict emotional states—such as happiness, sadness, or neutrality—based on simple signal statistics. In addition to mood classification, the project also aims to enhance user understanding through visual feedback by plotting brainwave signals and dynamically simulating brain network activity in 3D.

This project is built with educational intent and serves as a foundational prototype for future integration with real EEG data streams and advanced machine learning models.

---

# Example Usage

Let’s say you upload the included file: `emotions.csv`

Here’s a preview of its content:

```csv
Fp1,Fp2,Cz,P3,O2
1.2,2.2,0.5,3.1,1.0
2.1,2.5,0.8,2.9,1.3
2.8,2.7,1.0,3.2,1.5
3.2,3.0,1.2,3.5,1.7
2.0,2.3,1.1,3.0,1.6
```

Once you load this CSV into the app:

The EEG data is flattened (converted to a long list of values).
The average signal is calculated: in this case, it's greater than 2.0.
The app predicts:
    Mood: Happy
    Brain Network Info: Brain activity shows high energy, suggesting a happy mood.
You’ll see:
A line graph showing EEG activity over time.
An animated 3D brain network generated in real time.
A .gif file is automatically saved as:
    eeg_network_animation.gif

- No manual preprocessing is needed — just make sure your CSV contains only numbers in each column.
- You can use any CSV with similar structure — headers are optional, and label columns (like "Happy") are ignored.

---

# Features

- Upload EEG data from a `.csv` file
- Predict user mood: **Happy**, **Sad**, or **Neutral**
- Visualize EEG data as a 2D time-series plot
- Display a dynamic 3D brain network
- Save the animation as a `.gif` file
- Minimal and user-friendly GUI built with PyQt5

---

# What is EEG Data? (and what are we inputting?)

EEG (Electroencephalogram) data represents electrical activity recorded from the brain using electrodes placed on the scalp.

Each value in EEG data reflects the voltage fluctuation over time at a specific location on the head.

# In our context:
- The app expects a `.csv` file where:
  - Each column is a channel (e.g., Fp1, Cz, O2...).
  - Each row is a time sample.
- When input manually, users can enter EEG values like:
1.2, 2.4, 1.0, 3.2, 2.7

These are simulated EEG signal amplitudes from a session.

!!! Important !!!
- No labels or header are required (though they are handled gracefully).
- Labels like `"Happy"` or `"Neutral"` in the file are automatically ignored.

---

▶️ How to Use (with steps)

1. Launch the app
2. Choose one of the following:
Manually enter EEG values in the input box (e.g., 1.2, 2.3, 0.5, 3.2)
Or click “Load EEG CSV” to select a .csv file containing EEG signal data
3. Click "Predict Mood":
The app will show a mood result (Happy / Sad / Neutral)
A 2D EEG signal chart and 3D animated brain network will appear
4. Check the project folder:
The animation will be saved as eeg_network_animation.gif

---

## 📁 Project Structure

```
eeg-mood-classifier/
│
├── EEG.py                    → Main PyQt5 application file
├── emotions.csv              → Sample EEG input file
├── eeg_network_animation.gif → Generated animated brain network output
└── README.md                 → Project documentation
```

