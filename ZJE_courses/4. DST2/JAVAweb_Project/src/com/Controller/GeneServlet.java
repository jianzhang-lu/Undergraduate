package Controller;

import JavaBean.Gene;
import Service.GeneService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;

@WebServlet(name = "GeneServlet", value = "/GeneServlet")
public class GeneServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)  {
        GeneService geneService = new GeneService();
        String genename = request.getParameter("GeneName");
        ArrayList<Gene> genes;
        try {
            genes = geneService.query(genename);
            request.setAttribute("GeneResults", genes);
            request.getRequestDispatcher("/GeneDisplay.jsp").forward(request, response);
        } catch (SQLException | ServletException | IOException e) {
            e.printStackTrace();
        }
    }
}