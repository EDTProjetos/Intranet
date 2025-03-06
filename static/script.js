document.addEventListener("DOMContentLoaded", function () {
  let loggedIn = false;
  let requestedSection = null;
  let activeContainer = null;

  // Função de login
  const loginMenu = document.getElementById("loginMenu");
  const loginBtn = document.getElementById("loginBtn");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  const loginError = document.getElementById("loginError");

  loginBtn.addEventListener("click", function () {
    if (usernameInput.value === "admin" && passwordInput.value === "admin") {
      loggedIn = true;
      loginMenu.style.display = "none";
      if (requestedSection === "planejamentoBI") {
        document.getElementById("planejamentoSection").style.display = "block";
      }
    } else {
      loginError.style.display = "block";
    }
  });

  // Função para alternar a sidebar
  const toggleSidebarBtn = document.getElementById("toggleSidebarBtn");
  const sidebar = document.querySelector(".sidebar");

  toggleSidebarBtn.addEventListener("click", function () {
    if (sidebar.style.transform === "translateX(-100%)") {
      sidebar.style.transform = "translateX(0)";
      toggleSidebarBtn.innerText = "Ocultar Sidebar";
    } else {
      sidebar.style.transform = "translateX(-100%)";
      toggleSidebarBtn.innerText = "Mostrar Sidebar";
    }
  });

  // Função para atualizar o título do cabeçalho
  function updateHeaderTitle(text) {
    document.getElementById("headerTitle").innerText = text;
  }

  // Função para esconder todas as seções
  function hideAllMenus() {
    document.getElementById("loginMenu").style.display = "none";
    document.getElementById("profileMenu").style.display = "none";
    document.getElementById("driveSection").style.display = "none";
    document.getElementById("planejamentoSection").style.display = "none";
    document.getElementById("importacoesSection").style.display = "none";
    document.getElementById("monitoriaManuaisSection").style.display = "none";
    document.getElementById("hahVendasSection").style.display = "none";
  }

  // Função de exibição de conteúdo
  document.getElementById("planejamentoBtn").addEventListener("click", function () {
    if (loggedIn) {
      hideAllMenus();
      document.getElementById("planejamentoSection").style.display = "block";
      updateHeaderTitle("Planejamento");
    } else {
      requestedSection = "planejamento";
      loginMenu.style.display = "block";
      updateHeaderTitle("Login - Planejamento");
    }
  });
});
