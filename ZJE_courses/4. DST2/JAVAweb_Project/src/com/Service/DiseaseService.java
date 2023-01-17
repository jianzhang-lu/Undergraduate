package Service;

import Dao.DiseaseDao;
import JavaBean.Disease;

import java.sql.SQLException;
import java.util.ArrayList;

public class DiseaseService {
    DiseaseDao diseaseDao = new DiseaseDao();

    public ArrayList<Disease> query(String VarName) throws SQLException {
        ArrayList<Disease> diseases = diseaseDao.executeQuerySQL(VarName);;
        return diseases;
    }
}
