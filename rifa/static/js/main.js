document.addEventListener("DOMContentLoaded", () => {
  // MENU LATERAL
  const btnMenu = document.getElementById("btn-menu");
  const btnFecharMenu = document.getElementById("btn-fechar-menu");
  const menuLateral = document.getElementById("menu-lateral");

  if (btnMenu && btnFecharMenu && menuLateral) {
    btnMenu.addEventListener("click", () => {
      menuLateral.classList.add("open");
      document.body.style.overflow = "hidden";
    });

    btnFecharMenu.addEventListener("click", () => {
      menuLateral.classList.remove("open");
      document.body.style.overflow = "";
    });

    window.addEventListener("click", (e) => {
      if (
        menuLateral.classList.contains("open") &&
        !menuLateral.contains(e.target) &&
        e.target.id !== "btn-menu"
      ) {
        menuLateral.classList.remove("open");
        document.body.style.overflow = "";
      }
    });
  }

  // MODAL DE LOGIN
  const btnLoginMenu = document.getElementById("btnLoginMenu");
  const loginModal = document.getElementById("loginModal");

  if (btnLoginMenu && loginModal) {
    btnLoginMenu.addEventListener("click", () => {
      loginModal.style.display = "flex";
      document.body.style.overflow = "hidden";
      if (menuLateral) menuLateral.classList.remove("open");
    });
  }

  // CEP - AUTO PREENCHIMENTO
  const cepInput = document.getElementById("cep");
  if (cepInput) {
    cepInput.addEventListener("input", function () {
      const cep = this.value.replace(/\D/g, "");
      if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
          .then((res) => res.json())
          .then((data) => {
            console.log("ViaCEP retorno:", data); // Depuração
            if (!data.erro) {
              const logradouro = document.getElementById("logradouro");
              const bairro = document.getElementById("bairro");
              const cidade = document.getElementById("cidade");
              if (logradouro && bairro && cidade) {
                logradouro.value = data.logradouro || "";
                bairro.value = data.bairro || "";
                cidade.value = data.localidade || "";
              } else {
                alert("Algum campo de endereço não foi encontrado no formulário.");
              }
              // Seleciona o estado correto no select UF
              const ufSelect = document.getElementById("uf");
              if (ufSelect) {
                for (let i = 0; i < ufSelect.options.length; i++) {
                  if (ufSelect.options[i].value === data.uf) {
                    ufSelect.selectedIndex = i;
                    break;
                  }
                }
              }
            } else {
              alert("CEP não encontrado.");
            }
          })
          .catch(() => alert("Erro ao buscar o CEP."));
      }
    });
  }

  // FORMULÁRIO - VALIDAÇÃO
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      const senha = document.getElementById("senha").value;
      const senha2 = document.getElementById("senha2").value;
      const telefone = document.getElementById("telefone").value;
      const confirmaTelefone = document.getElementById("confirmaTelefone").value;

      if (senha !== senha2) {
        alert("As senhas não coincidem.");
        e.preventDefault();
        return;
      }

      if (telefone !== confirmaTelefone) {
        alert("Os telefones não coincidem.");
        e.preventDefault();
        return;
      }

      const loading = document.getElementById("loading");
      if (loading) loading.style.display = "block";
    });
  }
});
