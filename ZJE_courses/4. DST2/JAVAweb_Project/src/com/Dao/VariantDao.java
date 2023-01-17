package Dao;

import JavaBean.Variant;

import java.sql.SQLException;

public class VariantDao extends BaseDao{
    public Variant executeQuerySQL(String VarName) throws SQLException {
        Variant variant = new Variant();
        String sql = "select DISTINCT variant.VarID, variant.VarName, gene.genesymbol, variant_disease.DisName, variant_drug.Drug\n" +
                "from variant\n" +
                "    left join gene on variant.GeneSeq = gene.GeneSeq\n" +
                "    left join variant_disease on variant.VarSeq = variant_disease.VarSeq\n" +
                "    left join variant_drug on variant.VarSeq = variant_drug.VarSeq\n" +
                "where variant.VarName = ?";

        conn = VariantDao.getConnect();
        pstmt = conn.prepareStatement(sql);
        pstmt.setString(1, VarName);
        rs = pstmt.executeQuery();

        while (rs.next()){
            variant.setVarID(rs.getString(1));
            variant.setVarName(rs.getString(2));
            variant.setGeneSymbol(rs.getString(3));
            variant.setDisName(rs.getString(4));
            variant.setDrug(rs.getString(5));
        }
        VariantDao.closeAll(rs, pstmt, conn);
        return variant;
    }
}


