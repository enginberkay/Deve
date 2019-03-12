declare
  i integer;
begin
  for ef in (select 'create or replace public synonym ' || object_name || ' for ' ||
                     (select t.table_owner from sys.all_synonyms t where t.synonym_name = a.object_name) || '.' || object_name cmd
               from all_objects a
              where status = 'INVALID'
                and owner = 'PUBLIC'
                and object_type = 'SYNONYM'
             union
             select 'ALTER ' || object_type || ' ' || owner || '.' || '"' || object_name || '"' || ' COMPILE' cmd
               from dba_objects
              where status = 'INVALID'
                and object_type in ('PACKAGE', 'FUNCTION', 'PROCEDURE', 'TRIGGER', 'VIEW', 'TYPE')
             union
             select 'ALTER ' || ' PACKAGE ' || ' ' || owner || '.' || '"' || object_name || '"' || ' COMPILE BODY' cmd
               from dba_objects
              where status = 'INVALID'
                and object_type in ('PACKAGE BODY'))
  loop
    begin
      execute immediate (ef.cmd);
    exception
      when others then
        null;
    end;
  end loop;
end;
/