class Log:
    def __init__(self, path: str = 'console') -> None:
        if path == 'console':
            self.out = print
        else:
            self.out = open(path, 'ra').write
    def error(self, module_name: str, text: str):
        self.out(f'[ERROR from {module_name.upper()}]: {text}')
    def diag(self, module_name, text):
        self.out(f'[DIAG from {module_name.upper()}]: {text}')
    def start_message(self, module_name:str, module_version: str):
         self.out(f'[STARTED {module_name.upper()} ver {module_version}')
    
