package Service;

import Dao.VariantDao;
import JavaBean.Variant;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class VariantService {
    VariantDao variantDao = new VariantDao();
    public ArrayList<Variant> query(String VarName) throws SQLException {
        String[] VarNames = VarName.replaceAll(" ","").split(",");
        ArrayList<Variant> variants = new ArrayList<Variant>();
        for(String varName  : VarNames){
            variants.add(variantDao.executeQuerySQL(varName));
        }
        return variants;
    }


    public ArrayList<String> filequery(String FilePath) throws SQLException{
        ArrayList<String> vars = new ArrayList<>();
        try (FileReader reader = new FileReader(FilePath);
             BufferedReader br = new BufferedReader(reader)
        ) {
            String line;
            while ((line = br.readLine()) != null) {
                System.out.println(line);
                Pattern p = Pattern.compile("rs[0-9]*");
                Matcher m = p.matcher(line);
                while (m.find()) {
                    vars.add(m.group());
                }
            }
            System.out.println(vars);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return vars;
    }
}

