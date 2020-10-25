# activa el ambiente
source env/scripts/activate 

# crea una variable de entorno 
export USERS_FILE='users_test.csv'
export ID_FILE='ids_test.json'
export LOG_LEVEL='DEBUG'

# corre flask '-p' cambia de puerto, y llama al 5001; el & corre en background el proceso (me permite correr dos bash a la vez)
flask run -p 5001 &

# corre el archivo
python test.py

# mata cualquier proceso que quede corriendo (en este caso el flask)
kill %