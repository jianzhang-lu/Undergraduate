package Service;

import Dao.InterestDao;
import JavaBean.Interest;

import java.sql.SQLException;

public class InterestService {
    InterestDao interestDao = new InterestDao();
    public int add(Interest interest) throws SQLException{
        return interestDao.executeUpdateSQL(interest);
    }
}
