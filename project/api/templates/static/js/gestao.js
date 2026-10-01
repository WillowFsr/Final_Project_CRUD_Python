let managementProducts = [];

function toneClass(id) { return ((Number(id) || 1) % 5) + 1; }

function renderManagement() {
  const root = document.getElementById("management-list");
  if (!managementProducts.length) {
    root.innerHTML = `<div class="empty-state">Nenhum produto cadastrado. Use o formulário acima para começar.</div>`;
    return;
  }

  root.innerHTML = managementProducts.map((product) => `
    <article class="management-row">
      <div class="management-avatar" style="background:linear-gradient(145deg, hsl(${(Number(product.id_prod) * 37) % 360} 24% 78%), hsl(${(Number(product.id_prod) * 37) % 360} 20% 47%));">${escapeHtml(String(product.nome).charAt(0).toUpperCase())}</div>
      <div class="management-main">
        <h3>${escapeHtml(product.nome)}</h3>
        <p>${escapeHtml(product.descricao || "Sem descrição.")}</p>
        <div class="management-meta">
          <span>ID #${product.id_prod}</span>
          <span>${money(product.preco)}</span>
          <span>${Number(product.estoque)} em estoque</span>
        </div>
      </div>
      <div class="management-actions">
        <button class="action-button" data-action="stock-add" data-id="${product.id_prod}">+ estoque</button>
        <button class="action-button" data-action="stock-remove" data-id="${product.id_prod}">− estoque</button>
        <button class="action-button" data-action="edit" data-id="${product.id_prod}">Editar</button>
        <button class="action-button danger" data-action="delete" data-id="${product.id_prod}">Excluir</button>
      </div>
    </article>`).join("");

  root.querySelectorAll("[data-action]").forEach((button) => {
    const id = Number(button.dataset.id);
    const action = button.dataset.action;
    button.addEventListener("click", () => {
      if (action === "stock-add") adjustStock(id, true);
      if (action === "stock-remove") adjustStock(id, false);
      if (action === "edit") openEdit(id);
      if (action === "delete") deleteProduct(id);
    });
  });
}

async function loadManagement() {
  const root = document.getElementById("management-list");
  root.innerHTML = `<div class="loading-card">Atualizando catálogo...</div>`;
  try {
    managementProducts = await Api.getProducts();
    renderManagement();
  } catch (error) {
    root.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  }
}

document.getElementById("product-create-form")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const data = Object.fromEntries(new FormData(form).entries());
  data.preco = Number(data.preco);
  data.estoque = Number(data.estoque);
  try {
    const product = await Api.createProduct(data);
    document.getElementById("product-create-result").classList.remove("hidden");
    document.getElementById("product-create-result").textContent = `Produto #${product.id_prod} cadastrado com sucesso.`;
    form.reset();
    await loadManagement();
    showToast("Produto cadastrado e publicado na loja.");
  } catch (error) {
    showToast(error.message, "error");
  }
});

async function adjustStock(productId, increase) {
  const value = Number(window.prompt(`Quantidade para ${increase ? "adicionar" : "remover"}:`, "1"));
  if (!Number.isInteger(value) || value < 1) return;
  try {
    const updated = increase ? await Api.addStock(productId, value) : await Api.removeStock(productId, value);
    const prefix = increase ? "Estoque aumentado" : "Estoque reduzido";
    showToast(`${prefix}: ${updated.estoque} unidade(s) disponíveis.`);
    await loadManagement();
  } catch (error) {
    showToast(error.message, "error");
  }
}

function openEdit(productId) {
  const product = managementProducts.find((item) => Number(item.id_prod) === Number(productId));
  if (!product) return;
  document.getElementById("edit-product-id").value = product.id_prod;
  document.getElementById("edit-product-name").value = product.nome;
  document.getElementById("edit-product-price").value = Number(product.preco).toFixed(2);
  document.getElementById("edit-product-stock").value = product.estoque;
  document.getElementById("edit-product-description").value = product.descricao || "";
  document.getElementById("edit-product-title").textContent = product.nome;
  const modal = document.getElementById("product-edit-modal");
  modal.classList.remove("hidden");
  modal.setAttribute("aria-hidden", "false");
}

function closeEdit() {
  const modal = document.getElementById("product-edit-modal");
  modal.classList.add("hidden");
  modal.setAttribute("aria-hidden", "true");
}

document.getElementById("edit-modal-close")?.addEventListener("click", closeEdit);
document.getElementById("product-edit-modal")?.addEventListener("click", (event) => {
  if (event.target.id === "product-edit-modal") closeEdit();
});

document.getElementById("product-edit-form")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const id = Number(document.getElementById("edit-product-id").value);
  const payload = {
    nome: document.getElementById("edit-product-name").value.trim(),
    preco: Number(document.getElementById("edit-product-price").value),
    estoque: Number(document.getElementById("edit-product-stock").value),
    descricao: document.getElementById("edit-product-description").value.trim()
  };
  try {
    await Api.updateProduct(id, payload);
    closeEdit();
    await loadManagement();
    showToast("Produto atualizado.");
  } catch (error) {
    showToast(error.message, "error");
  }
});

async function deleteProduct(productId) {
  const product = managementProducts.find((item) => Number(item.id_prod) === Number(productId));
  const name = product?.nome || `#${productId}`;
  if (!window.confirm(`Excluir ${name}? Esta ação não pode ser desfeita.`)) return;
  try {
    await Api.deleteProduct(productId);
    await loadManagement();
    showToast("Produto removido do catálogo.");
  } catch (error) {
    showToast(error.message, "error");
  }
}

document.getElementById("management-refresh")?.addEventListener("click", loadManagement);
loadManagement();
