package JavaBean;

public class Variant {
    private Integer VarSeq;
    private String VarID;
    private String VarName;
    private String GeneSymbol;
    private String DisName;
    private String Drug;

    @Override
    public String toString() {
        return "Variant{" +
                "VarSeq=" + VarSeq +
                ", VarID='" + VarID + '\'' +
                ", VarName='" + VarName + '\'' +
                ", GeneSeq=" + GeneSymbol +
                ", DisName='" + DisName + '\'' +
                ", Drug='" + Drug + '\'' +
                '}';
    }

    public Integer getVarSeq() {
        return VarSeq;
    }

    public void setVarSeq(Integer varSeq) {
        VarSeq = varSeq;
    }

    public String getVarID() {
        return VarID;
    }

    public void setVarID(String varID) {
        VarID = varID;
    }

    public String getVarName() {
        return VarName;
    }

    public void setVarName(String varName) {
        VarName = varName;
    }

    public String getGeneSymbol() {
        return GeneSymbol;
    }

    public void setGeneSymbol(String geneSymbol) {
        GeneSymbol = geneSymbol;
    }

    public String getDisName() {
        return DisName;
    }

    public void setDisName(String disName) {
        DisName = disName;
    }

    public String getDrug() {
        return Drug;
    }

    public void setDrug(String drug) {
        Drug = drug;
    }
}
