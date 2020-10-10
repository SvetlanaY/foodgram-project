from django.db import migrations
import sqlite3
import pandas

   
def migration_ingredients(apps, schema_editor):
    conn = sqlite3.connect('db.sqlite3')
    
    table =  "recipes_ingredient"
    csv_file =  "ingredients.csv"
    
    filepath = f'data/{csv_file}'
    with open(filepath) as f:
        f = pandas.read_csv(filepath)
        
        f.columns = ['name', 'dimension']   
        
        f.to_sql(table, conn,  if_exists='append', index=True, index_label="id")
        
 
    conn.close()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migration_ingredients),
    ]
