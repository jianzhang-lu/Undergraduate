package Dao;

import JavaBean.Disease;

import java.sql.SQLException;
import java.util.ArrayList;

public class DiseaseDao extends BaseDao{
    public ArrayList<Disease> executeQuerySQL(String DisName) throws SQLException {
        ArrayList<Disease> diseases = new ArrayList<>();
        String sql = "select distinct Disease, Drug, Gsymbol, VarName\n" +
                "from clinical_annotation\n" +
                "where Disease LIKE ?";

        conn = DiseaseDao.getConnect();
        pstmt = conn.prepareStatement(sql);
        String DisName2 = "%" + DisName + "%";
        pstmt.setString(1, DisName2);
        rs = pstmt.executeQuery();

        while (rs.next()){
            Disease disease = new Disease();
            disease.setDisease(rs.getString(1));
            disease.setDrug(rs.getString(2));
            disease.setGeneSymbol(rs.getString(3));
            disease.setVarName(rs.getString(4));
            diseases.add(disease);
        }
        DiseaseDao.closeAll(rs, pstmt, conn);
        return diseases;
    }

}



