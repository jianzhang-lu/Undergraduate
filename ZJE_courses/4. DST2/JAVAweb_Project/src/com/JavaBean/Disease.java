package JavaBean;

public class Disease {
    private String Disease;
    private String Drug;
    private String GeneSymbol;
    private String VarName;
    private String PharmGKB_link;

    @Override
    public String toString() {
        return "Disease{" +
                "Disease='" + Disease + '\'' +
                ", Drug='" + Drug + '\'' +
                ", GeneSymbol='" + GeneSymbol + '\'' +
                ", VarName='" + VarName + '\'' +
                ", URL='" + PharmGKB_link + '\'' +
                '}';
    }

    public String getDisease() {
        return Disease;
    }

    public void setDisease(String disease) {
        Disease = disease;
    }

    public String getDrug() {
        return Drug;
    }

    public void setDrug(String drug) {
        Drug = drug;
    }

    public String getGeneSymbol() {
        return GeneSymbol;
    }

    public void setGeneSymbol(String geneSymbol) {
        GeneSymbol = geneSymbol;
    }

    public String getVarName() {
        return VarName;
    }

    public void setVarName(String varName) {
        VarName = varName;
    }

    public String getPharmGKB_link() {
        return PharmGKB_link;
    }

    public void setPharmGKB_link(String PharmGKB_link) {
        this.PharmGKB_link = PharmGKB_link;
    }
}
