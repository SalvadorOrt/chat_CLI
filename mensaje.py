class Mensaje():
    def __init__(self,emidorId= None,receptorId = None,contenido = None,FechaEnvio = None):
        self.e = emidorId
        self.r = receptorId
        self.c = contenido
        self.fe = FechaEnvio
    def insertarMensaje(self):
        query = '''
                insert into Mensajes values (?,?,?,?)
                '''
        datos = (self.e,self.r,self.c,self.fe)
        return (query,datos)
        