function toneFor(id) { return ((Number(id) || 1) % 5) + 1; }
function productCard(product, options = {}) {
  const disabled = Number(product.estoque) < 1;
  const home = Boolean(options.home);
  return `
    <article class="product-card">
      <div class="product-visual product-tone-${toneFor(product.id_prod)}">
        <span class="product-badge">${disabled ? "INDISPONÍVEL" : "AUREA SELECT"}</span>
        <span class="product-stock">${disabled ? "Sem estoque" : `${Number(product.estoque)} disponíveis`}</span>
        <div class="product-object"></div>
      </div>
      <div class="product-info">
        <div class="product-overline">Produto · ${String(product.id_prod).padStart(2, "0")}</div>
        <h3>${escapeHtml(product.nome)}</h3>
        <p>${escapeHtml(product.descricao || "Escolha para sua rotina.")}</p>
        <div class="product-price-row">
          <strong class="product-price">${money(product.preco)}</strong>
          <div class="product-action">
            <a class="button button-dark" href="/loja${home ? `?produto=${product.id_prod}` : ""}">${disabled ? "Ver produto" : "Adicionar"}</a>
          </div>
        </div>
      </div>
    </article>`;
}

async function loadHomeProducts() {
  const root = document.getElementById("home-products");
  if (!root) return;
  try {
    const products = await Api.getProducts();
    const visible = products.slice(0, 6);
    root.innerHTML = visible.length
      ? visible.map((product) => productCard(product, { home: true })).join("")
      : `<div class="empty-state">O catálogo ainda está vazio. Comece adicionando um produto na Gestão.</div>`;
  } catch (error) {
    root.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  }
}

loadHomeProducts();
