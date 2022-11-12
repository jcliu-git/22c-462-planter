import java.sql.*;
import java.lang.Math;

public class soilMoisturePopulate {
    public static void run(){
        databaseConnection db = new databaseConnection();
        Connection con = db.returnConnection();
    
        try{
            Statement st = con.createStatement();

            long begin = Timestamp.valueOf("2022-11-01 00:00:00").getTime();
            long end = Timestamp.valueOf("2022-12-01 00:00:00").getTime();
            long diff_milli = end - begin + 1; // in milisecond
            long diff_hour = diff_milli/(1000*60*60);
            System.out.println("Inserting...");
            for(int i=1; i<=diff_hour; i++){
                String t = (new Timestamp(begin + i*60*60*1000)).toString();
                String val1 = String.valueOf(Math.random());
                String val2 = String.valueOf(Math.random());
                String val3 = String.valueOf(Math.random());
                String val4 = String.valueOf(Math.random());
                String val5 = String.valueOf(Math.random());
                String val6 = String.valueOf(Math.random());
                String val7 = String.valueOf(Math.random());
                String val8 = String.valueOf(Math.random());

                st.executeUpdate("INSERT INTO moisture_level(timestamp, value, sensor_1, sensor_2, sensor_3, sensor_4, sensor_5, sensor_6, sensor_7, sensor_8) VALUES(\'" + t + "\'," + val1 + val2 + val3 + val4 + val5 + val6 + val7 + val8+");");
            }
            System.out.println("Done");
        }catch(Exception err){
            err.printStackTrace();
            System.err.println(err.getClass().getName()+": "+err.getMessage());
            System.exit(0);
        }
    }

    public static void main(String[] args) {
        soilMoisturePopulate.run();
    }
}