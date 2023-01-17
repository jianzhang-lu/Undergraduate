package JavaBean;

public class Gene {
    private Integer GeneSeq;
    private String GeneID;
    private String GeneName;
    private String GeneSymbol;
    private String Ensembl_id;
    private String Chrom;
    private Integer Start_GRCh37;
    private Integer End_GRCh37;
    private Integer Start_GRCh38;
    private Integer End_GRCh38;

    @Override
    public String toString() {
        return "Gene{" +
                "GeneSeq=" + GeneSeq +
                ", GeneID='" + GeneID + '\'' +
                ", GeneName='" + GeneName + '\'' +
                ", GeneSymbol='" + GeneSymbol + '\'' +
                ", Ensembl_id='" + Ensembl_id + '\'' +
                ", Chrom='" + Chrom + '\'' +
                ", Start_GRCh37=" + Start_GRCh37 +
                ", End_GRCh37=" + End_GRCh37 +
                ", Start_GRCh38=" + Start_GRCh38 +
                ", End_GRCh38=" + End_GRCh38 +
                '}';
    }

    public Integer getGeneSeq() {
        return GeneSeq;
    }

    public void setGeneSeq(Integer geneSeq) {
        GeneSeq = geneSeq;
    }

    public String getGeneID() {
        return GeneID;
    }

    public void setGeneID(String geneID) {
        GeneID = geneID;
    }

    public String getGeneName() {
        return GeneName;
    }

    public void setGeneName(String geneName) {
        GeneName = geneName;
    }

    public String getGeneSymbol() {
        return GeneSymbol;
    }

    public void setGeneSymbol(String geneSymbol) {
        GeneSymbol = geneSymbol;
    }

    public String getEnsembl_id() {
        return Ensembl_id;
    }

    public void setEnsembl_id(String ensembl_id) {
        Ensembl_id = ensembl_id;
    }

    public String getChrom() {
        return Chrom;
    }

    public void setChrom(String chrom) {
        Chrom = chrom;
    }

    public Integer getStart_GRCh37() {
        return Start_GRCh37;
    }

    public void setStart_GRCh37(Integer start_GRCh37) {
        Start_GRCh37 = start_GRCh37;
    }

    public Integer getEnd_GRCh37() {
        return End_GRCh37;
    }

    public void setEnd_GRCh37(Integer end_GRCh37) {
        End_GRCh37 = end_GRCh37;
    }

    public Integer getStart_GRCh38() {
        return Start_GRCh38;
    }

    public void setStart_GRCh38(Integer start_GRCh38) {
        Start_GRCh38 = start_GRCh38;
    }

    public Integer getEnd_GRCh38() {
        return End_GRCh38;
    }

    public void setEnd_GRCh38(Integer end_GRCh38) {
        End_GRCh38 = end_GRCh38;
    }
}
