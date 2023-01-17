package Controller;

import JavaBean.User;
import Service.UserService;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;
import java.io.IOException;
import java.sql.*;

@WebServlet(name = "ResetServlet", value = "/ResetServlet")
public class ResetServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        UserService userService = new UserService();
        //处理Reset事务
        String reset_username = request.getParameter("username3");
        String reset_password = request.getParameter("password3");
        User res_user = new User();

        try {
            if(!reset_username.equals("") & !reset_password.equals("")){
                if(userService.check(reset_username).getUseid() != null) {
                    res_user.setUsername(reset_username);
                    res_user.setPassword(reset_password);
                    int row = userService.update(res_user);
                    System.out.println(row);
                    request.setAttribute("info", 5);
                    request.getRequestDispatcher("Login.jsp").forward(request, response);
                }else{
                    request.setAttribute("info", 4);
                    request.getRequestDispatcher("Register.jsp").forward(request, response);
                }
            }else{
                request.setAttribute("info", 6);
                request.getRequestDispatcher("Loginerror.jsp").forward(request, response);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
