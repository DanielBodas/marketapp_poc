# Mock de streamlit para tests
class MockStreamlit:
    class SessionState(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.rerun_called = False

        def rerun(self):
            self.rerun_called = True

        def __setattr__(self, name, value):
            self[name] = value

        def __getattr__(self, name):
            if name not in self:
                return None
            return self[name]

    def __init__(self):
        self.session_state = self.SessionState()
        # Hacer session_state accesible globalmente
        global session_state
        session_state = self.session_state