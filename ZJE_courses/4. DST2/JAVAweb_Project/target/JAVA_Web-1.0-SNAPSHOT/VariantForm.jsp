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
    <title>InterestForm</title>

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
                <h2>Variant search</h2><br>
            </div>
            <div class="table-responsive">
                <b>You can input a variant name (example: rs2270777) or a list of variant names
                    separated by comma to query VariantID, related gene names,
                    related diseases and corresponding drugs. Also, you can upload a own txt file to query.
                    This txt file should be annotated by the ANNOVAR. </b><br><br>
                <form action="VariantServlet" method="post">
                    <div class="inputText">
                        <i class="fa fa-user-circle" style="color: whitesmoke;"></i>
                        <textarea type="text" placeholder="Variant Name" name="VarName" style="width:900px;height:100px"/></textarea>
                        <br><br>
                    </div> <br>
                    <input type="submit" class="inputButton" value="Query" />
                    <input type="reset" class="inputButton" value="Reset"><br><br>

                </form> <br><hr><br>

                <form action="uploaddata" method="post" enctype="multipart/form-data">
                    <div class="inputText">
                        <i class="fa fa-user-circle" style="color: whitesmoke;"></i>
                        <b>Upload your txt file containing variant name.</b><br>
                        <input type="file" class="inputButton" name="uploadFile"><br><br>
                    </div> <br>
                    <input type="submit" class="inputButton" value="Upload" />
                    <input type="reset" class="inputButton" value="Reset"><br><br>
                </form>
            </div>
        </main>
    </div>
</div>
</body>
</html>





