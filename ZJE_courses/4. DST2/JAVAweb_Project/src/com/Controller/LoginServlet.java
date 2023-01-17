package Controller;

import JavaBean.User;
import Service.UserService;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;
import java.io.IOException;
import java.sql.*;

@WebServlet(name = "LoginServlet", value = "/LoginServlet")
public class LoginServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        UserService userService = new UserService();
        String username = request.getParameter("username");
        String password = request.getParameter("password");

        User user = new User();
        //处理Login事务
        try {
            user = userService.check(username);
        } catch (SQLException e) {
            e.printStackTrace();
        }

        if(user.getUseid() != null && user.getPassword().equals(password)) {
            HttpSession session = request.getSession();
            session.setAttribute("username", username);
            request.getRequestDispatcher("Main.jsp").forward(request, response);
        }else{
            request.setAttribute("info", 1);
            request.getRequestDispatcher("Loginerror.jsp").forward(request, response);
        }
    }
}