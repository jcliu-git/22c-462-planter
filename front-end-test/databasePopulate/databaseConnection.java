package databasePopulate;
import java.sql.*;

public class databaseConnection{
    private Connection conn = null;

    public databaseConnection(){
        try {
            String dbUrl = "jdbc:postgresql://" + dbConfig.host + ':' + dbConfig.port + '/' + dbConfig.database;
            conn= DriverManager.getConnection(dbUrl, dbConfig.user, dbConfig.password);

         } catch (Exception err) {
            err.printStackTrace();
            System.err.println(err.getClass().getName()+": "+err.getMessage());
            System.exit(0);
         }
    }

    public Connection returnConnection(){
        return conn;
    }

}
