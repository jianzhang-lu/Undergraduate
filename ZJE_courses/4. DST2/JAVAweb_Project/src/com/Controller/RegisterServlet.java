package Controller;

import JavaBean.User;
import Service.UserService;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;
import java.io.IOException;
import java.sql.*;

@WebServlet(name = "RegisterServlet", value = "/RegisterServlet")
public class RegisterServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doPost(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        UserService userService = new UserService();
        //处理Register事务
        String reg_username = request.getParameter("username2");
        String reg_password = request.getParameter("password2");
        User new_user = new User();
        try {
            if(!reg_username.equals("") & !reg_password.equals("")){
                if(userService.check(reg_username).getUseid() == null) {
                    new_user.setUsername(reg_username);
                    new_user.setPassword(reg_password);
                    int row = userService.add(new_user);
                    System.out.println(row);
                    request.setAttribute("info", 2);
                    request.getRequestDispatcher("Login.jsp").forward(request, response);
                }else{
                    request.setAttribute("info", 3);
                    request.getRequestDispatcher("Loginerror.jsp").forward(request, response);
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
