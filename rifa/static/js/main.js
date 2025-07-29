document.addEventListener("DOMContentLoaded", () => {
  // Funções auxiliares
  const toggleScroll = (enable) => {
    document.body.style.overflow = enable ? '' : 'hidden';
  };

  const updateInputCotas = (valor) => {
    const input = document.getElementById('input-cotas');
    if (input) input.value = valor;
  };

  // MENU LATERAL
  const btnMenu = document.getElementById("btn-menu");
  const btnFecharMenu = document.getElementById("btn-fechar-menu");
  const menuLateral = document.getElementById("menu-lateral");

  if (btnMenu && btnFecharMenu && menuLateral) {
    btnMenu.addEventListener("click", () => {
      menuLateral.classList.add("open");
      toggleScroll(false);
    });

    btnFecharMenu.addEventListener("click", () => {
      menuLateral.classList.remove("open");
      toggleScroll(true);
    });

    window.addEventListener("click", (e) => {
      if (
        menuLateral.classList.contains("open") &&
        !menuLateral.contains(e.target) &&
        e.target.id !== "btn-menu"
      ) {
        menuLateral.classList.remove("open");
        toggleScroll(true);
      }
    });
  }

  // MODAL DE LOGIN
  const btnLoginMenu = document.getElementById("btnLoginMenu");
  const loginModal = document.getElementById("loginModal");

  if (btnLoginMenu && loginModal) {
    btnLoginMenu.addEventListener("click", () => {
      loginModal.style.display = "flex";
      toggleScroll(false);
      if (menuLateral) menuLateral.classList.remove("open");
    });

    // Fecha modal clicando fora do conteúdo
    loginModal.addEventListener("click", (e) => {
      if (e.target === loginModal) {
        loginModal.style.display = "none";
        toggleScroll(true);
      }
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
            if (!data.erro) {
              const logradouro = document.getElementById("logradouro");
              const bairro = document.getElementById("bairro");
              const cidade = document.getElementById("cidade");
              const ufSelect = document.getElementById("uf");

              if (!(logradouro && bairro && cidade && ufSelect)) {
                console.error("Alguns campos de endereço não foram encontrados.");
                return;
              }

              logradouro.value = data.logradouro || "";
              bairro.value = data.bairro || "";
              cidade.value = data.localidade || "";

              for (let i = 0; i < ufSelect.options.length; i++) {
                if (ufSelect.options[i].value === data.uf) {
                  ufSelect.selectedIndex = i;
                  break;
                }
              }
            } else {
              alert("CEP não encontrado.");
            }
          })
          .catch((error) => {
            console.error("Erro ao buscar o CEP:", error);
            alert("Erro ao buscar o CEP. Verifique sua conexão.");
          });
      }
    });
  }

  // FORMULÁRIO - VALIDAÇÃO
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      const senha = document.getElementById("senha")?.value;
      const senha2 = document.getElementById("senha2")?.value;
      const telefone = document.getElementById("telefone")?.value;
      const confirmaTelefone = document.getElementById("confirmaTelefone")?.value;

      if (senha && senha2 && senha !== senha2) {
        alert("As senhas não coincidem.");
        e.preventDefault();
        return;
      }

      if (telefone && confirmaTelefone && telefone !== confirmaTelefone) {
        alert("Os telefones não coincidem.");
        e.preventDefault();
        return;
      }

      const loading = document.getElementById("loading");
      if (loading) loading.style.display = "block";
    });
  }

  // MINI ABA DE COTAS (RIFA) - DELEGAÇÃO DE EVENTOS
  document.body.addEventListener("click", function (e) {
    // Botões de cotas rápidas
    if (e.target.classList.contains("btn-cotas")) {
      document.querySelectorAll(".btn-cotas").forEach((b) => b.classList.remove("active"));
      e.target.classList.add("active");
      const valor = parseInt(e.target.dataset.valor, 10);
      updateInputCotas(valor);
    }

    // Botão +
    if (e.target.id === "btn-plus") {
      const input = document.getElementById("input-cotas");
      if (input) {
        const valor = parseInt(input.value, 10) || 0;
        updateInputCotas(valor + 1);
        document.querySelectorAll(".btn-cotas").forEach((b) => b.classList.remove("active"));
      }
    }

    // Botão -
    if (e.target.id === "btn-minus") {
      const input = document.getElementById("input-cotas");
      if (input) {
        let valor = parseInt(input.value, 10);
        if (isNaN(valor) || valor <= 1) {
          valor = 1;
        } else {
          valor = valor - 1;
        }
        updateInputCotas(valor);
        document.querySelectorAll(".btn-cotas").forEach((b) => b.classList.remove("active"));
      }
    }
  });
});
