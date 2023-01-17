package Dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;


public class BaseDao {

    static protected Connection conn;
    protected PreparedStatement pstmt;
    protected ResultSet rs;


    public static Connection getConnect() {
        try {
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/java_web?useSSL=false",
                    "root",
                    "Ljzh20020718");
        } catch (ClassNotFoundException | SQLException e) {
            e.printStackTrace();
        }
        return conn;
    }

    public static void closeAll(ResultSet rs, Statement pstmt, Connection conn) throws SQLException {
        if(rs!=null){
            rs.close();
        }
        if(pstmt!=null){
            pstmt.close();
        }
        if(conn!=null){
            conn.close();
        }
    }
}
