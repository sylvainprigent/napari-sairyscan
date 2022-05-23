from qtpy.QtWidgets import QWidget, QLabel, QGridLayout, QLineEdit, QGroupBox, QComboBox
from ._psf_widget import SPsfWidget


class SEpsilonWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.method_box = QComboBox()
        self.method_box.addItems(['Map', 'Auto value', 'Manual value'])
        self.method_box.currentTextChanged.connect(self._on_method_change)
        layout.addWidget(QLabel('epsilon'), 0, 0)
        layout.addWidget(self.method_box, 0, 1)

        self.epsilon_line = QLineEdit()
        layout.addWidget(self.epsilon_line, 1, 1)
        self.epsilon_line.setVisible(False)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _on_method_change(self, name):
        if name == 'Manual value':
            self.epsilon_line.setVisible(True)
        else:
            self.epsilon_line.setVisible(False)

    def check_inputs(self):
        if self.method_box.currentText() == 'Manual value':
            try:
                _ = float(self.epsilon_line.text())
            except ValueError as err:
                self.show_error(f"Max Sigma input must be a number")
            return False
        else:
            return True

    def state(self):
        if self.method_box.currentText() == 'Manual value':
            return {'epsilon': float(self.epsilon_line.text())}
        elif self.method_box.currentText() == 'Map':
            return {'epsilon': 'map'}
        else:
            return {'epsilon': 'mode'}


class SDictWidget(QGroupBox):
    """Create a parameters widget from a dictionary

    Parameters
    ----------
    params: dict
        Dictionary describing the parameters

    """
    def __init__(self, params):
        super().__init__()
        self.metadata = params
        self.setTitle(params['label'])
        self.params = {}
        self.layout = QGridLayout()
        self.layout.setContentsMargins(3, 11, 3, 11)
        self.setLayout(self.layout)
        self._line_idx = 0
        for key, value in params['parameters'].items():
            # todo: add different widget depending on 'type'
            if key == 'epsilon':
                self.add_epsilon_edit(key, value)
            elif key == 'psf':
                self.add_psf_widget(key, value)
            elif value['type'] == 'select':
                self.add_select_edit(key, value)
            else:
                self.add_line_edit(key, value)
        # hide empty widget
        if len(params['parameters']) == 0:
            self.setFixedHeight(0)

    def add_psf_widget(self, key, value):
        psf_widget = SPsfWidget()
        self.layout.addWidget(psf_widget, self._line_idx, 0, 1, 2)
        self._line_idx += 1
        self.params[key] = {
            'type': value['type'],
            'label': value['label'],
            'help': value['help'],
            'default': value['default'],
            'range': None,
            'widget': psf_widget
        }

    def add_select_edit(self, key, value):
        print('add select with dict=', value)
        self.layout.addWidget(QLabel(value['label']), self._line_idx, 0)
        select_edit = QComboBox()
        select_edit.addItems([str(x) for x in value['values']])
        select_edit.setCurrentText(str(value['default']))
        self.layout.addWidget(select_edit, self._line_idx, 1)
        self._line_idx += 1
        self.params[key] = {
            'type': value['type'],
            'label': value['label'],
            'help': value['help'],
            'default': value['default'],
            'range': None,
            'widget': select_edit
        }

    def add_epsilon_edit(self, key, value):
        epsilon_widget = SEpsilonWidget()
        self.layout.addWidget(epsilon_widget, self._line_idx, 0, 1, 2)
        self._line_idx += 1
        self.params[key] = {
                            'type': value['type'],
                            'label': value['label'],
                            'help': value['help'],
                            'default': value['default'],
                            'range': None,
                            'widget': epsilon_widget
        }

    def add_line_edit(self, key, value):
        # print('line idx = ', self._line_idx)
        # print('label:', value)
        self.layout.addWidget(QLabel(value['label']), self._line_idx, 0)
        line_edit = QLineEdit()
        line_edit.setText(str(value['default']))
        self.layout.addWidget(line_edit, self._line_idx, 1)
        self._line_idx += 1
        range_ = None
        if 'range' in value:
            range_ = value['range']
        self.params[key] = {
                            'type': value['type'],
                            'label': value['label'],
                            'help': value['help'],
                            'default': value['default'],
                            'range': range_,
                            'widget': line_edit
        }

    @staticmethod
    def check_inputs():
        return True

    def state(self):
        """read the parameters from the widget

        Returns
        -------
        dict of parameters values

        """
        params = {}
        for key, value in self.params.items():
            if key == 'epsilon':
                params[key] = value['widget'].state()['epsilon']
            elif key == 'psf':
                params[key] = value['widget'].state()['psf']
            elif isinstance(value['widget'], QComboBox):
                params[key] = value['widget'].currentText()
            else:
                params[key] = value['widget'].text()
        return params
