import java.sql.*;
public class waterLevelPopulate {
    public static void run(){
        databaseConnection db = new databaseConnection();
        Connection con = db.returnConnection();
    
        try{
            Statement st = con.createStatement();
        }catch(Exception err){
            err.printStackTrace();
            System.err.println(err.getClass().getName()+": "+err.getMessage());
            System.exit(0);
        }
    }
}
