from qtpy.QtWidgets import QWidget, QLabel, QGridLayout, QLineEdit


class SDictWidget(QWidget):
    """Create a parameters widget from a dictionary

    Parameters
    ----------
    params: dict
        Dictionary describing the parameters

    """
    def __init__(self, params):
        super().__init__()
        self.metadata = params
        self.params = {}
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self._line_idx = 0
        print('params=', params)
        for key, value in params['parameters'].items():
            # todo: add different widget depending on 'type'
            self.add_line_edit(key, value)

    def add_line_edit(self, key, value):
        print('line idx = ', self._line_idx)
        print('label:', value)
        self.layout.addWidget(QLabel(value['label']), self._line_idx, 0)
        self._line_idx += 1
        line_edit = QLineEdit()
        line_edit.setText(str(value['default']))
        self.layout.addWidget(line_edit, self._line_idx, 1)
        self.params[key] = {
                            'type': value['type'],
                            'label': value['label'],
                            'help': value['help'],
                            'default': value['default'],
                            'range': value['range'],
                            'widget': line_edit
        }

    def parameters(self):
        """read the parameters from the widget

        Returns
        -------
        dict of parameters values

        """
        params = {}
        for key, value in self.params.items():
            # todo: check the parameter type and range
            params[key] = value['widget'].text()
