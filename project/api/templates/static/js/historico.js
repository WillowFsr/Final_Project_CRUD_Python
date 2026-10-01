function formatDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString("pt-BR", { dateStyle: "medium", timeStyle: "short" });
}

function renderHistory(history) {
  const root = document.getElementById("history-list");
  if (!history.length) {
    root.innerHTML = `<div class="empty-state">Nenhuma compra encontrada para este cliente.</div>`;
    return;
  }

  root.innerHTML = history.map((record) => `
    <article class="history-card">
      <div class="history-card-header">
        <div class="history-card-title">
          <strong>Compra #${record.id_historico}</strong>
          <span>${formatDate(record.data_compra)}</span>
        </div>
        <strong class="history-total">${money(record.valor_total)}</strong>
      </div>
      <div class="history-items">
        ${(record.itens || []).map((item) => `
          <div class="history-item">
            <span>Produto #${item.id_prod} · ${item.quantidade} unidade(s)</span>
            <strong>${money(item.preco_momento)} cada</strong>
          </div>`).join("")}
      </div>
    </article>`).join("");
}

async function loadHistory() {
  const input = document.getElementById("history-client-id");
  const id = Number(input?.value);
  if (!Number.isInteger(id) || id < 1) return showToast("Informe um ID de cliente válido.", "error");

  try {
    const client = await Api.getClient(id);
    Store.setClientId(id);
    document.getElementById("history-session-label").textContent = `${client.nome} · Cliente #${id}`;
    const history = await Api.getHistory(id);
    renderHistory(history);
  } catch (error) {
    showToast(error.message, "error");
  }
}

document.getElementById("history-load")?.addEventListener("click", loadHistory);

const savedClient = Store.getClientId();
if (savedClient) {
  document.getElementById("history-client-id").value = savedClient;
  loadHistory();
}
