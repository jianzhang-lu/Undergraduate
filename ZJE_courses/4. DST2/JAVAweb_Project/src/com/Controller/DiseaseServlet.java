package Controller;

import JavaBean.Disease;
import Service.DiseaseService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;

@WebServlet(name = "DiseaseServlet", value = "/DiseaseServlet")
public class DiseaseServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        DiseaseService diseaseService = new DiseaseService();
        String disname = request.getParameter("DiseaseName");
        ArrayList<Disease> diseases;
        try {
            diseases = diseaseService.query(disname);
            request.setAttribute("DiseaseResults", diseases);
            request.getRequestDispatcher("DiseaseDisplay.jsp").forward(request, response);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}