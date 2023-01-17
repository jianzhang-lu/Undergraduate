package Controller;

import JavaBean.Variant;
import Service.VariantService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;

@WebServlet(name = "VariantServlet", value = "/VariantServlet")
public class VariantServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("Success");
        VariantService variantService = new VariantService();
        String VarName = request.getParameter("VarName");
        String FilePath = (String) request.getAttribute("FilePath");
        System.out.println(FilePath);
        ArrayList<Variant> variants = new ArrayList<Variant>();

        if (VarName != null) {
            try {
                variants = variantService.query(VarName);
                request.setAttribute("VariantResults", variants);
                request.getRequestDispatcher("VariantDisplay.jsp").forward(request, response);
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }

        if (FilePath != null) {
            ArrayList<String> fileStrings = null;
            try {
                fileStrings = variantService.filequery(FilePath);
                System.out.println(fileStrings);
            } catch (SQLException e) {
                e.printStackTrace();
            }
            String FileVarName = String.join(",", fileStrings);
            System.out.println(FileVarName);
            try {
                variants = variantService.query(FileVarName);
            } catch (SQLException e) {
                e.printStackTrace();
            }
            request.setAttribute("VariantResults", variants);
            request.getRequestDispatcher("VariantDisplay.jsp").forward(request, response);
        }
    }
}