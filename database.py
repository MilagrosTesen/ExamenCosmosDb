from azure.cosmos import CosmosClient, exceptions, PartitionKey
 
COSMOS_ENDPOINT = ''
COSMOS_KEY = ''
 
DATABASE_NAME = 'Examen-db'
CONTAINE_NAME_USUARIOS = 'usuarios'
CONTAINE_NAME_PROYECTOS = 'proyectos'
 
# Inicializamos cliente de Cosmos
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
 
# Crea u obtiene la bade de datos
database = client.create_database_if_not_exists(id = DATABASE_NAME)
 
# Crea u obtiene el container
container_proyectos = database.create_container_if_not_exists(id = CONTAINE_NAME_PROYECTOS,
                                                   partition_key = PartitionKey(path = "/id"),
                                                   offer_throughput = 400)

container_usuarios = database.create_container_if_not_exists(id = CONTAINE_NAME_USUARIOS,
                                                   partition_key = PartitionKey(path = "/id"),
                                                   offer_throughput = 400)
                                                   