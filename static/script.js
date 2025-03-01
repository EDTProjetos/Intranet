// script.js
document.addEventListener("DOMContentLoaded", function () {
    const headerTitle = document.getElementById("headerTitle");
    const sidebar = document.querySelector(".sidebar");
    const toggleSidebarBtn = document.getElementById("toggleSidebarBtn");

    toggleSidebarBtn.addEventListener("click", function () {
        if (sidebar.style.transform === "translateX(-100%)") {
            sidebar.style.transform = "translateX(0)";
            toggleSidebarBtn.innerText = "Ocultar Sidebar";
        } else {
            sidebar.style.transform = "translateX(-100%)";
            toggleSidebarBtn.innerText = "Mostrar Sidebar";
        }
    });
});
