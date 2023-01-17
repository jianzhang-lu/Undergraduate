<%@ page import="java.io.PrintWriter" %>
<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>LoginError</title>
    <link rel="stylesheet" type="text/css" href="./static/CSS/style.css"/>
    <link rel="stylesheet" href="https://cdn.staticfile.org/font-awesome/4.7.0/css/font-awesome.css">
</head>
<body>
<div id="bigBox">
    <h1>LOGIN ERROR</h1>
    <div class="inputBox">
        <c:if test="${info == 1}">
            <h2 class="error">The username or password is incorrect!</h2>
        </c:if>

        <c:if test="${info == 3}">
            <h2 class="error">The username has been used!</h2>
        </c:if>

        <c:if test="${info == 6}">
            <h2 class="error">The username and password can not be null!</h2>
        </c:if>

        <a href = "Login.jsp" class="Register"><b>Retry</b></a><br>
        <a href = "Reset.jsp" class="Register"><b>Forget Password? Reset</b></a><br>
        <a href = "Register.jsp" class="Register"><b>Do not have an account? Register</b></a><br>
    </div>
</div>
</body>
</html>
