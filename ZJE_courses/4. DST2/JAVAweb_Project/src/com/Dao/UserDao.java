package Dao;

import JavaBean.User;

import java.sql.*;

public class UserDao extends BaseDao {
    public int executeUpdateSQL(User user) throws SQLException {

        String sql = "insert into user (User_name,Password) value (?,?)";
        int row;
        conn = UserDao.getConnect();
        pstmt = conn.prepareStatement(sql);
        pstmt.setString(1, user.getUsername());
        pstmt.setString(2, user.getPassword());
        row = pstmt.executeUpdate();
        UserDao.closeAll(rs, pstmt, conn);
        return row;
    }

    public User executeQuerySQL(String username) throws SQLException {
        User user = new User();
        String sql = "select * from user where User_name = ?";
        conn = UserDao.getConnect();
        pstmt = conn.prepareStatement(sql);
        pstmt.setString(1, username);
        rs = pstmt.executeQuery();

        while (rs.next()){
            user.setUseid(rs.getInt(1));
            user.setUsername(rs.getString(2));
            user.setPassword(rs.getString(3));
        }
        UserDao.closeAll(rs, pstmt, conn);
        return user;
    }

    public int executeResetSQL(User user) throws SQLException {

        String sql = "UPDATE user SET Password=? where User_name=?";
        int row;
        conn = UserDao.getConnect();
        pstmt = conn.prepareStatement(sql);
        pstmt.setString(1, user.getPassword());
        pstmt.setString(2, user.getUsername());
        row = pstmt.executeUpdate();
        UserDao.closeAll(rs, pstmt, conn);
        return row;
    }
}

