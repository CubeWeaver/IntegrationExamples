from types import SimpleNamespace as sn
import zipfile, psycopg2, psycopg2.extras, csv, io, json, urllib.request

            
def stage_zip(dbhost, dbname, schema, username, password, zip_file):
    conn = psycopg2.connect(f"""user='{username}' 
                                password='{password}' 
                                host='{dbhost}' 
                                port='{5432}'
                                dbname='{dbname}'""")    
    cur = conn.cursor()
    entries = []
    columns = None
    cur.execute(f'CREATE SCHEMA IF NOT EXISTS {schema}')
    
    def process_step_init(entry):

        entry.tbl_name = entry.filename[0:-4]
        entry.name = schema +'.'+ entry.tbl_name
        entry.is_dim = entry.filename.startswith('D_')
        
        if entry.is_dim:
            cur.execute(
                f'create table if not exists {entry.name}({entry.header[0]} text PRIMARY KEY, {entry.header[1]} text)')
            for col in entry.header[2:]:
                cur.execute(f'ALTER TABLE {entry.name} ADD COLUMN IF NOT EXISTS {col} text')
            entry.meta = columns.get(entry.tbl_name[2:], [])
            for col in entry.meta:
                cur.execute(f'alter table {entry.name} drop constraint if exists ' + col['ColumnId'] + '_MFK')
        else:
            entry.val_col = entry.header[-1]
            cur.execute(f'create table if not exists {entry.name}({entry.val_col} numeric)')
            for col in entry.header[:-1]:
                cur.execute(f'ALTER TABLE {entry.name} ADD COLUMN IF NOT EXISTS {col} text')
                cur.execute(f'ALTER TABLE {entry.name} DROP CONSTRAINT if exists {col}_FK')

            cur.execute(f'alter table {entry.name} drop constraint if exists {entry.tbl_name}_pkey')
            cur.execute(f'alter table {entry.name} ADD PRIMARY KEY (' + ','.join(entry.header[:-1]) + ')')

    def process_step_load(entry, data):
        cur.execute(f'truncate table {entry.name}')
        insert = 'insert into ' + entry.name + '(' + ','.join(entry.header) + ') values %s'
        psycopg2.extras.execute_values (cur, insert, data)

    def process_step_finish(entry):
        if entry.is_dim:
            for meta_info in entry.meta:
                if meta_info['Type']=='Reference':
                    cur.execute(f'alter table {entry.name} add constraint ' + meta_info['ColumnId'] + '_MFK FOREIGN KEY (' 
                            + meta_info['ColumnHeader'] + ') REFERENCES ' + schema + '.d_' + meta_info['ReferencedTable']
                                + ' (' + meta_info['ReferencedTable'] + '_ID)')
        else:
            for col in entry.header[:-1]:
                cur.execute(f"""ALTER TABLE {entry.name} 
                    ADD CONSTRAINT {col}_FK FOREIGN KEY ({col}) REFERENCES {schema}.d_{col[:-3]} ({col})""")    

    def get_reader(zip_entry):
        return csv.reader(io.TextIOWrapper(zip_entry, encoding='utf-8-sig'), delimiter='\t', quotechar='"')
    
    with zipfile.ZipFile(zip_file) as zip_file:
        with zip_file.open('columns.json') as zip_entry:
            columns = json.load(zip_entry)
        for text_file in zip_file.infolist():
            if text_file.filename.endswith('.csv'):
                with zip_file.open(text_file.filename) as zip_entry:
                    entries.append(sn(filename=text_file.filename, header=next(get_reader(zip_entry))))

        print("creating tables")
        for entry in entries:
            process_step_init(entry)
        conn.commit();

        for entry in entries:
            print(f"staging table {entry.name} ({('dimension' if entry.is_dim else 'fact')}): ", end='')         
            with zip_file.open(entry.filename) as zip_entry:
                reader = get_reader(zip_entry)
                next(reader) # skip header
                count = 0
                def process_rows():
                    nonlocal count
                    for line in reader:
                        count += 1
                        yield [(None if v == '' else v) for v in line]
                process_step_load(entry, process_rows())
                print(f'{count} row(s) loaded')
                conn.commit();

        print("setting up key constraints")
        for entry in entries:
            process_step_finish(entry)

    conn.commit();
    cur.close()
    conn.close()
    print('done')

def download_zip(url, repo, key, out_file):
    print('downloading data')
    urllib.request.urlretrieve(f'{url}api/{repo}.{key}/export_full/', out_file)

    
if __name__ == "__main__":
    download_zip(url = 'http://localhost:8080/', 
                 repo = 'NABHMAQ30MRVLZKPBVDB19SDOO4VBWFD', 
                 key = 'EVNLUMZHE4B2LABHCQ7Z6TBRCHITVROQ',
                 out_file = 'export.zip')
    stage_zip(dbhost = 'localhost',
              dbname = 'test',
              schema = 'test',
              username = 'postgres',
              password = 'test',
              zip_file = 'export.zip')    