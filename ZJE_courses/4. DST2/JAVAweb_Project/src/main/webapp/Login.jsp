<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Login</title>
    <link rel="stylesheet" type="text/css" href="./static/CSS/style.css"/>
    <link rel="stylesheet" href="https://cdn.staticfile.org/font-awesome/4.7.0/css/font-awesome.css">
</head>
<body>
<div id="bigBox">
    <h1>LOGIN</h1>
    <div class="inputBox">
        <c:if test="${info == 2}">
            <h2 class="error">Register success!</h2>
        </c:if>

        <c:if test="${info == 5}">
            <h2 class="error">Reset success!</h2>
        </c:if>
        <form action="LoginServlet" method="post">
            <div class="inputText">
                <i class="fa fa-user-circle" style="color: whitesmoke;"></i>
                <input type="text" placeholder="USERNAME" name="username"/>
            </div>
            <div class="inputText">
                <i class="fa fa-key" style="color: whitesmoke;"></i>
                <input type="password" placeholder="PASSWORD" name="password"/>
            </div>

            <input type="submit" class="inputButton" value="LOGIN" /><br><br>
            <a href="Reset.jsp" class="Register"><b>Forget password? Reset</b></a><br><br>
            <a href="Register.jsp" class="Register"><b>Do not have an account? Register</b></a>
        </form>
    </div>
</div>
</body>
</html>
