from subprocess import Popen, PIPE
import Config
import ExceptionManager
from pathlib import Path

exceptionFileName = "SQLPlus.py"


class Oracle:
    __connectString = Config.getDbConnectionString()

    def runScriptFiles(self, file):
        try:
            sqlCommand = b"@" + bytes(file.path)
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "runScriptFiles", exceptionFileName)
        queryResult, errorMessage = self.__runSqlQuery(
            sqlCommand, str(file.spoolPath))
        # self.__stringParse(queryResult)
        # print('--QueryResult-------------------------')
        # print(queryResult)
        # print('-ErrorResult-------------------------')
        # print(errorMessage)
        return queryResult, errorMessage

    def __runSqlQuery(self, sqlCommand, spoolPath):
        try:
            session = Popen("cmd.exe", stdin=PIPE, stdout=PIPE, stderr=PIPE)
            session.stdin.write(b"set nls_lang=.utf8 \n")
            # session = Popen(['sqlplus', '-S', self.__connectString],
            #                 stdin=PIPE, stdout=PIPE, stderr=PIPE,start_new_session=False)
            sqlplus = 'sqlplus ' + '-S ' + self.__connectString + ' \n'
            session.stdin.write(bytes(sqlplus, "utf-8"))
            session.stdin.write(b" SET  DEFINE  OFF; \n")
            spool = "spool " + spoolPath + "; \n"
            session.stdin.write(bytes(spool, "utf-8"))
            session.stdin.write(sqlCommand)
            session.stdin.write(b"\n show errors; \n")
            session.stdin.write(b"\n spool off; \n")
            session.stdin.write(b" exit; \n")
            queryResult, errorMessage = session.communicate()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "__runSqlQuery", exceptionFileName)
        return queryResult, errorMessage

    def __stringParse(self, queryResult):
        #queryResult = str(queryResult, "utf-8")
        splitlist = queryResult.split(b"\n")
        # print splitlist
        # print len(splitlist)
        # for str in splitlist:
        #       print "The String is %s" % str
        for counter in range(3, len(splitlist) - 2):
            # print splitlist[counter]
            print("This is line #  %u" % counter)
            splittab = splitlist[counter].split()
            for tb_counter in range(0, len(splittab)):
                print(splittab[tb_counter])
        return

    def getInvalidObjects(self, path):
        spoolPath = "spool " + str(path.resolve() / "InvalidObjects.log") + "; \n"
        sqlPath = Path("./invalid_objects.sql")

        session = Popen(['sqlplus', '-S', self.__connectString],
                        stdin=PIPE, stdout=PIPE, stderr=PIPE)
        session.stdin.write(b"SET WRAP OFF; \n")
        session.stdin.write(b"SET PAGESIZE 0; \n")
        session.stdin.write(b"SET LINESIZE 32000; \n")
        session.stdin.write(bytes(spoolPath,"utf-8"))
        sqlCommand = b"@" + bytes(sqlPath)
        session.stdin.write(sqlCommand)
        session.stdin.write(b"\n spool off; \n")
        session.stdin.write(b"exit;")
        queryResult, errorMessage = session.communicate()
