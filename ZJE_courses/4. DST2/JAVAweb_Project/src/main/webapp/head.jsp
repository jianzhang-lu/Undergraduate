<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
    <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">
        <b>Welcome to Precision Medicine Matching System (Project created by Group 5). </b>
    </a>
    <ul class="navbar-nav px-3">
        <li class="nav-item text-nowrap">
            <b class="session">Hi, ${sessionScope.username}</b>
            <form action="logoutServlet">
                <input type="submit" value="Log out">
            </form>
        </li>
    </ul>
</nav>