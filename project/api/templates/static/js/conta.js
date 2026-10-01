async function loadClientAccount(clientId) {
  const client = await Api.getClient(clientId);
  Store.setClientId(client.id_cli);
  Store.clearCart();
  const panel = document.getElementById("account-client-panel");
  panel.classList.remove("empty-account");
  panel.innerHTML = `
    <strong>${escapeHtml(client.nome)}</strong>
    <span>Cliente #${client.id_cli} · ${escapeHtml(client.nacionalidade)} · ${client.idade} anos</span>
    <span>${escapeHtml(client.endereco)}</span>`;
  document.getElementById("account-client-status").textContent = "Ativo";
  document.getElementById("account-client-id").value = client.id_cli;
  document.getElementById("saved-card-label").textContent = Store.getCardId() ? `#${Store.getCardId()}` : "Nenhum";
  await refreshNavCart();
  return client;
}

document.getElementById("account-load-client")?.addEventListener("click", async () => {
  const id = Number(document.getElementById("account-client-id")?.value);
  if (!Number.isInteger(id) || id < 1) return showToast("Informe um ID válido.", "error");
  try {
    await loadClientAccount(id);
    showToast("Conta carregada.");
  } catch (error) {
    showToast(error.message, "error");
  }
});

document.getElementById("client-create-form")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const data = Object.fromEntries(new FormData(form).entries());
  data.idade = Number(data.idade);
  try {
    const client = await Api.createClient(data);
    await loadClientAccount(client.id_cli);
    form.reset();
    form.querySelector('[name="nacionalidade"]').value = "Brasileira";
    showToast(`Conta #${client.id_cli} criada com sucesso.`);
  } catch (error) {
    showToast(error.message, "error");
  }
});

document.getElementById("card-create-form")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const clientId = Store.getClientId();
  if (!clientId) return showToast("Selecione um cliente antes de cadastrar o cartão.", "error");
  const form = event.currentTarget;
  const data = Object.fromEntries(new FormData(form).entries());
  try {
    const card = await Api.createCard(clientId, data);
    Store.setCardId(card.id_cartao);
    document.getElementById("saved-card-label").textContent = `#${card.id_cartao}`;
    document.getElementById("saved-card-balance").textContent = money(card.saldo);
    document.getElementById("card-result").classList.remove("hidden");
    document.getElementById("card-result").textContent = `Cartão #${card.id_cartao} salvo. Saldo atual: ${money(card.saldo)}.`;
    form.reset();
    showToast("Cartão cadastrado.");
  } catch (error) {
    showToast(error.message, "error");
  }
});

async function refreshSavedCard() {
  const clientId = Store.getClientId();
  const cardId = Store.getCardId();
  if (!clientId || !cardId) return;
  try {
    const card = await Api.getCard(clientId, cardId);
    document.getElementById("saved-card-label").textContent = `#${card.id_cartao}`;
    document.getElementById("saved-card-balance").textContent = money(card.saldo);
    document.getElementById("balance-card-id").value = card.id_cartao;
  } catch (_) {}
}

document.getElementById("balance-add")?.addEventListener("click", async () => {
  const clientId = Store.getClientId();
  const cardId = Number(document.getElementById("balance-card-id")?.value);
  const value = Number(document.getElementById("balance-value")?.value);
  if (!clientId) return showToast("Selecione um cliente.", "error");
  if (!Number.isInteger(cardId) || cardId < 1 || !(value > 0)) return showToast("Informe cartão e valor válidos.", "error");
  try {
    const card = await Api.addBalance(clientId, cardId, value);
    Store.setCardId(card.id_cartao);
    document.getElementById("saved-card-label").textContent = `#${card.id_cartao}`;
    document.getElementById("saved-card-balance").textContent = money(card.saldo);
    document.getElementById("balance-value").value = "";
    showToast(`Saldo atualizado para ${money(card.saldo)}.`);
  } catch (error) {
    showToast(error.message, "error");
  }
});

(async function init() {
  const clientId = Store.getClientId();
  if (clientId) {
    try { await loadClientAccount(clientId); } catch (_) {}
  }
  await refreshSavedCard();
})();
