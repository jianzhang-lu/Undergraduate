<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <meta name="generator" content="">
    <title>VariantDisplay</title>

    <!-- Bootstrap core CSS -->
    <link href="<%=request.getContextPath()%>/static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <script src="<%=request.getContextPath()%>/static/jquery/jquery-3.4.1.js"></script>
    <script src="<%=request.getContextPath()%>/static/bootstrap/js/bootstrap.bundle.min.js"></script>
    <!-- Custom styles for this template -->
    <link href="<%=request.getContextPath()%>/static/CSS/app.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="./static/CSS/table.css"/>
    <style>
        .bd-placeholder-img {
            font-size: 1.125rem;
            text-anchor: middle;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }

        @media (min-width: 768px) {
            .bd-placeholder-img-lg {
                font-size: 3.5rem;
            }
        }
    </style>
</head>
<body>
<jsp:include page="head.jsp" />

<div class="container-fluid">
    <div class="row">
        <jsp:include page="nav.jsp" >
            <jsp:param name="active" value="dashboard" />
        </jsp:include>

        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
            <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                <h2>Variant query results</h2><br>
            </div>
            <div class="table-responsive">
                <table>
                    <tr>
                        <th>Index</th>
                        <th>Variant Name</th>
                        <th>Variant ID</th>
                        <th>Gene Symbol</th>
                        <th>Disease</th>
                        <th>Drug</th>
                    </tr>
                    <c:forEach items="${VariantResults}" var="Variant" varStatus="status">
                        <c:if test="${Variant.varName == null}">
                            <tr>
                                <td><b>${status.count}</b></td>
                                <td><b>Variant name is not found!</b></td>
                                <td> Not Found! </td>
                                <td> Not Found! </td>
                                <td> Not Found! </td>
                                <td> Not Found! </td>
                            </tr>
                        </c:if>
                        <c:if test="${Variant.varName != null}">
                            <tr>
                                <td><b>${status.count}</b></td>
                                <td>${Variant.varName}</td>
                                <td>${Variant.varID}</td>
                                <td>${Variant.geneSymbol}</td>
                                <td>${Variant.disName}</td>
                                <td>${Variant.drug}</td>
                            </tr>
                        </c:if>
                    </c:forEach>
                </table>
            </div>
        </main>
    </div>
</div>
</body>
</html>





