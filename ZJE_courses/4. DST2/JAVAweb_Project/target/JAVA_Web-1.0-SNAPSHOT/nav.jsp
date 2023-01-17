<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<nav class="col-md-2 d-none d-md-block bg-light sidebar">
    <div class="sidebar-sticky">
        <ul class="nav flex-column">
            <li class="nav-item">
                <a class='nav-link ${param.active == "dashboard" ? "active" : ""}' href="Main.jsp">
                    <span data-feather="home"></span>
                    Dashboard <span class="sr-only">(current)</span>
                </a>
            </li>
        </ul>

        <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
            <span>Precision Medicine Knowledge Base</span>
            <a class="d-flex align-items-center text-muted" href="#">
                <span data-feather="plus-circle"></span>
            </a>
        </h6>
        <ul class="nav flex-column mb-2">
            <li class="nav-item">
                <a class='nav-link active' href="GeneForm.jsp">
                    <span data-feather="file-text"></span>
                    Genes
                </a>
            </li>
            <li class="nav-item">
                <a class='nav-link active' href="VariantForm.jsp">
                    <span data-feather="file-text"></span>
                    Variants
                </a>
            </li>
            <li class="nav-item">
                <a class='nav-link active' href="DiseaseForm.jsp">
                    <span data-feather="file-text"></span>
                    Diseases
                </a>
            </li>
            <li class="nav-item">
                <a class='nav-link active' href="InterestForm.jsp">
                    <span data-feather="file-text"></span>
                    Your Interests
                </a>
            </li>
        </ul>
    </div>
</nav>