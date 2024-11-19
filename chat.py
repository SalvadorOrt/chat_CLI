import pyodbc as sql
from mensaje import Mensaje
from datetime import datetime
cadena_conexion = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-9NIFOJB;DATABASE=chat;Trusted_Connection=yes;"
id = None
usuario = ''
contraseña = ''
nombre = ''
def inicio_sesion()->bool:
    global id
    global usuario
    global contraseña
    global nombre
    conexion = sql.connect(cadena_conexion)
    cursor = conexion.cursor()
    usuario = str(input('ingrese usuario: '))
    contraseña = str(input('ingrese contraseña: '))
    query = '''
            select Id,Username , Contraseña,Nombre
            from Usuarios
            where Username = ? and Contraseña = ?
            '''
    datos = (usuario,contraseña)
    if cursor.execute(query,datos).fetchone():
        id = cursor.execute(query,datos).fetchone()[0]
        nombre = cursor.execute(query,datos).fetchone()[3]
        
        print('conectado')
        conexion.close()
        return True
    else:
        print('error')
        conexion.close()
        return False

def cargar_chat(id):
    conexion = sql.connect(cadena_conexion)
    cursor = conexion.cursor()
    query = '''
            SELECT DISTINCT Usuarios.Id,Usuarios.Nombre
            FROM Mensajes
            INNER JOIN Usuarios
            ON Mensajes.ReceptorId = Usuarios.id
            WHERE Mensajes.EmisorId = ?;
            '''
    datos = (id,)
    chats_historial = cursor.execute(query,datos).fetchall()
    return chats_historial


def cargar_mensajes_chat(EmisorId,ReceptorId,EmisorId1,ReceptorId1):
    conexion = sql.connect(cadena_conexion)
    cursor = conexion.cursor()
    query = '''
          SELECT Emisor.Id as 'Emisor ID',Emisor.Nombre, Mensajes.Contenido,Receptor.Id AS 'Recetor Id',Receptor.Nombre
        FROM Mensajes
        INNER JOIN Usuarios as Receptor
        ON Mensajes.ReceptorId = Receptor.id
        INNER JOIN Usuarios as Emisor
        on Mensajes.EmisorId = Emisor.Id
        WHERE( Mensajes.EmisorId = ? and Mensajes.ReceptorId = ?) or (Mensajes.EmisorId = ? and Mensajes.ReceptorId = ?)  ;  

            '''
    datos = (EmisorId,ReceptorId,EmisorId1,ReceptorId1)
    chats_usuario = cursor.execute(query,datos).fetchall()
    return chats_usuario

if inicio_sesion():
        print(f'bienvenido {nombre} con id {id}!\n')
        for i in range(len(cargar_chat(id))):
            print(cargar_chat(id)[i][0], '.- ',cargar_chat(id)[i][1])
        id_chat_seleccionado = input('seleccione chat ')


        chats = cargar_mensajes_chat(id,id_chat_seleccionado,id_chat_seleccionado,id)
        
        for i in range(len(chats)):
            if id == chats[i][0]:
                print(f'                                                                    De {chats[i][1]} : {chats[i][2]}')
            else:
                print(f'Para {chats[i][1]}: {chats[i][2]}\n')
        while True:
            mensaje = input('[+] Desea enviar Mensaje: [y/n]  ').upper()
            if mensaje == 'Y':
                conexion = sql.connect(cadena_conexion)
                cursor = conexion.cursor()
                fecha_actual = datetime.now()
                fecha_formateada = fecha_actual.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] 
                contenido = str(input('ingrese mensaje : '))
                mensaje = Mensaje(id,id_chat_seleccionado,contenido,fecha_formateada)
                cursor.execute(*mensaje.insertarMensaje())
                conexion.commit()
                conexion.close()
            else:
                break
        
            