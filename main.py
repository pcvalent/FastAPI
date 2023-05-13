from fastapi import FastAPI, Body, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token 
from fastapi.security import HTTPBearer 
from fastapi import Request, HTTPException

# Creación de variable
movies = [
     {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Rey León',
        'overview': "Género infantíl con personajes animados",
        'year': '2009',
        'rating': 7.8,
        'category': 'Comedia'    
    },
    {
        'id': 3,
        'title': 'Mario Bros',
        'overview': "Género infantíl con personajes animados",
        'year': '2023',
        'rating': 7.8,
        'category': 'Comedia'    
    }
]

# Inicialización
app = FastAPI() # Creación de instancia. 
app.title = "Mi aplicación con FastAPI" 
app.version = "0.0.1" 

# Creación de clase para solicitud de token
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth =  await super().__call__(request) # Devuelve el token 
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com": 
            raise HTTPException(status_code = 403, detail = "Credenciales son invalidas")

# Creación de clase para añadir información del usario.
class User(BaseModel):
    email : str
    password : str

# Creación de clase para 
class Movie(BaseModel):
    id: Optional[int] = None # Se asigna que sea un parámetro opcional con valor por defecto None.
    title:str = Field( min_lengrh = 5, max_length=15) 
    overview:str = Field( min_lengrh = 15, max_length=50) 
    year: int = Field(le=2022) # Menor al 2022.
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config: # Se pone de manera más compacta el default. Los defaults sirven para dar guías de como dar los parámetros.
        schema_extra = {
            "example": {
                "id":1,
                "title":"Mi película",
                "overview":"Descripción película",
                "year": "2022",
                "rating": 9.8,
                "category":"Acción"


            }                              
        }

# Creacón de rutas para inicio.Esto se usa para agrupar determinadas rutas en la aplicación.
@app.get('/',tags = ['Home'])                               
def message():
    return HTMLResponse('<h1> Primer proyecto con FastAPI </h1>') # Retorna en formato HTML.

# Creación de ruta para el login.
@app.post('/Login', tags=['Authentication'])
def login(user: User):
    
    if user.email == "aadmin@gmail.com" and user.password == "aadmin":
        token: str = create_token(user.dict())
    return JSONResponse(status_code = 200, content=token)
    

# Creación de rutas para obtener todas las películas.
@app.get('/movies', tags = ['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]: # Creación de función que me devuelve el listado.

    return JSONResponse(status_code = 200,content=movies)

# Para indicarle a una ruta que va a requerir de parámetros, se debe añadir la siguiente ruta de la siguiente manera:
# donde en llaves va el parámetro que se quiera consultar {parámetro}
# Luego se realiza el filtrado de la película mediante la función get_movie.

@app.get('/movies/{id}',tags = ['movies'], response_model= Movie) 
def get_movie(id:int = Path(ge=1, le=2000) ) -> Movie:
    for item in movies:
        if item['id'] == id: 
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])


# Uso de parámetros Query. Sirve para realizar búsqueda a partir de categorías
@app.get('/movies/',tags = ['movies'], response_model=List[Movie]) 
def get_movies_by_category(category:str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category] # La función da listado de datos que coincidan con la categoría solicitada.
    return JSONResponse(status_code=404,content=data)

# Creación de película.
@app.post('/movies',tags = ['movies'], response_model=dict, status_code = 201) 
def create_movie(movie: Movie) -> dict:
     movies.append(movie)
     return JSONResponse(status_code=201, content={"message": "Se ha reistrado la película"})


# Método que permite realizar modificaciones en la API.
@app.put('/movies/{id}', tags=['movies'],response_model=dict, status_code=200)
def update_movie(id:int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id: # Por cada item de la lista de películas realiza un filtrado
            item['title '] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category 
            return JSONResponse(status_code= 200,content={"message": "Se ha modificado la película"})


# Método para eliminar datos
@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code = 200)
def delete_movie(id:int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code= 200, content={"message": "Se ha eliminado la película"})




