package Dao;

import JavaBean.Interest;

import java.sql.SQLException;

public class InterestDao extends BaseDao {
    public int executeUpdateSQL(Interest interest) throws SQLException {
        String sql = "insert into interest (username,information) value (?,?)";
        int row;
        conn = InterestDao.getConnect();
        pstmt = conn.prepareStatement(sql);
        pstmt.setString(1, interest.getName());
        pstmt.setString(2, interest.getInformation());
        row = pstmt.executeUpdate();
        InterestDao.closeAll(rs, pstmt, conn);
        return row;
    }
}

