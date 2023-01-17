package Controller;

import JavaBean.Interest;
import Service.InterestService;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;

@WebServlet(name = "InterestServlet", value = "/InterestServlet")
public class InterestServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        InterestService interestService = new InterestService();
        String email = request.getParameter("Email");
        String information = request.getParameter("Information");

        Interest interest = new Interest();
        interest.setName(email);
        interest.setInformation(information);
        try {
            int row = interestService.add(interest);
            request.getRequestDispatcher("/InterestDisplay.jsp").forward(request, response);
        } catch (SQLException e) {
            e.printStackTrace();
        }

    }
}