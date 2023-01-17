package Dao;

import JavaBean.Gene;

import java.sql.SQLException;

public class GeneDao extends BaseDao{
    public Gene executeQuerySQL(String GeneSymbol) throws SQLException {
        Gene gene = new Gene();
        String sql = "select gene.GeneSymbol, GeneID, GeneName, Ensembl_Id, Chrom, `Start.GRCh38`, `Stop.GRCh38` " +
                "from gene, chromsome " +
                "where gene.GeneSymbol = chromsome.GeneSymbol AND gene.GeneSymbol = ?";
        conn = GeneDao.getConnect();
        pstmt = conn.prepareStatement(sql);
        pstmt.setString(1, GeneSymbol);
        rs = pstmt.executeQuery();

        while (rs.next()){
            gene.setGeneSymbol(rs.getString(1));
            gene.setGeneID(rs.getString(2));
            gene.setGeneName(rs.getString(3));
            gene.setEnsembl_id(rs.getString(4));
            gene.setChrom(rs.getString(5));
            gene.setStart_GRCh38(rs.getInt(6));
            gene.setEnd_GRCh38(rs.getInt(7));
        }
        GeneDao.closeAll(rs, pstmt, conn);
        return gene;
    }
}
