from src.modelo.album import Album, Medio
from src.modelo.cancion import Cancion
from src.modelo.interprete import Interprete
from src.modelo.declarative_base import engine, Base, session


class Coleccion():

    def __init__(self):
        Base.metadata.create_all(engine)

    def agregar_album(self, titulo, anio, descripcion, medio):
        busqueda = session.query(Album).filter(Album.titulo == titulo).all()
        if len(busqueda) == 0:
            album = Album(titulo=titulo, ano=anio, descripcion=descripcion, medio=medio)
            session.add(album)
            session.commit()
            return True
        else:
            return False

    def editar_album(self, album_id, titulo, anio, descripcion, medio):
        busqueda = session.query(Album).filter(Album.titulo == titulo, Album.id != album_id).all()
        if len(busqueda) == 0:
            album = session.query(Album).filter(Album.id == album_id).first()
            album.titulo = titulo
            album.ano = anio
            album.descripcion = descripcion
            album.medio = medio
            session.commit()
            return True
        else:
            return False

    def dar_album_por_id(self, album_id):
        return session.query(Album).get(album_id).__dict__

    def obtener_canciones(self):
        canciones = session.query(Cancion).all()

        print('Las canciones almacenadas son:')
        for cancion in canciones:
            print("Titulo: " + cancion.titulo + " (00:" +
                    str(cancion.minutos) + ":" +
                    str(cancion.segundos) + ")")

            print("Intérpretes")
            for interprete in cancion.interpretes:
                print(" - " + interprete.nombre)

            for album in cancion.albumes:
                print(" -- Presente en el album: " + album.titulo)

            print("")


        print('Los álbumes almacenados en discos son:')
        albumes = session.query(Album).filter(Album.medio == Medio.DISCO).all()
        for album in albumes:
            print("Album: " + album.titulo)

        # session.close()

    def actualizar_cancion(self):
        cancion = session.query(Cancion).get(2)
        interprete = session.query(Interprete).get(4)

        cancion.minutos = 5
        cancion.segundos = 30
        cancion.compositor = "Pedro Pérez"
        cancion.interpretes.append(interprete)
        session.add(cancion)
        session.commit()
        # session.close()

    def eliminar_cancion(self, cancion_id):
        cancion = session.query(Cancion).get(cancion_id)
        session.delete(cancion)
        session.commit()
        # session.close()
