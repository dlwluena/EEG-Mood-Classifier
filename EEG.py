import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx # We will draw a random “node and link” graph for brain network simulation.

from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

"""
PyQt5 Widget Descriptions

| Widget         | Description                         |
|----------------|-------------------------------------|
| QApplication   | Application Runner (Main Loop)      |
| QWidget        | Basic Window Class (Main Screen)    |
| QVBoxLayout    | Vertically arranges components      |
| QPushButton    | Clickable button                    |
| QLabel         | To display text                     |
| QLineEdit      | Area for user to enter text         |
| QFileDialog    | To open a file selection window     |
"""

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog
)
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plots

# Simple mood prediction logic based on average EEG value
def predict_mood(eeg_values):
    avg = np.mean(eeg_values) 
    if avg > 2: # The threshold (min, max, mean values ​​are examined, classes are defined according to standard deviation.) value of 2 is a completely random value.
        return "Happy", "Brain activity shows high energy, suggesting a happy mood."
    elif avg < -2:
        return "Sad", "Low energy detected, may indicate sadness."
    else:
        return "Neutral", "Balanced activity, likely a neutral mood."

""" 
    3D Brain Network Plotting (randomized for visualization)
    It creates a “brain network simulation” 
    from randomly generated nodes and connections. We redraw this network after each EEG prediction, adding visuality and meaning.
"""

def plot_3d_network(ax):
    
    """ 
        This means “probability of connection”.
        0.3 → So there is a 30% chance of a line between every two nodes.
    This way:
    Not everyone is connected → realistic
    But there is no connection either → visually meaningful

"""
    G = nx.erdos_renyi_graph(10, 0.3) #The graphic object (network) we created + 10 nodes are ideal for giving the impression of a neuronal network.
    pos = {i: np.random.rand(3) for i in G.nodes}

    ax.scatter(*zip(*pos.values()), s=200, c='skyblue', alpha=0.6) # Converts the list [ [x,y,z], [x,y,z], ... ] into separate lists x, y, z.

    for (i, j) in G.edges:
        ax.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]], [pos[i][2], pos[j][2]], 'k-', alpha=0.6)

    for i, (x, y, z) in pos.items():
        ax.text(x, y, z, f"Node {i}", fontsize=10, ha='center')

    ax.set_title("3D Brain Network")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    """
        This __init__ function creates the entire interface. 
        All buttons, input fields and the drawing area are initialized and positioned here
        - load_csv_file (file upload)
        - on_button_click (prediction initialization)
        - create_animation (chart drawing)
   
        + self refers to itself within the class so when you create an EEGApp object, self is that object itself.
            1. To define data (variables) belonging to the class
            2. To access from other functions 
    """

class EEGApp(QWidget): # Because it derives from QWidget, this class behaves like a window.
    def __init__(self): # a constructor method.
        super().__init__() # It calls the functions of the superclass QWidget.
        self.setWindowTitle("EEG Mood Classifier with Animation")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.eeg_input = QLineEdit()
        self.eeg_input.setPlaceholderText("Enter EEG data separated by commas: 1.2, 2.3, ...")
        layout.addWidget(self.eeg_input)

        self.example_label = QLabel("Example: 1.2, 2.3, 0.5, 3.2")
        layout.addWidget(self.example_label)

        self.load_csv_button = QPushButton("Load EEG CSV")
        self.load_csv_button.clicked.connect(self.load_csv_file)
        layout.addWidget(self.load_csv_button)

        self.button = QPushButton("Predict Mood")
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        self.result_label = QLabel("Mood: ")
        layout.addWidget(self.result_label)

        self.network_info_label = QLabel("Brain Network Info: ")
        layout.addWidget(self.network_info_label)

        self.canvas = FigureCanvas(plt.figure()) # FigureCanvas: places the graphic in the Qt interface.
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def load_csv_file(self):
        #QFileDialog.getOpenFileName(...): Opens a file selection window, self: Indicates which window it belongs to (this is GUI).
        file_path, _ = QFileDialog.getOpenFileName(self, "Open EEG CSV", "", "CSV Files (*.csv)") 
        if file_path:
            try:
                df = pd.read_csv(file_path)
                if "label" in df.columns:
                    df = df.drop("label", axis=1)
                values = df.values.flatten()[:100]
                self.eeg_input.setText(', '.join(map(str, values)))
            except Exception as e:
                self.result_label.setText("Could not read CSV file.")
                self.network_info_label.setText(str(e))

    def on_button_click(self):
        try:
            eeg_values = np.array([float(x) for x in self.eeg_input.text().split(',')])
            mood, info = predict_mood(eeg_values)
            self.result_label.setText(f"Mood: {mood}")
            self.network_info_label.setText(info)
            self.create_animation(eeg_values)
        except:
            self.result_label.setText("Invalid EEG input.")
            self.network_info_label.setText("Animation failed.")

    def create_animation(self, eeg_values):
        self.canvas.figure.clf()
        
        """
        drawing area (ax1): EEG signal (2D drawing) 
        drawing area (ax2): Brain network (3D)
        We draw the EEG signal to ax1, The title and axis names are set.
        """
        
        ax1 = self.canvas.figure.add_subplot(121)
        ax2 = self.canvas.figure.add_subplot(122, projection='3d')

        time = np.linspace(0, len(eeg_values), len(eeg_values))
        ax1.plot(time, eeg_values, label="EEG Data", color='b')
        ax1.set_title("Brain Activity (EEG)")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Amplitude")
        ax1.legend()

        plot_3d_network(ax2)
        self.animate(ax1, ax2, eeg_values)

        self.canvas.draw()

    def animate(self, ax1, ax2, eeg_values):
        def update(frame):
            ax1.clear()
            ax1.plot(np.linspace(0, frame, frame), eeg_values[:frame], label="EEG Data", color='b')
            ax1.set_title("Brain Activity (EEG)")
            ax1.set_xlabel("Time")
            ax1.set_ylabel("Amplitude")
            ax1.legend()

            G = nx.erdos_renyi_graph(10, 0.3) #The brain network is redrawn in each frame (giving a dynamic appearance).
            pos = {i: np.random.rand(3) for i in G.nodes}
            ax2.clear()
            ax2.scatter(*zip(*pos.values()), s=200, c='skyblue', alpha=0.6)
            for (i, j) in G.edges:
                ax2.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]], [pos[i][2], pos[j][2]], 'k-', alpha=0.6)
            for i, (x, y, z) in pos.items():
                ax2.text(x, y, z, f"N{i}", fontsize=10, ha='center')
            ax2.set_title("Brain Network")
            ax2.set_xlabel("X")
            ax2.set_ylabel("Y")
            ax2.set_zlabel("Z")

        ani = FuncAnimation(self.canvas.figure, update, frames=np.arange(1, len(eeg_values)+1), interval=100)
        try:
            ani.save("eeg_network_animation.gif", writer=PillowWriter(fps=10)) # PillowWriter is used to save the animation as .gif.
            print("Animation saved as GIF.")
        except Exception as e:
            print("Could not save animation:", e)

            """
                QApplication → is the heart of the PyQt application.
                EEGApp() → our GUI window.
                window.show() → makes the window visible.
                app.exec_() → runs the event loop, keeps the GUI active.        
            """
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EEGApp()
    window.show()
    sys.exit(app.exec_())
