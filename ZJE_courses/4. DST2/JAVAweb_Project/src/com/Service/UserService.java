package Service;

import Dao.UserDao;
import JavaBean.User;

import java.sql.SQLException;

public class UserService {
    UserDao userDao = new UserDao();

    public int add(User user) throws SQLException {
        return userDao.executeUpdateSQL(user);
    }

    public User check(String username) throws SQLException {
        return userDao.executeQuerySQL(username);
    }

    public int update(User user) throws SQLException{
        return userDao.executeResetSQL(user);
    }
}
