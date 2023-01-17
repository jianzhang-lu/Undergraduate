package Service;

import Dao.GeneDao;
import JavaBean.Gene;

import java.sql.SQLException;
import java.util.ArrayList;

public class GeneService {
    GeneDao geneDao = new GeneDao();

    public ArrayList<Gene> query(String GeneSymbol) throws SQLException {
        String[] Symbols = GeneSymbol.replaceAll(" ","").split(",");
        ArrayList<Gene> genes = new ArrayList<Gene>();
        for(String symbol : Symbols){
            genes.add(geneDao.executeQuerySQL(symbol));
        }
        return genes;
    }
}
