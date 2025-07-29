// Funções para cotas na página de detalhes da rifa
function somarCotas(qtd) {
  let input = document.getElementById("quantidade");
  let atual = parseInt(input.value);
  let novo = atual + Number(qtd);
  if (novo < 10) novo = 10;
  input.value = novo;
  atualizarTotal();
}

function ajustarQtd(delta) {
  let input = document.getElementById("quantidade");
  let atual = parseInt(input.value);
  let novo = Math.max(10, atual + delta);
  input.value = novo;
  atualizarTotal();
}

function selecionarCotas(qtd) {
  let novo = Math.max(10, Number(qtd));
  document.getElementById("quantidade").value = novo;
  atualizarTotal();
}

function atualizarTotal() {
  let input = document.getElementById("quantidade");
  let totalCotas = parseInt(input.value);
  document.getElementById("totalSelecionado").innerText = `Total selecionado: ${totalCotas}`;
  let valorUnitario = parseFloat(document.getElementById("btnAdquirir").dataset.valorUnitario || '0.76');
  let total = (totalCotas * valorUnitario).toFixed(2).replace('.',',');
  document.getElementById("btnAdquirir").innerHTML = `✅ Adquirir Bilhete — R$ ${total}`;
}

document.addEventListener("DOMContentLoaded", function() {
  atualizarTotal();
});
