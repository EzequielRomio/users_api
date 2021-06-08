source env/scripts/activate

python create_data_base.py -f 'users_test.db'

pytest || echo pytest execution failed

rm -rf users_test.db