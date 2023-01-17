<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <meta name="generator" content="">
    <title>GeneForm</title>

    <!-- Bootstrap core CSS -->
    <link href="<%=request.getContextPath()%>/static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <script src="<%=request.getContextPath()%>/static/jquery/jquery-3.4.1.js"></script>
    <script src="<%=request.getContextPath()%>/static/bootstrap/js/bootstrap.bundle.min.js"></script>
    <!-- Custom styles for this template -->
    <link href="<%=request.getContextPath()%>/static/CSS/app.css" rel="stylesheet">
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
                <h2>Gene search</h2><br>
            </div>
            <div class="table-responsive">
                <b>You can input a gene name or a list of gene names separated by comma to query the
                    geneID, gene full name, chromosome, start position, end position
                    and the link to the Ensembl Genome Browser.</b> <br> <br>
                <form action="GeneServlet" method="post">
                    <div class="inputText">
                        <i class="fa fa-user-circle" style="color: whitesmoke;"></i>
                        <textarea type="text" placeholder="Gene Name" name="GeneName" style="width:900px;height:100px"/></textarea>
                    </div> <br>
                    <input type="submit" class="inputButton" value="Query" />
                    <input type="reset" class="inputButton" value="Reset"><br><br>
                </form>
            </div>
        </main>
    </div>
</div>
</body>
</html>



