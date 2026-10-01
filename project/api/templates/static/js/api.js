const Api = {
  async request(url, options = {}) {
    const config = { ...options, headers: { ...(options.headers || {}) } };
    if (config.body && !config.headers["Content-Type"]) {
      config.headers["Content-Type"] = "application/json";
    }

    const response = await fetch(url, config);
    if (response.status === 204) return null;

    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
      ? await response.json()
      : await response.text();

    if (!response.ok) {
      const detail = data && typeof data === "object" && data.detail
        ? data.detail
        : "Não foi possível concluir a operação.";
      throw new Error(detail);
    }

    return data;
  },

  getProducts() { return this.request("/produtos"); },
  getProduct(id) { return this.request(`/produtos/${id}`); },
  createProduct(payload) { return this.request("/produtos", { method: "POST", body: JSON.stringify(payload) }); },
  updateProduct(id, payload) { return this.request(`/produtos/${id}`, { method: "PUT", body: JSON.stringify(payload) }); },
  deleteProduct(id) { return this.request(`/produtos/${id}`, { method: "DELETE" }); },
  addStock(id, quantity) { return this.request(`/produtos/${id}/estoque`, { method: "POST", body: JSON.stringify({ quantidade: Number(quantity) }) }); },
  removeStock(id, quantity) { return this.request(`/produtos/${id}/estoque/remover`, { method: "POST", body: JSON.stringify({ quantidade: Number(quantity) }) }); },

  getClient(id) { return this.request(`/clientes/${id}`); },
  createClient(payload) { return this.request("/clientes", { method: "POST", body: JSON.stringify(payload) }); },
  updateClient(id, payload) { return this.request(`/clientes/${id}`, { method: "PUT", body: JSON.stringify(payload) }); },
  createCard(clientId, payload) { return this.request(`/clientes/${clientId}/cartoes`, { method: "POST", body: JSON.stringify(payload) }); },
  getCard(clientId, cardId) { return this.request(`/clientes/${clientId}/cartoes/${cardId}`); },
  addBalance(clientId, cardId, value) { return this.request(`/clientes/${clientId}/cartoes/${cardId}/saldo`, { method: "POST", body: JSON.stringify({ valor: Number(value) }) }); },

  addCartItem(clientId, productId, quantity) { return this.request(`/clientes/${clientId}/carrinho/itens`, { method: "POST", body: JSON.stringify({ id_prod: Number(productId), quantidade: Number(quantity) }) }); },
  getCart(clientId, cartId) { return this.request(`/clientes/${clientId}/carrinho/${cartId}`); },
  removeCartItem(clientId, productId) { return this.request(`/clientes/${clientId}/carrinho/itens/${productId}`, { method: "DELETE" }); },
  checkout(clientId, cardId) { return this.request(`/clientes/${clientId}/compras`, { method: "POST", body: JSON.stringify({ id_cartao: Number(cardId) }) }); },
  getHistory(clientId) { return this.request(`/clientes/${clientId}/historico`); }
};
