from burp import IBurpExtender, ITab
from javax.swing import JPanel, JList, JScrollPane, JTextArea, DefaultListModel, ListSelectionListener
import json

class BurpExtender(IBurpExtender, ITab, ListSelectionListener):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName("CMD App Explorer")

        # Load JSON Data
        self.load_json()

        # Create UI
        self.panel = JPanel()
        self.panel.setLayout(None)

        # Application List
        self.app_list_model = DefaultListModel()
        for app in self.app_data.keys():
            self.app_list_model.addElement(app)

        self.app_list = JList(self.app_list_model)
        self.app_list.addListSelectionListener(self)

        scroll_list = JScrollPane(self.app_list)
        scroll_list.setBounds(10, 10, 200, 300)
        self.panel.add(scroll_list)

        # Details Area
        self.details_area = JTextArea()
        self.details_area.setEditable(False)

        scroll_details = JScrollPane(self.details_area)
        scroll_details.setBounds(220, 10, 350, 300)
        self.panel.add(scroll_details)

        # Add the UI to Burp
        callbacks.customizeUiComponent(self.panel)
        callbacks.addSuiteTab(self)

    def getTabCaption(self):
        return "CMD Apps"

    def getUiComponent(self):
        return self.panel

    def load_json(self):
        try:
            with open("./cmd_apps.json", "r") as f:
                self.app_data = json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            self.app_data = {}

    def valueChanged(self, event):
        if event.getValueIsAdjusting():
            return  # Prevent double firing of events

        selected_app = self.app_list.getSelectedValue()
        if selected_app and selected_app in self.app_data:
            details = self.app_data[selected_app]
            description = details.get("description", "No description available.")
            parameters = "\n".join(details.get("parameters", []))
            self.details_area.setText(f"Description:\n{description}\n\nParameters:\n{parameters}")

