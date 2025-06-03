# logic/state.py

class SoundboardState:
    def __init__(self):
        """ 
        Initialisiert den Zustand des Soundboards.
        Erstellt ein Dictionary, das die Zuweisungen der Buttons zu Sounddateien speichert.
        Die Tasten sind von 0 bis 5 indiziert, entsprechend den 6 Buttons.
        """
        # Button-Index -> Sounddatei-Pfad
        self.assignments = {}

    def assign_sound(self, button_index, filepath, label=None):
        """
        Weist einem Button eine Sounddatei und optional einen Label-Namen zu.
        :param button_index: Index des Buttons (0-5)
        :param filepath: Pfad zur Sounddatei
        :param label: Optionaler Label-Name für den Button
        """
        if label is None:
            label = filepath
        self.assignments[button_index] = {
            "filepath": filepath,
            "label": label
        }

    def get_sound(self, button_index):
        """ 
        Gibt den Pfad der Sounddatei für den angegebenen Button zurück.
        Wenn kein Sound zugewiesen ist, wird None zurückgegeben.
        :param button_index: Index des Buttons (0-5)
        :return: Pfad der Sounddatei oder None
        """
        entry = self.assignments.get(button_index)
        return entry['filepath'] if entry else None
    
    def get_label(self, button_index):
        """
        Gibt den Label-Namen für den angegebenen Button zurück.
        Wenn kein Label zugewiesen ist, wird None zurückgegeben.
        :param button_index: Index des Buttons (0-5)
        :return: Label-Name oder None
        """
        entry = self.assignments.get(button_index)
        return entry['label'] if entry else None

    def clear_assignment(self, button_index):
        """
        Entfernt die Zuweisung für den angegebenen Button.
        :param button_index: Index des Buttons (0-5)
        """
        if button_index in self.assignments:
            del self.assignments[button_index]