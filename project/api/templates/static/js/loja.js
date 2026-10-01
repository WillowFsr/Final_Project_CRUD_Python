let storeProducts = [];

function storeTone(id) { return ((Number(id) || 1) % 5) + 1; }

function renderStoreProducts(products) {
  const grid = document.getElementById("product-grid");
  if (!grid) return;

  if (!products.length) {
    grid.innerHTML = `<div class="empty-state">Nenhum produto encontrado.</div>`;
    return;
  }

  grid.innerHTML = products.map((product) => {
    const disabled = Number(product.estoque) < 1;
    return `
      <article class="product-card">
        <div class="product-visual product-tone-${storeTone(product.id_prod)}">
          <span class="product-badge">AUREA</span>
          <span class="product-stock">${disabled ? "Sem estoque" : `${Number(product.estoque)} em estoque`}</span>
          <div class="product-object"></div>
        </div>
        <div class="product-info">
          <div class="product-overline">ID ${String(product.id_prod).padStart(2, "0")}</div>
          <h3>${escapeHtml(product.nome)}</h3>
          <p>${escapeHtml(product.descricao || "Produto selecionado da coleção.")}</p>
          <div class="product-price-row">
            <strong class="product-price">${money(product.preco)}</strong>
            <div class="product-action">
              ${disabled ? `<span class="status-chip">Indisponível</span>` : `
                <button class="button button-dark add-product-button" type="button" data-id="${product.id_prod}">Adicionar</button>`}
            </div>
          </div>
          ${!disabled ? `
            <div class="quantity-control" style="margin-top:12px;display:flex;gap:8px;align-items:center;">
              <label class="field" style="flex:1"><span>Quantidade</span><input class="store-quantity" data-id="${product.id_prod}" type="number" min="1" max="${Number(product.estoque)}" value="1"></label>
            </div>` : ""}
        </div>
      </article>`;
  }).join("");

  grid.querySelectorAll(".add-product-button").forEach((button) => {
    button.addEventListener("click", () => addProductToCart(Number(button.dataset.id)));
  });
}

function applyFilters() {
  const search = (document.getElementById("store-search")?.value || "").trim().toLowerCase();
  const sort = document.getElementById("store-sort")?.value || "featured";
  let filtered = storeProducts.filter((product) => `${product.nome} ${product.descricao || ""}`.toLowerCase().includes(search));

  if (sort === "name") filtered.sort((a, b) => a.nome.localeCompare(b.nome));
  if (sort === "price-asc") filtered.sort((a, b) => Number(a.preco) - Number(b.preco));
  if (sort === "price-desc") filtered.sort((a, b) => Number(b.preco) - Number(a.preco));
  if (sort === "stock") filtered.sort((a, b) => Number(b.estoque) - Number(a.estoque));
  renderStoreProducts(filtered);
}

async function selectClient() {
  const input = document.getElementById("store-client-id");
  const id = Number(input?.value);
  if (!Number.isInteger(id) || id < 1) {
    showToast("Informe um ID de cliente válido.", "error");
    return;
  }

  try {
    const client = await Api.getClient(id);
    Store.setClientId(client.id_cli);
    Store.clearCart();
    document.getElementById("store-session-label").textContent = client.nome;
    document.getElementById("store-session-detail").textContent = `Cliente #${client.id_cli} selecionado. Agora você pode adicionar produtos.`;
    showToast(`Conta de ${client.nome} selecionada.`);
    await refreshNavCart();
  } catch (error) {
    showToast(error.message, "error");
  }
}

async function addProductToCart(productId) {
  const clientId = Store.getClientId();
  if (!clientId) {
    showToast("Selecione um cliente antes de adicionar produtos.", "error");
    return;
  }
  const quantityInput = document.querySelector(`.store-quantity[data-id="${productId}"]`);
  const quantity = Number(quantityInput?.value || 1);
  if (!Number.isInteger(quantity) || quantity < 1) {
    showToast("Informe uma quantidade válida.", "error");
    return;
  }

  try {
    const cart = await Api.addCartItem(clientId, productId, quantity);
    Store.setCartId(cart.id_carrinho);
    updateNavCartCount((cart.produto_carrinho || []).reduce((sum, item) => sum + Number(item.quantidade || 0), 0));
    showToast("Produto adicionado à sacola.");
    window.setTimeout(() => { window.location.href = "/sacola"; }, 450);
  } catch (error) {
    showToast(error.message, "error");
  }
}

async function loadStore() {
  const input = document.getElementById("store-client-id");
  const clientId = Store.getClientId();
  if (clientId && input) {
    input.value = clientId;
    try {
      const client = await Api.getClient(clientId);
      document.getElementById("store-session-label").textContent = client.nome;
      document.getElementById("store-session-detail").textContent = `Cliente #${client.id_cli} selecionado.`;
    } catch (_) {}
  }

  try {
    storeProducts = await Api.getProducts();
    renderStoreProducts(storeProducts);
  } catch (error) {
    document.getElementById("product-grid").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  }
}

document.getElementById("store-client-save")?.addEventListener("click", selectClient);
document.getElementById("store-search")?.addEventListener("input", applyFilters);
document.getElementById("store-sort")?.addEventListener("change", applyFilters);
loadStore();
