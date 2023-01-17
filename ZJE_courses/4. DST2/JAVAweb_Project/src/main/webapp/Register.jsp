<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Register</title>
    <link rel="stylesheet" type="text/css" href="./static/CSS/style.css"/>
    <link rel="stylesheet" href="https://cdn.staticfile.org/font-awesome/4.7.0/css/font-awesome.css">
</head>
<body>
<div id="bigBox">
    <h1>REGISTER</h1>
    <div class="inputBox">
        <c:if test="${info == 4}">
            <h2 class="error">No account. Please register first.</h2>
        </c:if>
        <form action="RegisterServlet" method="post">
            <div class="inputText">
                <i class="fa fa-user-circle" style="color: whitesmoke;"></i>
                <input type="text" placeholder="NEW USERNAME" name="username2"/>
            </div>
            <div class="inputText">
                <i class="fa fa-key" style="color: whitesmoke;"></i>
                <input type="password" placeholder="PASSWORD" name="password2"/>
            </div>

            <input type="submit" class="inputButton" value="REGISTER" /><br><br>
            <a href="Login.jsp" class="Register"><b>Have an account? Login in</b></a>
        </form>
    </div>
</div>
</body>
</html>
