# DESIGN PATTERN API WITH FASTAPI PYTHON

# Layers
[Models]: models the entities and schemas for db
[Repositories]:
[Services]:
[Routes]:

Extras:
[Utils]:
[Providers]:
[Middlewares]:

Important Files:
> main
> server
> .env


# Structures and Syntax
> [Models]:
    class Class(BaseModel):
        attribute: type = Field(...)
        
        class Config:
            json_schema_extra = {
                'nameCollection' {
                    'attr': 'type'     
                }
            }

> [Repositories]: 
    DB = config('DB)
    client = motor.moto_asyncio...(DB)
    database = client.nameDatabase
    name_collection = database.get_collection('collection')

    class ...:
        async def CRUD(self, model: Model, ...) -> dict:
            ... = await name_collection.method()
            ...

> [Services]:
    classRepository = ClassRepository()
    
    class ...:
        async def CRUD(self, model: Model, ...)
            try:
                ... = await classRepository.method()
                
                if not ...:
                    return {
                        'message': 'Not found.',
                        'data': '',
                        'status': 404
                    }
            
                return {
                    'message': 'Found.',
                    'data': ...,
                    'status': 200
                }
            
            except Exception as error:
                return {
                    'message': '',
                    'data': error,
                    'status': ?
                }

> [Routes]:
    classService = ClassService
    router = APIRouter()
    
    @router.route('/path', response_description='')
    async def CRUD(self, model: Model = Depends(Model)):
        try:
            result = await classService.method()

            if not result['status'] == 000;
                raise HTTPException(status_code=result['status'], detail=result['message']

            return result

        except Exception as error:
            raise error



----------------------------------------
# Use of Naming Pattern:
Usually, in python, the functions/methods use [snake_case] instead of [camelCase]

----------------------------------------

# Libs Storage
Libraries installed in a Python API using `pip` are stored in a specific directory in the 
virtual environment or conda environment, depending on how the environment was configured. 
Usually, they are not in folders like 'node_modules' or libs.

----------------------------------------


``TO FIX:``
UpdateUser: update_logged_user (service) [PARTIALLY CORRECTED]
FollowUnfollow
UserCreateModel / user_dict
Delete Comment [{'message': 'Internal server error.', 'data': "string indices must be integers, not 'str'", 'status': 500}]
Update Comment [{'message': 'Internal server error.', 'data': "string indices must be integers, not 'str'", 'status': 500}]
List Posts [o problema está em post_helper: 'comments']

``TO CREATE``
Posts in UserModel
